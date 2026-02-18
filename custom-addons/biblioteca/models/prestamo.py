# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
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
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code('biblioteca.prestamo.seq') or 'Nuevo'
        
        prestamos = super(Prestamo, self).create(vals_list)
        for p in prestamos:
            if p.libro_id:
                # Cambiamos el estado del libro a prestado
                p.libro_id.write({'estado': 'prestado'})
        return prestamos

    def action_devolver(self):
        for record in self:
            record.write({
                'estado': 'devuelto',
                'fecha_devolucion_real': fields.Date.today()
            })
            if record.libro_id:
                # Cambiamos el estado del libro a disponible
                record.libro_id.write({'estado': 'disponible'})

    # --- NUEVA FUNCIÓN PARA EL CRON ---
    @api.model
    def _cron_actualizar_retrasados(self):
        """Esta es la función que llama el archivo biblioteca_cron.xml"""
        hoy = fields.Date.today()
        # Buscamos préstamos activos cuya fecha prevista sea anterior a hoy
        prestamos_vencidos = self.search([
            ('estado', '=', 'activo'),
            ('fecha_devolucion_prevista', '<', hoy)
        ])
        if prestamos_vencidos:
            prestamos_vencidos.write({'estado': 'retrasado'})