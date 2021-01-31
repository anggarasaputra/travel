# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class TravelSchedule(models.Model):
	_name = 'travel.schedule'

	departure = fields.Many2one('travel.pool.city', required=True)
	destination = fields.Many2one('travel.pool.city', required=True)
	track = fields.Many2one('travel.pool.jalur', required=True)
	departure_date = fields.Date('Departure Date',required=True)
	# departure_time = fields.Float('Departure Time',required=True)
	vehicle = fields.Many2one('fleet.vehicle', required=True)
	order_list = fields.One2many('travel.order', 'schedule_id')
	order_tiket = fields.One2many('travel.pool.line', 'schedule', ondelete='cascade')
	pool_list_dep = fields.One2many('travel.pool.line', 'schedule')
	pool_list_dest = fields.One2many('travel.pool.line', 'schedule_dest')
	seat_list = fields.One2many('travel.seat', 'schedule_id')
	#price = fields.Float('Price', required=True)
	name = fields.Char(string='Schedule Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New Schedule'))
	state = fields.Selection([
		('draft', 'Draft'),
		('confirm', 'Confirm'),
	], string='Status', readonly=True, default='draft')
	fasilitas = fields.Text(string='Fasilitas')

	def action_confim(self):
		for rec in self:
			rec.state = 'confirm'

	@api.model
	def create(self, vals):
		if vals.get('name', _('New Schedule')) == _('New Schedule'):
			vals['name'] = self.env['ir.sequence'].next_by_code('travel.schedule') or _('New Schedule')
			result = super(TravelSchedule, self).create(vals)

		return result

	def get_max_seats(self):
		return self.vehicle.seats;

	@api.onchange('track', 'departure', 'destination')
	def jadwal_tujuan(self):
		if self.track and self.departure and self.destination:
			for rec in self:
				lines = [(5, 0, 0)]
				number = 1
				var = {
					'pool_location_from': self.departure.id,
					'pool_location': self.destination.id,
					'number': int(number),
				}
				lines.append((0, 0, var))
				number +=1
				for line in self.track.city:
					var = {
						'pool_location_from': self.departure.id,
						'pool_location': line.rute_jalur.id,
						'number': int(number),
					}
					lines.append((0, 0, var))
					number += 1
				for line in self.track.city:
					var = {
						'pool_location_from': line.rute_jalur.id,
						'pool_location': self.destination.id,
						'number': int(number),
					}
					lines.append((0, 0, var))
					number += 1
				print('line', lines)
				rec.order_tiket = lines

class PoolLine(models.Model):
	_name = 'travel.pool.line'
	schedule = fields.Many2one('travel.schedule', string="Schedule",ondelete='cascade')
	schedule_dest = fields.Many2one('travel.schedule', string="Schedule",ondelete='cascade')
	pool_location_from = fields.Many2one('travel.pool.city')
	pool_location = fields.Many2one('travel.pool.city')
	name = fields.Char(compute="_compute_pool_name", store=False)
	departure_perpool = fields.Float('Departure Time')
	price_from_destination = fields.Float('Price')
	number = fields.Integer(string='Number')

	@api.multi
	def _compute_pool_name(self):
		for record in self:
			record.name = record.pool_location.city

	def get_schedule(self):
		return self.schedule

class VehicleSeatLine(models.Model):
	_name = 'travel.seat.line'
	# _sql_constraints = [('travel_seat_line_unique', 'UNIQUE (seat_list)', 'Seat have been booked')]
	order_id = fields.Many2one('travel.order')
	seat_list = fields.Many2one('travel.seat')
	price = fields.Float('Price', related='seat_list.price')

	def isBooked(self):
		return self.order_id is not None 
#	@api.model
#	def create(self, vals):
#		vals['price'] = self.seat_list.price
#		return super(VehicleSeatLine, self).create(vals)
#
#	@api.model
#	def write(self, vals):
#		vals['price'] = self.seat_list.price
#		return super(VehicleSeatLine, self).write(vals)

class VehicleSeat(models.Model):
	_name = 'travel.seat'
	# _sql_constraints = [('travel_seat_unique', 'UNIQUE (seat_number)', 'Seat have been created')]
	name = fields.Char(compute="_compute_seat_name", store=False)
	schedule_id = fields.Many2one('travel.schedule', string="Schedule", ondelete='cascade')
	seat_line = fields.One2many('travel.seat.line', 'seat_list')
	seat_number = fields.Integer('Seat Number')
	price = fields.Float('Price')
	hasil = fields.Char(string='Hasil')
	
	@api.multi
	def _compute_seat_name(self):
		cek = 0
		for x in self:
			cek += 1
		for record in self:
			hasil = 0
			for x in record.seat_line:
				hasil = x.order_id.price_travel / cek
			print(cek)
			record.name = "Seat %d | Rp%.2f" % (record.seat_number, hasil)