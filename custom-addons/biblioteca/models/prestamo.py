# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class Prestamo(models.Model):
    _name = 'biblioteca.prestamo'
    _description = 'Registro de Préstamos'

    name = fields.Char(string='Código', required=True, readonly=True, copy=False, default='Nuevo')
    libro_id = fields.Many2one('biblioteca.libro', string='Libro', required=True)
    socio_id = fields.Many2one('res.partner', string='Socio', required=True)
    
    fecha_prestamo = fields.Date(string='Fecha Préstamo', default=fields.Date.today, required=True)
    fecha_devolucion_prevista = fields.Date(
        string='Devolución Prevista', 
        required=True,
        default=lambda self: fields.Date.today() + relativedelta(weeks=2)
    )
    fecha_devolucion_real = fields.Date(string='Devolución Real', readonly=True)
    
    estado = fields.Selection([
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('retrasado', 'Retrasado'),
    ], string='Estado', default='activo', required=True)
    
    notas = fields.Text(string='Observaciones')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # 1. Gestión de Secuencia
            if vals.get('name', 'Nuevo') == 'Nuevo':
                # Le pedimos permiso al administrador para avanzar el contador
                codigo = self.env['ir.sequence'].sudo().next_by_code('biblioteca.prestamo.seq')
                vals['name'] = codigo or 'Nuevo'
        
        # 2. Crear los registros (Llamada al padre)
        records = super(Prestamo, self).create(vals_list)
        
        # 3. Cambio de estado del libro
        for rec in records:
            if rec.libro_id:
                if rec.libro_id.estado != 'disponible':
                    raise ValidationError(f"El libro {rec.libro_id.titulo} ya está prestado.")
                
                # pueda marcar el libro como prestado.
                rec.libro_id.write({'estado': 'prestado'})
                
        return records

    def action_devolver(self):
        for record in self:
            record.write({
                'estado': 'devuelto',
                'fecha_devolucion_real': fields.Date.today()
            })
            if record.libro_id:
                # Cambiamos el estado del libro a disponible
                record.libro_id.write({'estado': 'disponible'})

    @api.model
    def _cron_actualizar_retrasados(self):
        hoy = fields.Date.today()
        prestamos_vencidos = self.search([
            ('estado', '=', 'activo'),
            ('fecha_devolucion_prevista', '<', hoy)
        ])
        if prestamos_vencidos:
            prestamos_vencidos.write({'estado': 'retrasado'})

    @api.constrains('fecha_prestamo', 'fecha_devolucion_prevista')
    def _check_fechas_logicas(self):
        for record in self:
            # Verificamos que ambas fechas existan antes de comparar
            if record.fecha_prestamo and record.fecha_devolucion_prevista:
                if record.fecha_devolucion_prevista < record.fecha_prestamo:
                    raise ValidationError("La fecha de devolución debe ser posterior a la fecha de préstamo.")