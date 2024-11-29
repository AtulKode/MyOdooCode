# -*- coding: utf-8 -*-

from odoo import models, api


class SaleTaxWizard(models.TransientModel):
    _name = "sale.tax.wizard"
    _description = "Sale Tax wizard"

    def confirm_sale_order(self):
        active_id = self.env.context.get('active_id')
        tax_ids = self.env.context.get('tax_ids_to_apply')
        if active_id and tax_ids:
            sale_order = self.env['sale.order'].browse(active_id)
            sale_order.order_line.write({'tax_id': [(6, [], tax_ids)]})
            sale_order.with_context(confirm_wizard=True).action_confirm()
        return {'type': 'ir.actions.act_window_close'}
