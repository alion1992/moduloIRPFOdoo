SIMULACRO PRUEBA PRÁCTICA
• Módulo: Calculadora IRPF
Se desea desarrollar un módulo nuevo en Odoo llamado Calculadora IRPF,
cuyo objetivo es calcular el IRPF y el salario neto de un asalariado en función de
distintos parámetros personales y económicos.
Estructura del módulo
El módulo contará con dos opciones de menú principales:
Responsable
Representa a la persona que realiza los cálculos de IRPF.
Campos obligatorios y calculados:
• Nombre
• Apellidos
• Nombre completo (campo calculado, no se almacena en base de datos)
• Fecha de nacimiento
• Edad (campo calculado a partir de la fecha de nacimiento, no se almacena
en base de datos)
Se deberán implementar:
• Vista tree
• Vista form
Cálculo IRPF (Renta)
Representa un cálculo de IRPF realizado para un asalariado concreto.
Cada cálculo:
• Debe estar asociado obligatoriamente a un Responsable
• Corresponde a una persona sobre la que se calcula el IRPF
Datos a introducir:
• Nombre del asalariado (obligatorio)
• Apellidos del asalariado (obligatorio)
• Salario bruto anual
• Edad
• Situación laboral:
o Trabajador
o Jubilado
• Número de hijos (no puede ser 0)
• Número de pagas:
o 12
o 14
Campos calculados:
• IRPF aplicado (%)
• Salario neto mensual
• Importe de las pagas extra (si las hubiera)
Se deberán implementar:
• Vista tree
• Vista form
• Cálculo del IRPF
Tramos de IRPF según salario bruto anual
Salario bruto anual IRPF
De 0 a 12.450 € 19%
De 12.450 € a 20.200 € 24%
De 20.200 € a 35.200 € 30%
De 35.200 € a 60.000 € 37%
De 60.000 € a 300.000 € 45%
Más de 300.000 € 47%
Ajustes sobre el IRPF
• Edad entre 18 y 45 años → se incrementa el IRPF en 1 punto
• Número de hijos:
o 1 hijo → se reduce 2 puntos
o 2 o 3 hijos → se reduce 4 puntos
o 3 o más hijos → se reduce 5 puntos
• Situación: Jubilado
o Se reduce el IRPF final en un 30%
o No se tienen en cuenta los hijos
Validaciones obligatorias
Se deberá validar que:
• El nombre y los apellidos del asalariado están informados
• El número de hijos no puede ser 0
Las validaciones deberán impedir guardar el registro si no se cumplen las
condiciones.
• Restricciones de borrado
• No se podrá borrar ningún cálculo de IRPF cuyo salario neto mensual
sea superior a 3.000 €
• Al borrar un Responsable, se deberán eliminar automáticamente todos
los cálculos de IRPF asociados a dicho responsable
https://cincodias.elpais.com/herramientas/calculadora-irpf/
Ampliación:
Ejercicio 1
Establecer un nuevo modelo etiquetas:
Con nombre y descripción.
Este nuevo modelo va relacionado con calculadora iprf ya que en función de
algunas rentas se le asignaran una serie de etiquetas.
Por defecto se tienen que cargar las siguientes etiquetas:
- Joven (persona entre 16 y 36 años)
- Adulto (persona entre 37 y 65 años)
- Jubilado (persona de más de 65 años)
- Salario medio: Persona entre 0 y 1500 euros limpios mensuales)
- Millonario: Más de 1500 euros
Ejercicio2
Tanto para crear como para modificar una renta se tiene que introducir de forma
automática las etiquetas sobre la persona que cumpla las condiciones. Si esta
renta ya tiene las etiquetas no se deben introducir.
“Insertar datos con créate”
https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.ht
ml
Añadir a la renta dos imágenes: Vista frontal y Vista Trasera que se debe adjuntar
el dni de la persona sobre la que se está realizando la venta.
Diseñar la tarjeta kanvan donde se vea las imágenes del dni y el salario bruto y
neto.
Explicar luego
https://www.odoo.com/documentation/19.0/applications/studio/fields.html
https://developer.mozilla.org/es/docs/Web/HTML/Reference/Elements/progress
