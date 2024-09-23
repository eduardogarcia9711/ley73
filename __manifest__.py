# -*- coding: utf-8 -*-
##############################################################################
#                 @author Agilezip
#
##############################################################################

{
    'name': 'Agilezip-Ley 73',
    'version': '1.0',
    'description': '''
        Extensiones y personalizaciones de Odoo para cliente Ley 73
    ''',
    'category': 'Customizations',
    'author': 'Agilezip',
    'website': 'agilezip.mx',
    'depends': [
        'appointment',
        'base',
        'website',
    ],
    'data': [
        'views/az_appointment_templates_registration.xml',
        'views/az_appointment_type_views.xml',
        'views/az_appointment_templates_appointments.xml',
    ],
    'application': False,
    'installable': True,
    'price': 5000.00,
    'currency': 'USD',
    'license': 'Other proprietary',
}
