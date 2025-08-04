import io
import csv
import os
from datetime import datetime, date
from ftplib import FTP
from odoo import models, api, fields
import logging
import base64

_logger = logging.getLogger(__name__)

class FtpExporter(models.Model):
    _name = 'ftp.exporter'
    _description = 'Exportador a FTP de Inventario y Ventas por Tienda'

    name = fields.Char(string="Descripción")

    @api.model
    def export_and_send_daily_data(self):
        today = date.today().strftime('%Y-%m-%d')
        file_name = f'Inventario_Tiendas_{today}.csv'
        local_path = 'C:/PLANOS_FLOWSOFT'  # o '/tmp' en Linux

        os.makedirs(local_path, exist_ok=True)
        full_path = os.path.join(local_path, file_name)

        try:
            # Generar el archivo CSV
            self._generate_inventory_store_csv(full_path)

            # Leer el contenido para guardarlo como binario
            with open(full_path, 'rb') as f:
                file_data = base64.b64encode(f.read())

            # Enviar por FTP
            self._send_multiple_csv_to_ftp(local_path)

            # Guardar en el historial
            self.env['ftp.export.history'].create({
                'file_name': file_name,
                'status': 'success',
                'message': f'Archivo {file_name} generado y enviado exitosamente.',
                'file_binary': file_data,
            })

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Éxito',
                    'message': f'Archivo {file_name} exportado y enviado correctamente por FTP.',
                    'type': 'success',
                    'sticky': False,
                }
            }

        except Exception as e:
            self.env['ftp.export.history'].create({
                'file_name': file_name,
                'status': 'error',
                'message': str(e),
            })

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': f'Falló la exportación: {str(e)}',
                    'type': 'danger',
                    'sticky': True,
                }
            }

    def _generate_inventory_store_csv(self, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['codigo_tienda', 'codigo_producto', 'fecha_envio', 'cantidad_existente', 'cantidad_vendida_dia'])

            today = date.today().strftime('%Y-%m-%d')

            tiendas = self.env['stock.location'].search([('usage', '=', 'internal')])
            for tienda in tiendas:
                productos = self.env['product.product'].search([])
                for producto in productos:
                    if not producto.default_code:
                        continue

                    qty_available = producto.with_context(location=tienda.id).qty_available

                    ventas = self.env['pos.order.line'].search([
                        ('create_date', '>=', f'{today} 00:00:00'),
                        ('create_date', '<=', f'{today} 23:59:59'),
                        ('product_id', '=', producto.id),
                        ('order_id.state', 'in', ['paid', 'invoiced', 'done']),
                    ])
                    qty_vendida = sum(ventas.mapped('qty'))

                    if qty_available or qty_vendida:
                        writer.writerow([
                            tienda.name,
                            producto.default_code,
                            today,
                            int(qty_available),
                            int(qty_vendida)
                        ])

    def _send_multiple_csv_to_ftp(self, local_dir):

        #host = '3.91.146.176'
        #user = 'comertex'
        #ftp_pass = 'comertex_F10w'
        #ruta_remota = '/archivos'

        config = self.env['ir.config_parameter'].sudo()
        ftp_host = config.get_param('custom_ftp_export.ftp_host', default='127.0.0.1')
        ftp_user = config.get_param('custom_ftp_export.ftp_user', default='anonymous')
        ftp_pass = config.get_param('custom_ftp_export.ftp_pass', default='')
        ruta_remota = config.get_param('custom_ftp_export.ftp_path', default='/')

        archivos_subidos = []

        try:
            ftp = FTP(ftp_host)
            ftp.login(ftp_user, ftp_pass)
            ftp.cwd(ruta_remota)
            ftp.set_pasv(True)

            for file_name in os.listdir(local_dir):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(local_dir, file_name)
                    with open(file_path, 'rb') as file:
                        ftp.storbinary(f'STOR {file_name}', file)
                        archivos_subidos.append(file_name)
                        _logger.info(f"Archivo {file_name} subido correctamente por FTP.")

            ftp.quit()

            if archivos_subidos:
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "title": "Éxito",
                        "message": "Se subieron correctamente los archivos: %s" % ', '.join(archivos_subidos),
                        "type": "success",
                        "sticky": False,
                    }
                }
            else:
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "title": "Advertencia",
                        "message": "No se encontraron archivos CSV para enviar.",
                        "type": "warning",
                        "sticky": False,
                    }
                }

        except Exception as e:
            _logger.error(f"Error al subir archivos al FTP: {e}")
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Error",
                    "message": "Error al subir archivos al FTP: %s" % str(e),
                    "type": "danger",
                    "sticky": True,
                }
            }

    def action_test_export(self):
        self.ensure_one()
        self.export_and_send_daily_data()
