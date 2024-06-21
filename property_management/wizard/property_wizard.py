# -*- coding: utf-8 -*-
from odoo import fields, models
import io
import json
import xlsxwriter
from odoo.tools import date_utils
from datetime import date
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
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError('Sorry, end date must be greater than start date...')
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
            sub_where.append(f" rm.start_date >= '{data['start_date']}'")
        if data.get('end_date'):
            sub_where.append(f" rm.end_date <= '{data['end_date']}'")
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
        cell_format = workbook.add_format({'font_size': '11px', 'align': 'center', 'bold': True})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.write('A1', 'Printed Date:' + str(date.today()), txt)
        sheet.merge_range('B1:G3', 'EXCEL REPORT', head)
        sheet.merge_range('H1:I1', self.env.company.name, txt)
        sheet.merge_range('H2:I2', self.env.company.email, txt)
        sheet.merge_range('H3:I3', self.env.company.phone, txt)

        sheet.set_column('A:A', 19)
        sheet.set_column('B:B', 18)
        sheet.set_column('C:C', 18)
        sheet.set_column('D:D', 18)
        sheet.set_column('E:E', 18)
        sheet.set_column('F:F', 18)
        sheet.set_column('G:G', 18)
        sheet.set_column('H:H', 18)
        sheet.set_column('I:I', 18)

        if data['property']:
            sheet.write('A4', 'Property:' + self.env['property.management'].search([
                ('id', '=', data['property'])]).name, cell_format)
            sheet.set_column('B:B', None, None, {"hidden": True})
        else:
            sheet.set_row(3, None, None, {"hidden": True})
        if data['owner']:
            sheet.write('A5', 'Owner:' + self.env['res.partner'].search([('id', '=', data['owner'])]).name, cell_format)
            sheet.set_column('C:C', None, None, {"hidden": True})
        else:
            sheet.set_row(4, None, None, {"hidden": True})
        if data['type']:
            sheet.write('A6', 'Type:' + dict(self.env['rental.management']._fields['type'].selection).get(
                data['type']), cell_format)
            sheet.set_column('D:D', None, None, {"hidden": True})
        else:
            sheet.set_row(5, None, None, {"hidden": True})
        if data['tenant']:
            sheet.write('A7', 'Tenant:' + self.env['res.partner'].search([('id', '=', data['tenant'])]).name, txt)
            sheet.set_column('E:E', None, None, {"hidden": True})
        else:
            sheet.set_row(6, None, None, {"hidden": True})
        if data['state']:
            sheet.write('A8', 'State:' + dict(self.env['rental.management']._fields['rent_states'].selection).get(
                data['state']), cell_format)
            sheet.set_column('I:I', None, None, {"hidden": True})
        else:
            sheet.set_row(7, None, None, {"hidden": True})

        sheet.write('A10', 'No.', cell_format)
        if not data['property']:
            sheet.write('B10', 'Property', cell_format)
        if not data['owner']:
            sheet.write('C10', 'Owner', cell_format)
        if not data['type']:
            sheet.write('D10', 'Type', cell_format)
        if not data['tenant']:
            sheet.write('E10', 'Tenant', cell_format)
        sheet.write('F10', 'Start Date', cell_format)
        sheet.write('G10', 'End date', cell_format)
        sheet.write('H10', 'Rent/Lease Amount', cell_format)
        if not data['state']:
            sheet.write('I10', 'State', cell_format)

        row = 10
        number = 1
        for rec in report:
            sheet.set_row(row, 20)
            sheet.write(row, 0, number, txt)
            if not data['property']:
                sheet.write(row, 1, rec['property'], txt)
            if not data['owner']:
                sheet.write(row, 2, rec['owner'], txt)
            if not data['type']:
                sheet.write(row, 3, dict(self.env['rental.management']._fields['type'].selection).get(rec['type']), txt)
            if not data['tenant']:
                sheet.write(row, 4, rec['tenant'], txt)
            sheet.write(row, 5, str(rec['start_date']), txt)
            sheet.write(row, 6, str(rec['end_date']), txt)
            sheet.write(row, 7, rec['amount'], txt)
            if not data['state']:
                sheet.write(row, 8, dict(self.env['rental.management']._fields['rent_states'].selection).get(
                    rec['rent_states']), txt)
            row += 1
            number += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        if not report:
            raise ValidationError("""No Data\n""")
