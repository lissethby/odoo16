from odoo import models, fields, api, _
from datetime import date

class BibliotecaPrestamo(models.Model):
    _name = 'biblioteca.prestamo'
    _description = 'Préstamos de Libros'
    _order = 'name desc'

    # Campos del modelo
    name = fields.Char(string='Código de Préstamo', required=True, copy=False, readonly=True, default=lambda self: _('Nuevo'))
    libro_id = fields.Many2one('biblioteca.libro', string='Libro', required=True)
    socio_id = fields.Many2one('res.partner', string='Socio', required=True)
    
    fecha_prestamo = fields.Date(string='Fecha de Préstamo', default=fields.Date.context_today, required=True)
    fecha_devolucion_prevista = fields.Date(string='Fecha Prevista Devolución', required=True)
    fecha_devolucion_real = fields.Date(string='Fecha Real Devolución', readonly=True)
    
    estado = fields.Selection([
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('retrasado', 'Retrasado')
    ], string='Estado', default='activo', required=True)
    
    notas = fields.Text(string='Observaciones')

    # --- Lógica de Negocio ---

    @api.model
    def create(self, vals):
        # 1. Gestionar la secuencia
        if vals.get('name', _('Nuevo')) == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code('biblioteca.prestamo') or _('Nuevo')
        
        # 2. Crear el registro
        record = super(BibliotecaPrestamo, self).create(vals)
        
        # 3. Cambiar el estado del libro a 'prestado' automáticamente
        if record.libro_id:
            record.libro_id.estado = 'prestado'
            
        return record

    def action_devolver(self):
        """Método para registrar la devolución desde un botón en la vista"""
        for rec in self:
            rec.estado = 'devuelto'
            rec.fecha_devolucion_real = fields.Date.today()
            # Al devolver, el libro vuelve a estar disponible
            if rec.libro_id:
                rec.libro_id.estado = 'disponible'