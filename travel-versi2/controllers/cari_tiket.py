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
        print('hasil sechedule',schedule)

        seat = []
        for x in schedule.schedule.seat_list:
            print('line seat',x.seat_number,x.hasil)
            ada = False
            if x.hasil:
                c = eval(x.hasil)
                print('c',c)
                if schedule.number not in c:
                    ada = True
                    print('ada',ada)
            var ={
                'id': x.id,
                'seat_number': x.seat_number,
                'ada': ada
            }
            seat.append(var)
        print(seat)
        return request.render('travel-versi2.tiketseat', {
            'schedules': schedule,
            'seat_list': seat,
        })


