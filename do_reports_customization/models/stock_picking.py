from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def get_default_quality_assurance_user(self):
        company_id = self.env.company.id
        
        quality_assurance_employee = self.env['hr.employee'].sudo().search([
            ('is_qlty_assurance_manager', '=', True),
            ('company_id', '=', company_id)
        ], limit=1)
        # If found, get the associated user
        if quality_assurance_employee and quality_assurance_employee.user_id:
            return quality_assurance_employee.user_id.id
        return False

    def get_default_warehouse_user(self):
        company_id = self.env.company.id
        
        warehouse_partner = self.env['res.partner'].sudo().search([
            ('is_warehouse_manager', '=', True),
            ('company_id', '=', company_id)
        ], limit=1).id
        warehouse_user = self.env['res.users'].sudo().search([('partner_id','=', warehouse_partner)],limit=1)
        # If found, get the associated user
        if warehouse_user:
            return warehouse_user.id
        return False

    quality_assurance_user_id = fields.Many2one('res.users', default=get_default_quality_assurance_user, store=False)
    validated_user_id = fields.Many2one('res.users', string='Warehouse Manager User', default=get_default_warehouse_user, store=False)

    def button_validate(self):
        self.write({'validated_user_id': self.env.user.id})
        return super(StockPicking, self).button_validate()


class ResPartner(models.Model):

    _inherit = 'res.partner'

    is_invoice_salesperson = fields.Boolean(string='Is Invoice Salesperson?', default=False)

    is_warehouse_manager = fields.Boolean("Is Warehouse manager", default=False)

    @api.constrains('is_warehouse_manager')
    def _check_single_warehouse_manager(self):
        for record in self:
            if record.is_warehouse_manager:
                existing_records = self.search([
                    ('is_warehouse_manager', '=', True),
                    ('company_id', '=', record.company_id.id),
                    ('id', '!=', record.id)
                ])
                if existing_records:
                    raise ValidationError("Only one partner per company can be set as Warehouse Manager.")


class AccountInvoice(models.Model):

    _inherit = 'account.move'

    invoice_sales_person_id = fields.Many2one('res.partner', string='Invoice Salesperson', domain="[('is_invoice_salesperson','=',True),('company_id', '=', company_id)]")


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    is_qlty_assurance_manager = fields.Boolean("Is Quality Assurance Manager", default=False)

    @api.constrains('is_qlty_assurance_manager')
    def _check_single_quality_assurance_manager(self):
        for record in self:
            if record.is_qlty_assurance_manager:
                # Check if there is another employee in the same company with this field set to True
                existing_records = self.search([
                    ('is_qlty_assurance_manager', '=', True),
                    ('company_id', '=', record.company_id.id),
                    ('id', '!=', record.id)
                ])
                if existing_records:
                    raise ValidationError("Only one employee per company can be set as Quality Assurance Manager.")

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    requestioner = fields.Selection(selection=[
            ('anas', 'Anas Iqbal'),
            ('firas', 'Firas Albanna'),],string="Requestioner")
    ship_via = fields.Selection(selection=[('by_land', 'By Land'),('by_air', 'By Air'),('by_sea', 'By Sea')], string="Ship Via")
    terms_id = fields.Many2one("terms.condition", string="Terms & Conditions")