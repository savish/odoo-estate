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


class Estate(models.Model):
    _name = "estate.estate"
    _description = "An estate with a number of properties"

    name = fields.Char()
    property_ids = fields.One2many("estate.property", "estate_id", string="Properties")


class PropertyInvoice(models.Model):
    _inherit = "account.invoice"

    property_id = fields.Many2one("estate.property", string="Property")
