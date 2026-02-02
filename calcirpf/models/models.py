# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class calcirpf(models.Model):
    _name = 'calcirpf.responsable'
    _description = 'Persona responsable de el calculo del irpf'

    nombre = fields.Char(string="Nombre", required=True)
    apellido1 = fields.Char(string="Primer Apellido", required=True)
    apellido2 = fields.Char(string="Segundo Apellido", required=True)
    fecha_nacimiento = fields.Date(string="Fecha Nacimiento")
    edad = fields.Integer(
        string="Edad",
        compute="_compute_edad",
        store=False
    )
    
    nombreCompleto = fields.Char(compute="_nombre_completo", store=False)
    calculos_ids = fields.One2many('calcirpf.calculo', 'responsable_id')

    @api.depends('nombre','apellido1','apellido2')
    def _nombre_completo(self):
        for record in self:
            if record.nombre and record.apellido1 and record.apellido2:
                record.nombreCompleto = f"{record.nombre} {record.apellido1} {record.apellido2}"
            else:
                record.nombreCompleto = ''

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        today = datetime.today()
        for record in self:
            if record.fecha_nacimiento:
                nacimiento = record.fecha_nacimiento
                record.edad = today.year - nacimiento.year - (
                    (today.month, today.day) < (nacimiento.month, nacimiento.day)
                )
            else:
                record.edad = 0

   

class calculo(models.Model):
    _name = 'calcirpf.calculo'
    _description = 'calculos del irpf'

    nombre = fields.Char(required=True)
    apellidos = fields.Char(required=True)
    salarioBruto = fields.Integer(required=True, sprint="Salario Bruto", string="Salario Bruto")
    edad = fields.Integer(required=True)
    hijos = fields.Selection([('0','0'),('1','1'),('2','2 o 3'),('4','4 o más')],default='0')
    situacionActual = fields.Selection([('none','Selecciona una opción'),('trabajador','Trabajador'),('jubilado','Jubilado')], required=True, default='none',string="Situación Actual")
    numeroPagas = fields.Selection([('12','12'),('14','14')],string="Número de pagas",default='12')
    responsable_id = fields.Many2one('calcirpf.responsable')
    irpf = fields.Integer(string="%IRPF",compute="_compute_irpf",
        store=False,required=True)
    salario_mensual = fields.Integer(compute="_compute_salario_mensual")
    pagas_extra = fields.Integer(compute="_compute_paga_extra")
    etiquetas = fields.Many2many('calcirpf.etiqueta')

    @api.depends('salarioBruto','numeroPagas','situacionActual','hijos')
    def _compute_irpf(self):
        for calculo in self:
            match calculo.salarioBruto:
                case s if s >= 0 and s < 12450:
                    calculo.irpf = 19
                case s if s >= 12450 and s < 20000:
                    calculo.irpf = 24
                case s if s >= 20200 and s < 35200:
                    calculo.irpf = 30
                case s if s >= 35200 and s < 60000:
                    calculo.irpf = 37
                case s if s >= 60000 and s < 300000:
                    calculo.irpf = 45
                case s if s >= 300000:
                    calculo.irpf = 47

        if calculo.situacionActual == 'trabajador':
            if int(calculo.hijos) == 1:
                calculo.irpf = calculo.irpf - 2
            elif int(calculo.hijos) == 2:
                calculo.irpf = calculo.irpf - 4
            elif int(calculo.hijos) == 4:
                calculo.irpf = calculo.irpf -5
        else:
            calculo.irpf = calculo.irpf*0.70
    
    @api.depends('salarioBruto','irpf','numeroPagas')
    def _compute_salario_mensual(self):
        for calculo in self:
            if calculo.numeroPagas == '12':
                calculo.salario_mensual = calculo.salarioBruto/12 * ((100-calculo.irpf)/100)
            else:
                calculo.salario_mensual = calculo.salarioBruto/14 * ((100-calculo.irpf)/100)

    @api.depends('salario_mensual','numeroPagas')     
    def _compute_paga_extra(self):
        for calculo in self:
            if calculo.numeroPagas == '14':
                calculo.pagas_extra = calculo.salarioBruto/12 * ((100-calculo.irpf-5)/100)
            else:
                calculo.pagas_extra = 0
              

    @api.model
    def create(self, vals):
        
        calculo = super().create(vals)
        
        _logger.info("Creando modelo")
        
        if calculo.salario_mensual and calculo.salario_mensual > 3000:
            _logger.info("Miro si gana mas de 3000")
            etiqueta = self.env['calcirpf.etiqueta'].search(
                [('nombre', '=', 'Millonario')],
                limit=1
            )
            if not etiqueta:
                etiqueta = self.env['calcirpf.etiqueta'].create({
                    'nombre': 'Millonario',
                    'descripcion': 'Salario mensual superior a 3000€'
                })
            _logger.info("Se asigna etiqueta Millonario")
            calculo.etiquetas = [(4, etiqueta.id)]
        elif calculo.salario_mensual and calculo.salario_mensual < 1000:
            _logger.info("Bajo Salario")
            #Tambien esta search_count que devuelve un numero
            #Select * from etiqueta where nombre like 'baja'
            # select count(*) from etiqueta where nombre like 'baja'
            etiqueta = self.env['calcirpf.etiqueta'].search(
                [('nombre', '=', 'Baja')],
                limit=1
            )
            if not etiqueta:
                #insert into etiqueta (..) values ('baja',)
                etiqueta = self.env['calcirpf.etiqueta'].create({
                    'nombre': 'Baja',
                    'descripcion': 'Salario mensual superior a 3000€'
                })
            _logger.info("Se asigna etiqueta bajo")
            calculo.etiquetas = [(4, etiqueta.id)]

        return calculo


class etiquetas(models.Model):
    _name = 'calcirpf.etiqueta'
    _description = 'etiqueta'

    nombre = fields.Char()
    descripcion = fields.Char()

