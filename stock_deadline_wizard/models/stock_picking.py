from odoo import models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_open_change_deadline_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cambiar Fecha Límite',
            'res_model': 'change.deadline.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_picking_id': self.id,
            }
        }
