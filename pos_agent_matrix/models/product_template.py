from odoo import api,models,fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_service_agent = fields.Boolean("Is Service Agent")