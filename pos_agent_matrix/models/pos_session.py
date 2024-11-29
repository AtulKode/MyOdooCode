from odoo import api,models,fields

class PosSession(models.Model):
	_inherit = "pos.session"

	def _pos_ui_models_to_load(self):
	    result = super()._pos_ui_models_to_load()
	    result.append('agent.model')
	    return result

	def _loader_params_agent_model(self):
    
		return {     
		'search_params': {                  
		'fields': ['name', 'is_active_agent',],      
		},
		    
		}

	def _get_pos_ui_agent_model(self, params):
		return self.env['agent.model'].search_read(**params['search_params'])
		

	def _loader_params_product_product(self):
		result = super()._loader_params_product_product()
		print("result",result)
		result['search_params']['fields'].extend(['is_service_agent'])
		print("after nresult",result)   
		return result 