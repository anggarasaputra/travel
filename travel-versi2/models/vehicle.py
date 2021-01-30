from odoo import _, api, exceptions, fields, models


class ResUsers(models.Model):
    _inherit = 'fleet.vehicle'

    maps_seat = fields.Binary(string="Maps Seat")