from odoo import models, fields, api

class BibliotecaAutorLibro(models.Model):
    _name = 'biblioteca.autor_libro'
    _description = 'Relación intermedia Autor-Libro'
    _rec_name = 'display_name'

    libro_id = fields.Many2one('biblioteca.libro', string='Libro', required=True, ondelete='cascade')
    autor_id = fields.Many2one('biblioteca.autor', string='Autor', required=True, ondelete='cascade')
    es_autor_principal = fields.Boolean(string='Principal', default=False)
    orden = fields.Integer(string='Orden', default=1)
    display_name = fields.Char(compute='_compute_display_name')

    @api.depends('libro_id', 'autor_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.autor_id.name or ''} - {rec.libro_id.name or ''}"

    _sql_constraints = [
        ('unique_autor_libro', 'unique(libro_id, autor_id)', 'Este autor ya está asignado a este libro.')
    ]