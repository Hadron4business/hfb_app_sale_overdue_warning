# -*- coding: utf-8 -*-
#################################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2017-2026 Hadron for Business sp. z o.o. (http://hadronforbusiness.com)
#
# This program is proprietary software, licensed under the Odoo Proprietary
# License v1.0 (OPL-1). Its use is governed by the Odoo Apps terms available
# at https://www.odoo.com/documentation/user/legal/licenses.html and the
# license agreement accepted at purchase / installation.
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the
# Software or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in
# all copies or substantial portions of the Software.
#
#################################################################################
"""	@version	18.0.1.0.0
	@owner  Hadron for Business
	@author Hadron for Business sp. z o.o.
	@date   2026.10.08

	Customer Overdue Warning - customers
	Overdue amount of a customer from its open receivable items due before today
	minus the tolerance (customer setting or company default), list of the
	overdue invoices, data of the Overdue Statement report and the action
	sending it by e-mail.
"""
from datetime import timedelta

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    overdue_tolerance_days = fields.Integer(
        string="Overdue Tolerance (days)",
        help="Days after the due date before an invoice of this customer counts as overdue. "
             "0: use the company setting.")
    overdue_amount = fields.Monetary(
        string="Overdue Amount", compute='_compute_overdue_amount', currency_field='overdue_currency_id')
    overdue_currency_id = fields.Many2one('res.currency', compute='_compute_overdue_amount')
    overdue_invoice_count = fields.Integer(string="Overdue Invoices", compute='_compute_overdue_amount')

    def _overdue_tolerance(self, company):
        commercial = self.commercial_partner_id
        return commercial.overdue_tolerance_days or company.overdue_tolerance_days

    def _overdue_lines(self, company=None):
        """Open receivable items of the commercial partner, due before today minus the tolerance."""
        self.ensure_one()
        company = company or self.env.company
        cutoff = fields.Date.context_today(self) - timedelta(days=self._overdue_tolerance(company))
        return self.env['account.move.line'].sudo().search([
            ('partner_id', 'child_of', self.commercial_partner_id.id),
            ('company_id', '=', company.id),
            ('account_id.account_type', '=', 'asset_receivable'),
            ('parent_state', '=', 'posted'),
            ('reconciled', '=', False),
            ('amount_residual', '!=', 0),
            ('date_maturity', '<', cutoff),
        ], order='date_maturity, id')

    @api.depends_context('company')
    def _compute_overdue_amount(self):
        company = self.env.company
        for partner in self:
            lines = partner._overdue_lines(company) if partner.id else self.env['account.move.line']
            partner.overdue_amount = sum(lines.mapped('amount_residual'))
            partner.overdue_currency_id = company.currency_id
            partner.overdue_invoice_count = len(lines.move_id.filtered(lambda m: m.is_invoice()))

    def get_overdue_statement_lines(self):
        """Lines of the Overdue Statement report (one per overdue receivable item)."""
        self.ensure_one()
        today = fields.Date.context_today(self)
        return [{
            'move': line.move_id,
            'date': line.move_id.invoice_date or line.date,
            'due': line.date_maturity,
            'days': (today - line.date_maturity).days,
            'total': line.move_id.amount_total_signed if line.move_id.is_invoice() else line.balance,
            'residual': line.amount_residual,
        } for line in self._overdue_lines()]

    def action_view_overdue_invoices(self):
        self.ensure_one()
        moves = self._overdue_lines().move_id
        return {
            'name': _("Overdue Invoices"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', moves.ids)],
            'context': {'create': False},
        }

    def action_send_overdue_statement(self):
        self.ensure_one()
        template = self.env.ref('hfb_app_sale_overdue_warning.mail_template_overdue_statement')
        return {
            'name': _("Send Overdue Statement"),
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'res.partner',
                'default_res_ids': self.ids,
                'default_template_id': template.id,
                'default_composition_mode': 'comment',
            },
        }

#EoF
