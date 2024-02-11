from odoo import fields, models, api
from odoo.exceptions import ValidationError

class AccourTableModel(models.Model):
    _name = "accour.report.table"
    _description = "custom pdf report table data"

    pos = fields.Integer(string="Pos")
    code = fields.Char(string="Código")
    concept = fields.Char("Concepto")
    price = fields.Float("Tarifa", default=0)
    uds = fields.Float("Uds.", default=1)
    discount = fields.Float(check="0 <= discount <= 100", default=0, string=".%Desc.")

    net = fields.Float(readonly=True, string="Neto", default=0, compute="_compute_total", store=True)
    total = fields.Float(readonly=True, string="Total", default=0, compute="_compute_total", store=True)

    table_id = fields.Many2one('accour.report.data')

    @api.constrains('discount')
    def _check_discount_range(self):
        for record in self:
            if record.discount < 0 or record.discount > 100:
                raise ValidationError("El descuento debe estar comprendido entre 0 y 100.")
            

    @api.depends('price', 'uds', 'discount')
    def _compute_total(self):
        for record in self:
            record.total = (record.price * record.uds) * (1 - record.discount / 100)
            record.net = (record.price) * (1 - record.discount / 100)
