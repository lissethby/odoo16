from odoo import models, fields

class BibliotecaAutor(models.Model):
    _name = 'biblioteca.autor'
    _description = 'Autor de libros en la biblioteca'

    name = fields.Char(string='Nombre', required=True)
    nacionalidad = fields.Char(string='Nacionalidad')
    biografia = fields.Text(string='Biografía')
    
    # Campo para almacenar la foto del autor
    image_1920 = fields.Binary(string="Foto del Autor")
    
    libro_autor_ids = fields.One2many(
        'biblioteca.autor_libro', 
        'autor_id', 
        string='Libros del Autor'
    )
    
    