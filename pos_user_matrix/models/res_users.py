from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    pos_customer_note = fields.Boolean()
    pos_refund = fields.Boolean()
    pos_info = fields.Boolean()
    pos_discount = fields.Boolean()
    pos_enter_code =fields.Boolean()
    pos_reward = fields.Boolean()
    pos_quatation_order = fields.Boolean()
    pos_clear_cart = fields.Boolean()
    pos_clear_coupon = fields.Boolean()