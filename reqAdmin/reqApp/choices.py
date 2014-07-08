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
    ("critico","urgente"),
    ("deseable","normal"),
    ("innecesario","pronto"),
]

ESTADO_CHOICES = [
    ("cumple", "cumple"),
    ("no_cumple", "no cumple"),
    ("ambiguo", "ambiguo"),
]

PARRAFOS_CHOICES = [
    ("introduccion", "Introducción"),
    ("proposito", "Introducción/Propósito"),
    ("alcance", "Introducción/Alcance"),
    ("contexto", "Introducción/Contexto"),
    ("definiciones", "Introducción/Definiciones"),
    ("referencias", "Introducción/Referencias"),
    ("descripcion_general", "Descripción General"),
    ("usuarios", "Descripción General/Usuarios"),
    ("producto", "Descripción General/Producto"),
    ("ambiente", "Descripción General/Ambiente"),
    ("proyectos_relacionados", "Descripción General/Proyectos Relacionados"),
    ("diseno", "Diseño"),
    ("arquitectura_fisica", "Diseño/Arquitectura Física"),
    ("arquitectura_logica", "Diseño/Arquitectura Lógica"),
    ("modelo", "Diseño/Modelo de Datos"),
    ("detalle_modulos", "Diseño Detallado/Detalle Módulos"),
    ("navegacion", "Diseño Detallado/Navegación"),
    ("interfaz", "Diseño Detallado/Interfaz"),
]

TASK_CHOICES = [
    ("realizada", "realizada"),
    ("no_realizada", "no realizada"),
    ("aprobada", "aprobada"),
    ("reprobada", "reprobada"),
    ("cancelada", "cancelada"),
]
