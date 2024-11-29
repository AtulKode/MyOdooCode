from odoo import models, fields


class TermsCondition(models.Model):
	_name = "terms.condition"
	_description = "Terms And Condition"
	_rec_name = 'name'

	name = fields.Char("Name")
	term_condition = fields.Html("Terms And Condition")