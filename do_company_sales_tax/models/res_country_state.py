# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCountryState(models.Model):
    _inherit = "res.country.state"

    tax_ids = fields.Many2many("account.tax", domain="[('type_tax_use', '=', 'sale')]")