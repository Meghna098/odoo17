from odoo import api, Command, fields, models
from datetime import datetime
from odoo.exceptions import ValidationError


class RentalModel(models.Model):
    _name = "rental.management"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Rental Model"
    _rec_name = 'sequence_no'

    sequence_no = fields.Char(default='New', String='Number', copy=False, readonly=True)
    property_ids = fields.One2many('property.lines', 'property_details_id', string='Property')
    type = fields.Selection(
        string='Type',
        selection=[('rent', 'Rent'), ('lease', 'Lease')])
    tenant_id = fields.Many2one("res.partner", string="Tenant")
    rent_lease_amount = fields.Monetary(compute='_compute_calculate_amount', store=True)
    currency_id = fields.Many2one('res.currency', string="Currency")
    start_date = fields.Datetime()
    end_date = fields.Datetime()
    total_days = fields.Integer()
    rent_states = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'), ('to approve', 'To Approve'), ('approved', 'Approved'),
                   ('confirmed', 'Confirmed'), ('closed', 'Closed'), ('returned', 'Returned'),
                   ('expired', 'Expired')],
        copy=False, default='draft', tracking=True)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)
    invoice_count = fields.Integer("Invoice Count", compute="_compute_invoice_count")
    invoice_ids = fields.One2many("account.move", "related_records_id")
    related_invoice_id = fields.Many2one("account.move", String="Invoice")
    pay_state = fields.Selection(String="Payment State", related="related_invoice_id.payment_state")
    invoice_state = fields.Selection(related="related_invoice_id.state")

    @api.model
    def create(self, vals):
        vals['sequence_no'] = self.env['ir.sequence'].next_by_code('rental_sequence_code')
        return super(RentalModel, self).create(vals)

    @api.onchange('start_date', 'end_date', 'total_days')
    def _onchange_total_days(self):
        if self.start_date and self.end_date:
            start_day = datetime.strptime(str(self.start_date.date()), '%Y-%m-%d')
            end_day = datetime.strptime(str(self.end_date.date()), '%Y-%m-%d')
            total = end_day - start_day
            self.total_days = total.days

    @api.depends('type', 'property_ids')
    def _compute_calculate_amount(self):
        for record in self:
            if record.type in ['rent']:
                record.rent_lease_amount = sum(record.property_ids.mapped('property_rent_amount'))
            elif record.type in ['lease']:
                record.rent_lease_amount = sum(record.property_ids.mapped('property_lease_amount'))
            else:
                record.rent_lease_amount = 0

    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = self.env['account.move'].search_count(
                [('related_records_id', '=', record.id)])

    def action_draft(self):
        self.write({'rent_states': 'draft'})

    def action_request(self):
        self.write({'rent_states': 'to approve'})

    def action_approve(self):
        self.write({'rent_states': 'approved'})

    def action_confirm(self):
        self.write({'rent_states': 'confirmed'})

        if self.env['ir.attachment'].search([('res_model', '=', self._name), ('res_id', '=', self._ids)]):
            self.rent_states = "confirmed"
        else:
            raise ValidationError("Please add attachments")

        for rec in self.env['property.management'].search(
                [('id', 'in', [rec.property_id.id for rec in self.property_ids])]):
            rec.status = 'rented' if self.type == 'rent' else 'leased'

        mail_template = self.env.ref('property_management.property_email_template')
        mail_template.send_mail(self.id, force_send=True)

    def action_close(self):
        self.write({'rent_states': 'closed'})
        mail_template = self.env.ref('property_management.property_email_template')
        mail_template.send_mail(self.id, force_send=True)

    def action_return(self):
        self.write({'rent_states': 'returned'})

    def action_expire(self):
        self.write({'rent_states': 'expired'})
        mail_template = self.env.ref('property_management.property_email_template')
        mail_template.send_mail(self.id, force_send=True)

    def action_date_expiry(self):
        for rec in self.env['rental.management'].search([]):
            if rec.end_date and rec.end_date <= datetime.today():
                rec.action_expire()

    def action_create_invoice(self):
        if self.env['account.move'].search([('related_records_id', '=', self.id)]):
            self.env['account.move'].search([('related_records_id', '=', self.id)]).update({
                'invoice_line_ids': [(fields.Command.clear())]
            })
            self.env['account.move'].search([('related_records_id', '=', self.id)]).write({
                'partner_id': self.tenant_id.id,
                'invoice_line_ids': [Command.create(
                    {
                        'name': self.env['property.management'].search([('id', '=', record.property_id.id)]).name,
                        'price_unit': record.property_rent_amount if self.type == 'rent'
                        else record.property_lease_amount
                    }) for record in self.property_ids]})
            new_invoice = self.env['account.move'].search([('related_records_id', '=', self.id)])
        else:
            new_invoice = self.env['account.move'].create([
                {
                    'move_type': 'out_invoice',
                    'invoice_date': fields.Date.context_today(self),
                    'partner_id': self.tenant_id.id,
                    'invoice_date_due': self.end_date,
                    'related_records_id': self.id,
                    'invoice_line_ids': [Command.create(
                        {
                            'name': self.env['property.management'].search(
                                [('id', '=', record.property_id.id)]).name,
                            'price_unit': record.property_rent_amount if self.type == 'rent'
                            else record.property_lease_amount
                        }) for record in self.property_ids
                    ],
                },
            ])
            self.related_invoice_id = new_invoice.id

        return {
            'name': 'Invoice',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'current',
            'view_type': 'form',
            'res_id': new_invoice.id
        }

    def action_view_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('related_records_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def action_track_invoice(self, body):
        for rec in self:
            rec.message_post(body=body)
