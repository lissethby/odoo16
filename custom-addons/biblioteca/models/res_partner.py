from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'  # Le decimos a Odoo: "Coge tus contactos y añade esto"

    es_socio_biblioteca = fields.Boolean(string="¿Es socio de la biblioteca?")
    
    # Relación para ver sus préstamos desde su propia ficha
    prestamo_ids = fields.One2many(
        'biblioteca.prestamo', 
        'socio_id', 
        string="Histórico de préstamos"
    )