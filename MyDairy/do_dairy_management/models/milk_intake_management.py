from odoo import models, fields, api,_
from odoo.exceptions import ValidationError,UserError


class MilkIntakeManagement(models.Model):
    _name = 'milk.intake.management'
    _inherit = ['mail.thread']
    _description = 'Milk Intake Management'
    _rec_name = 'milk_dairy_id'


    milk_dairy_id = fields.Many2one('milk.dairy', string='Milk Dairy',tracking=True, required=True)
    customer_id = fields.Many2one('customer.registration', string='Customer',tracking=True, required=True)
    active = fields.Boolean('Active', default=True)
    for_date = fields.Datetime(string='For Date',tracking=True, default=fields.Datetime.now)
    animal_id = fields.Many2one('animal.animal', string='Animal',tracking=True, required=True)
    quantity = fields.Float(string='Quantity (In Litter)',tracking=True)
    fat = fields.Float(string='Fat')
    price = fields.Float(string='Price',tracking=True, compute='_calculate_milk_price')

    @api.constrains('quantity')
    def _check_quantity_positive(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError('Quantity must be positive value')

    @api.constrains('fat')
    def _check_fat_positive(self):
        for record in self:
            if record.fat <= 0:
                raise ValidationError('fat must be positive value')

    @api.depends('animal_id','for_date')
    def _calculate_milk_price(self):
        self.price = None
        for record in self:
            if record.for_date and record.animal_id:
                from_date = (record.for_date).date()
                rate_id = self.env['rate.management'].search([('from_date', '<=', from_date), ('to_date', '>=', from_date),('animal_id','=',record.animal_id.id),('dairy_id','=',record.milk_dairy_id.id)],limit=1)
                if rate_id:
                    record.price = (rate_id.rate_per_fat * record.fat) * record.quantity
                else:
                    raise UserError('Rate is not available for this date. Please select any other date')

    @api.model
    def get_dairies(self):
        return self.env['milk.dairy'].search_read(['|',('owner_id', '=', self.env.user.id),
            ('incharge_id', '=', self.env.user.id)], fields=['id','name','supported_animal_ids'])


    def _get_customer_data(self):
        data = {}
        data['form_view_id'] = self.env.ref('do_dairy_management.view_milk_intake_management_form').id
        return data