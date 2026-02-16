from odoo import models, fields, api

class BibliotecaLibro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro de la Biblioteca'
    # El _rec_name es 'name' por defecto, pero lo definimos por claridad
    _rec_name = 'name'

    # --- Campos Obligatorios ---
    name = fields.Char(string='Título del Libro', required=True)
    isbn = fields.Char(string='ISBN', required=True, help="Código ISBN del libro")

    # --- Relaciones ---
    # Relación con tabla intermedia (One2many hacia la tabla que une libro y autor)
    autor_libro_ids = fields.One2many(
        'biblioteca.autor_libro', 
        'libro_id', 
        string='Autores'
    )

    # Many2many simple: Odoo creará la tabla relacional automáticamente
    genero_ids = fields.Many2many(
        'biblioteca.genero', 
        string='Géneros'
    )

    # Relación inversa con préstamos (un libro puede tener muchos préstamos)
    prestamo_ids = fields.One2many(
        'biblioteca.prestamo', 
        'libro_id', 
        string='Historial de Préstamos'
    )

    # --- Información Básica ---
    editorial = fields.Char(string='Editorial')
    ano_publicacion = fields.Integer(string='Año de Publicación')
    foto = fields.Binary(string="Portada") 
    
    # --- Estado y Finanzas ---
    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('reparacion', 'En Reparación'),
        ('perdido', 'Perdido')
    ], string='Estado', default='disponible', copy=False, tracking=True)
    
    fecha_adquisicion = fields.Date(string='Fecha de Adquisición', default=fields.Date.context_today)
    precio = fields.Float(string='Precio de Adquisición')
    
    # --- Otros ---
    descripcion = fields.Text(string='Sinopsis o Resumen')
    active = fields.Boolean(string='Activo', default=True) # Campo para archivar