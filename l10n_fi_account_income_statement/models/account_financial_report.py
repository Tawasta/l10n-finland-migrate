# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class AccountFinancialReport(models.Model):
    
    # Constants:
    # Use underscore uppercase notation for global variables or constants.

    # 1. Private attributes
    _inherit = 'account.financial.report'

    # 2. Fields declaration
    code = fields.Char('Unique code')
    company = fields.Many2one('res.company', 'Company')

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods

    @api.model
    def _init_income_statement_reports(self):
        # When the module is installed,
        # fetch all companies and create income statements
        companies = self.company.search([])
        
        for company in companies:
            self._delete_internal_income_statement_report(company)
            self._create_internal_income_statement_report(company)
            
            self._delete_external_income_statement_report(company)
            self._create_external_income_statement_report(company)
            
            self._delete_balance_sheet_report(company)
            self._create_balance_sheet_report(company)
     
    def _delete_internal_income_statement_report(self, company):
        reports = self.search([
            ('company', '=', company.id),
            '|', '|',
            ('code', '=', 'STU'),
            ('parent_id.code', '=', 'STU'),
            ('parent_id.parent_id.code', '=', 'STU')
        ])
        
        # Remote related accounting reports
        self.env['accounting.report'].search([
            ('account_report_id', 'in', reports.ids)
        ]).unlink()
        
        reports.unlink()

    def _delete_external_income_statement_report(self, company):
        reports = self.search([
            ('company', '=', company.id),
            '|', '|',
            ('code', '=', 'UTU'),
            ('parent_id.code', '=', 'UTU'),
            ('parent_id.parent_id.code', '=', 'UTU')
        ])
        
        # Remote related accounting reports
        self.env['accounting.report'].search([
            ('account_report_id', 'in', reports.ids)
        ]).unlink()
        
        reports.unlink()
        
    def _delete_balance_sheet_report(self, company):
        reports = self.search([
            ('company', '=', company.id),
            '|', '|',
            ('code','=', 'TASE'),
            ('parent_id.code', '=', 'TASE'),
            ('parent_id.parent_id.code', '=', 'TASE')
        ])
        
        # Remote related accounting reports
        self.env['accounting.report'].search([
            ('account_report_id', 'in', reports.ids)
        ]).unlink()
        
        reports.unlink()
     
    # CREATE METHODS
    def _create_internal_income_statement_report(self, company):
        self._create_income_statement_report(company, 'internal')

    def _create_external_income_statement_report(self, company):
        self._create_income_statement_report(company, 'external')

    def _create_income_statement_report(self, company, statement='internal'):
        if statement not in ('internal', 'external'):
            return False

        if statement == 'internal':
            display_detail = 'detail_flat'
            prefix = 'S'

            report_header = self.create({
                'company': company.id,
                'code': 'STU',
                'name': 'Sisäinen Tuloslaskelma'
            })

        if statement == 'external':
            display_detail = 'no_detail'
            prefix = 'U'

            report_header = self.create({
                'company': company.id,
                'code': 'UTU',
                'name': 'Ulkoinen Tuloslaskelma'
            })

        # Sales header (turnover)
        report_turnover = self.create({
            'company': company.id,
            'code': '%sTUT'  % prefix,
            'name': 'LIIKEVAIHTO',
            'type': 'sum',
            'sequence': '10',
            'display_detail': display_detail,
            'sign': -1,
            'parent_id': report_header.id,
        })

        # Sales
        for account in self._get_statement_income_accounts(company):
            self.create({
                'company': company.id,
                'code': '%s%s' % (prefix, account.code),
                'name': account.name,
                'type': 'accounts',
                'sequence': '10',
                'display_detail': display_detail,
                'sign': -1,
                'parent_id': report_turnover.id,
                'account_ids': [(6, 0, account.ids)]
            })

        # Expenses header
        report_expenses = self.create({
            'company': company.id,
            'code': '%sTUE' % prefix,
            'name': 'KULUT',
            'type': 'sum',
            'sequence': '100',
            'display_detail': display_detail,
            'sign': -1,
            'parent_id': report_header.id,
        })

        # Expenses
        for account in self._get_statement_expenses_accounts(company):
            self.create({
                'company': company.id,
                'code': '%s%s' % (prefix, account.code),
                'name': account.name,
                'type': 'accounts',
                'sequence': '110',
                'display_detail': display_detail,
                'sign': -1,
                'parent_id': report_expenses.id,
                'account_ids': [(6, 0, account.ids)]
            })

        # Summary
        for account in self._get_statement_summary_accounts(company):
            self.create({
                'company': company.id,
                'code': '%s%s' % (prefix, account.code),
                'name': account.name,
                'type': 'accounts',
                'sequence': '120',
                'display_detail': 'no_detail',
                'sign': -1,
                'parent_id': report_header.id,
                'account_ids': [(6, 0, account.ids)]
            })

        # Post results
        for account in self._get_statement_post_result_accounts(company):
            self.create({
                'company': company.id,
                'code': '%s%s' % (prefix, account.code),
                'name': account.name,
                'type': 'accounts',
                'sequence': '130',
                'display_detail': display_detail,
                'sign': -1,
                'parent_id': report_expenses.id,
                'account_ids': [(6, 0, account.ids)]
            })

        # Profit / Loss
        for account in self._get_result_accounts(company):
            self.create({
                'company': company.id,
                'code': '%s%s' % (prefix, account.code),
                'name': account.name,
                'type': 'accounts',
                'sequence': '140',
                'display_detail': 'no_detail',
                'sign': -1,
                'parent_id': report_header.id,
                'account_ids': [(6, 0, account.ids)]
            })

    def _get_statement_income_accounts(self, company):
        accounts = self.env['account.account'].search([
            ('company_id', '=', company.id),
            ('code', 'in', [
                'TUMT',  # Myyntituotot
                'TULT',  # Liiketoiminnan muut tuotot
            ])
        ])

        return sorted(accounts, key=lambda l: l.code, reverse=True)

    def _get_statement_expenses_accounts(self, company):
        accounts = self.env['account.account'].search([
            ('company_id', '=', company.id),
            ('code', 'in', [
                'TUHK',  # Henkilöstökulut
                'TULK',  # Liiketoiminnan muut kulut
                'TUMP',  # Materiaalit ja palvelut
                'TUOV',  # Osuus osakkuusyritysten voitosta (tappiosta)
                'TUPA',  # Poistot ja arvonalentumiset
            ])
        ])

        return accounts

    def _get_statement_summary_accounts(self, company):
        accounts = self.env['account.account'].search([
            ('company_id', '=', company.id),
            ('code', 'in', [
                'TUTT',  # TILIKAUDEN VOITTO (TAPPIO)
                # 'TUTV',  # Tuloverot
            ])
        ])

        return accounts

    def _get_statement_post_result_accounts(self, company):
        accounts = self.env['account.account'].search([
            ('company_id', '=', company.id),
            ('code', 'in', [
                'TURR',  # Rahoitustuotot ja -kulut
                'TUES',  # Tulos ennen satunnaisia eriä
                'TUET',  # Tulos ennen tilinpäätössiirtoja ja veroja
            ])
        ])

        return accounts

    def _get_result_accounts(self, company):
        accounts = self.env['account.account'].search([
            ('company_id', '=', company.id),
            ('code', 'in', [
                'TULOS',  # TULOS
            ])
        ])

        return accounts

    def _create_balance_sheet_report(self, company):
        ## ASSETS AND LIABILITIES
        report_header = self.create({
            'company': company.id,
            'code': 'TASE',
            'name': 'Tase',
            'type': 'sum',
            'sequence': '10',
            'display_detail': 'detail_flat',
        })

        tavv = self.env['account.account'].search([
            ('company_id', '=', company.id),
            ('code', 'in', ['TAVV'])
        ])
        self.create({
            'company': company.id,
            'code': 'TAVV',
            'name': 'VASTAAVAA',
            'type': 'accounts',
            'sequence': '10',
            'display_detail': 'detail_with_hierarchy',
            'parent_id': report_header.id,
            'account_ids': [(6, 0, tavv.ids)]
        })

        tavt = self.env['account.account'].search([
            ('company_id', '=', company.id),
            ('code', 'in', ['TAVT'])
        ])
        self.create({
            'company': company.id,
            'code': 'TAVT',
            'name': 'VASTATTAVAA',
            'type': 'accounts',
            'sequence': '20',
            'display_detail': 'detail_with_hierarchy',
            'parent_id': report_header.id,
            'account_ids': [(6, 0, tavt.ids)]
        })
