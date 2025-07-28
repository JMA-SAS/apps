{
    "name": "Documento de Entrega Personalizado",
    "version": "17.0.1.0.0",
    "category": "Stock",
    "summary": "Personalización del reporte de entrega (albarán) en Odoo",
    "author": "JMA",
    "website": "",
    "license": "LGPL-3",
    "depends": ["stock"],
    "data": [
        'report/report.xml',
        'report/report_template.xml',
    ],
    "description": """
Custom Delivery Report - Documento de Entrega Personalizado

Este módulo permite personalizar completamente el reporte QWeb `stock.report_delivery_document` en Odoo, mejorando la presentación del albarán o documento de entrega impreso. Desarrollado por Luis Felipe Paternina Vital, ofrece una base profesional y escalable para adaptar el formato de entregas a las necesidades reales de cada empresa.

Características destacadas:
- Hereda y modifica el QWeb original `stock.report_delivery_document`.
- Añade nuevas columnas, como el código interno del producto.
- Permite cambiar encabezados, títulos, estilos y contenido dinámico.
- Compatible con Odoo 17 Community y Enterprise.
- Ideal para empresas que desean reportes claros, organizados y personalizados para logística o clientes.

Fácil de extender:
Este módulo está preparado para añadir más campos como ubicación, firma, totales, lotes/seriales o cualquier información de picking.

Autor:
JMA
Cel: +57 3215062353

Requiere:
- Módulo base `stock`.
    """,
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": False,
}
