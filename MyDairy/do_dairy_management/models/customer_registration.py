from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class CustomerRegistration(models.Model):
    _name = 'customer.registration'
    _inherit = ['mail.thread']
    _description = 'Customer Registration'
    _rec_name = 'partner_id'

    dairy_cust_id = fields.Char(string='Dairy Customer Id', required=True,
                          readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Name', required=True)
    active = fields.Boolean('Active', default=True)
    animal_ids = fields.Many2many('animal.animal', string='Animal List')
    no_of_animals = fields.Integer(string='No of Animals', tracking=True)
    member_since = fields.Date(string='Member Since', tracking=True)
    dairy_id = fields.Many2one('milk.dairy')


    @api.model
    def get_customers_for_dairy(self, dairy_id):
        customers = self.env['customer.registration'].search([('dairy_id', '=', dairy_id)])
        customer_data = []
        for customer in customers:
            customer_info = {
                'dairy_cust_id': customer.dairy_cust_id,
                'partner_id': {
                    'id': customer.partner_id.id,
                    'name': customer.partner_id.name,
                    'mobile': customer.partner_id.mobile,
                },
                'animal_ids': [{'id': animal.id, 'name': animal.name} for animal in customer.animal_ids],
            }
            customer_data.append(customer_info)
        print("customer data ====== \n\n\n",customer_data)
        return customer_data


    @api.constrains('no_of_animals')
    def _check_no_of_animals(self):
        for record in self:
            if record.no_of_animals < 0:
                raise ValidationError('Number of animals must be non-negative.')

    @api.constrains('member_since')
    def _check_member_since(self):
        for record in self:
            if record.member_since and record.member_since > fields.Date.today():
                raise ValidationError('Member Since date cannot be in the future.')

    @api.model
    def create(self, vals):
       if vals.get('dairy_cust_id', _('New')) == _('New'):
           vals['dairy_cust_id'] = self.env['ir.sequence'].next_by_code(
               'customer.registration') or _('New')
       res = super(CustomerRegistration, self).create(vals)
       return res

