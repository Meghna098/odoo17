from odoo import models, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        due_amount = self.amount_calc()
        if due_amount > self.partner_id.customer_warning_amount > 0:
            res = {'warning': {
                'title': "Customer Warning",
                'message': 'Customer has reached his credit limit'
            }}
            return res

    def action_confirm(self):
        due_amount = self.amount_calc()
        if due_amount > self.partner_id.customer_blocking_amount > 0:
            raise ValidationError('This customer is blocked')
        return super().action_confirm()

    def amount_calc(self):
        total = 0
        partner = self.partner_id
        if partner.active_credit_limit:
            amount = self.env['account.move'].search(
                [('partner_id', '=', self.partner_id.id), ('payment_state', 'in', ['not_paid']),
                 ('move_type', 'in', ['out_invoice'])])
            for rec in amount:
                total = total + rec.amount_residual
        return total

