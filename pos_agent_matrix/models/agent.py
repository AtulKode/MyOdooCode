from odoo import api,models,fields

class AgentModel(models.Model):
	_name = 'agent.model'

	name = fields.Char("Name")
	is_active_agent = fields.Boolean("Is Active")

class ResConfigSettings(models.TransientModel):
	_inherit = "res.config.settings"

	is_agent = fields.Boolean(related='pos_config_id.is_agent', store=True, readonly=False)

class PosConfig(models.Model):
    _inherit = 'pos.config'

    is_agent = fields.Boolean("Is Agent") 

