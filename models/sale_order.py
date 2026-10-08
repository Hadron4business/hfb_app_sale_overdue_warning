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
"""	@version	19.0.1.0.0
	@owner  Hadron for Business
	@author Hadron for Business sp. z o.o.
	@date   2026.10.08

	Customer Overdue Warning - sales orders
	Overdue amount of the customer on the quotation / order, shortcuts to the
	overdue invoices and the statement, and the optional block of the
	confirmation (sales managers can still confirm; the confirmation is logged
	in the chatter).
"""
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    overdue_amount = fields.Monetary(
        string="Customer Overdue Amount", compute='_compute_overdue_amount', currency_field='overdue_currency_id')
    overdue_currency_id = fields.Many2one('res.currency', compute='_compute_overdue_amount')

    @api.depends('partner_id', 'company_id')
    def _compute_overdue_amount(self):
        for order in self:
            partner = order.partner_id.with_company(order.company_id)
            order.overdue_amount = partner.overdue_amount if order.partner_id else 0.0
            order.overdue_currency_id = order.company_id.currency_id

    def action_view_overdue_invoices(self):
        self.ensure_one()
        return self.partner_id.with_company(self.company_id).action_view_overdue_invoices()

    def action_print_overdue_statement(self):
        self.ensure_one()
        return self.env.ref('hfb_app_sale_overdue_warning.action_report_overdue_statement').report_action(
            self.partner_id.commercial_partner_id)

    def action_confirm(self):
        is_manager = self.env.user.has_group('sales_team.group_sale_manager')
        for order in self:
            if order.company_id.currency_id.compare_amounts(order.overdue_amount, 0) <= 0:
                continue
            amount = order.company_id.currency_id.format(order.overdue_amount)
            if order.company_id.overdue_block_confirmation and not is_manager:
                raise UserError(_(
                    "%(customer)s has overdue invoices for %(amount)s. Only a sales manager can confirm %(order)s.",
                    customer=order.partner_id.commercial_partner_id.display_name, amount=amount, order=order.name))
            order.message_post(body=_("Confirmed while the customer has overdue invoices for %s.", amount))
        return super().action_confirm()

#EoF
