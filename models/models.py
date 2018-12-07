# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Property(models.Model):
    _name = "estate.property"
    _description = "A property in an estate"

    name = fields.Char()
    levy_amount = fields.Float(string="Levy amount")
    partner_id = fields.Many2one("res.partner", string="Partner")
    estate_id = fields.Many2one("estate.estate", string="Estate")
    invoice_ids = fields.One2many("account.invoice", "property_id", string="Invoices")

    def generate_property_invoice(self):
        self.ensure_one()

        existing_product = self.env["product.product"].search(
            [["name", "=", f"Levy: {self.estate_id.name}"]]
        )
        if len(existing_product) == 0:
            product = self.env["product.product"].create(
                {"name": f"Levy: {self.estate_id.name}", "price": self.levy_amount}
            )
        else:
            product = existing_product[0]

        invoice = self.env["account.invoice"].create(
            {
                "type": "out_invoice",
                "state": "open",
                "partner_id": self.partner_id.id,
                "property_id": self.id,
            }
        )

        existing_acc_type = self.env["account.account.type"].search([["name", "=", "Levy Account"]])
        if len(existing_acc_type) == 0:
            account_type = self.env["account.account.type"].create(
                {"name": "Levy Account", "type": "receivable", "internal_group": "income"}
            )
        else:
            account_type = existing_acc_type[0]

        existing_account = self.env["account.account"].search([["name", "=", "My Account"]])
        if len(existing_account) == 0:
            account = self.env["account.account"].create(
                {
                    "name": "My Account",
                    "code": "MYACC123",
                    "user_type_id": account_type.id,
                    "reconcile": True,
                }
            )
        else:
            account = existing_account[0]

        self.env["account.invoice.line"].create(
            {
                "name": f"Levy: {self.estate_id.name}",
                "invoice_id": invoice.id,
                "product_id": product.id,
                "price_unit": self.levy_amount,
                "account_id": account.id,
            }
        )

        return {
            "name": "Property Invoice Form",
            "view_type": "form",
            "view_mode": "form",
            "target": "new",
            "res_model": "account.invoice",
            "type": "ir.actions.act_window",
            "res_id": invoice.id,
        }


class Estate(models.Model):
    _name = "estate.estate"
    _description = "An estate with a number of properties"

    name = fields.Char()
    property_ids = fields.One2many("estate.property", "estate_id", string="Properties")


class PropertyInvoice(models.Model):
    _inherit = "account.invoice"

    property_id = fields.Many2one("estate.property", string="Property")
