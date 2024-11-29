# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    theme_color = fields.Char(related='company_id.theme_color',readonly=False)


class Company(models.Model):
    _inherit = "res.company"

    theme_color = fields.Char(name="Theme Color")

    @api.model
    def get_color(self):
        company = self.search([])
        return {
            'success': True,
            'theme_color': company.theme_color,
        }

