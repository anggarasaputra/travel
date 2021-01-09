# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Jurusantravel(models.Model):
	_name = 'travel.pool.jalur'
	_rec_name = 'jurusan'
	jurusan = fields.Char('jurusan',required=True)
	pools = fields.One2many('travel.pool.track','city_ids')
	
class Tracktravel(models.Model):
	_name = 'travel.pool.track'
	city_ids = fields.Many2one('travel.pool.jalur')
	rute_jalur = fields.Text('track rute')