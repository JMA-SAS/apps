{
    "name": "Invoice Report Wizard",
    "version": "17.0.1.0.0",
    "summary": "Genera un informe consolidado de facturas (Contabilidad + POS)",
    "description": """
Módulo desarrollado para JMA SAS.

Permite generar un informe consolidado de facturas emitidas desde la Contabilidad (Account Move) y desde el Punto de Venta (POS Order), en un rango de fechas seleccionado.

Características:
- Nuevo menú en Contabilidad > Informes
- Wizard con selección de rango de fechas
- Opción para visualizar resultados en pantalla (vista tipo tree)
- Opción para generar el informe en PDF
- Incluye información del cliente, diario, medio de pago y nombre de factura

Desarrollado por Servicios de Ingeniería JMA.
""",
    "author": "JMA",
    "website": "https://sites.google.com/jmasas.com/jma",
    "category": "Accounting",
    "license": "LGPL-3",
    "depends": [
        "account",
        "point_of_sale"
    ],
    "data": [

        "security/ir.model.access.csv",
        "views/invoice_report_views.xml",
        "views/menu.xml",
        "reports/invoice_report_templates.xml",
        "reports/report_invoice_consolidated_template.xml",

    ],
    "images": ["static/description/imagen.png"],
    "installable": True,
    "application": False,
    "auto_install": False,
}

