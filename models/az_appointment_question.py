# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class AppointmentQuestion(models.Model):
    _inherit = "appointment.question"

    for_appointment_connection = fields.Boolean('Para conexión de citas', default=False, help='Si está marcado, significa que esta pregunta será utilizada para la conexión de citas.')
    identifier = fields.Char('Identificador', help='Este identificador será utilizado para la conexión de citas.')
