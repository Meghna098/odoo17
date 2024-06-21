from odoo.http import request, Controller, route


class WebFormController(Controller):
    @route('/webform', auth='public', website=True)
    def web_form(self, **kwargs):
        rental_details = request.env['rental.management'].sudo().search([])
        property_details = request.env['property.management'].sudo().search([])
        print(rental_details)
        print(property_details)
        return request.render('property_management.web_form_template', {
            'rent_details': rental_details,
            'prop_details': property_details
        })

    @route('/web_details/<int:id>', auth='public', website=True)
    def web_details_form(self, id):
        print(id)
        prop_web_details = request.env['rental.management'].browse(id)
        return request.render('property_management.web_details_form_template', {
            'web_details': prop_web_details
        })

    @route('/new_form', auth='public', website=True)
    def web_details_form(self, **kwargs):
        return request.render('property_management.new_web_form_template')


    # @route('/webform', auth='public', website=True)
    # def create(self, **kwargs):
    #     return request.render('property_management.web_form_template')
    #
    # @route('/webform/submit', type='http', auth='public', website=True, methods=['POST'])
    # def web_form_submit(self, **post):
    #     request.env['custom.web.form.property'].sudo().create({
    #                 'name': post.get('name'),
    #                 'type': post.get('type'),
    #                 'tenant_name': post.get('tenant_name'),
    #                 'start_date': post.get('start_date'),
    #                 'end_date': post.get('end_date'),
    #                 'state': post.get('rent_states'),
    #             })
    #     return request.redirect('/thank-you-page')
