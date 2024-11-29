from odoo import api, models, fields

class PosConfig(models.Model):
	_inherit = 'pos.config'

	customer_note_config = fields.Boolean("Customer Note Config")
	pos_config_date = fields.Boolean("Pos Date")

class PosOrder(models.Model):
	_inherit = 'pos.order'

	pos_customer_note = fields.Text("Customer Note")
	Pos_Order_Date = fields.Datetime(string='POS Date')

	@api.model
	def _order_fields(self, ui_order):
		res = super(PosOrder,self)._order_fields(ui_order)
		res['pos_customer_note'] = ui_order.get('pos_customer_note')
		return res