# -*- coding: utf-8 -*-
# vim: tabstop=4 softtabstop=0 shiftwidth=4 smarttab expandtab fileformat=unix
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
{
    'name': "Customer Overdue Warning",
    'summary': "See a customer's overdue invoices right on the quotation, optionally block the confirmation, "
               "and send an overdue statement",
    'description': """
Customer Overdue Warning
========================

Odoo's credit limit looks at the total amount due, not at invoices that are
already late. Salespeople keep confirming orders for customers who have not
paid for months.

This app shows a warning with the overdue amount on quotations and sales
orders, with a tolerance in days (per company, overridable per customer), so
an invoice that is one day late does not trigger it. Optionally, confirming
the order is blocked until the customer pays - sales managers can still
confirm. A printable and e-mailable Overdue Statement lists the late
invoices of the customer.
""",
    'version': "18.0.1.0.1",
    'author': "Hadron for Business sp. z o.o.",
    'website': "http://hadronforbusiness.com",
    'license': "OPL-1",
    'category': "Sales/Sales",
    'depends': [
        'sale',
    ],
    'data': [
        'report/overdue_statement_report.xml',
        'data/mail_template_data.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
    ],
    'images': [
        'static/description/banner_screenshot.png',
    ],
    'installable': True,
    'application': False,
}
