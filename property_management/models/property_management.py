from odoo import fields, models


class PropertyModel(models.Model):
    _name = "property.management"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Property Model"

    name = fields.Char(required=True, ondelete="cascade")
    build_date = fields.Date(default=fields.Date.today())
    can_be_sold = fields.Boolean()
    legal_amount = fields.Monetary()
    rent = fields.Monetary()
    currency_id = fields.Many2one('res.currency', string="Currency")
    status = fields.Selection(
        string='Status',
        selection=[('draft', 'Draft'), ('rented', 'Rented'), ('leased', 'Leased'), ('sold', 'Sold')],
        copy=False, default='draft', tracking=True)
    description = fields.Text()
    owner_id = fields.Many2one("res.partner", string="Owner")
    address = fields.Char()
    country_id = fields.Many2one('res.country', "Country")
    state_id = fields.Many2one('res.country.state', "State")
    street = fields.Char()
    image = fields.Binary("Image")
    tag_ids = fields.Many2many("property.tag", "property_tag_rel", string="Facilities")
    property_count = fields.Integer(compute='_compute_count')
    active = fields.Boolean(default=True)

    def _compute_count(self):
        for record in self:
            record.property_count = self.env['rental.management'].search_count(
                [('property_ids.property_id', '=', record.name)])

    def action_count(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rent/Lease',
            'view_mode': 'tree,form',
            'res_model': 'rental.management',
            'domain': [('property_ids.property_id', '=', self.name)],
            'context': "{'create': True}"
        }
