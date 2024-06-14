from odoo import fields, models, Command


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_count = fields.Integer(compute='_compute_count')

    def _compute_count(self):
        for record in self:
            record.project_count = 1

    def action_project(self):
        project_model = self.env['project.project'].create({
            'name': f'{self.name}-Sales Order',
            'partner_id': self.partner_id.id,
        })
        self.project_id = project_model
        for rec in self.order_line:
            milestone_name = f'Milestone{rec.milestone}'
            if milestone_name not in project_model.task_ids.mapped('name'):
                task_model = self.env['project.task'].create([
                    {
                        'name': milestone_name,
                        'project_id': project_model.id,
                        'child_ids': [Command.create({
                            'name': f"Milestone{rec.milestone}-{rec.product_template_id.name}"
                        })]
                    }
                ])
            else:
                existing_task = task_model.filtered(lambda x: x.name == milestone_name)
                existing_task.write({
                    'child_ids': [Command.create({
                            'name': f"Milestone{rec.milestone}-{rec.product_template_id.name}"
                        })]
                })

    def get_project(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'project',
            'view_mode': 'tree,form',
            'res_model': 'project.project',
            'domain': [('id', '=', self.project_id.id)],
            'context': "{'create': False}"
        }

    def action_update_project(self):
        line_vals = set()
        for rec in self.order_line:
            main_task_name = f'Milestone{rec.milestone}'
            child_task_name = f"Milestone{rec.milestone}-{rec.product_template_id.name}"
            main_task = self.project_id.task_ids.filtered(lambda x: x.name == main_task_name)
            if main_task_name in self.project_id.task_ids.mapped('name'):
                if child_task_name not in main_task.child_ids.mapped('name'):
                    self.env['project.task'].create(
                        {
                            'name': child_task_name,
                            'parent_id': main_task.id,
                        })
            else:
                self.env['project.task'].create([
                    {
                        'name': main_task_name,
                        'project_id': self.project_id.id,
                        'child_ids': [Command.create({
                            'name': child_task_name,
                        })]
                    }
                ])
            line_vals.update([main_task_name, child_task_name])
            remove_task = self.project_id.task_ids.filtered(lambda x: x.name not in line_vals)
            remove_task.unlink()
