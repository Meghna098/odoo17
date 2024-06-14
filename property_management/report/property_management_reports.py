# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PropertyManagementReports(models.AbstractModel):
    _name = "report.property_management.report_property"
    _description = 'print pdf reports'

    @api.model
    def _get_report_values(self, docids, data=None, where_clause=''):
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
            sub_where.append("""rm.start_date >= '%s' and rm.end_date <= '%s'""" % (data['start_date'], data['end_date']))
        if data.get('state'):
            sub_where.append(f" rm.rent_states = '{data['state']}'")
        if sub_where:
            where_clause += 'WHERE %s' % ' AND '.join(sub_where)

        query = f"""select pm.name as property,ow.name as owner,rm.type,pa.name as tenant,rm.start_date,rm.end_date,
                                      pm.rent,pm.legal_amount,rm.rent_states from rental_management as rm
                                      inner join property_lines as pl on pl.property_details_id = rm.id 
                                      inner join property_management as pm on pm.id = pl.property_id 
                                      inner join res_partner as pa on pa.id = rm.tenant_id
                                      inner join res_partner as ow on ow.id = pm.owner_id {where_clause}"""
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()

        if report:
            for rec in report:
                rec['prop_type'] = dict(self.env['rental.management']._fields['type'].selection).get(rec['type'])
                rec['prop_state'] = dict(self.env['rental.management']._fields['rent_states'].selection).get(
                    rec['rent_states'])
            return {
                'doc_model': 'rental.management',
                'docs': report,
                'data': data,
            }
        else:
            raise ValidationError("""No Data\n""")
