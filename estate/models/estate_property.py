from odoo import fields, models


class TestModel(models.Model):
    _name = "estate.property"
    _description = "Estate Model"

    name = fields.Char(required=True)
    property_type = fields.Many2one("estate.property.type", string="Property Type", copy="False")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer received', 'Offer received'), ('offer accepted', 'Offer accepted'),
                   ('sold', 'Sold'), ('cancelled', 'Cancelled')], default='new', required=True)
    active = fields.Boolean(default=True)
    user_id = fields.Many2one('res.users', string='Salesman', index=True, tracking=True,
                              default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Partner", copy="False")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer = fields.One2many("estate.property.offer", "property_id")
