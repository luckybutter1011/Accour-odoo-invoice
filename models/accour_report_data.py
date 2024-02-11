from odoo import fields, models, api
from odoo.exceptions import ValidationError

class AccourModel(models.Model):
    _name = "accour.report.data"
    _description = "custom pdf report"

    budget = fields.Char()
    reference = fields.Char()
    date = fields.Date()
    amount = fields.Float()
    expiration_date = fields.Date()
    form_of_payment = fields.Char()
    table_data = fields.One2many('accour.report.table', 'table_id')

    sub_total = fields.Float(readonly=True, string="Subtotal", default=0, compute="_compute_sub_total", store=True)
    total_sum = fields.Float(readonly=True, string="Total", default=0, compute="_compute_calc", store=True)
    tax = fields.Float(readonly=True, string="Tax(21%)", default=0, compute="_compute_calc", store=True)
    total_sum_tax = fields.Float(readonly=True, string="TOTAL(€)", default=0, compute="_compute_calc", store=True)

    charges = fields.Float(string="Charges", default=0)
    other_discounts = fields.Float(check="0 <= other_discounts  <= 100", default=0, string="Otros descuentos*")
    pre_pay = fields.Float(string="Pre-pago", default=0)

    @api.constrains('other_discounts')
    def _check_discount_range_other(self):
        for record in self:
            if record.other_discounts < 0 or record.other_discounts > 100:
                raise ValidationError("Los demás descuentos deben estar comprendidos entre 0 y 100.")
 
    @api.depends('table_data.price', 'table_data.uds', 'table_data.discount')
    def _compute_sub_total(self):
        for record in self:
            record.sub_total = sum((line.price * line.uds) * (1 - line.discount / 100) for line in record.table_data)

    @api.depends('pre_pay', 'charges', 'other_discounts', 'sub_total')
    def _compute_calc(self):
        self.total_sum = (self.sub_total + self.charges) * (1 - self.other_discounts / 100) 
        self.tax = self.total_sum * 0.21
        self.total_sum_tax = self.total_sum + self.tax + self.pre_pay