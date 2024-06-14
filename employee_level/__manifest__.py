{
    'name': 'Employee Level',
    'version': '1.0',
    'depends': ['base','hr'],
    'author': "Author",
    'category': 'Category',
    'description': """
    Description text
    """,
    'application':'True',
    'data': [
        'security/ir.model.access.csv',
        'views/employee_level.xml',
        'views/employee_menus.xml',
        'views/employees.xml'
    ],
}
