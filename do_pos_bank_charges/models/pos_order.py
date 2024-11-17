# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    bnk_charge = fields.Float("Bank Charge")


    @api.model
    def _order_fields(self, ui_order):

      result = super(PosOrder, self)._order_fields(ui_order)
      if ui_order['total_bank_charge']:
          result['amount_paid'] = ui_order['amount_paid'] - ui_order['total_bank_charge']
          result['amount_total'] = ui_order['amount_total'] - ui_order['total_bank_charge']
          result['bnk_charge'] = ui_order.get('total_bank_charge',0.0)
      return result


    @api.model
    def _payment_fields(self, order, ui_paymentline):
      result = super(PosOrder, self)._payment_fields(order, ui_paymentline)
      if(ui_paymentline['currency_amount']):
          amount = ui_paymentline['amount'] or 0.0
          bnkCharge = ui_paymentline['currency_amount']
          result['amount'] = (amount - bnkCharge)
          result['bnk_charge'] = bnkCharge

      return result



class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_pos_payment_method(self):
      result = super()._loader_params_pos_payment_method()
      result['search_params']['fields'].extend(['is_bank_charge','cahrges_type','cahrges_amount','bank_charge_prod_id'])
      return result
