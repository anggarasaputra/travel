from odoo import fields, models, api

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    numberva = fields.Integer('Number VA', default=0)

