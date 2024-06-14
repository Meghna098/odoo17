from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    active_credit_limit = fields.Boolean(string="Active credit limit")
    customer_warning_amount = fields.Integer(string="Warning Amount")
    customer_blocking_amount = fields.Integer(string="Blocking Amount")
