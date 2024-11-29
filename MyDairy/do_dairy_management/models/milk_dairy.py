from odoo import models,fields,api,_
from odoo.exceptions import ValidationError


class MilkDairy(models.Model):
    _name = 'milk.dairy'
    _inherit = ['mail.thread','format.address.mixin']
    _description = 'Milk Dairy Registration'

    name = fields.Char(string='Name',required=True)
    active = fields.Boolean('Active', default=True)
    owner_id = fields.Many2one('res.users', string='Owner Details',tracking=True,required=True)
    incharge_id = fields.Many2one('res.users', string='Incharge Details',tracking=True)
    state = fields.Selection([('new','New'),('submit','Submit'),('under_review','Under Review'),('approved','Approved'),('rejected','Rejected')], default='new',tracking=True)
    certificate_no = fields.Char(string='Certificate No', required=True)
    # certificate_photo = fields.Binary(string='Certificate Photo')
    supported_animal_ids = fields.Many2many('animal.animal', string='Supported Animal List',default=lambda self: self._get_default_supported_animals())
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')


    @api.constrains('supported_animal_ids')
    def _check_supported_animals(self):
        for rec in self:
            if not rec.supported_animal_ids:
                raise ValidationError(_("Please select at least one supported animal"))

    @api.constrains('certificate_no')
    def _check_certificate_no_unique(self):
        for rec in self:
            if rec.certificate_no and self.search_count([('certificate_no', '=', rec.certificate_no)]) > 1:
                raise ValidationError(_("Certificate number must be unique"))

    @api.model
    def _get_default_supported_animals(self):
        animal_model = self.env['animal.animal'].search([])
        return animal_model

    def action_new(self):
        self.write({'state': 'new'})

    def action_submit(self):
        self.write({'state': 'submit'})

    def action_under_review(self):
        self.write({'state': 'under_review'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_rejected(self):
        self.write({'state': 'rejected'})