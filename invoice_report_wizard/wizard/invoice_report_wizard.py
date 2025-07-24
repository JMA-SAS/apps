from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class InvoiceReportWizard(models.TransientModel):
    _name = 'invoice.report.wizard'
    _description = 'Asistente para generar reporte de facturas'

    date_start = fields.Date(string="Fecha desde", required=True)
    date_end = fields.Date(string="Fecha hasta", required=True)
    pos_ids = fields.Many2many(
        comodel_name='pos.config',
        string='Puntos de Venta',
        help="Filtra por uno o varios puntos de venta. Si se deja vacío, se incluirán todos.")
    results_ids = fields.One2many(
        comodel_name='invoice.report.line',
        inverse_name='wizard_id',
        string="Líneas del Reporte")
    payment_summary_ids = fields.One2many(
        comodel_name='invoice.report.payment.summary',
        inverse_name='wizard_id',
        string="Resumen por método de pago")
    refund_line_ids = fields.One2many(
        comodel_name='invoice.report.refund.line',
        inverse_name='wizard_id',
        string="Reembolsos")
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Compañía',
        default=lambda self: self.env.company,
        required=True,
        readonly=True)
    current_datetime = fields.Datetime(
        string='Fecha actual',
        default=lambda self: fields.Datetime.now(),
        readonly=True)
    gross_sales = fields.Float(
        string="Valor Ventas Brutas",
        readonly=True)
    discount_total = fields.Float(
        string="Descuentos",
        readonly=True)
    vat_total = fields.Float(
        string="IVA Ventas",
        readonly=True)
    total_invoices = fields.Integer(
        string="Total facturas",
        readonly=True)

    @api.constrains('date_start', 'date_end')
    def _check_date_range(self):
        for record in self:
            if record.date_start and record.date_end and record.date_start > record.date_end:
                raise ValidationError("La fecha de inicio no puede ser mayor que la fecha final.")

    def _generate_report_lines(self):
        self.ensure_one()
        self.results_ids.unlink()
        self.payment_summary_ids.unlink()
        self.refund_line_ids.unlink()

        gross_total = 0.0
        payment_method_totals = {}

        domain = [
            ('state', 'in', ['paid', 'invoiced']),
            ('date_order', '>=', self.date_start),
            ('date_order', '<=', self.date_end),
        ]
        if self.pos_ids:
            domain += [('session_id.config_id', 'in', self.pos_ids.ids)]

        pos_orders = self.env['pos.order'].search(domain)

        for order in pos_orders:
            journal_id = order.session_id.config_id.journal_id.id if order.session_id.config_id.journal_id else False
            pos_name = order.session_id.config_id.name or 'N/A'
            partner_id = order.partner_id.id
            total = order.amount_total

            payment_lines = order.payment_ids.filtered(lambda p: p.payment_method_id)
            payment_method_names = list(set(payment_lines.mapped('payment_method_id.name')))
            payment_method = ", ".join(payment_method_names) if payment_method_names else 'N/A'

            self.env['invoice.report.line'].create({
                'wizard_id': self.id,
                'move_name': order.name,
                'reference': '',
                'partner_id': partner_id,
                'journal_id': journal_id,
                'payment_method': payment_method,
                'origin': 'pos',
                'amount_total': total,
                'pos': pos_name,
            })

            for payment in payment_lines:
                method = payment.payment_method_id.name
                payment_method_totals[method] = payment_method_totals.get(method, 0.0) + payment.amount

            gross_total += order.amount_total

        for method, total in payment_method_totals.items():
            self.env['invoice.report.payment.summary'].create({
                'wizard_id': self.id,
                'payment_method': method,
                'total_amount': total,
            })

        # Reembolsos
        refund_domain = domain + [('amount_total', '<', 0)]
        refund_orders = self.env['pos.order'].search(refund_domain)

        for refund in refund_orders:
            journal_id = refund.session_id.config_id.journal_id.id if refund.session_id.config_id.journal_id else False
            pos_name = refund.session_id.config_id.name or 'N/A'
            partner_id = refund.partner_id.id
            total = refund.amount_total

            refund_lines = refund.payment_ids.filtered(lambda p: p.payment_method_id)
            refund_method_names = list(set(refund_lines.mapped('payment_method_id.name')))
            refund_method = ", ".join(refund_method_names) if refund_method_names else 'N/A'

            self.env['invoice.report.refund.line'].create({
                'wizard_id': self.id,
                'refund_name': refund.name,
                'partner_id': partner_id,
                'journal_id': journal_id,
                'refund_method': refund_method,
                'origin': 'pos',
                'pos': pos_name,
                'amount_total': total,
            })

        self.gross_sales = gross_total
        self.discount_total = 0.0
        self.vat_total = 0.0
        self.total_invoices = len(pos_orders)

    def action_generate_tree(self):
        self.ensure_one()
        self._generate_report_lines()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reporte de Facturas',
            'res_model': 'invoice.report.line',
            'view_mode': 'tree',
            'views': [(self.env.ref('invoice_report_wizard.view_invoice_report_line_tree_custom').id, 'tree')],
            'target': 'current',
        }

    def action_generate_pdf(self):
        self.ensure_one()
        self._generate_report_lines()
        return self.env.ref('invoice_report_wizard.action_invoice_report_pdf').report_action(self)


class InvoiceReportLine(models.TransientModel):
    _name = 'invoice.report.line'
    _description = 'Línea del Reporte de Facturas'

    wizard_id = fields.Many2one('invoice.report.wizard', string="Asistente")
    move_name = fields.Char(string="Documento")
    reference = fields.Char(string="Referencia")
    partner_id = fields.Many2one('res.partner', string="Cliente")
    journal_id = fields.Many2one('account.journal', string="Diario")
    payment_method = fields.Char(string="Método de pago")
    origin = fields.Selection([
        ('account', 'Factura'),
        ('pos', 'Punto de venta')
    ], string="Origen")
    pos = fields.Char(string="Punto de venta")
    amount_total = fields.Float(string="Total")


class InvoiceReportPaymentSummary(models.TransientModel):
    _name = 'invoice.report.payment.summary'
    _description = 'Resumen de métodos de pago'

    wizard_id = fields.Many2one('invoice.report.wizard', string="Asistente")
    payment_method = fields.Char(string="Método de Pago")
    total_amount = fields.Float(string="Total")


class InvoiceReportRefundLine(models.TransientModel):
    _name = 'invoice.report.refund.line'
    _description = 'Línea de reembolso en el reporte de facturas'

    wizard_id = fields.Many2one('invoice.report.wizard', string="Asistente")
    refund_name = fields.Char(string="Reembolso")
    partner_id = fields.Many2one('res.partner', string="Cliente")
    journal_id = fields.Many2one('account.journal', string="Diario")
    refund_method = fields.Char(string="Método de pago")
    origin = fields.Selection([
        ('account', 'Factura'),
        ('pos', 'Punto de venta')
    ], string="Origen")
    pos = fields.Char(string="Punto de venta")
    amount_total = fields.Float(string="Total")
