# -*- coding: utf-8 -*-
from odoo import fields,models


class DoPosProductSold(models.Model):
    _name = "do.pos.product.sold"
    _description = "Pos Product Sold"
    _order = 'qty desc'
    _rec_name = 'product_id'

    product_id = fields.Many2one("product.product")
    qty = fields.Integer("Sold Quantity")