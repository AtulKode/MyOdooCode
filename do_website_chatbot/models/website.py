# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Website(models.Model):
    _inherit = 'website'

    def get_default_chatbot(self):
        website_id = self.env['website'].get_current_website()
        chatbot_id = self.env['chatbot.chatbot'].sudo().search([('website_id', 'in', (website_id.id, False))], limit=1)
        return chatbot_id
