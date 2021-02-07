import base64
import hashlib
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError
import requests

from odoo import http
from odoo.http import request, Response
from datetime import datetime
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
            uid = request.uid
            partner = request.env['res.users'].browse(uid)
            if not partner.partner_id.street or not partner.partner_id.phone or not partner.partner_id.city:
                payload = {'phone': '', 'street': '', 'city': ''}
                return request.redirect('/my/account')
            asal = request.params.get('asal')
            tujuan = request.params.get('tujuan')
            tanggal = request.params.get('tanggal')
            hari = datetime.now().date()
            cek = datetime.strptime(tanggal, '%Y-%m-%d').date()
            if hari > cek:
                return request.render('travel-versi2.order_success', {
                    'title': 'CEK INPUT!',
                    'message': 'Pilih Tanggal Minimal Hari INI!!',
                })
            else:
                scedule = request.env['travel.pool.line'].search(
                    [('schedule.departure_date', '=', tanggal), ('pool_location_from', '=', asal),
                     ('pool_location', '=', tujuan)])
                return request.render('travel-versi2.hasiltiket', {
                    'schedules': scedule,
                })

    @http.route('/travel/respons', methods=['POST'], auth='public', csrf=False, website=True)
    def respons_ipay88(self, **kwargs):
        MerchantCode = request.params.get('MerchantCode')
        PaymentId = request.params.get('PaymentId')
        RefNo = request.params.get('RefNo')
        Amount = request.params.get('Amount')
        eCurrency = request.params.get('Currency')
        Remark = request.params.get('Remark')
        TransId = request.params.get('TransId')
        AuthCode = request.params.get('AuthCode')
        eStatus = request.params.get('Status')
        ErrDesc = request.params.get('ErrDesc')
        Signature = request.params.get('Signature')

        if eStatus == '1':
            order_travel = request.env['travel.order'].sudo().search(
                [('name', '=', RefNo), ('state', '=', 'waiting')], limit=1)
            order_travel.validate()
            return Response("RECEIVEOK")
        else:
            return Response("Tolak")

    @http.route('/travel/backend', methods=['POST'], auth='public', csrf=False, website=True)
    def respons_ipay88_1(self, **kwargs):
        MerchantCode = request.params.get('MerchantCode')
        PaymentId = request.params.get('PaymentId')
        RefNo = request.params.get('RefNo')
        Amount = request.params.get('Amount')
        eCurrency = request.params.get('Currency')
        Remark = request.params.get('Remark')
        TransId = request.params.get('TransId')
        AuthCode = request.params.get('AuthCode')
        eStatus = request.params.get('Status')
        ErrDesc = request.params.get('ErrDesc')
        Signature = request.params.get('Signature')

        if eStatus == '1':
            order_travel = request.env['travel.order'].sudo().search([])

            for x in order_travel:
                x.write({'latitut': RefNo + "," + Signature})

            return Response("RECEVEIOK")
        else:
            order_travel = request.env['travel.order'].sudo().search([])

            for x in order_travel:
                x.write({'latitut': eStatus})

            return Response("RECEVEIOK")

    @http.route('/travel/cari_tiket/seat/<model("travel.pool.line"):schedule>/', auth='user', website=True)
    def web_tiketseat(self, schedule):
        seat = []
        for x in schedule.schedule.seat_list:
            ada = False
            if x.hasil:
                c = eval(x.hasil)
                cek = schedule.number
                if int(cek) in c:
                    ada = True
                else:
                    ada = False
            var = {
                'id': x.id,
                'seat_number': x.seat_number,
                'ada': ada
            }
            seat.append(var)
        uid = request.uid
        allow_payment_cash = request.env['res.users'].browse(uid).allow_payment_cash
        if allow_payment_cash == True:
            pembayaran = request.env['account.journal'].sudo().search(
                ['|', ('type', '=', 'bank'), ('type', '=', 'cash')])
        else:
            pembayaran = request.env['account.journal'].sudo().search([('type', '=', 'bank')])
        return request.render('travel-versi2.tiketseat', {
            'schedules': schedule,
            'seat_list': seat,
            'pembayaran': pembayaran,
        })

    @http.route('/travel/cari_tiket/seat/<model("travel.pool.line"):schedule>/order', type='http', auth="user",
                methods=['POST'], website=True)
    def web_tiket_order(self, schedule, **kw):
        # seat = request.params.get('seat')
        uid = request.uid
        partner = request.env['res.users'].sudo().browse(uid).partner_id
        seats = request.httprequest.form.getlist('seats[]')
        # seats = eval(seat)
        cek = False
        price = 0

        for seat in seats:
            cek = True
            se = int(seat)
            price += schedule.price_from_destination
            # if cek:
            hasil1 = request.env['travel.pool.line'].search(
                [('schedule.name', '=', schedule.schedule.name),
                 ('pool_location_from.city', '=', schedule.pool_location_from.city)])
            hasil2 = request.env['travel.pool.line'].search(
                [('schedule.name', '=', schedule.schedule.name),
                 ('pool_location.city', '=', schedule.pool_location.city)])
            all = request.env['travel.pool.line'].search([('schedule.name', '=', schedule.schedule.name)])
            id_schedule = request.env['travel.schedule'].search([('name', '=', schedule.schedule.name)])
            hasil_terbalik = request.env['travel.pool.line'].search(
                [('schedule.name', '=', schedule.schedule.name),
                 ('pool_location_from.city', '=', schedule.pool_location_from.city)],
                order="number desc")
            id_seat = request.env['travel.seat'].search(
                [('schedule_id', '=', id_schedule.id), ('id', '=', int(se))])
            penampung = []
            if schedule.pool_location_from.city == schedule.schedule.departure.city:
                if int(schedule.number) == 1:
                    for y in all:
                        penampung.append(y.number)
                    if id_seat.hasil:
                        ambil = id_seat.hasil
                        hasil = eval(ambil)
                        for h in hasil:
                            penampung.append(h)
                        hasil_sort = sorted(penampung)
                        hasil_sort = list(dict.fromkeys(hasil_sort))
                        id_seat.write({'hasil': hasil_sort})
                    else:
                        penampung = list(dict.fromkeys(penampung))
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
                    if id_seat.hasil:
                        ambil = id_seat.hasil
                        hasil = eval(ambil)
                        for h in hasil:
                            hasil_marge.append(h)
                        hasil_sort = sorted(hasil_marge)
                        hasil_sort = list(dict.fromkeys(hasil_sort))
                        id_seat.write({'hasil': hasil_sort})
                    else:
                        hasil_marge = list(dict.fromkeys(hasil_marge))
                        id_seat.write({'hasil': hasil_marge})
            if schedule.pool_location.city == schedule.schedule.destination.city:
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
                if id_seat.hasil:
                    ambil = id_seat.hasil
                    hasil = eval(ambil)
                    for h in hasil:
                        hasil_marge.append(h)
                    hasil_sort = sorted(hasil_marge)
                    hasil_sort = list(dict.fromkeys(hasil_sort))
                    id_seat.write({'hasil': hasil_sort})
                else:
                    hasil_sorted = sorted(hasil_marge)
                    hasil_sorted = list(dict.fromkeys(hasil_sorted))
                    id_seat.write({'hasil': hasil_sorted})
        pembayaran = request.params.get('pembayarans')
        penjemputan = request.params.get('penjemputan')
        cek_cash = request.env['account.journal'].sudo().search([('id', '=', int(pembayaran))])
        data_order = {}
        data_order['schedule_id'] = schedule.schedule.id
        data_order['departure'] = schedule.pool_location_from.id
        data_order['departure_date'] = schedule.schedule.departure_date
        data_order['departure_time'] = schedule.departure_perpool
        data_order['destination'] = schedule.pool_location.id
        data_order['partner_id'] = partner.id
        data_order['pembayaran'] = int(pembayaran)
        data_order['lokasi_penjemputan'] = penjemputan
        data_order['price_travel'] = float(price)
        data_order['state'] = 'waiting'
        data_order['pesanan'] = schedule.pool_location_from.city + ' - ' + schedule.pool_location.city
        travel_order = request.env['travel.order'].sudo()
        order = travel_order.create(data_order)
        seat_line = request.env['travel.seat.line']
        merchant_code = request.env['ir.config_parameter'].sudo().get_param('travel-versi2.merchant_code')
        jurnal = request.env['account.journal'].sudo().search([('id', '=', int(pembayaran))])
        for seat in seats:
            se = int(seat)
            data = {'order_id': order.id, 'seat_list': se}
            seat_line.create(data)
        numberva = jurnal.numberva
        MerchantKey = '9oXTV52noa'
        Currency = 'IDR'
        convert_harga = str(int(price)) + "00"
        signaturea = MerchantKey + merchant_code + order.name + convert_harga + Currency
        digest = hashlib.sha1(signaturea.encode('utf-8')).digest()
        hasil_signature = base64.b64encode(digest)
        if cek_cash.type == 'cash':
            return request.render('travel-versi2.order_success_cash', {
                'title': 'Order Success!',
                'message': 'Please Pay Your Invoice',
            })
        else:
            return request.render('travel-versi2.order_success', {
                'nama': partner.name,
                'nomer': partner.phone,
                'tagihan': float(price),
                'MerchantCode': merchant_code,
                'PaymentId': str(numberva),
                'RefNo': order.name,
                'Amount': convert_harga,
                'Currency': "IDR",
                'ProdDesc': "Tiket",
                'UserName': partner.name,
                'UserEmail': partner.email,
                'UserContact': partner.phone,
                'Remark': '',
                'Lang': "UTF-8",
                'Signature': hasil_signature,
                'ResponseURL': "http://nafatrans.com/travel/response",
                'BackendURL': "http://nafatrans.com/travel/backend",
            })
