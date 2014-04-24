# -*- encoding: utf-8 -*-
""" *_CHOICES: Se definen aqui y de forma estatica para evitar que
modificaciones indeseadas en la base de datos arruinen el codigo. """
ESTABILIDAD_CHOICES = [
    ("intransable", "intransable"),
    ("transable", "transable"),
]

TIPO_RU_CHOICES = [
    ("funcional", "funcional"),
    ("calidad", "calidad"),
    ("restriccion", "restricción"),
]

TIPO_RS_CHOICES = [
    ("funcional", "funcional"),
    ("usabilidad", "usabilidad"),
    ("mantenibilidad", "mantenibilidad"),
    ("rendimiento", "rendimiento"),
    ("portabilidad", "portabilidad"),
    ("escalabilidad", "escalabilidad"),
    ("confiabilidad", "confiabilidad"),
    ("interoperabilidad", "interoperabilidad"),
    ("interfaz", "interfaz"),
    ("operacional", "operacional"),
    ("recursos", "recursos"),
    ("documentacion", "documentación"),
]

PRIORIDAD_CHOICES = [
    ("critico","crítico"),
    ("deseable","deseable"),
    ("innecesario","innecesario"),
]

ESTADO_CHOICES = [
    ("cumple", "cumple"),
    ("no_cumple", "no cumple"),
    ("ambiguo", "ambiguo"),
]
