# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api


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
        store=False)
    salario_mensual = fields.Integer()
    pagas_extra = fields.Integer()

    @api.depends('salarioBruto','numeroPagas','situacionActual','hijos')
    def _compute_irpf(self):
        for calculo in self:
            match self.salarioBruto:
                case s if s >= 0 and s < 12450:
                    self.irpf = 19
                case s if s >= 12450 and s < 20000:
                    self.irpf = 24
                case s if s >= 20200 and s < 35200:
                    self.irpf = 30
                case s if s >= 35200 and s < 60000:
                    self.irpf = 37
                case s if s >= 60000 and s < 300000:
                    self.irpf = 45
                case s if s >= 300000:
                    self.irpf = 47

        if self.situacionActual == 'trabajador':
            if int(self.hijos) == 1:
                self.irpf = self.irpf - 2
            elif int(self.hijos) == 2:
                self.irpf = self.irpf - 4
            elif int(self.hijos) == 4:
                self.irpf = self.irpf -5
        else:
            self.irpf = self.irpf*0.70





