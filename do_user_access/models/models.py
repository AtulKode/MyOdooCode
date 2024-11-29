# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        # Get the current user
        user = self.env.user
        if user.has_group('do_user_access.group_own_records'):
            # Add the domain to filter records by user_id or create_uid
            if domain:
                domain = ['|', ('user_id', '=', user.id), ('create_uid', '=', user.id)] + domain
            else:
                domain = ['|', ('user_id', '=', user.id), ('create_uid', '=', user.id)]        
        return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        # Get the current user
        user = self.env.user
        if user.has_group('do_user_access.group_own_records'):
            # Add the domain to filter records by user_id or create_uid
            if domain:
                domain = ['|', ('user_id', '=', user.id), ('create_uid', '=', user.id)] + domain
            else:
                domain = ['|', ('user_id', '=', user.id), ('create_uid', '=', user.id)]        
        return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
