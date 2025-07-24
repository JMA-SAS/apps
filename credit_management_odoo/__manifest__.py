{
    'name': 'Credit Management Odoo',
    'version': '1.0',
    'category': 'Sales/Accounting',
    'summary': 'Custom module for credit management integrated with contacts.',
    'description': """
        This module provides custom credit management functionalities for Odoo 17,
        integrated with the native contacts module. It includes:
        - Credit limit and validation fields on customer contacts.
        - Informative alerts during invoicing if credit limit is exceeded.
        - Multi-currency support for credit calculations.
        - General report for customers with credit.
        - Role-based permissions for credit management features.
    """,
    'author': 'JMA',
    "website": "https://sites.google.com/jmasas.com/jma",
    'depends': ['contacts', 'account', 'base'],
    'data': [
        'security/credit_security.xml',
        'security/ir.model.access.csv',
        'views/credit_management_views.xml',
        'views/account_move_views.xml',

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
