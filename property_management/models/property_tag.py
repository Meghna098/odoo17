from odoo import fields, models


class PropertyTagModel(models.Model):
    _name = "property.tag"
    _description = "Tag Model"

    name = fields.Char(required=True)
