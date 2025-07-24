from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Campos para Ventas
    # Campo monetario editable para el límite máximo de crédito
    credit_limit = fields.Monetary(
        string='Límite de Crédito Ventas', 
        tracking=True,
        help="Límite máximo de crédito permitido para este cliente",
        currency_field='company_currency_id'
    )
    
    # Campo booleano para activar/desactivar la validación de crédito
    enable_credit_validation = fields.Boolean(
        string='Activar Validación de Crédito', 
        default=False, 
        tracking=True,
        help="Indica si se debe activar la validación de crédito para este cliente"
    )
    
    # Campo calculado para el total actualmente adeudado
    total_credit_used = fields.Monetary(
        string='Crédito Total Usado', 
        compute='_compute_total_credit_used', 
        store=True, 
        currency_field='company_currency_id',
        help="Total actualmente adeudado por el cliente basado en facturas pendientes"
    )
    
    # Campo relacionado para la moneda de la compañía
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', 
        string="Moneda de la Compañía", 
        readonly=True
    )
    
    # Campo calculado para crédito disponible
    available_credit = fields.Monetary(
        string='Crédito Disponible',
        compute='_compute_available_credit',
        currency_field='company_currency_id',
        help="Crédito disponible restante (Límite - Usado)"
    )

    @api.depends('invoice_ids.amount_residual', 'invoice_ids.state', 'invoice_ids.payment_state')
    def _compute_total_credit_used(self):
        """
        Calcula el total de crédito usado basado en facturas de cliente pendientes.
        Solo considera facturas validadas (posted) que no estén completamente pagadas.
        """
        for partner in self:
            total_used = 0.0
            
            # Buscar facturas de cliente pendientes
            outstanding_invoices = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('payment_state', 'in', ('not_paid', 'partial'))
            ])

            for invoice in outstanding_invoices:
                # Convertir el amount_residual a la moneda de la compañía
                if invoice.currency_id and invoice.currency_id != partner.company_currency_id:
                    converted_amount = invoice.currency_id._convert(
                        invoice.amount_residual,
                        partner.company_currency_id,
                        invoice.company_id,
                        invoice.invoice_date or fields.Date.today()
                    )
                    total_used += converted_amount
                else:
                    total_used += invoice.amount_residual
                    
            partner.total_credit_used = total_used

    @api.depends('credit_limit', 'total_credit_used')
    def _compute_available_credit(self):
        """
        Calcula el crédito disponible restante.
        """
        for partner in self:
            partner.available_credit = partner.credit_limit - partner.total_credit_used

    # campos para compras

    # Campo monetario editable para el límite máximo de crédito
    credit_limit_purchase = fields.Monetary(
        string='Límite de Crédito Compras', 
        tracking=True,
        help="Límite máximo de crédito permitido para este Proveedor",
        currency_field='company_currency_id'
    )
    
    # Campo booleano para activar/desactivar la validación de crédito
    enable_credit_validation_purchase = fields.Boolean(
        string='Activar Validación de Crédito Compras', 
        default=False, 
        tracking=True,
        help="Indica si se debe activar la validación de crédito para este cliente"
    )
    
    # Campo calculado para el total actualmente adeudado
    total_credit_used_purchase = fields.Monetary(
        string='Crédito Total Usado', 
        compute='_compute_total_credit_used_purchase', 
        store=True, 
        currency_field='company_currency_id',
        help="Total actualmente Pendiete por pagar basado en facturas pendientes"
    )
    
    
    # Campo calculado para crédito disponible
    available_credit_purchase = fields.Monetary(
        string='Crédito Disponible',
        compute='_compute_available_credit_purchase',
        currency_field='company_currency_id',
        help="Crédito disponible restante (Límite - Usado)"
    )



    @api.depends('invoice_ids.amount_residual', 'invoice_ids.state', 'invoice_ids.payment_state')
    def _compute_total_credit_used_purchase(self):
        """
        Calcula el total de crédito usado basado en facturas de proveedor pendientes.
        Solo considera facturas validadas (posted) que no estén completamente pagadas.
        """
        for partner in self:
            total_used_purchase = 0.0
            
            # Buscar facturas de Proveedor pendientes
            outstanding_invoices = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('move_type', '=', 'in_invoice'),
                ('state', '=', 'posted'),
                ('payment_state', 'in', ('not_paid', 'partial'))
            ])

            for invoice in outstanding_invoices:
                # Convertir el amount_residual a la moneda de la compañía
                if invoice.currency_id and invoice.currency_id != partner.company_currency_id:
                    converted_amount = invoice.currency_id._convert(
                        invoice.amount_residual,
                        partner.company_currency_id,
                        invoice.company_id,
                        invoice.invoice_date or fields.Date.today()
                    )
                    total_used_purchase += converted_amount
                else:
                    total_used_purchase += invoice.amount_residual
                    
            partner.total_credit_used_purchase = total_used_purchase  # ✅ Correcto
    
    @api.depends('credit_limit_purchase', 'total_credit_used_purchase')
    def _compute_available_credit_purchase(self):
        """
        Calcula el crédito disponible restante.
        """
        for partner in self:
            partner.available_credit_purchase = partner.credit_limit_purchase - partner.total_credit_used_purchase 