{
    'name': 'Property Management',
    'version': '1.0',
    'depends': ['base', 'mail', 'account', 'sale'],
    'author': "New Author",
    'category': 'New Category',
    'description': """
       Description text
       """,
    'application': 'True',
    'data': [
        'security/ir.model.access.csv',
        'security/user_groups.xml',
        'data/rental_sequence.xml',
        'data/email_template.xml',
        'data/expiry_scheduler.xml',
        'views/property_management_views.xml',
        'views/rental_management_views.xml',
        'views/property_tag_views.xml',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
        'wizard/property_wizard_views.xml',
        'views/property_management_menus.xml',

        'views/website_menus.xml',
        'views/property_web_template.xml',
        'views/property_web_details_template.xml',
        'views/property_new_web_form_template.xml',
        'views/new_customer.xml',
        'views/thank_you_form_template.xml',
        'views/property_invoice_template.xml',
        'views/website_snippet.xml',
        'views/website_snippet_template.xml',

        'report/property_management_reports.xml',
        'report/property_management_templates.xml',
        'report/paperformat_property_report.xml',
    ],
    'assets': {
            'web.assets_backend': [
                'property_management/static/src/js/action_manager.js',
            ],
            'web.assets_frontend': [
                'property_management/static/src/css/property_style_sheet.css',
                'property_management/static/src/js/property_action_manager.js',
                'property_management/static/src/js/property_action_snippet.js',
                'property_management/static/src/xml/property_snippet_templates.xml',
            ],
    },
    'demo': [
        'demo/demo_data.xml',
    ],
}
