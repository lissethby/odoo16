from odoo import models, fields

class BibliotecaGenero(models.Model):
    _name = 'biblioteca.genero'
    _description = 'Género Literario'

    name = fields.Char(string='Nombre del Género', required=True)
    descripcion = fields.Text(string='Descripción')
    # Relación Many2many simple hacia libros
    libro_ids = fields.Many2many('biblioteca.libro', string='Libros')

    _sql_constraints = [
        ('unique_genero_name', 'unique(name)', 'Ya existe un género con este nombre.')
    ]