from odoo import models, fields

class ChangeDeadlineWizard(models.TransientModel):
    _name = 'change.deadline.wizard'
    _description = 'Wizard para cambiar la fecha límite'

    picking_id = fields.Many2one('stock.picking', string='Transferencia', required=True)
    fecha_limine = fields.Datetime(string='Fecha efectiva', required=True)

    def confirmar_fecha(self):
        if self.picking_id:
            self.picking_id.date_done = self.fecha_limine
        return {'type': 'ir.actions.act_window_close'}
