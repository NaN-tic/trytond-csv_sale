# This file is part of csv_sale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['CSVArchive']
__metaclass__ = PoolMeta


class CSVArchive:
    __name__ = 'csv.archive'

    @classmethod
    def _add_default_values(cls, model, values, parent_values=None):
        '''
        Get default values from Sale and SaleLine objects
        '''
        values = super(CSVArchive, cls)._add_default_values(model, values, parent_values)

        pool = Pool()
        Sale = pool.get('sale.sale')
        SaleLine = pool.get('sale.line')
        Company = pool.get('company.company')

        model_name =  model.__name__

        if model_name == 'sale.sale':
            party = values.get('party')
            if party:
                Party = pool.get('party.party')
                party = Party(party)
                model.party = party
                vals = Sale(**values).on_change_party()
                vals.update(values)
                values = vals.copy()

        if model_name == 'sale.line':
            if values.get('product') and values.get('quantity'):
                currency = parent_values.get('currency')
                if not currency:
                    company = Transaction().context.get('company')
                    if company:
                        currency = Company(company).currency.id
                sale = Sale.get_sale_data(parent_values.get('party'))
                values = {
                    'product': values.get('product'),
                    '_parent_sale.currency': currency,
                    '_parent_sale.party': parent_values.get('party'),
                    'sale': sale,
                    'type': 'line',
                    'quantity': values.get('quantity'),
                    'unit': None,
                    'description': None
                }
                values.update(SaleLine(**values).on_change_product())
                values.update(SaleLine(**values).on_change_quantity())
                del values['_parent_sale.currency']
                del values['_parent_sale.party']
                del values['sale']

        return values
