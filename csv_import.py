# This file is part of csv_sale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta

__all__ = ['CSVArchive']


class CSVArchive:
    __metaclass__ = PoolMeta
    __name__ = 'csv.archive'

    @classmethod
    def _import_data_sale(cls, record, values, parent_values=None):
        '''
        Sale and Sale Line data
        '''
        pool = Pool()
        Sale = pool.get('sale.sale')
        SaleLine = pool.get('sale.line')
        Party = pool.get('party.party')

        record_name = record.__name__

        if record_name == 'sale.sale':
            party = values.get('party')

            if party:
                party = Party(party)

                if not record.id:
                    record = Sale.get_sale_data(values.get('party'))

                    if hasattr(record, 'shop') and not getattr(record, 'shop'):
                        shop, = pool.get('sale.shop').search([], limit=1)
                        record.shop = shop

                if values.get('invoice_address') \
                        and values.get('invoice_address') in party.addresses:
                    record.invoice_address = values.get('invoice_address')

                if values.get('shipment_address') \
                        and values.get('shipment_address') in party.addresses:
                    record.shipment_address = values.get('shipment_address')

                if values.get('customer_reference'):
                    record.customer_reference = values.get('customer_reference')

                if values.get('lines'):
                    record.lines = values.get('lines')

                return record

        if record_name == 'sale.line':
            if values.get('product') and values.get('quantity'):
                sale = Sale.get_sale_data(parent_values.get('party'))
                line = SaleLine.get_sale_line_data(
                            sale,
                            values.get('product'),
                            values.get('quantity')
                            )
                line.on_change_product()

                return line

        return record
