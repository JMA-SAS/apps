{
    "name": "MRP Production Report",
    "version": "18.0",
    "author": "JMA",
    "website": "https://sites.google.com/jmasas.com/jma",
    "depends": ["mrp", "sale_management", "stock"],
    "category": "Manufacturing",
    "summary": "Genera reportes detallados y personalizados de órdenes de producción",
    "description": """
Este módulo extiende la funcionalidad del módulo de Manufactura (MRP) en Odoo, 
permitiendo generar reportes PDF personalizados para las órdenes de producción.

Características principales:
- Reporte en formato PDF con diseño personalizado.
- Incluye información relacionada con ventas, cantidades, y productos.
- Integra datos de manufactura, inventario y ventas.
- Ideal para seguimiento y trazabilidad de procesos productivos.

Requisitos:
- Módulos base: mrp, sale_management y stock.

Desarrollado por: JMA
    """,
    "data": [
        "reports/mrp_production_report_template.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}

