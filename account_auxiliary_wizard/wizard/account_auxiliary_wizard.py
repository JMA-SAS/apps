# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime

class AccountAuxiliaryWizard(models.TransientModel):
    _name = 'account.auxiliary.wizard'
    _description = 'Asistente de Balance Auxiliar'

    report_type = fields.Selection([
        ('summary', 'Resumen'),
        ('detail', 'Detalle'),
    ], string='Tipo de Reporte', default='summary')

    date_from = fields.Date(string='Fecha Inicial', required=True)
    date_to = fields.Date(string='Fecha Final', required=True)

    group_by_partner = fields.Boolean(string='Agrupar por Tercero', default=False)
    line_state = fields.Selection([
        ('draft', 'Borrador'),
        ('posted', 'Publicado'),
        ('all', 'Todos'),
    ], string='Estado de Línea', default='posted')

    currency_by = fields.Boolean(string='Convertir a Moneda de la Compañía')
    no_zero = fields.Boolean(string='Omitir Saldos en Cero')
    account_by = fields.Boolean(string='Agrupar por Cuenta')
    partner_by = fields.Boolean(string='Agrupar por Tercero')
    group_by = fields.Boolean(string='Agrupar Líneas')

    accounts_ids = fields.Many2many('account.account', string='Cuentas')
    partners_ids = fields.Many2many('res.partner', string='Terceros')

    def preview_html(self):
        self.ensure_one()

        domain = []

        if self.accounts_ids:
            domain.append(('account_id', 'in', self.accounts_ids.ids))
        if self.partners_ids:
            domain.append(('partner_id', 'in', self.partners_ids.ids))
        if self.date_from and self.date_to:
            domain.append(('date', '>=', self.date_from))
            domain.append(('date', '<=', self.date_to))
        if self.line_state == 'posted':
            domain.append(('move_id.state', '=', 'posted'))
        elif self.line_state == 'draft':
            domain.append(('move_id.state', '=', 'draft'))

        move_lines = self.env['account.move.line'].search(domain)

        self.env['account.auxiliary.doc.line'].search([]).unlink()

        for line in move_lines:
            # Cálculo del saldo inicial
            initial_domain = [
                ('date', '<', self.date_from),
                ('account_id', '=', line.account_id.id),
            ]
            if line.partner_id:
                initial_domain.append(('partner_id', '=', line.partner_id.id))
            if self.line_state == 'posted':
                initial_domain.append(('move_id.state', '=', 'posted'))
            elif self.line_state == 'draft':
                initial_domain.append(('move_id.state', '=', 'draft'))

            initial_balance = self.env['account.move.line'].search(initial_domain).mapped('balance')
            initial_balance = sum(initial_balance) if initial_balance else 0.0

            self.env['account.auxiliary.doc.line'].create({
                'code': line.account_id.code,
                'move_id': line.move_id.id,
                'move_line_name': line.name,
                'date': line.date,
                'journal_id': line.journal_id.id,
                'account_id': line.account_id.id,
                'partner_id': line.partner_id.id,
                'partner_name': line.partner_id.name if line.partner_id else '',
                'partner_vat': line.partner_id.vat if line.partner_id else '',
                'sequence': line.sequence,
                'initial_balance': initial_balance,
                'debit': line.debit,
                'credit': line.credit,
                'balance': line.balance,
                'currency_id': line.currency_id.id,
            })

        return {
            'name': 'Auxiliar',
            'type': 'ir.actions.act_window',
            'res_model': 'account.auxiliary.doc.line',
            'view_mode': 'tree',
            'views': [(self.env.ref('account_auxiliary_wizard.view_account_auxiliary_doc_line_tree').id, 'tree')],
            'target': 'current',
        }

    def action_confirm(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Confirmado',
                'message': 'Se ha confirmado el balance.',
                'type': 'success',
            }
        }
