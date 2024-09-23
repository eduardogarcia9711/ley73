import datetime
import requests

from odoo import http, _
from odoo.http import request
from odoo.addons.base.models.ir_qweb import keep_query
from odoo.addons.appointment.controllers.appointment import AppointmentController


class AzAppointmentController(AppointmentController):
    
    @http.route(['/appointment/<int:appointment_type_id>/submit'],
                type='http', auth="public", website=True, methods=["POST"])
    def appointment_form_submit(self, **kwargs):
        res = super(AzAppointmentController, self).appointment_form_submit(**kwargs)
        body = {
            'nombre': kwargs.get('name'),
            'ape_pat': kwargs.get('father_surname'),
            'ape_mat': kwargs.get('mother_surname'),
            'correo': kwargs.get('email', ''),
            'telefono': kwargs.get('phone'),
            'start': kwargs.get('datetime_str'),
            'end': str(datetime.datetime.strptime(kwargs.get('datetime_str'), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=float(kwargs.get('duration')))),
            
        }
        questions_for_connection = request.env['appointment.question'].sudo().search([('id', 'in', [el.get('question_id',0) for el in res.qcontext.get('answer_input_values', [])]), ('for_appointment_connection', '!=', False)])
        for question in questions_for_connection:
            if question.question_type in ['select', 'radio', 'checkbox']:
                answer = request.env['appointment.answer'].sudo().browse(int(kwargs.get('question_%s' % question.id)))
                body[question.identifier] = answer.name
            else:
                body[question.identifier] = kwargs.get('question_%s' % question.id)
        # Send a post request to the external service
        response = requests.post('https://espinozapymes.com/pensiones/backend/public/api/citasodoo', json=body, params={'key': 'AvemFweW1lcy5jb20iLC'}, headers={'Content-Type': 'application/json', 'User-Agent': 'Thunder Client (https://www.thunderclient.com)'})
        
        if response.status_code != 200:
            event = request.env['calendar.event'].sudo().search([('access_token', '=', res.qcontext.get('event_access_token'))])
            event.unlink()
            return request.redirect('/appointment/%s?%s' % (res.qcontext.get('appointment_type'), keep_query('*', state='failed-sync')))
        
        return res
    
    def _handle_appointment_form_submission(
        self, appointment_type,
        date_start, date_end, duration,  # appointment boundaries
        description, answer_input_values, name, customer, appointment_invite, guests=None,  # customer info
        staff_user=None, asked_capacity=1, booking_line_values=None  # appointment staff / resources
    ):
        res = super(AzAppointmentController, self)._handle_appointment_form_submission(
            appointment_type, date_start, date_end, duration, description, answer_input_values, name, customer, appointment_invite, guests, staff_user, asked_capacity, booking_line_values)
        
        res.qcontext.update({
            'answer_input_values': answer_input_values,
            'event_access_token': res.location.split('/')[3].split('?')[0],
            'appointment_type': appointment_type.id,
        })
        
        return res
