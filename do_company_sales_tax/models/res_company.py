# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sale_tax_limit_ids = fields.One2many("sale.tax.limit", "company_id")