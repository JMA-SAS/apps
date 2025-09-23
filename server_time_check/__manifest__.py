# -*- coding: utf-8 -*-
{
    "name": "Server Time Check",
    "version": "17.0.1.0.0",
    "summary": "Consulta y visualiza la hora del servidor, Odoo y PostgreSQL.",
    "description": """
Server Time Check
=================
Este módulo permite consultar y mostrar tres valores de tiempo en Odoo:

- **Hora del Servidor**: obtenida desde el sistema operativo.
- **Hora de Odoo**: calculada con `fields.Datetime.now()`.
- **Hora de PostgreSQL**: obtenida directamente con `SELECT NOW()`.

Características
---------------
- Menú dedicado en Odoo para visualizar las horas.
- Seguridad configurable por grupos.
- Modelo transitorio para evitar acumulación de registros.
    """,
    "author": "JMA",
    "maintainers": ["JMA"],
    "website": "https://fsf3cj7zbi8.cloudpepper.site/",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": [
        "base",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/server_time_views.xml",
    ],
    "images": [
        "static/description/icon.png",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
