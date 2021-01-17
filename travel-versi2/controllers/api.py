from odoo import http
from odoo.http import request
from datetime import datetime


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
            seats = []
            for line in i.order_tiket:
                v = {
                    'id_line': line.id,
                    'id_pool_location': line.pool_location.id,
                    'id_pool_location_from': line.pool_location_from.id,
                    'pool_location': line.pool_location.city,
                    'pool_location_from': line.pool_location_from.city,
                    'price_from_destination' : line.price_from_destination,
                    'departure_perpool': line.departure_perpool,
                    'number': line.number,
                }
                list.append(v)
            for seat in i.seat_list:
                v = {
                    'seat_number': seat.seat_number,
                    'hasil':seat.hasil,
                }
                seats.append(v)
            val = {
                'name': i.name,
                'id_departure': i.departure.id,
                'id_destination': i.destination.id,
                'departure': i.departure.city,
                'destination': i.destination.city,
                'departure_date': i.departure_date,
                'line': list,
                'seat': seats,
            }
            response.append(val)
        data = {'status': 200, 'response': response, 'massege': 'Success'}
        return data

    @http.route('/api/pencarian_order/', type='json', auth='user')
    def pencarian_order(self, **rec):
        tanggal = datetime.strptime(rec['departure_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
        scedule = request.env['travel.pool.line'].search([('schedule.departure_date', '=', tanggal),('pool_location_from', '=', rec['pool_location_from']), ('pool_location', '=', rec['pool_location'])])
        response = []
        for i in scedule:
            list = []
            seats = []
            for x in i.schedule.seat_list:
                v = {
                    'seat_number': x.seat_number,
                    'hasil': x.hasil,
                }
                seats.append(v)
            var = {
                'group': i.schedule.name,
                'departure': i.schedule.departure.city,
                'destination': i.schedule.destination.city,
                'track': i.schedule.track.jurusan,
                'departure_date': i.schedule.departure_date,
                'vehicle': i.schedule.vehicle.name,
                'pool_location': i.pool_location.city,
                'pool_location_from': i.pool_location_from.city,
                'departure_perpool': i.departure_perpool,
                'seat': seats,
            }
            response.append(var)
        data = {'status': 200, 'response': response, 'massege': 'Success'}
        return data

    @http.route('/api/tiket_order/', type='json', auth='user')
    def tiket_order(self, **rec):
        hasil1 = request.env['travel.pool.line'].search([('schedule.name', '=', rec['group']),('pool_location_from.city','=', rec['departure'])])
        hasil2 = request.env['travel.pool.line'].search([('schedule.name', '=', rec['group']), ('pool_location.city', '=', rec['destination'])])
        all = request.env['travel.pool.line'].search([('schedule.name', '=', rec['group'])])
        id_schedule = request.env['travel.schedule'].search([('name', '=', rec['group'])], limit=1)
        hasil_terbalik = request.env['travel.pool.line'].search([('schedule.name', '=', rec['group']),('pool_location_from.city','=', rec['departure'])],order="number desc")
        id_seat = request.env['travel.seat'].search([('schedule_id', '=', id_schedule.id),('seat_number','=', int(rec['seat']))],limit=1)
        penampung = []
        if rec['pool_location_from'] == rec['departure']:
            if int(rec['number']) == 1:
                for y in all:
                    penampung.append(y.number)
            else:
                hasil_tahap1 = []
                hasil_tahap2 = []
                for x in hasil1:
                    hasil_tahap1.append(x.number)
                for y in hasil2:

                    if rec['pool_location'] == y.pool_location_from.city:
                        break
                    else:
                        hasil_tahap2.append(y.number)
                marge = hasil_tahap1 + hasil_tahap2
                hasil_marge = []
                for i in marge:
                    if i not in hasil_marge:
                        hasil_marge.append(i)
                response = hasil_marge
                id_seat.write({'hasil':hasil_marge})
        if rec['pool_location'] == rec['destination']:
            hasil_tahap1 = []
            hasil_tahap2 = []
            for x in hasil2:
                hasil_tahap2.append(x.number)
            for y in hasil_terbalik:
                if rec['pool_location_from'] == y.pool_location.city:
                    break
                else:
                    hasil_tahap1.append(y.number)

            marge = hasil_tahap1 + hasil_tahap2
            hasil_marge = []
            for i in marge:
                if i not in hasil_marge:
                    hasil_marge.append(i)
            hasil_sorted=sorted(hasil_marge)
            id_seat.write({'hasil': hasil_sorted})
            response = hasil_sorted
        data = {'status': 200, 'response': response, 'massege': 'Success'}
        return data