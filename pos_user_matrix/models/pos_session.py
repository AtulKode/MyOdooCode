# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_users(self):
    	res = super(PosSession, self)._loader_params_res_users()
    	
    	res['search_params']['fields'].extend(['pos_customer_note','pos_refund',
	            'pos_info','pos_discount','pos_enter_code','pos_reward','pos_quatation_order',
	            'pos_clear_cart','pos_clear_coupon'])
    	# print("print res: ",res)
    	return res
