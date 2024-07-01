# -*- encoding: utf-8 -*-
from odoo import http


class PropertySnippet(http.Controller):
    @http.route(['/latest_properties'], type="json", auth="public", website=True)
    def all_properties(self):
        print('hiii')
        properties = http.request.env['property.management'].search_read(
             [('website_published', '=', True)], ['name', 'id', 'image_1920'], order='create_date desc', limit=4)
        # return properties
