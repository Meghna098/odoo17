{
    'name': 'estate',
    'version': '1.0',
    'depends': ['base'],
    'author': "John",
    'category': 'Category',
    'description': """
    Description text
    """,
    'application':'True',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [

    ],
}
