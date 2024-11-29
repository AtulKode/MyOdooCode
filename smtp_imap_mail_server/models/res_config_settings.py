from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    select = fields.Selection([
        ('company', "Company"),
        ('user', "User")], default=False)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['select'] = self.env['ir.config_parameter'].sudo().get_param('smtp_imap_mail_server.select')
        return res

    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('smtp_imap_mail_server.select', self.select)

        super(ResConfigSettings, self).set_values()