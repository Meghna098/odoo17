from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    owned_property_id = fields.One2many('property.management', 'owner_id', string="Property")
