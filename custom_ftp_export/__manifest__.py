{
    'name': 'Exportador FTP: Inventario y Ventas Diarias',
    'version': '17.0',
    'summary': 'Exporta automáticamente el inventario y ventas diarias a un servidor FTP.',
    'description': """
Este módulo genera archivos CSV con:
- Inventario actual por producto
- Ventas diarias por producto (cantidad y total)

Los archivos se suben automáticamente a un servidor FTP mediante una acción programada.
""",
    'author': 'JMA',
    'website': 'https://sites.google.com/jmasas.com/jma',
    'category': 'Tools',
    'license': 'LGPL-3',
    'price': 100.00,
    'currency': 'USD',
    'depends': ['stock', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/ftp_exporter_views.xml',
        'views/ftp_menu.xml',
        'views/ftp_exporter_history_views.xml',
        'views/res_config_settings_views.xml',
    ],
    "images": ["static/description/icon.png"],
    'installable': True,
    'application': False,
    'auto_install': False,
}