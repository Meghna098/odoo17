# -*- coding: utf-8 -*-
from odoo import api, fields, models
import io
import json
import xlsxwriter
from odoo.tools import date_utils
from odoo.exceptions import ValidationError


class PropertyWizard(models.TransientModel):
    _name = "property.wizard"

    property_id = fields.Many2one('property.management', string='Property')
    type = fields.Selection(
        string='Type',
        selection=[('rent', 'Rent'), ('lease', 'Lease')],
        default='rent')
    tenant_id = fields.Many2one("res.partner", string="Tenant")
    owner_id = fields.Many2one("res.partner", string="Owner")
    start_date = fields.Datetime()
    end_date = fields.Datetime()
    rent_states = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'), ('to approve', 'To Approve'), ('approved', 'Approved'),
                   ('confirmed', 'Confirmed'), ('closed', 'Closed'), ('returned', 'Returned'),
                   ('expired', 'Expired')])

    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError('Sorry, end date must be greater than start date...')

    def action_done(self):
        data = {'property': self.property_id.id,
                'type': self.type,
                'tenant': self.tenant_id.id,
                'owner': self.owner_id.id,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'state': self.rent_states}
        return self.env.ref('property_management.action_report_rental_form').report_action(None, data=data)

    def property_report_excel(self):
        data = {
                'property': self.property_id.id,
                'type': self.type,
                'tenant': self.tenant_id.id,
                'owner': self.owner_id.id,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'state': self.rent_states
        }

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'property.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Property Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response, where_clause=''):
        sub_where = []
        if data.get('property'):
            sub_where.append(f" pl.property_id = {data['property']}")
        if data.get('owner'):
            sub_where.append(f" pm.owner_id = {data['owner']}")
        if data.get('type'):
            sub_where.append(f" rm.type = '{data['type']}'")
        if data.get('tenant'):
            sub_where.append(f" rm.tenant_id = {data['tenant']}")
        if data.get('start_date'):
            sub_where.append(
                """rm.start_date >= '%s' and rm.end_date <= '%s'""" % (data['start_date'], data['end_date']))
        if data.get('state'):
            sub_where.append(f" rm.rent_states = '{data['state']}'")
        if sub_where:
            where_clause += 'WHERE %s' % ' AND '.join(sub_where)
        query = f"""select pm.name as property,ow.name as owner,rm.type,pa.name as tenant,rm.start_date,rm.end_date,
                                    case when rm.type = 'rent' then pm.rent
                                    else pm.legal_amount end as amount,rm.rent_states 
                                    from rental_management as rm
                                    inner join property_lines as pl on pl.property_details_id = rm.id 
                                    inner join property_management as pm on pm.id = pl.property_id 
                                    inner join res_partner as pa on pa.id = rm.tenant_id
                                    inner join res_partner as ow on ow.id = pm.owner_id {where_clause}"""
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('B2:J3', 'EXCEL REPORT', head)
        sheet.write('B5', 'No.', cell_format)
        sheet.write('C5', 'Property', cell_format)
        sheet.write('D5', 'Owner', cell_format)
        sheet.write('E5', 'Type', cell_format)
        sheet.write('F5', 'Tenant', cell_format)
        sheet.write('G5', 'Start Date', cell_format)
        sheet.write('H5', 'End date', cell_format)
        sheet.write('I5', 'Rent/Lease Amount', cell_format)
        sheet.write('J5', 'State', cell_format)
        row = 5
        number = 1
        for rec in report:
            sheet.set_column(0, 9, 17)
            sheet.set_row(row, 20)
            sheet.write(row, 1, number, txt)
            sheet.write(row, 2, rec['property'], txt)
            if not data['owner']:
                sheet.write(row, 3, rec['owner'], txt)
            sheet.write(row, 4, rec['type'], txt)
            sheet.write(row, 5, rec['tenant'], txt)
            sheet.write(row, 6, str(rec['start_date']), txt)
            sheet.write(row, 7, str(rec['end_date']), txt)
            sheet.write(row, 8, rec['amount'], txt)
            sheet.write(row, 9, rec['rent_states'], txt)
            row += 1
            number += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        if not report:
            raise ValidationError("""No Data\n""")
