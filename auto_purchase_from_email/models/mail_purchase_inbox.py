from odoo import models, fields, api
import logging
import pdfplumber
import base64
import io
import re
from odoo.tools import html2plaintext
from email.utils import parseaddr

_logger = logging.getLogger(__name__)

class MailPurchaseInbox(models.Model):
    _name = 'mail.purchase.inbox'
    _inherit = ['mail.thread']
    _description = 'Bandeja de correos entrantes para compras'
    _order = 'create_date desc'

    email_from = fields.Char("Correo del proveedor", tracking=True)
    subject = fields.Char("Asunto", tracking=True)
    body = fields.Text("Cuerpo del mensaje")
    processed = fields.Boolean("Procesado", default=False, tracking=True)
    attachment_ids = fields.Many2many('ir.attachment', string="Adjuntos")
    partner_id = fields.Many2one('res.partner', string="Contacto")

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        record = self.create({
            'email_from': msg_dict.get('email_from'),
            'subject': msg_dict.get('subject'),
            'body': html2plaintext(msg_dict.get('body', '')),
        })

        attachments = msg_dict.get('attachments', [])
        for attach in attachments:
            if isinstance(attach, dict):
                attachment = self.env['ir.attachment'].create({
                    'name': attach.get('filename'),
                    'datas': attach.get('payload'),
                    'res_model': 'mail.purchase.inbox',
                    'res_id': record.id,
                })
                record.attachment_ids |= attachment
            elif isinstance(attach, models.BaseModel):
                attach.write({
                    'res_model': 'mail.purchase.inbox',
                    'res_id': record.id,
                })
                record.attachment_ids |= attach

        return record

    def process_pdf_and_create_po(self):
        for record in self:
            if record.processed or not record.attachment_ids:
                continue

            for attachment in record.attachment_ids:
                if attachment.mimetype == 'application/pdf':
                    pdf_content = base64.b64decode(attachment.datas)
                    with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                        text = ""
                        for page in pdf.pages:
                            page_text = page.extract_text() or ""
                            _logger.info(f"[Página PDF] {page_text}")
                            text += page_text + "\n"

                        proveedor_email = self._extract_email(text)

                        if not proveedor_email or proveedor_email == 'unknown@example.com':
                            raw_name, proveedor_email = parseaddr(record.email_from)
                            proveedor_name = raw_name or proveedor_email.split('@')[0]
                        else:
                            proveedor_name = proveedor_email.split('@')[0]

                        if not proveedor_email:
                            _logger.warning("No se pudo determinar el correo del proveedor.")
                            continue

                        partner = self.env['res.partner'].search([('email', '=', proveedor_email)], limit=1)
                        if not partner:
                            partner = self.env['res.partner'].create({
                                'name': proveedor_name,
                                'email': proveedor_email,
                                'supplier_rank': 1,
                            })

                        record.partner_id = partner.id

                        productos = self._extract_products_from_text(text)
                        _logger.info(f"Productos extraídos del PDF: {productos}")

                        order_lines = []
                        for p in productos:
                            product = self.env['product.product'].search([('name', 'ilike', p['name'])], limit=1)
                            if not product:
                                product = self.env['product.product'].create({
                                    'name': p['name'],
                                    'purchase_ok': True,
                                    'type': 'consu',
                                    'uom_id': self.env.ref('uom.product_uom_unit').id,
                                    'uom_po_id': self.env.ref('uom.product_uom_unit').id,
                                })

                            order_lines.append((0, 0, {
                                'product_id': product.id,
                                'name': p['name'],
                                'product_qty': p['qty'],
                                'price_unit': p['price'],
                                'product_uom': product.uom_id.id,
                            }))

                        if order_lines:
                            try:
                                po = self.env['purchase.order'].create({
                                    'partner_id': partner.id,
                                    'origin': record.subject,
                                    'order_line': order_lines,
                                })
                                record.processed = True
                                _logger.info(f"Orden de compra creada desde PDF: {po.name}")
                            except Exception as e:
                                _logger.exception("Error al crear la orden de compra: %s", e)
                        else:
                            _logger.warning("No se extrajeron productos del PDF.")

    def _extract_email(self, text):
        match = re.search(r'[\w\.-]+@[\w\.-]+', text)
        return match.group(0) if match else 'unknown@example.com'

    def _parse_float(self, value):
        try:
            value = value.replace(',', '')
            return float(value)
        except:
            return 0.0

    def _extract_products_from_text(self, text):
        productos = []
        lines = text.splitlines()
        i = 0

        while i < len(lines):
            line = lines[i].strip()
            _logger.info(f"LINEA ANALIZADA: {line}")

            match_product = re.match(r'(?:\[(.+?)\]\s+)?(.+)', line)
            if match_product:
                product_name = match_product.group(2).strip()

                if i + 1 < len(lines):
                    valores_line = lines[i + 1].strip()
                    _logger.info(f"LINEA DE VALORES: {valores_line}")

                    match_values = re.search(r'([\d.,]+)\s+([\d.,]+)\s+.*?\$\s*([\d.,]+)', valores_line)
                    if match_values:
                        try:
                            qty = self._parse_float(match_values.group(1))
                            price = self._parse_float(match_values.group(2))
                            total = self._parse_float(match_values.group(3))
                            if price > 0:
                                qty = round(total / price, 2)
                            productos.append({
                                'name': product_name,
                                'qty': qty,
                                'price': price,
                            })
                            _logger.info(f"Producto detectado: {product_name} | Cant: {qty} | Precio: {price}")
                            i += 1  # Salta la línea extra
                        except Exception as e:
                            _logger.error(f"Error al interpretar valores: {e}")
            i += 1

        return productos

    def sync_chatter_attachments(self):
        for record in self:
            messages = self.env['mail.message'].search([
                ('model', '=', 'mail.purchase.inbox'),
                ('res_id', '=', record.id),
                ('attachment_ids', '!=', False),
            ])
            for message in messages:
                for attach in message.attachment_ids:
                    if attach not in record.attachment_ids:
                        record.attachment_ids = [(4, attach.id)]
