# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp.exceptions import ValidationError

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ResPartner(models.Model):
    
    # 1. Private attributes
    _inherit = 'res.partner'

    # 2. Fields declaration
    business_id = fields.Char('Business id')

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.onchange('business_id')
    def onchange_business_id_update_format(self):
        # Reformat business id from 12345671 to 1234567-1
        if isinstance(self.business_id, basestring) and re.match('^[0-9]{8}$', self.business_id):
            self.business_id = self.business_id[:7] + '-' + self.business_id[7:]

    @api.constrains('business_id')
    def _validate_business_id(self):
        business_id = self.business_id

        # Country code is not FI, skip this
        if self.country_id.code != 'FI':
            return True

        # Business id is not set. This is fine.
        if not business_id:
            return True

        # Validate registered association format
        # TODO: validate this
        if re.match('^[0-9]{3}[.][0-9]{3}$', business_id):
            # Registered association(rekisteröity yhdistys, ry / r.y.). Format 123.456
            return True

        # Validate business id formal format
        if not re.match('^[0-9]{7}[-][0-9]{1}$', business_id):
            raise ValidationError("Your business id is invalid. Please use format 1234567-1")

        # The formal format is ok, check the validation number
        multipliers = [7, 9, 10, 5, 8, 4, 2]  # Number-space spesific multipliers
        validation_multiplier = 0  # Initial multiplier
        number_index = 0  # The index of the number we are parsing

        business_id_number = re.sub("[^0-9]", "", business_id)  # business id without "-" for validation
        validation_bit = business_id_number[7:8]

        # Test the validation bit
        for number in business_id_number[0:7]:
            validation_multiplier += multipliers[number_index] * int(number)
            number_index += 1

        modulo = validation_multiplier % 11

        # Get the final modulo
        if modulo >= 2 and modulo <= 10:
            modulo = 11 - modulo

        if int(modulo) != int(validation_bit):
            raise ValidationError("Your business check number is invalid. Please check the given business id")

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
