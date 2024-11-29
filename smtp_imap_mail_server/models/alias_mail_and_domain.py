# -*- coding: utf-8 -*-
#########################

import re
from odoo.exceptions import ValidationError
from odoo.tools import remove_accents
from odoo import _, api, exceptions, fields, models, tools

class AliasDomain(models.Model):
    _name = 'alias.domain'
    _rec_name = 'domain_name'
    
    domain_name = fields.Char(string="Domain Name")
    company_id = fields.Many2one('res.company', string="Company")

class Alias(models.Model):
    _inherit = "mail.alias"
    
    def _default_alias_domain(self):
        current_user = self.env['res.users'].browse(self._context.get('uid') or self._uid or self.env.user.id)
        alias = self.env["alias.domain"].sudo().search([('company_id','=',current_user.company_id.id)],limit=1)
        return alias
    
    alias_domain = fields.Many2one('alias.domain',default=lambda self:self._default_alias_domain())

    
    _sql_constraints = [
        ('alias_unique', 'UNIQUE(alias_name)', 'Unfortunately this email alias is already used, please choose a unique one')
    ]

    

    def _clean_and_check_unique(self, names):
        """When an alias name appears to already be an email, we keep the local
        part only. A sanitizing / cleaning is also performed on the name."""

        def _sanitize_alias_name(name):
            """ Cleans and sanitizes the alias name """
            sanitized_name = remove_accents(name).lower().split('@')[0]
            sanitized_name = re.sub(r'[^\w+.]+', '-', sanitized_name)
            sanitized_name = re.sub(r'^\.+|\.+$|\.+(?=\.)', '', sanitized_name)
            return sanitized_name

        sanitized_names = [_sanitize_alias_name(name) for name in names]

        return sanitized_names



    def name_get(self):
        """Return the mail alias display alias_name, including the implicit
           mail catchall domain if exists from config otherwise "New Alias".
           e.g. `jobs@mail.odoo.com` or `jobs` or 'New Alias'
        """
        res = []
        for record in self:
            if record.alias_name and record.alias_domain:
                res.append((record['id'], "%s@%s" % (record.alias_name, record.alias_domain.domain_name)))
            elif record.alias_name:
                res.append((record['id'], "%s" % (record.alias_name)))
            else:
                res.append((record['id'], _("Inactive Alias")))
        return res

class AccountJournal(models.Model):
    _inherit = "account.journal"
    
    alias_domain = fields.Many2one('alias.domain',related='alias_id.alias_domain')
    
    @api.model
    def create(self, vals):
        res = super(AccountJournal, self).create(vals)
        if 'alias_domain' in vals:
            if vals.get('alias_domain'):
                res.alias_id.sudo().write({'alias_domain':vals.get('alias_domain')})
                del(vals['alias_domain'])
            else:
                alias = self.env["alias.domain"].sudo().search([('company_id','=',self.env.user.company_id.id)],limit=1)
                if alias:
                    res.alias_id.sudo().write({'alias_domain':alias.id})
        return res
    
    def write(self, vals):
        for journal in self:
            if 'alias_domain' in vals:
                journal.alias_id.sudo().write({'alias_domain':vals.get('alias_domain')})
                if vals.get('alias_domain'):
                    del(vals['alias_domain'])
        return super(AccountJournal, self).write(vals)
    
    
