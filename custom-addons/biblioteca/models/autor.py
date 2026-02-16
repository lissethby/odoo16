from odoo import models, fields

class BibliotecaAutor(models.Model):
    _name = 'biblioteca.autor'
    _description = 'Autor'

    name = fields.Char(string='Nombre', required=True)
    nacionalidad = fields.Char(string='Nacionalidad')
    biografia = fields.Text(string='Biografía')
    # Relación con la tabla intermedia
    libro_autor_ids = fields.One2many('biblioteca.autor_libro', 'autor_id', string='Libros del Autor')