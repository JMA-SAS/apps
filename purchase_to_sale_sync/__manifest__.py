# -*- coding: utf-8 -*-
{
    'name': 'Purchase to Sale Sync',
    'version': '17.0',
    'summary': 'Sincroniza una orden de compra como orden de venta en otra instancia Odoo',
    'category': 'Purchase',
    'author': 'JMA',
    'website': 'https://sites.google.com/jmasas.com/jma',
    'license': 'LGPL-3',
    'depends': ['purchase', 'sale'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    "images": ["static/description/icon.png"],
    'installable': True,
    'license': 'LGPL-3',
}
