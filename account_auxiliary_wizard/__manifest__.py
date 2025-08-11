# -*- coding: utf-8 -*-
{
    'name': 'Account Auxiliary Report',
    'version': '17.0.1.0.0',
    'summary': 'Reporte auxiliar contable con filtros por cuenta, fechas y socios',
    'description': """
        Este módulo agrega un asistente (wizard) que permite generar un reporte auxiliar contable 
        con múltiples filtros como fechas, cuentas contables y socios. 
        Permite visualizar el reporte en HTML o exportarlo en formato Excel (.xlsx).
    """,
    'category': 'Accounting/Reports',
    'author': 'JMA',
    'website': 'https://sites.google.com/jmasas.com/jma',
    'license': 'LGPL-3',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_auxiliary_doc_line.xml',
        'wizard/account_auxiliary_wizard_view.xml',
        'reports/report_account_auxiliary_template.xml',
        'reports/ir_actions_report.xml',
    ],
    "images": ["static/description/icon.png"],
    'application': False,
    'installable': True,
    'auto_install': False,
}
