# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_logo = fields.Binary(related='website_id.company_logo',
                                 string="Company Logo",
                                 help="This field holds the image"
                                      " used for the Company Logo",
                                 readonly=False)
    company_name = fields.Char(related='website_id.company_name',
                               string="Company Name",
                               readonly=False)
    company_website = fields.Char(related='website_id.company_website',
                                  readonly=False)

    dynamic_brand_primary_color = fields.Char(related='website_id.dynamic_brand_primary_color',readonly=False)

    def error(self):
        raise ValueError

    def show_warning(self):
        raise Warning(_('This is a .'))

    def company_title_data(self):
      val = self.env['res.config.settings'].search([],order="id desc",limit=1)

class Website(models.Model):
    _inherit = 'website'

    @api.depends('favicon')
    def get_favicon(self):
        if self.favicon:
            favicon_base64 = base64.b64encode(self.favicon).decode('utf-8')
            self.favicon_url = f'data:image/png;base64,{favicon_base64}'
        else:
            self.favicon_url = False
            
    @api.depends('company_logo')
    def get_company_logo(self):
        if self.company_logo:
            company_logo_base64 = base64.b64encode(self.company_logo).decode('utf-8')
            self.company_logo_url = f'data:image/png;base64,{company_logo_base64}'
        else:
            self.company_logo_url = False

    company_logo = fields.Binary("Logo", attachment=True,
                                 help="This field holds"
                                      " the image used "
                                      "for the Company Logo")
    company_name = fields.Char("Company Name", help="Branding Name")
    company_website = fields.Char("Company URL")
    favicon_url = fields.Char("Url", compute='get_favicon')
    company_logo_url = fields.Char("Url", compute='get_company_logo')
    dynamic_brand_primary_color = fields.Char(string='Dynamic Brand Primary Color')
