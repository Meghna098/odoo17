from odoo.http import request, Controller, route
from odoo import Command


class WebFormController(Controller):
    @route('/webform', auth='public', website=True)
    def web_form(self, **kwargs):
        new_tenant_id = request.env.user.partner_id.id
        property_details = request.env['property.management'].sudo().search([])
        rental_details = request.env['rental.management'].sudo().search([('tenant_id', '=', new_tenant_id)])
        return request.render('property_management.web_form_template', {
            'rent_details': rental_details,
            'prop_details': property_details
        })

    @route('/web_details/<int:id>', auth='public', website=True)
    def web_details_form(self, id):
        prop_web_details = request.env['rental.management'].sudo().browse(id)
        return request.render('property_management.web_details_form_template', {
            'web_details': prop_web_details
        })

    @route('/new_form', auth='public', website=True)
    def new_web_form(self, **kwargs):
        properties = request.env['property.management'].sudo().search([])
        tenant_details = request.env['res.partner'].sudo().search([])
        print(tenant_details)
        return request.render('property_management.new_web_form_template', {
            'properties': properties,
            'tenant': tenant_details
        })

    @route('/webform_submit', type='json', auth='public', website=True)
    def web_form_submit(self, **post):
        new_property = post.get('properties')
        request.env['rental.management'].sudo().create({
            'property_ids': [Command.create({
                'property_id': int(rec),
            })for rec in new_property],
            'type': post.get('type'),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
            'tenant_id': post.get('tenant'),
            'rent_lease_amount': post.get('rent_lease_amount'),
        })

    @route('/new_customer', type='http', auth='public', website=True)
    def new_customer_form(self):
        return request.render('property_management.new_customer_template')

    @route('/new_customer_submit', type='http', auth='public', website=True)
    def new_customer_submit(self, **post):
        request.env['res.partner'].sudo().create({
             'name': post.get('cust_name'),
             'email': post.get('cust_email')
        })
        return request.redirect('/new_form')

    @route('/thank_you', type='http', auth='public', website=True)
    def thank_you_form(self):
        return request.render('property_management.thank_you_template')


