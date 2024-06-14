from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    related_records_id = fields.Many2one('rental.management', string="Related Record")

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for rec in self:
            self.env['rental.management'].search([('id', '=', rec.related_records_id.id)]).action_track_invoice(
                    body=f'Invoice is in {self.state}')
        return res
