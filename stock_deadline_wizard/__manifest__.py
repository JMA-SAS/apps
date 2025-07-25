{
    'name': 'Stock Deadline Wizard',
    'version': '18.0',
    'summary': 'Modificar la fecha límite de los albaranes mediante un asistente',
    'description': '''
Este módulo permite modificar la fecha límite (`scheduled_date`) de los albaranes
desde un asistente tipo wizard, facilitando la gestión de entregas o recepciones
en el módulo de Inventario.
''',
    'category': 'Inventory/Operations',
    'author': 'JMA',
    'website': 'https://sites.google.com/jmasas.com/jma',
    'license': 'LGPL-3',
    'depends': ['stock'],
    'data': [

        'security/ir.model.access.csv',
        'views/stock_picking.xml',
        'wizard/change_deadline_wizard_view.xml',
        
    ],
    "images": ["static/description/icon.png"],
    'installable': True,
    'application': False,
    'auto_install': False,
}
