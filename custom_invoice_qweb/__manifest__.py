{
    'name': 'Factura Personalizada',
    'version': '16.0',
    'summary': 'Factura con diseño personalizado en PDF usando QWeb',
    'description': """
Factura Personalizada QWeb
==========================

Este módulo permite generar facturas (account.move) con un diseño personalizado, similar a una imagen, utilizando plantillas QWeb en Odoo 16.

Características:
----------------
- Factura PDF con diseño personalizado tipo imagen.
- Plantillas flexibles y editables con QWeb.
- Totalmente integrado con el módulo de contabilidad (`account`).

Ideal para empresas que desean un formato de factura corporativo o con branding específico.
""",
    'category': 'Accounting/Invoicing',
    'author': 'JMA',
    'website': '',
    'license': 'AGPL-3',
    'maintainer': 'Luis Felipe Paternina',
    'depends': [
        'account',
    ],
    'data': [
        'views/report_templates.xml',
        'report/invoice_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
