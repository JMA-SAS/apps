{
    'name': 'Factura Autoenvío',
    'version': '16.0',
    'summary': 'Envía automáticamente las facturas por correo al validarlas:',
    'description': """
Factura Autoenvío
=================

Este módulo permite que, al validar una factura de cliente (`account.move`), 
esta se envíe automáticamente al cliente mediante correo electrónico usando 
la plantilla estándar de Odoo o una definida por el usuario.

Características:
----------------
- Envío automático de facturas de cliente al validar.
- Uso de plantillas de correo configurables en Odoo.
- Integración con el módulo de contabilidad (`account`) y mensajería (`mail`).
- Reduce pasos manuales y mejora la automatización del ciclo de facturación.

Ideal para empresas que desean agilizar el proceso de entrega de facturas a sus clientes.
""",
    'category': 'Accounting/Invoicing',
    'author': 'JMA',
    'website': '',
    'license': 'LGPL-3',
    'maintainer': 'JMA',
    'depends': [
        'account',
        'mail',
    ],
    'data': [
        # 'data/mail_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/chatter.png'],
}
