# -*- coding: utf-8 -*-
# from odoo import http


# class PosProject(http.Controller):
#     @http.route('/pos_project/pos_project', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_project/pos_project/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_project.listing', {
#             'root': '/pos_project/pos_project',
#             'objects': http.request.env['pos_project.pos_project'].search([]),
#         })

#     @http.route('/pos_project/pos_project/objects/<model("pos_project.pos_project"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_project.object', {
#             'object': obj
#         })

