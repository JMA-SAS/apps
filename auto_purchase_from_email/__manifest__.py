{
    "name": "Auto Purchase from Email",
    "version": "1.0.0",
    "summary": "Crea automáticamente contactos y órdenes de compra desde correos electrónicos con PDF",
    "description": """
Procesamiento automático de correos entrantes para compras.

Este módulo permite capturar correos electrónicos dirigidos al área de compras,
analizar archivos PDF adjuntos y generar automáticamente órdenes de compra 
y contactos de proveedores si no existen previamente.

Características:
- Lectura automática de correos entrantes con adjuntos PDF.
- Extracción de productos, precios y cantidades desde el PDF.
- Creación automática de órdenes de compra.
- Asociación o creación del proveedor a partir del correo.
    """,
    "author": "JMA",
    "website": "https://sites.google.com/jmasas.com/jma",
    "category": "Purchases",
    "version": "18.0",
    "license": "LGPL-3",
    "depends": [
        "purchase",
        "account",
        "mail"
    ],
    "data": [
        "views/mail_purchase_inbox.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": False,
    "auto_install": False,
}
