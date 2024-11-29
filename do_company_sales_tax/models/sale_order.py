# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _calculate_tax(self, to_update=False, need_confirmation=False):
        self.ensure_one()
        limit_line = self.env['sale.tax.limit'].search([('start_date','<=',self.date_order),('end_date','>=',self.date_order)])
        assert len(limit_line) == 1, "Missing Configuration on Company"
        confirm_sub_total = limit_line.total_sales
        thresold = limit_line.threshold
        source_state = self.company_id.state_id
        dest_state = self.partner_id.state_id
        taxes_to_apply = self.env['account.tax']

        if dest_state.country_id.code == "US" and source_state.country_id.code == "US":
            if source_state == dest_state:
                taxes_to_apply = dest_state.tax_ids
            else:
                if confirm_sub_total + self.amount_untaxed >= thresold:
                    taxes_to_apply = dest_state.tax_ids
            if need_confirmation:
                if self.order_line.mapped('tax_id') != taxes_to_apply:
                    return {
                        "name": _("Need Confirmation?"),
                        "type": "ir.actions.act_window",
                        "res_model": "sale.tax.wizard",
                        "target": "new",
                        "views": [[False, "form"]],
                        "context": {"is_modal": True, "tax_ids_to_apply":taxes_to_apply.ids},
                    }
            
            self.order_line.write({'tax_id': [(6, [], taxes_to_apply.ids)]})

    @api.model
    def create(self, vals):
        sale_order = super(SaleOrder, self).create(vals)
        sale_order._calculate_tax()
        return sale_order

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if not self.env.context.get('skip_calculate') and 'order_line' in vals:
            self.with_context(skip_calculate=True)._calculate_tax()
        return res

    def action_confirm(self):
        limit_line = self.env['sale.tax.limit'].search([('start_date','<=',self.date_order),('end_date','>=',self.date_order)])
        res = self._calculate_tax(True, True)
        ctx = self.env.context.get('confirm_wizard')
        if not ctx:
            if isinstance(res, dict):
                return res
        limit_line.total_sales += self.amount_untaxed
        return super(SaleOrder, self).action_confirm()

