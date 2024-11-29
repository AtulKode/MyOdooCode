from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dairy_signup = fields.Boolean()


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['dairy_signup'] = self.env['ir.config_parameter'].sudo().get_param("base.dairy_signup", default="")
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].set_param("base.dairy_signup", self.dairy_signup or '')
        super(ResConfigSettings, self).set_values()