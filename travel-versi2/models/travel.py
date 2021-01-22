# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime

class TravelOrder(models.Model):
	_name = 'travel.order'

	partner_id = fields.Many2one('res.partner', default=lambda self: self.env['res.users'].browse(self.env.uid).partner_id)
	schedule_id = fields.Many2one('travel.schedule')

	isPay = fields.Boolean(default=False)

	price_travel = fields.Float('Price',required=True)

	departure = fields.Many2one('travel.pool.city',required=True)
	destination = fields.Many2one('travel.pool.city',required=True)

	departure_date = fields.Date('Departure Date',required=True,related='schedule_id.departure_date', store=True)
	departure_time = fields.Float('Departure Time',required=True,related='schedule_id.order_tiket.departure_perpool', store=True)

	lokasi_penjemputan = fields.Char(string="Lokasi Penjemputan")
	latitut = fields.Char(string='Latitut')
	longtitude = fields.Char(string='Longtitude')
	pembayaran = fields.Many2one('account.journal')

	state = fields.Selection([
            ('order', 'Order'),
            ('waiting', 'Waiting Payment'),
            ('travel', 'Travel Order')
            ],default='order')

	tree_seat_number = fields.One2many('travel.seat.line', 'order_id')
	name = fields.Char(string='Travel Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))

	@api.model
	def create(self, vals):

		if vals.get('name', _('New')) == _('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('travel.order') or _('New')
			
		return super(TravelOrder, self).create(vals)

	# @api.model
	# def write(self, vals):
	# 	vals['price_travel'] = sum(seat_line.price for seat_line in self.tree_seat_number)
	#
	#
	# 	return super(TravelOrder, self).write(vals)

	def get_cr(self):
		return self._cr

	def confirm(self):
		self.write({'state' : 'waiting'})

	def validate(self):
		invoice = self.env['account.invoice']
		productss = self.env['ir.config_parameter'].sudo().get_param('travel-versi2.produk_travel')
		product_data = self.env['product.product'].search([('id','=', productss)])
		coa = self.env['ir.config_parameter'].sudo().get_param('travel-versi2.coa_travel')
		lines = []
		line_inv = {
			'product_id': product_data.id,
			'name': product_data.name,
			'quantity': 1,
			'price_unit': self.price_travel,
			'invoice_line_tax_ids': False,
			'account_id': coa,
		}
		lines.append((0, 0, line_inv))
		heder_inv ={
			'partner_id': self.partner_id.id,
			'date_invoice': datetime.now().date(),
			'invoice_line_ids': lines
		}
		validate_invoice = invoice.create(heder_inv)
		validate_invoice.action_invoice_open()
		self.write({'state' : 'travel'})

	def cancel(self):
		self.write({'state' : 'order'})


	@api.onchange('departure')
	def destination_onchange(self):
#	Pemilihan lokasi tujuan (Destination) berdasarkan keberangkatan (Departure) pada jadwal yang sama
		res = {}
		res['domain'] = {'destination': ['&',('schedule', '=', self.departure.schedule.id),('pool_location', '!=', self.departure.pool_location.id),('pool_location.city_ids','!=',self.departure.pool_location.city_ids.id)]}
		return res

	@api.onchange('destination')
	def destination_onchange(self):
#	Pemilihan lokasi keberangkatan (Departure) berdasarkan tujuan (Destination) pada jadwal yang sama
		res = {}
		res['domain'] = {'departure': ['|',('schedule', '=', self.destination.schedule.id),('pool_location', '!=', self.destination.pool_location.id),('pool_location.city_ids','!=',self.destination.pool_location.city_ids.id)]}
		return res