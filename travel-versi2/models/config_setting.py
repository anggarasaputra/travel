from odoo import models, fields, api
from ast import literal_eval

class SetttingTravel(models.TransientModel):
    # Private attributes
    _inherit = 'res.config.settings'

    coa_travel = fields.Many2one('account.account', string='Coa Trevel')
    produk_travel = fields.Many2one('product.product', string='Product Trevel')
    time_book = fields.Integer(string="Time Book")
    merchant_code = fields.Char(string="Merchant Code IP88")

    def set_values(self):
        res = super(SetttingTravel, self).set_values()
        self.env['ir.config_parameter'].set_param('travel-versi2.coa_travel', self.coa_travel.id)
        self.env['ir.config_parameter'].set_param('travel-versi2.produk_travel', self.produk_travel.id)
        self.env['ir.config_parameter'].set_param('travel-versi2.time_book', self.time_book)
        self.env['ir.config_parameter'].set_param('travel-versi2.merchant_code', self.merchant_code)
        return res

    @api.model
    def get_values(self):
        res = super(SetttingTravel, self).get_values()
        coa = self.env['ir.config_parameter'].sudo().get_param('travel-versi2.coa_travel', default=False)
        product1 = self.env['ir.config_parameter'].sudo().get_param('travel-versi2.produk_travel', default=False)
        time_book1 = self.env['ir.config_parameter'].sudo().get_param('travel-versi2.time_book', default=False)
        merchant_code1 = self.env['ir.config_parameter'].sudo().get_param('travel-versi2.merchant_code', default=False)
        res.update(
            coa_travel=int(coa),
            produk_travel=int(product1),
            time_book=int(time_book1),
            merchant_code=merchant_code1
        )
        return res