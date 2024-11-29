# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleTaxLimit(models.Model):
    _name = "sale.tax.limit"
    _description = "Sale Tax"

    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    threshold = fields.Float("Threshold")
    total_sales = fields.Float("Total Sales")
    company_id = fields.Many2one("res.company")