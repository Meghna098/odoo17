from odoo import fields, models


class PropertyLinesModel(models.Model):
    _name = "property.lines"
    _description = "Property Line Model"

    property_id = fields.Many2one('property.management', string="Property")
    property_rent_amount = fields.Monetary(string="Rent Amount", related='property_id.rent', readonly=False)
    property_lease_amount = fields.Monetary(string="Lease Amount", related='property_id.legal_amount', readonly=False)
    currency_id = fields.Many2one('res.currency', string="Currency")
    property_details_id = fields.Many2one('rental.management', string="Property details")
