# Customer Overdue Warning

Overdue warning on quotations and orders, with a tolerance in days, an optional confirmation block and an Overdue Statement.

## What it does

- **Warning on the quotation** - A banner shows the customer's overdue amount, with shortcuts to the late invoices and to the statement.
- **Tolerance in days** - Invoices only a few days late are ignored. Set a company default and override it per customer.
- **Optional block** - Block the confirmation of orders for customers with overdue invoices. Sales managers can still confirm - it is logged.
- **Overdue Statement** - Printable PDF with every late invoice: dates, days overdue, amount due and total.
- **Send by e-mail** - One click on the customer sends the statement with a ready-to-edit e-mail template.
- **Accurate amounts** - Computed from open receivable items, so partial payments and credit notes are taken into account.

## How to use it

1. Go to Sales > Configuration > Settings, section Quotations & Orders: set the Overdue Tolerance (days) and, if you want, tick Block Orders of Customers with Overdue Invoices.
2. Optionally, on a customer (tab Sales & Purchase, section Misc), set a different tolerance.
3. Open a quotation for a customer with late invoices: a yellow banner shows the overdue amount, with View and Print Statement.
4. On the customer form, the red Overdue button lists the late invoices and Send Overdue Statement e-mails the PDF.

## Good to know

- Amounts are in the company currency and per company.
- Overdue = open receivable items whose due date is before today minus the tolerance.
- Without the block option, orders can always be confirmed; the confirmation is noted in the chatter.

## Technical

- Depends only on `sale`.
- Overdue items: `account.move.line` with a receivable account, posted, not reconciled, `date_maturity` before the cut-off.
- Hook: `sale.order.action_confirm()`; report `hfb_app_sale_overdue_warning.report_overdue_statement` on `res.partner`.

## Status

Odoo 19 build. Tested on the Odoo.sh test instances (automated RPC tests and manual tests, 2026-10-09). Icon and banner included - ready for publication.
