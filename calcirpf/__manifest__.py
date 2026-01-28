# -*- coding: utf-8 -*-
{
    'name': "Calculo IRPF",

    'summary': "módulo hecho por Francisco Alía para calcular el irpf",

    'description': """
    Se desea desarrollar un módulo nuevo en Odoo llamado Calculadora IRPF, cuyo objetivo es calcular el IRPF y el salario neto de un asalariado en función de distintos parámetros personales y económicos.

    """,

    'author': "Francisco Alía Hernández",
    'website': "https://github.com/alion1992",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

