from odoo import fields, models


class EstateOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "estate Offer Model"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", string="Partner", copy="False")
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')], required=True, copy="False")
    property_id = fields.Many2one("estate.property", string="Property ID", required=True)
