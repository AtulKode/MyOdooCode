from odoo import models, fields, api


class AnimalAnimal(models.Model):
	_name = "animal.animal"
	_inherit = ['mail.thread']
	_description = 'Animal Registration'

	name = fields.Char(string="Name")

