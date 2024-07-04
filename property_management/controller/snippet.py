# -*- encoding: utf-8 -*-
from odoo.http import request, Controller, route


class PropertySnippet(Controller):
    @route('/latest_properties', type='json', auth='public', website=True)
    def all_properties(self):
        properties = request.env['property.management'].sudo().search_read([], order='create_date desc')
        return properties

    @route('/property_details/<int:item_id>', auth='public', website=True)
    def web_details_form(self, item_id):
        property_details = request.env['property.management'].sudo().browse(item_id)
        return request.render('property_management.web_snippet_card_details', {
            'property': property_details
        })
