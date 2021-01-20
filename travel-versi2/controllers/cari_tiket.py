from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class Caritiket(http.Controller):
    @http.route('/travel/cari_tiket', auth='user', website=True)
    def web_listcity(self, **kw):
        listcity = request.env['travel.pool.city'].search([])
        return request.render('travel-versi2.caritiket', {
            'listcitys': listcity
        })

    @http.route('/travel/cari_tiket/cari', auth='user', website=True)
    def web_caritiket(self, **kwargs):
        if request.httprequest.method == 'POST':
            asal = request.params.get('asal')
            tujuan = request.params.get('tujuan')
            tanggal = request.params.get('tanggal')
            scedule = request.env['travel.pool.line'].search(
                [('schedule.departure_date', '=', tanggal), ('pool_location_from', '=', asal),
                 ('pool_location', '=', tujuan)])
            return request.render('travel-versi2.hasiltiket', {
                'schedules': scedule
            })

    @http.route('/travel/cari_tiket/seat/<model("travel.pool.line"):schedule>/', auth='user', website=True)
    def web_tiketseat(self, schedule):
        seat = []
        for x in schedule.schedule.seat_list:
            ada = False
            if x.hasil:
                c = eval(x.hasil)
                cek = schedule.number
                if str(cek) not in c:
                    ada = True
            var ={
                'id': x.id,
                'seat_number': x.seat_number,
                'ada': ada
            }
            seat.append(var)
        return request.render('travel-versi2.tiketseat', {
            'schedules': schedule,
            'seat_list': seat,
        })

    @http.route('/travel/cari_tiket/seat/<model("travel.pool.line"):schedule>/order', type='http', auth="user", methods=['POST'], website=True)
    def web_tiket_order(self, schedule, **kw):
        seats = request.httprequest.form.getlist('seats[]')
        cek = False
        for seat in seats:
            cek = True
            se = int(seat)
        print('numbersss',se)
        if cek:
            print('cek',schedule.pool_location_from.city,schedule.schedule.departure.city)
            hasil1 = request.env['travel.pool.line'].search(
                [('schedule.name', '=', schedule.schedule.name), ('pool_location_from.city', '=', schedule.pool_location_from.city)])
            hasil2 = request.env['travel.pool.line'].search(
                [('schedule.name', '=', schedule.schedule.name), ('pool_location.city', '=', schedule.pool_location.city)])
            all = request.env['travel.pool.line'].search([('schedule.name', '=', schedule.schedule.name)])
            id_schedule = request.env['travel.schedule'].search([('name', '=', schedule.schedule.name)], limit=1)
            hasil_terbalik = request.env['travel.pool.line'].search(
                [('schedule.name', '=', schedule.schedule.name), ('pool_location_from.city', '=', schedule.pool_location_from.city)],
                order="number desc")
            id_seat = request.env['travel.seat'].search(
                [('schedule_id', '=', id_schedule.id), ('id', '=', int(se))], limit=1)
            penampung = []
            if schedule.pool_location_from.city == schedule.schedule.departure.city:
                if int(schedule.number) == 1:
                    for y in all:
                        penampung.append(y.number)
                    response = penampung
                    id_seat.write({'hasil': penampung})
                else:
                    hasil_tahap1 = []
                    hasil_tahap2 = []
                    for x in hasil1:
                        hasil_tahap1.append(x.number)
                    for y in hasil2:

                        if schedule.pool_location.city == y.pool_location_from.city:
                            break
                        else:
                            hasil_tahap2.append(y.number)
                    marge = hasil_tahap1 + hasil_tahap2
                    hasil_marge = []
                    for i in marge:
                        if i not in hasil_marge:
                            hasil_marge.append(i)
                    response = hasil_marge
                    id_seat.write({'hasil': hasil_marge})
            if schedule.pool_location_from.city == schedule.schedule.destination.city:
                hasil_tahap1 = []
                hasil_tahap2 = []
                for x in hasil2:
                    hasil_tahap2.append(x.number)
                for y in hasil_terbalik:
                    if schedule.pool_location_from.city == y.pool_location.city:
                        break
                    else:
                        hasil_tahap1.append(y.number)

                marge = hasil_tahap1 + hasil_tahap2
                hasil_marge = []
                for i in marge:
                    if i not in hasil_marge:
                        hasil_marge.append(i)
                hasil_sorted = sorted(hasil_marge)
                id_seat.write({'hasil': hasil_sorted})
                response = hasil_sorted
            print('respons',response)
            # data = {'status': 200, 'response': response, 'massege': 'Success'}
            # return data



