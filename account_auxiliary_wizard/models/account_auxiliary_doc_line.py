from odoo import models, fields, api

class AccountAuxiliaryDocLine(models.Model):
    _name = 'account.auxiliary.doc.line'
    _description = 'Línea de Auxiliar Contable'

    move_id = fields.Many2one('account.move', string='Asiento')
    move_line_name = fields.Char(string='Línea')
    date = fields.Date(string='Fecha')
    journal_id = fields.Many2one('account.journal', string='Diario')
    account_id = fields.Many2one('account.account', string='Cuenta')
    partner_id = fields.Many2one('res.partner', string='Tercero')
    partner_name = fields.Char(string='Nombre del Tercero')
    partner_vat = fields.Char(string='NIT')
    sequence = fields.Integer(string='Posición')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Cuenta Analítica')
    analytic_tag_origin_id = fields.Many2one('account.analytic.tag', string='Origen')
    analytic_tag_dest_id = fields.Many2one('account.analytic.tag', string='Destino')
    initial_balance = fields.Monetary(string='Saldo Inicial')
    debit = fields.Monetary(string='Débito')
    credit = fields.Monetary(string='Crédito')
    balance = fields.Monetary(string='Saldo Final')
    currency_id = fields.Many2one('res.currency', string='Moneda')
    analytic_distribution_html = fields.Html(string="Distribución Analítica")
    code = fields.Char(string="Código")
