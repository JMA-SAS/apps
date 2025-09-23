from datetime import datetime
from odoo import models, fields, api
import pytz

class ServerTime(models.Model):
    _name = "server.time"
    _description = "Server Time"

    name = fields.Char("Descripción")
    server_time = fields.Datetime("Hora del Servidor")
    odoo_time = fields.Datetime("Hora en Odoo")
    postgres_time = fields.Datetime("Hora en PostgreSQL")

    def get_times(self):
        # Hora del servidor
        server_time = datetime.now().replace(tzinfo=None)

        # Hora de Odoo
        odoo_time = fields.Datetime.now().replace(tzinfo=None)

        # Hora de Postgres
        self.env.cr.execute("SELECT NOW()")
        postgres_time = self.env.cr.fetchone()[0]
        if postgres_time.tzinfo:
            postgres_time = postgres_time.replace(tzinfo=None)

        self.write({
            "server_time": server_time,
            "odoo_time": odoo_time,
            "postgres_time": postgres_time,
        })

        return {
            "type": "ir.actions.act_window",
            "res_model": "server.time",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }
