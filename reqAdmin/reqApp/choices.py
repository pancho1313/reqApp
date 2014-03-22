# -*- encoding: utf-8 -*-
""" *_CHOICES: Se definen aqui y de forma estatica para evitar que
modificaciones indeseadas en la base de datos arruinen el codigo. """
ESTABILIDAD_CHOICES = [
    ("transable", "transable"),
    ("intransable", "intransable"),
]

TIPO_RU_CHOICES = [
    ("funcional", "funcional"),
    ("calidad", "calidad"),
    ("restricción", "restricción"),
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
    ("documentación", "documentación"),
]

PRIORIDAD_CHOICES = [
    ("crítico","crítico"),
    ("deseable","deseable"),
    ("innecesario","innecesario"),
]

ESTADO_CHOICES = [
    ("cumple", "cumple"),
    ("no cumple", "no cumple"),
    ("ambiguo", "ambiguo"),
]
