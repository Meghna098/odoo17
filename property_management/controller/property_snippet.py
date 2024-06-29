from odoo import http


class PropertySnippet(http.Controller):
    @http.route(['/latest_properties'], type="json", auth="public", website=True, methods=['POST'])
    def all_properties(self):
        properties = http.request.env['property.management'].search_read(
             [('website_published', '=', True)], ['name', 'id'], order='create_date desc', limit=4)
        return properties
