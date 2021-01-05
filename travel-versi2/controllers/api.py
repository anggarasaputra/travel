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

    @http.route('/api/bank_statement/', type='json', auth='user')
    def bank_statement(self, **rec):
        banks = request.env['account.journal'].search([])
        bank = []
        for i in banks:
            val = {
                'name': i.name,
                'bank_acc_number': i.bank_acc_number,
            }
            bank.append(val)
        data = {'status': 200, 'response': bank, 'massege': 'Success'}
        return data