# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Jarmo Kortetjärvi
#    Copyright 2015 Oy Tawasta OS Technologies Ltd.
#    Copyright 2015 Vizucom Oy
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Finland - Accounting',
    'category': 'Localization/Account Charts',
    'version': '1.2',
    'author': 'Vizucom Oy, Oy Tawasta OS Technologies Ltd., Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'http://www.vizucom.com, http://www.tawasta.com',
    'depends': [
        'account',
        'account_chart',
        'base_vat',
        'base_iban'
    ],
    'description': """
Odoo Finnish Localization (l10n_fi_liikekirjuri)
===================================

A Finnish chart of accounts and tax localization for Odoo.
Based on 'Liikekirjurit' accounts chart version 7.0
(http://www.kirjurituote.fi/tuotteet/liikekirjuri/)

This is the comprehensive version of the accounts chart,
and should be sufficient for all industries and company types.

The number of accounts is approx. 950
The number of headers is approx. 300
""",
    'data': [
        'data/account.account.type.csv',
        'data/account.account.template.csv',
        'data/account.tax.code.template.csv',
        'data/account.chart.template.csv',
        'data/account.tax.template.csv',
    ],
    'installable': 'True',
    'images': [],
}
