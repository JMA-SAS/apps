from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ftp_host = fields.Char(
        string="FTP Host",
        config_parameter='custom_ftp_export.ftp_host'
    )
    ftp_user = fields.Char(
        string="FTP Usuario",
        config_parameter='custom_ftp_export.ftp_user'
    )
    ftp_pass = fields.Char(
        string="FTP Contraseña",
        config_parameter='custom_ftp_export.ftp_pass'
    )
    ftp_path = fields.Char(
        string="Ruta Remota FTP",
        config_parameter='custom_ftp_export.ftp_path'
    )
