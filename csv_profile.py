# This file is part of csv_sale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal
from trytond.pool import Pool, PoolMeta

__all__ = ['CSVArchive']
__metaclass__ = PoolMeta


class CSVArchive:
    __name__ = 'csv.archive'

    @classmethod
    def _add_default_values(cls, csv_model, values):
        pool = Pool()
        model = csv_model.model.model
        ModelToImport = pool.get(model)
        Product = pool.get('product.product')
        default_values = {}
        if model == 'sale.sale' and values[model].get('party'):
            Party = pool.get('party.party')
            party = Party(values[model]['party'])
            sale = ModelToImport()
            sale.party = party
            default_values = sale.on_change_party()
            default_values['state'] = 'quotation'
        elif model == 'sale.line' and values[model].get('product'):
            product = values[model]['product']
            default_values['description'] = product.name
            default_values['unit'] = product.sale_uom
            default_values['cost_price'] = product.cost_price
            unit_price = Product.get_sale_price(
                [product], values[model]['quantity'] or 0)[product.id]
            if unit_price:
                default_values['unit_price'] = unit_price.quantize(
                    Decimal(1) / 10 ** ModelToImport.unit_price.digits[1])
        elif model in ('sale.sale', 'sale.line'):
            cls.raise_user_error('cant_update',
                error_args=(model, values[model]))
        for x in default_values:
            if x not in values[model] and '.rec_name' not in x:
                values[model].update({x: default_values[x]})
        super(CSVArchive, cls)._add_default_values(csv_model, values)

    @classmethod
    def _search_children(cls, csv_model, parent_record, values):
        res = super(CSVArchive, cls)._search_children(csv_model,
            parent_record, values)
        pool = Pool()
        model = csv_model.model.model
        ModelToUpdate = pool.get(model)
        rel_field = csv_model.rel_field.name
        res.extend(ModelToUpdate.search([
                (rel_field, '=', parent_record.id),
                ('product', '=', values[model].get('product')),
                ]))
        return res
