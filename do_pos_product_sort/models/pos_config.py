# -*- coding: utf-8 -*-
from odoo import fields,models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    show_prod_filter = fields.Boolean("Show Product Filter", default=True)
    default_filter = fields.Selection(string="Default Filter", selection=[('default_order', 'Default Order'),
        ('most_sold','Most Sold'),('new_arrivals', 'New Arrivals'),
        ('price_asc', 'Price ASC'),('price_desc', 'Price DESC'),
        ('name_asc', 'Name ASC'),('name_desc', 'Name DESC'),('least_sold', 'Least Sold')], default='default_order') 


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_show_prod_filter = fields.Boolean(related="pos_config_id.show_prod_filter", readonly=False)
    pos_default_filter = fields.Selection(related="pos_config_id.default_filter", readonly=False) 
