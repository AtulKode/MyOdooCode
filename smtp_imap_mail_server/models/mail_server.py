import ast
import base64
import datetime
import dateutil
import email
import hashlib
import hmac
import lxml
import logging
import pytz
import re
import socket
import time

from collections import namedtuple
from email.message import EmailMessage
from email.utils import formataddr
from lxml import etree
from werkzeug.urls import url_encode
from werkzeug import urls

from odoo import _, api, exceptions, fields, models, tools
from odoo.tools import pycompat, ustr
from odoo.tools.misc import clean_context
from odoo.tools.safe_eval import safe_eval
from odoo.addons.base.models.ir_mail_server import MailDeliveryException

_logger = logging.getLogger(__name__)

class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    default_company = fields.Many2one('res.company', string="Company")
    default_user = fields.Many2one('res.users', string="User")
    company_bool = fields.Boolean(compute="compute_company")
    user_bool = fields.Boolean(compute="compute_user")
    

    def compute_company(self):
        select = self.env['ir.config_parameter'].sudo().get_param('smtp_imap_mail_server.select')
        if select == "company":
            self.company_bool = True
        else:
            self.company_bool = False 

    def compute_user(self):
        select = self.env['ir.config_parameter'].sudo().get_param('smtp_imap_mail_server.select')
        if select == "user":
            self.user_bool = True
        else:
            self.user_bool = False 
    

class MailMail(models.Model):
    _inherit = "mail.mail"

    def send(self, auto_commit=False, raise_exception=False):
        """ Sends the selected emails immediately, ignoring their current
            state (mails that have already been sent should not be passed
            unless they should actually be re-sent).
            Emails successfully delivered are marked as 'sent', and those
            that fail to be deliver are marked as 'exception', and the
            corresponding error mail is output in the server logs.

            :param bool auto_commit: whether to force a commit of the mail status
                after sending each mail (meant only for scheduler processing);
                should never be True during normal transactions (default: False)
            :param bool raise_exception: whether to raise an exception if the
                email sending process has failed
            :return: True
        """
        for mail_server_id, smtp_from, batch_ids in self._split_by_mail_configuration():
            smtp_session = None

            active_company_id = self.env['res.users'].browse(self._context.get('uid') or self._uid or self.env.user.id).company_id
            active_user_id = self.env['res.users'].browse(self._context.get('uid') or self._uid or self.env.user.id)
            company_server_id = self.env['ir.mail_server'].search(['|',('default_company', '=', active_company_id.id),('default_user', '=', active_user_id.id)])
            mail_server_id = company_server_id and company_server_id.id or mail_server_id

            try:
                smtp_session = self.env['ir.mail_server'].connect(mail_server_id=mail_server_id, smtp_from=smtp_from)
            except Exception as exc:
                if raise_exception:
                    # To be consistent and backward compatible with mail_mail.send() raised
                    # exceptions, it is encapsulated into an Odoo MailDeliveryException
                    raise MailDeliveryException(_('Unable to connect to SMTP Server'), exc)
                else:
                    batch = self.browse(batch_ids)
                    batch.write({'state': 'exception', 'failure_reason': exc})
                    batch._postprocess_sent_message(success_pids=[], failure_type="mail_smtp")
            else:
                self.browse(batch_ids)._send(
                    auto_commit=auto_commit,
                    raise_exception=raise_exception,
                    smtp_session=smtp_session)
                _logger.info(
                    'Sent batch %s emails via mail server ID #%s',
                    len(batch_ids), mail_server_id)
            finally:
                if smtp_session:
                    smtp_session.quit()
                    

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'
    
    @api.model
    def message_route(self, message, message_dict, model=None, thread_id=None, custom_values=None):
        """ Attempt to figure out the correct target model, thread_id,
        custom_values and user_id to use for an incoming message.
        Multiple values may be returned, if a message had multiple
        recipients matching existing mail.aliases, for example.

        The following heuristics are used, in this order:

         * if the message replies to an existing thread by having a Message-Id
           that matches an existing mail_message.message_id, we take the original
           message model/thread_id pair and ignore custom_value as no creation will
           take place;
         * look for a mail.alias entry matching the message recipients and use the
           corresponding model, thread_id, custom_values and user_id. This could
           lead to a thread update or creation depending on the alias;
         * fallback on provided ``model``, ``thread_id`` and ``custom_values``;
         * raise an exception as no route has been found

        :param string message: an email.message instance
        :param dict message_dict: dictionary holding parsed message variables
        :param string model: the fallback model to use if the message does not match
            any of the currently configured mail aliases (may be None if a matching
            alias is supposed to be present)
        :type dict custom_values: optional dictionary of default field values
            to pass to ``message_new`` if a new record needs to be created.
            Ignored if the thread record already exists, and also if a matching
            mail.alias was found (aliases define their own defaults)
        :param int thread_id: optional ID of the record/thread from ``model`` to
            which this mail should be attached. Only used if the message does not
            reply to an existing thread and does not match any mail alias.
        :return: list of routes [(model, thread_id, custom_values, user_id, alias)]

        :raises: ValueError, TypeError
        """
        if not isinstance(message, EmailMessage):
            raise TypeError('message must be an email.message.EmailMessage at this point')

        MailMessage = self.env['mail.message']
        Alias, dest_aliases = self.env['mail.alias'], self.env['mail.alias']

        catchall_alias = self.env['ir.config_parameter'].sudo().get_param("mail.catchall.alias")
        catchall_domain_lowered = self.env["ir.config_parameter"].sudo().get_param("mail.catchall.domain", "").strip().lower()
        catchall_domains_allowed = self.env["ir.config_parameter"].sudo().get_param("mail.catchall.domain.allowed")
        if catchall_domain_lowered and catchall_domains_allowed:
            catchall_domains_allowed = catchall_domains_allowed.split(',') + [catchall_domain_lowered]
        bounce_alias = self.env['ir.config_parameter'].sudo().get_param("mail.bounce.alias")
        fallback_model = model

        # get email.message.Message variables for future processing
        local_hostname = socket.gethostname()
        message_id = message_dict['message_id']

        # compute references to find if message is a reply to an existing thread
        thread_references = message_dict['references'] or message_dict['in_reply_to']
        msg_references = [
            re.sub(r'[\r\n\t ]+', r'', ref)  # "Unfold" buggy references
            for ref in tools.mail_header_msgid_re.findall(thread_references)
            if 'reply_to' not in ref
        ]
        mail_messages = self.env['mail.message'].sudo().search([('message_id', 'in', msg_references)], limit=1, order='id desc, message_id')
        is_a_reply = bool(mail_messages)
        reply_model, reply_thread_id = mail_messages.model, mail_messages.res_id


        # author and recipients
        email_from = message_dict['email_from']
        email_from_localpart = (tools.email_split(email_from) or [''])[0].split('@', 1)[0].lower()
        email_to = message_dict['to']
        email_to_localparts = [
            e.split('@', 1)[0].lower()
            for e in (tools.email_split(email_to) or [''])
        ]

        # Delivered-To is a safe bet in most modern MTAs, but we have to fallback on To + Cc values
        # for all the odd MTAs out there, as there is no standard header for the envelope's `rcpt_to` value.
        rcpt_tos = ','.join([
            tools.decode_message_header(message, 'Delivered-To'),
            tools.decode_message_header(message, 'To'),
            tools.decode_message_header(message, 'Cc'),
            tools.decode_message_header(message, 'Resent-To'),
            tools.decode_message_header(message, 'Resent-Cc')])
        rcpt_tos_localparts = [e.split('@')[0].lower() for e in tools.email_split(rcpt_tos)]
        
        email_to_alias_domain_list = [e.split('@')[1].lower() for e in tools.email_split(rcpt_tos)]



        # 0. Handle bounce: verify whether this is a bounced email and use it to collect bounce data and update notifications for customers
        #    Bounce alias: if any To contains bounce_alias@domain
        #    Bounce message (not alias)
        #       See http://datatracker.ietf.org/doc/rfc3462/?include_text=1
        #        As all MTA does not respect this RFC (googlemail is one of them),
        #       we also need to verify if the message come from "mailer-daemon"
        #    If not a bounce: reset bounce information
        if bounce_alias and bounce_alias in email_to_localparts:
            self._routing_handle_bounce(message, message_dict)
            return []
        if message.get_content_type() == 'multipart/report' or email_from_localpart == 'mailer-daemon':
            self._routing_handle_bounce(message, message_dict)
            return []
        self._routing_reset_bounce(message, message_dict)

        # 1. Handle reply
        #    if destination = alias with different model -> consider it is a forward and not a reply
        #    if destination = alias with same model -> check contact settings as they still apply
        if reply_model and reply_thread_id:
            reply_model_id = self.env['ir.model']._get_id(reply_model)
            other_model_aliases = self.env['mail.alias'].search([
                '&', '&',
                ('alias_name', '!=', False),
                ('alias_name', 'in', email_to_localparts),
                ('alias_model_id', '!=', reply_model_id),
            ])
            if other_model_aliases:
                is_a_reply = False
                rcpt_tos_localparts = [to for to in rcpt_tos_localparts if to in other_model_aliases.mapped('alias_name')]

        if is_a_reply and reply_model:
            reply_model_id = self.env['ir.model']._get_id(reply_model)
            dest_aliases = self.env['mail.alias'].search([
                ('alias_name', 'in', rcpt_tos_localparts),
                ('alias_model_id', '=', reply_model_id)
            ], limit=1)

            user_id = self._mail_find_user_for_gateway(email_from, alias=dest_aliases).id or self._uid
            route = self._routing_check_route(
                message, message_dict,
                (reply_model, reply_thread_id, custom_values, user_id, dest_aliases),
                raise_exception=False)
            if route:
                _logger.info(
                    'Routing mail from %s to %s with Message-Id %s: direct reply to msg: model: %s, thread_id: %s, custom_values: %s, uid: %s',
                    email_from, email_to, message_id, reply_model, reply_thread_id, custom_values, self._uid)
                return [route]
            elif route is False:
                return []

        # 2. Handle new incoming email by checking aliases and applying their settings
        if rcpt_tos_localparts:
            # no route found for a matching reference (or reply), so parent is invalid
            message_dict.pop('parent_id', None)

            # check it does not directly contact catchall
            if catchall_alias and email_to_localparts and all(email_localpart == catchall_alias for email_localpart in email_to_localparts):
                _logger.info('Routing mail from %s to %s with Message-Id %s: direct write to catchall, bounce', email_from, email_to, message_id)
                body = self.env['ir.qweb']._render('mail.mail_bounce_catchall', {
                    'message': message,
                })
                self._routing_create_bounce_email(email_from, body, message, references=message_id, reply_to=self.env.company.email)
                return []

            alias_domain_id = self.env['alias.domain'].search([('domain_name','in',email_to_alias_domain_list)])
            
            if alias_domain_id:
                dest_aliases = Alias.search([('alias_domain','in',alias_domain_id.ids),('alias_name', 'in', rcpt_tos_localparts)])

            # dest_aliases = self.env['mail.alias'].search([('alias_name', 'in', rcpt_tos_localparts)])
            if dest_aliases:
                routes = []
                for alias in dest_aliases:
                    user_id = self._mail_find_user_for_gateway(email_from, alias=alias).id or self._uid
                    route = (alias.sudo().alias_model_id.model, alias.alias_force_thread_id, ast.literal_eval(alias.alias_defaults), user_id, alias)
                    route = self._routing_check_route(message, message_dict, route, raise_exception=True)
                    if route:
                        _logger.info(
                            'Routing mail from %s to %s with Message-Id %s: direct alias match: %r',
                            email_from, email_to, message_id, route)
                        routes.append(route)
                return routes

        # 3. Fallback to the provided parameters, if they work
        if fallback_model:
            # no route found for a matching reference (or reply), so parent is invalid
            message_dict.pop('parent_id', None)
            user_id = self._mail_find_user_for_gateway(email_from).id or self._uid
            route = self._routing_check_route(
                message, message_dict,
                (fallback_model, thread_id, custom_values, user_id, None),
                raise_exception=True)
            if route:
                _logger.info(
                    'Routing mail from %s to %s with Message-Id %s: fallback to model:%s, thread_id:%s, custom_values:%s, uid:%s',
                    email_from, email_to, message_id, fallback_model, thread_id, custom_values, user_id)
                return [route]

        # ValueError if no routes found and if no bounce occurred
        raise ValueError(
            'No possible route found for incoming message from %s to %s (Message-Id %s:). '
            'Create an appropriate mail.alias or force the destination model.' %
            (email_from, email_to, message_id)
        )


    @api.model
    def _message_route_process(self, message, message_dict, routes):
        self = self.with_context(attachments_mime_plainxml=True) # import XML attachments as text
        # postpone setting message_dict.partner_ids after message_post, to avoid double notifications
        original_partner_ids = message_dict.pop('partner_ids', [])
        thread_id = False
        for model, thread_id, custom_values, user_id, alias in routes or ():
            subtype_id = False
            related_user = self.env['res.users'].browse(user_id)
            Model = self.env[model].with_context(mail_create_nosubscribe=True, mail_create_nolog=True)
            if not (thread_id and hasattr(Model, 'message_update') or hasattr(Model, 'message_new')):
                raise ValueError(
                    "Undeliverable mail with Message-Id %s, model %s does not accept incoming emails" %
                    (message_dict['message_id'], model)
                )


            # disabled subscriptions during message_new/update to avoid having the system user running the
            # email gateway become a follower of all inbound messages
            ModelCtx = Model.with_user(related_user).sudo()
            if thread_id and hasattr(ModelCtx, 'message_update'):
                thread = ModelCtx.browse(thread_id)
                thread.message_update(message_dict)
            else:
                # if a new thread is created, parent is irrelevant
                message_dict.pop('parent_id', None)
                thread = ModelCtx.message_new(message_dict, custom_values)
                print("thread=================",thread)
                thread.sudo().write({'company_id': alias.alias_domain.company_id.id})
                thread_id = thread.id
                subtype_id = thread._creation_subtype().id


            # replies to internal message are considered as notes, but parent message
            # author is added in recipients to ensure they are notified of a private answer
            parent_message = False
            if message_dict.get('parent_id'):
                parent_message = self.env['mail.message'].sudo().browse(message_dict['parent_id'])
            partner_ids = []
            if not subtype_id:
                if message_dict.get('is_internal'):
                    subtype_id = self.env['ir.model.data']._xmlid_to_res_id('mail.mt_note')
                    if parent_message and parent_message.author_id:
                        partner_ids = [parent_message.author_id.id]
                else:
                    subtype_id = self.env['ir.model.data']._xmlid_to_res_id('mail.mt_comment')

            post_params = dict(subtype_id=subtype_id, partner_ids=partner_ids, **message_dict)




            # remove computational values not stored on mail.message and avoid warnings when creating it
            for x in ('from', 'to', 'cc', 'recipients', 'references', 'in_reply_to', 'bounced_email', 'bounced_message', 'bounced_msg_id', 'bounced_partner'):
                post_params.pop(x, None)
            new_msg = False
            if thread._name == 'mail.thread':  # message with parent_id not linked to record
                new_msg = thread.message_notify(**post_params)
            else:
                # parsing should find an author independently of user running mail gateway, and ensure it is not odoobot
                partner_from_found = message_dict.get('author_id') and message_dict['author_id'] != self.env['ir.model.data']._xmlid_to_res_id('base.partner_root')
                thread = thread.with_context(mail_create_nosubscribe=not partner_from_found)
                new_msg = thread.message_post(**post_params)

            if new_msg and original_partner_ids:
                # postponed after message_post, because this is an external message and we don't want to create
                # duplicate emails due to notifications
                new_msg.write({'partner_ids': original_partner_ids})
        return thread_id

