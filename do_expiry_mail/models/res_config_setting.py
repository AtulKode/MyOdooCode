from odoo import models, api, fields
from datetime import datetime, timedelta

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    send_expiry_mail = fields.Boolean("Send Expiry Mail", store=True)
    set_days = fields.Integer(string="Set Days", config_parameter='do_expiry_mail.set_days')


    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('do_expiry_mail.send_expiry_mail', self.send_expiry_mail)
        self.env['ir.config_parameter'].sudo().set_param('do_expiry_mail.set_days', self.set_days)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            send_expiry_mail=ICPSudo.get_param('do_expiry_mail.send_expiry_mail'),
            set_days=ICPSudo.get_param('do_expiry_mail.set_days'),
        )
        return res

    def check_expiry_and_send_mail(self):
        send_expiry_mail = self.env['ir.config_parameter'].sudo().get_param('do_expiry_mail.send_expiry_mail')
        set_days = int(self.env['ir.config_parameter'].sudo().get_param('do_expiry_mail.set_days'))
        expiration_date_str = self.env['ir.config_parameter'].sudo().get_param('database.expiration_date')
        if not expiration_date_str:
            expiry_id = self.env.ref('mail.ir_cron_module_update_notification')
            if expiry_id:
                expiry_id.method_direct_trigger()
            return

        if send_expiry_mail:
            expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d %H:%M:%S')
            today = datetime.today()
            warning_date = expiration_date - timedelta(days=set_days)

            if today >= warning_date:
                template_id = self.env.ref('do_expiry_mail.mail_template_expiry_notification')
                email_to = self.env.user.email
                template_id.sudo().send_mail(self.env.user.id, force_send=True, email_values={'email_to': email_to})
