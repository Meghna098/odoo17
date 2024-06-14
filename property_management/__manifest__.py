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
        'report/property_management_reports.xml',
        'report/property_management_templates.xml',
        'report/paperformat_property_report.xml',
    ],
    'assets': {
            'web.assets_backend': [
                'property_management/static/src/js/action_manager.js'
            ]
    },
    'demo': [
        'demo/demo_data.xml',
    ],
}
