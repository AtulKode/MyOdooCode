# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
	_inherit = "product.template"

	measuring_unit = fields.Many2one("uom.uom", "Measuring Unit")
	measure_price = fields.Monetary("Measure Price")
