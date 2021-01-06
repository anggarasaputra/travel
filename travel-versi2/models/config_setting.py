from odoo import models, fields, api
from ast import literal_eval

class SetttingTravel(models.TransientModel):
    # Private attributes
    _inherit = 'res.config.settings'

    coa_travel = fields.Many2one('account.account', string='Setting Coa Trevel')

    def set_values(self):
        res = super(SetttingTravel, self).set_values()
        self.env['ir.config_parameter'].set_param('travel-versi2.coa_travel', self.coa_travel.id)
        return res

    @api.model
    def get_values(self):
        res = super(SetttingTravel, self).get_values()
        coa = self.env['ir.config_parameter'].sudo().get_param('travel-versi2.coa_travel', default=False)
        res.update(
            coa_travel=int(coa),
        )
        return res
