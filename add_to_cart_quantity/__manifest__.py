{
    'name': 'Add to Cart Quantity',
    'depends': ['base', 'website'],
    'author': "New Author",
    'category': 'New Category',
    'description': """
       Description text
       """,
    'application': 'False',
    'data': [
        'views/website_quantity.xml',
        'views/website_snippets_quantity.xml',
        'views/products_quantity.xml'
    ],
    'assets': {
                'web.assets_backend': [

                ],
                'web.assets_frontend': [
                    # 'add_to_cart_quantity/static/src/js/snippet_quantity.js',
                ],
        },
}