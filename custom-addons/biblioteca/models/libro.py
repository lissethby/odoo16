# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Libro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro de la biblioteca'

    # Campos Obligatorios según la tabla del profesor
    name = fields.Char('Título', required=True)
    isbn = fields.Char('ISBN', size=13, required=True)
    editorial = fields.Char(string='Editorial')
    ano_publicacion = fields.Integer('Año de publicación')
    fecha_adquisicion = fields.Date('Fecha de compra')
    precio = fields.Float('Precio de adquisición')
    descripcion = fields.Text('Sinopsis o resumen')
    active = fields.Boolean('Activo', default=True)
    
    # Tu mejora personal
    foto = fields.Binary(string="Portada") 

    # Relaciones (Tipos determinados)
    autor_libro_ids = fields.One2many(
        comodel_name='biblioteca.autor_libro', 
        inverse_name='libro_id',
        string='Autores'
    )
    
    genero_ids = fields.Many2many(
        comodel_name='biblioteca.genero',
        string='Géneros'
    )
    
    prestamo_ids = fields.One2many(
        comodel_name='biblioteca.prestamo',
        inverse_name='libro_id',
        string='Préstamos'   
    )

    estado = fields.Selection(
        selection=[
            ('disponible', 'Disponible'),
            ('prestado',   'En préstamo'),
            ('reparacion', 'En reparación'),
            ('perdido',    'Perdido'),
        ],
        string='Estado', default='disponible', required=True
    )

    # Campo calculado para el total (opcional, pero recomendado)
    total_prestamos = fields.Integer(string='Total Préstamos', compute='_compute_total_prestamos')

    @api.depends('prestamo_ids')
    def _compute_total_prestamos(self):
        for record in self:
            record.total_prestamos = len(record.prestamo_ids)