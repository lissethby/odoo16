# -*- coding: utf-8 -*-
{
    'name': 'Gestión de Biblioteca',
    'version': '16.0.0.1.0',
    'summary': 'Módulo para gestión de libros, autores y préstamos',
    'author': 'Lisseth Bentura',
    'depends': ['base', 'web'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml', 
        'views/autor_views.xml',
        'views/genero_views.xml',
        'views/libro_views.xml',
        'views/prestamo_views.xml', 
        'views/res_partner_views.xml',
        'views/menu.xml',
        'data/biblioteca_cron.xml', 
    'installable': True,
    'application': True,
}