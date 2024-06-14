from odoo import fields, models


class NewModel(models.Model):
    _name = "estate.property.type"
    _description = "estate property Model"

    name = fields.Char(required=True)

