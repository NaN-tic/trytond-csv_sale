#:after:csv_import/csv_import:section:ejemplos#

.. inheritref:: csv_import/csv_import:section:importacion_csv_para_pedidos_de_venta

Importación CSV para pedidos de venta
=====================================

En los ficheros CSV que crean pedidos de venta no hace falta añadir en el fichro 
todas las columnas del pedido y de las líneas. Los campos del pedido y de las líneas
serán calculados a partir de la información por defecto.

De este modo podrá crear pedidos de venta sólo con las columnas del CSV:

* Nombre tercero
* Código de producto
* Cantidad

Todos los demás campos, se calcularán: (unidades, moneda, impuestos, tarifas, mensajeros, etc)

Ejemplo de fichero para pedidos de venta
----------------------------------------

.. code-block:: csv

    "Cliente","Producto","Cantidad"
    "Zikzakmedia","PROD1",1
    ,,,"PROD2",10
    ,,,"PROD3",20

Es importante en este ejemplo ens los mapeos, hacer algunos cálculos:

* Cliente:

.. code-block:: python

    result = None
    Party = pool.get('party.party')
    parties = Party.search([('name', '=', values)])
    if parties:
        result = parties[0]

* Producto:

.. code-block:: python

    result = None
    Product = pool.get('product.product')
    products = Product.search([('code', '=', values)])
    if products:
        result = products[0]
