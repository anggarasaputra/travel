from odoo import http
from odoo.http import request


class TesApi(http.Controller):

    @http.route('/api/history_order/', type='json', auth='user')
    def history_order(self, **rec):
        id = int(rec['partner_id'])
        travels = request.env['travel.order'].search([('partner_id', '=', id)])
        travel = []
        for i in travels:
            val = {
                'name': i.name,
                'departure' : i.departure.name,
                'destination' : i.destination.name,
                'departure_date': i.departure_date,
                'departure_time': i.departure_time,
                'state': i.state,
                'schedule': i.schedule_id.vehicle.name,
            }
            travel.append(val)
        data = {'status': 200, 'response': travel, 'massege': 'Success'}
        return data