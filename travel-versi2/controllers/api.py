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

    @http.route('/api/scedule/', type='json', auth='user')
    def scedule_brangkat(self, **rec):
        scedule = request.env['travel.schedule'].search([('state', '=', 'confirm')])
        response = []
        for i in scedule:
            list = []
            for line in i.order_tiket:
                v = {
                    'pool_location': line.pool_location.city,
                    'pool_location_from': line.pool_location_from.city,
                    'price_from_destination' : line.price_from_destination,
                    'departure_perpool': line.departure_perpool,
                }
                list.append(v)
            val = {
                'name': i.name,
                'line': list,
            }
            response.append(val)
        data = {'status': 200, 'response': response, 'massege': 'Success'}
        return data