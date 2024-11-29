from odoo import api,models,fields

class PosOrderLine(models.Model):
	_inherit = 'pos.order.line'

	agent_id = fields.Many2one("agent.model")
	date = fields.Date("Pos Date")

