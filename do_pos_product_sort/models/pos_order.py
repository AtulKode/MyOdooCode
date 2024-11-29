# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _process_order(self, order, draft, existing_order):
        do_pos_obj = self.env['do.pos.product.sold']
        order_data = order['data']['lines']
        for line in order_data:
            product_id = line[2].get('product_id')
            qty = line[2].get('qty', 0)
            
            # Check if there's an existing record for the product in DoPosProductSold
            existing_product = do_pos_obj.search([('product_id', '=', product_id)], limit=1)
            if existing_product:
                existing_product.qty += qty
            else:
                do_pos_obj.create({
                    'product_id': product_id,
                    'qty': qty,
                })
        return super(PosOrder, self)._process_order(order, draft, existing_order)
