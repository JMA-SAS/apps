from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    credit_warning = fields.Html(
        string='Alerta de crédito',
        compute='_compute_credit_warning',
        store=False
    )

    @api.depends('partner_id', 'invoice_line_ids.price_subtotal')
    def _compute_credit_warning(self):
        for move in self:
            warning = ''
            partner = move.partner_id
            if not partner:
                move.credit_warning = ''
                continue

            invoice_total = sum(move.invoice_line_ids.mapped('price_subtotal')) or 0.0

            # === FACTURAS DE CLIENTE ===
            if move.move_type == 'out_invoice' and partner.enable_credit_validation:
                available = partner.available_credit
                credit_limit = partner.credit_limit

                if credit_limit == 0.0:
                    warning = ''
                elif available <= 0:
                    warning = f"""
                        <div class="alert alert-danger d-flex align-items-center" role="alert">
                            <i class="fa fa-exclamation-circle fa-3x" style="margin-right: 15px;"></i>
                            <div>
                                <strong>Crédito insuficiente (Ventas):</strong><br/>
                                El cliente <strong>{partner.name}</strong> no tiene saldo disponible.
                            </div>
                        </div>
                    """
                elif invoice_total > available:
                    warning = f"""
                        <div class="alert alert-warning d-flex align-items-center" role="alert">
                            <i class="fa fa-info-circle fa-3x" style="margin-right: 15px;"></i>
                            <div>
                                <strong>Factura excede el crédito disponible:</strong><br/>
                                Cliente <strong>{partner.name}</strong><br/>
                                Disponible: <strong>{available:,.2f}</strong><br/>
                                Factura: <strong>{invoice_total:,.2f}</strong>
                            </div>
                        </div>
                    """
                else:
                    warning = f"""
                        <div class="alert alert-success d-flex align-items-center" role="alert">
                            <i class="fa fa-check-circle fa-3x" style="margin-right: 15px;"></i>
                            <div>
                                <strong>Crédito suficiente (Ventas) ✅</strong><br/>
                                Cliente: <strong>{partner.name}</strong><br/>
                                Disponible: <strong>{available:,.2f}</strong>
                            </div>
                        </div>
                    """

            # === FACTURAS DE PROVEEDOR ===
            elif move.move_type == 'in_invoice' and partner.enable_credit_validation_purchase:
                available = partner.available_credit_purchase
                credit_limit = partner.credit_limit_purchase

                if credit_limit == 0.0:
                    warning = ''
                elif available <= 0:
                    warning = f"""
                        <div class="alert alert-danger d-flex align-items-center" role="alert">
                            <i class="fa fa-exclamation-triangle fa-3x" style="margin-right: 15px;"></i>
                            <div>
                                <strong>Crédito insuficiente (Compras):</strong><br/>
                                El proveedor <strong>{partner.name}</strong> no tiene crédito disponible.
                            </div>
                        </div>
                    """
                elif invoice_total > available:
                    warning = f"""
                        <div class="alert alert-warning d-flex align-items-center" role="alert">
                            <i class="fa fa-info-circle fa-3x" style="margin-right: 15px;"></i>
                            <div>
                                <strong>Factura de compra excede crédito:</strong><br/>
                                Proveedor: <strong>{partner.name}</strong><br/>
                                Disponible: <strong>{available:,.2f}</strong><br/>
                                Factura: <strong>{invoice_total:,.2f}</strong>
                            </div>
                        </div>
                    """
                else:
                    warning = f"""
                        <div class="alert alert-success d-flex align-items-center" role="alert">
                            <i class="fa fa-check-circle fa-3x" style="margin-right: 15px;"></i>
                            <div>
                                <strong>Crédito suficiente (Compras) ✅</strong><br/>
                                Proveedor: <strong>{partner.name}</strong><br/>
                                Disponible: <strong>{available:,.2f}</strong>
                            </div>
                        </div>
                    """

            move.credit_warning = warning
