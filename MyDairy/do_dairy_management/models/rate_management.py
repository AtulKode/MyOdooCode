from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RateManagement(models.Model):
    _name = 'rate.management'
    _inherit = ['mail.thread']
    _description = 'Rate Management'
    _rec_name = 'animal_id'
    
    dairy_id = fields.Many2one("milk.dairy", string="Dairy")
    active = fields.Boolean('Active', default=True)
    from_date = fields.Date(string='From Date',required=True)
    to_date = fields.Date(string='To Date',required=True)
    animal_id = fields.Many2one('animal.animal', string='Animal',required=True, tracking=True)
    rate_per_fat = fields.Float(string='Rate Per Fat',tracking=True)

    @api.constrains('from_date', 'to_date')
    def _check_date_order(self):
        for record in self:
            if record.from_date > record.to_date:
                raise ValidationError("'From Date' must be earlier than 'To Date'")

    @api.constrains('rate_per_fat')
    def _check_positive_rate(self):
        for record in self:
            if record.rate_per_fat <= 0:
                raise ValidationError("'Rate Per Fat' must be a positive value")

    @api.model
    def get_rate_per_fat(self, dairy_id):
        dairy = self.env['milk.dairy'].browse(dairy_id)
        animal_rates = {}
        for animal in dairy.supported_animal_ids:
            rate = self.search([('dairy_id', '=', dairy_id), ('animal_id', '=', animal.id)], limit=1).rate_per_fat
            animal_rates[animal.name] = rate
        return animal_rates


        