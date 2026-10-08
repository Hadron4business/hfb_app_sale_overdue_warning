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
"""	@version	20.0.1.0.0
	@owner  Hadron for Business
	@author Hadron for Business sp. z o.o.
	@date   2026.10.08

	Customer Overdue Warning - company settings
	Default tolerance in days before an invoice counts as overdue, and the
	option to block the confirmation of orders of customers with overdue
	invoices.
"""
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    overdue_tolerance_days = fields.Integer(
        string="Overdue Tolerance (days)", default=0,
        help="Invoices due fewer days ago than this are not considered overdue.")
    overdue_block_confirmation = fields.Boolean(string="Block Orders of Customers with Overdue Invoices")

#EoF
