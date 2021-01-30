from odoo import fields, models, osv


class res_usersinheritt(models.Model):
    _inherit = 'res.users'

    allow_payment_cash = fields.Boolean("allow payment cash", default=True)
