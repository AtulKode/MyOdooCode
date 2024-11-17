# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    is_bank_charge = fields.Boolean("POS Bank Charges")

    journal_type = fields.Selection(string='Journal Type', related='journal_id.type', readonly=True)
    cahrges_type = fields.Selection([
        ('percentage', 'Percentage'),
        ], string="Bank Charge Type",default='percentage')

    cahrges_amount = fields.Float(string="Bank Charge Amount")

    bank_charge_prod_id = fields.Many2one('product.product', domain = [('type', '=', 'service'),
        ('available_in_pos', '=', True)],string="Bank Charge Product")


    @api.onchange('journal_id')
    def journal_bank(self):
        for pm in self:
            pm.is_bank_charge = False


class PosPayment(models.Model):
    _inherit = "pos.payment"

    bnk_charge = fields.Float("Bank Charge")
