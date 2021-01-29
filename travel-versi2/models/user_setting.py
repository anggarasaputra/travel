# -*- coding: utf-8 -*-
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    # allow_cash = fields.Boolean("Payment Place", default=False)
