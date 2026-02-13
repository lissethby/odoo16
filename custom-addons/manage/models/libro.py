from odoo import models, fields

class LibreriaLibros(models.Model):
    _name = 'biblioteca_escolar.libro'
    _description = 'Datos de los libros de la librería'

    name = fields.Char(string='Título', required=True)
    author = fields.Char(string='Autor')
    isbn = fields.Char(string='ISBN')
    state = fields.Selection([
        ('available', 'Disponible'),
        ('borrowed', 'Prestado')], default='available', string='Estado')