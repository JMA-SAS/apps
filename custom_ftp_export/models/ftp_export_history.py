from odoo import models, fields

class FtpExportHistory(models.Model):
    _name = 'ftp.export.history'
    _description = 'Histórico de exportaciones FTP'

    file_name = fields.Char(string='Nombre del Archivo')
    export_date = fields.Datetime(string='Fecha de Exportación', default=fields.Datetime.now)
    status = fields.Selection([
        ('success', 'Éxito'),
        ('error', 'Error'),
    ], string='Estado', default='success')
    message = fields.Text(string='Mensaje')
    file_binary = fields.Binary(string='Archivo Enviado')
