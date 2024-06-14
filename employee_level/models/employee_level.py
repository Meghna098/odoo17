from odoo import fields, models


class EmployeeLevelModel(models.Model):
    _name = "employee.level"
    _description = "Employee level Model"

    employee_level = fields.Char(string='Employee Level')
    emp_salary = fields.Float()
