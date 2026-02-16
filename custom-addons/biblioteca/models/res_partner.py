from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    es_socio_biblioteca = fields.Boolean(string='Es Socio de Biblioteca', default=False)
    prestamo_ids = fields.One2many('biblioteca.prestamo', 'socio_id', string='Historial de Préstamos')