from odoo import fields, models


class EstateTypeModel(models.Model):
    _name = "estate.property.tag"
    _description = "estate Tag Model"

    name = fields.Char(required=True)
