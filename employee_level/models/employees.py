from odoo import api, fields, models


class Employees(models.Model):
    _inherit = 'hr.employee'

    employee_level_id = fields.Many2one('employee.level')
    employee_salary = fields.Float()

    def action_promote(self):
        level = self.env['employee.level'].search_read([])
        list=[]
        for rec in level:
            print('hii')
            print(rec)
            print(self.id)
            print(rec.id)
            print(rec.employee_level)
            if rec.employee_level == self.id:
                print('heyy')
                self.write({'employee_salary': rec.emp_salary})
                # rec.employee_salary = self.employee_salary
                print(rec.employee_salary)
                print(rec.employee_level)


