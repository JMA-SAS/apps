from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class MailThreadInherit(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        model = self._name

        if model == 'purchase.order':
            email_from = msg_dict.get('email_from', '').strip()
            subject = msg_dict.get('subject', 'Compra desde correo')
            body = msg_dict.get('body', '')

            # Buscar o crear el proveedor
            partner = self.env['res.partner'].search([('email', '=', email_from)], limit=1)
            if not partner:
                partner = self.env['res.partner'].create({
                    'name': email_from.split('@')[0],
                    'email': email_from,
                    'supplier_rank': 1,
                    'company_type': 'company',
                })

            # Crear factura de proveedor
            factura = self.env['account.move'].create({
                'move_type': 'in_invoice',
                'partner_id': partner.id,
                'invoice_date': fields.Date.today(),
                'invoice_origin': subject,
                'invoice_line_ids': [
                    (0, 0, {
                        'name': 'Producto desde correo',
                        'quantity': 1,
                        'price_unit': 100.0,
                        'account_id': self.env['account.account'].search([('user_type_id.type', '=', 'expense')], limit=1).id,
                    }),
                ],
            })

            _logger.info(f"Factura de proveedor creada desde correo: {factura.name}")
        
        return super().message_new(msg_dict, custom_values)
