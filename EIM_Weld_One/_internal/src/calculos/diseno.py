"""
En este módulo se le darán forma a las funciones necesarias para ejecutar los cálculos de diseño
"""

from math import pi
from sympy import symbols, solve, sqrt, lambdify
from src.calculos import analisis
from scipy.optimize import newton
import numpy as np


# Obtener carga alternante y media en función de F = Fmin
def obtener_carga_alt_y_med(relacion_cargas):
    f = symbols("F")
    f_alt = f * (relacion_cargas - 1) / 2
    f_med = f * (relacion_cargas + 1) / 2
    return f_alt, f_med


# Despejar la carga F = Fmin de la ecuación de Gerber
def despejar_carga_ecuacion_gerber(esfuerzo_alternante, esfuerzo_medio, resistencia_fatiga, resistencia_ultima, fd):
    # Definir la variable a calcular
    f = symbols("F")

    # Definir la ecuación
    ecuacion_gerber = ((fd * esfuerzo_medio / resistencia_ultima) ** 2 + (fd * esfuerzo_alternante / resistencia_fatiga)
                       - 1)

    # Resolver la ecuación
    soluciones_carga = solve(ecuacion_gerber, f)

    # Seleccionar la solución positiva de la ecuación
    for solucion in soluciones_carga:
        if solucion.is_real and solucion > 0:
            return solucion


# Despejar la carga Fmax de la ecuación del FD por carga estática
def despejar_carga_max_fd_estatica(fd, resistencia, esfuerzo_soportado):
    f_max = symbols("F")

    # Definir la ecuación (Despejada igual a cero)
    ecuacion_fd_estatica = fd - resistencia / esfuerzo_soportado

    # Despejar Fmax
    soluciones_carga = solve(ecuacion_fd_estatica, f_max)

    # Seleccionar la solución positiva de la ecuación
    for solucion in soluciones_carga:
        if solucion.is_real and solucion > 0:
            return solucion


# Despejar el momento torsor Tmax de la ecuación del FD por carga estática
def despejar_torque_max_fd_estatica(fd, resistencia, esfuerzo_soportado):
    t_max = symbols("T")

    # Definir la ecuación (Despejada igual a cero)
    ecuacion_fd_estatica = fd - resistencia / esfuerzo_soportado

    # Despejar Tmax
    soluciones_carga = solve(ecuacion_fd_estatica, t_max)

    # Seleccionar la solución positiva de la ecuación
    for solucion in soluciones_carga:
        if solucion.is_real and solucion > 0:
            return solucion


# Obtener momento torsor alternante y media en función de T = Tmin
def obtener_torque_alt_y_med(relacion_cargas):
    t = symbols("T")
    t_alt = t * (relacion_cargas - 1) / 2
    t_med = t * (relacion_cargas + 1) / 2
    return t_alt, t_med


# Despejar el momento torsor (torque) T = Tmin de la ecuación de Gerber
def despejar_torque_ecuacion_gerber(esfuerzo_alternante, esfuerzo_medio, resistencia_fatiga, resistencia_ultima, fd):
    # Definir la variable a calcular
    t = symbols("T")

    # Definir la ecuación
    ecuacion_gerber = ((fd * esfuerzo_medio / resistencia_ultima) ** 2 + (fd * esfuerzo_alternante / resistencia_fatiga)
                       - 1)

    # Resolver la ecuación
    soluciones_carga = solve(ecuacion_gerber, t)

    # Seleccionar la solución positiva de la ecuación
    for solucion in soluciones_carga:
        if solucion.is_real and solucion > 0:
            return solucion


# Despejar la pierna (h) del cordón de soldadura de la ecuación de Gerber
def despejar_pierna_ecuacion_gerber(esfuerzo_alternante, esfuerzo_medio, resistencia_fatiga, resistencia_ultima, fd):
    # Definir la variable a calcular
    h = symbols("h")

    # Definir la ecuación
    ecuacion_gerber = ((fd * esfuerzo_medio / resistencia_ultima) ** 2 + (fd * esfuerzo_alternante / resistencia_fatiga)
                       - 1)

    # Resolver la ecuación
    soluciones_carga = solve(ecuacion_gerber, h)

    # Seleccionar la solución positiva de la ecuación
    for solucion in soluciones_carga:
        if solucion.is_real and solucion > 0:
            return solucion


# Despejar la pierna hmin de la ecuación del FD por carga estática
def despejar_h_min_fd_estatica(fd, resistencia, esfuerzo_soportado):
    # Definir la variable a calcular
    h = symbols("h")

    # Definir la ecuación (Despejada igual a cero)
    ecuacion_fd_estatica = fd - resistencia / esfuerzo_soportado

    # Despejar Fmax
    soluciones_carga = solve(ecuacion_fd_estatica, h)

    # Seleccionar la solución positiva de la ecuación
    for solucion in soluciones_carga:
        if solucion.is_real and solucion > 0:
            return solucion


# Mensaje con la carga máxima permisible en la junta
def conclusion_fuerza_permisible(sistema_unidades, f_max_calculada):
    if sistema_unidades == "Internacional":
        conclusion = f"La fuerza máxima permisible en la junta es Fperm = {"{:.2f}".format(f_max_calculada)} N"
    else:
        conclusion = f"La fuerza máxima permisible en la junta es Fperm = {"{:.2f}".format(f_max_calculada)} lbs"

    return conclusion


# Mensaje con el momento torsor máximo permisible en la junta
def conclusion_torque_permisible(sistema_unidades, t_max_calculado):
    if sistema_unidades == "Internacional":
        conclusion = f"El momento torsor máximo permisible en la junta es Tperm = {"{:.2f}".format(t_max_calculado / 1000)} N.m"
    else:
        conclusion = f"El momento torsor máximo permisible en la junta es Tperm = {"{:.2f}".format(t_max_calculado)} lb.pulg"

    return conclusion


# Mensaje de conclusión de diseño por fatiga
def generar_conclusion_diseno_fatiga(falla_comprobacion_estatica):
    if falla_comprobacion_estatica:
        conclusion = "Al presentarse la falla por carga estática, se debe proceder a diseñar por estática"
    else:
        conclusion = "Diseño completado con éxito"

    return conclusion


# Mensaje con la pierna mínima (hmin necesaria en la junta)
def conclusion_pierna_min(sistema_unidades, h_min_calculada):
    if sistema_unidades == "Internacional":
        conclusion = f"La pierna mínima necesaria en la junta es hmin = {h_min_calculada} mm"
    else:
        conclusion = f"La pierna mínima necesaria en la junta es hmin = {h_min_calculada} pulg"

    return conclusion


#######################################################################################################################
# SOLDADURA DE FILETE

# Clase para el cálculo de la carga permisible en la junta
class DisenoCargaPermisibleFilete:
    # Factores de diseño mínimo
    fd_min_sold = 3.33
    fd_min_pieza = 2.5

    def __init__(self, sistema_unidades, tipo_union, relacion_cargas, brazo, material_base_1, material_base_2,
                 electrodo, geometria, geometria_params, espesor_menor_piezas):
        self.sistema_unidades = sistema_unidades
        self.tipo_union = tipo_union
        self.relacion_cargas = relacion_cargas
        self.brazo = brazo
        self.material_base_1 = material_base_1
        self.material_base_2 = material_base_2
        self.electrodo = electrodo
        self.geometria = geometria
        self.geometria_params = geometria_params
        self.espesor_menor_piezas = espesor_menor_piezas

    ###################################################################################################################
    # GEOMETRIA

    # Calcular la gargante del cordón de soldadura
    def calcular_garganta(self):
        pierna = self.geometria_params["pierna"]
        garganta = 0.707 * pierna
        return garganta

    # Calcular longitud total del cordón de soldadura
    def calcular_longitud_total(self):
        l = self.geometria_params.get("largo", 0)
        a = self.geometria_params.get("ancho", 0)
        r = self.geometria_params.get("radio", 0)

        geometrias_longitudes = {
            "uno": l,
            "dos": l,
            "tres": (l + a),
            "cuatro": (l + a),
            "cinco": (2 * l),
            "seis": (2 * l),
            "siete": (2 * l + a),
            "ocho": (2 * pi * r),
            "nueve": 2 * l + a,
            "diez": 2 * l + a,
            "once": 2 * l + 2 * a,
            "doce": 2 * l + 2 * a
        }

        lt_ecuaciones = {
            "uno": 'l',
            "dos": 'l',
            "tres": 'l + a',
            "cuatro": 'l + a',
            "cinco": '2 * l',
            "seis": '2 * l',
            "siete": '2 * l + a',
            "ocho": '2 * pi * r',
            "nueve": '2 * l + a',
            "diez": '2 * l + a',
            "once": '2 * l + 2 * a',
            "doce": '2 * l + 2 * a'
        }

        longitud_total = geometrias_longitudes[self.geometria]
        ecuacion = lt_ecuaciones[self.geometria]
        return longitud_total, ecuacion

    # Realizar cálculo del área de la pierna del cordón de soldadura
    def calcular_area_sold(self):
        pierna = self.geometria_params["pierna"]
        longitud_total = self.calcular_longitud_total()[0]
        area_sold = pierna * longitud_total
        return area_sold

    # Calcular momento de inercia en la soldadura (I)
    def calcular_momento_inercia_sold(self):
        h = self.geometria_params.get("pierna", 0)
        l = self.geometria_params.get("largo", 0)
        a = self.geometria_params.get("ancho", 0)
        r = self.geometria_params.get("radio", 0)

        if l == 0 and a == 0:
            momento_de_inercia = 0.707 * h * pi * r ** 3
            ecuacion = "0.707 * h * pi * r^3"
        else:
            momentos_inercia_geometrias = {
                "uno": (0.059 * h * l ** 3),
                "dos": (0.059 * h ** 3 * l),
                "tres": (0.059 * (h * l ** 2 * (l ** 2 + 4 * a * l)) / (l + a)),
                "cuatro": (0.059 * (h * a ** 2 * (a ** 2 + 4 * l * a)) / (a + l)),
                "cinco": (0.118 * h * l ** 3),
                "seis": (0.354 * h * l * a ** 2),
                "siete": (0.059 * h * l ** 2 * (6 * l + a)),
                "ocho": (0.707 * h * pi * r ** 3),
                "nueve": (0.707 * h * ((9 * l ** 4 + 2 * l ** 3 * (a + 2 * l)) / (3 * (a + 2 * l)))),
                "diez": (0.707 * h * ((9 * l ** 4 + 2 * l ** 3 * (a + 2 * l)) / (3 * (a + 2 * l)))),
                "once": (0.118 * h * l ** 2 * (3 * a + l)),
                "doce": (0.118 * h * l ** 2 * (3 * a + l))
            }

            momento_inercia_ecuaciones = {
                "uno": "0.059 * h * l^3",
                "dos": "0.059 * h^3 * l",
                "tres": "0.059 * (h * l^2 * (l^2 + 4 * a * l)) / (l + a)",
                "cuatro": "0.059 * (h * a^2 * (a^2 + 4 * l * a)) / (a + l)",
                "cinco": "0.118 * h * l^3",
                "seis": "0.354 * h * l * a^2",
                "siete": "0.059 * h * l^2 * (6 * l + a)",
                "ocho": "0.707 * h * pi * r^3",
                "nueve": "0.707 * h * ((9 * l^4 + 2 * l^3 * (a + 2 * l)) / (3 * (a + 2 * l)))",
                "diez": "0.707 * h * ((9 * l^4 + 2 * l^3 * (a + 2 * l)) / (3 * (a + 2 * l)))",
                "once": "0.118 * h * l^2 * (3 * a + l)",
                "doce": "0.118 * h * l^2 * (3 * a + l)"
            }

            momento_de_inercia = momentos_inercia_geometrias[self.geometria]
            ecuacion = momento_inercia_ecuaciones[self.geometria]

        return momento_de_inercia, ecuacion

        # Calcular momento de inercia en la pieza (I)

    def calcular_momento_inercia_pieza(self):
        h = self.geometria_params.get("pierna", 0)
        l = self.geometria_params.get("largo", 0)
        a = self.geometria_params.get("ancho", 0)
        r = self.geometria_params.get("radio", 0)

        if l == 0 and a == 0:
            momento_de_inercia = h * pi * r ** 3
            ecuacion = "h * pi * r^3"
        else:
            momentos_inercia_geometrias = {
                "uno": (0.0834 * h * l ** 3),
                "dos": (0.0834 * h ** 3 * l),
                "tres": (0.084 * (h * l ** 2 * (l ** 2 + 4 * a * l)) / (l + a)),
                "cuatro": (0.084 * (h * a ** 2 * (a ** 2 + 4 * l * a)) / (a + l)),
                "cinco": (0.167 * h * l ** 3),
                "seis": (0.5 * h * l * a ** 2),
                "siete": (0.0834 * h * l ** 2 * (6 * l + a)),
                "ocho": (h * pi * r ** 3),
                "nueve": (h * ((9 * l ** 4 + 2 * l ** 3 * (a + 2 * l)) / (3 * (a + 2 * l)))),
                "diez": (h * ((9 * l ** 4 + 2 * l ** 3 * (a + 2 * l)) / (3 * (a + 2 * l)))),
                "once": (0.167 * h * l ** 2 * (3 * a + l)),
                "doce": (0.167 * h * l ** 2 * (3 * a + l))
            }

            momento_inercia_ecuaciones = {
                "uno": "0.0834 * h * l^3",
                "dos": "0.0834 * h^3 * l",
                "tres": "0.084 * (h * l^2 * (l^2 + 4 * a * l)) / (l + a)",
                "cuatro": "0.084 * (h * a^2 * (a ** 2 + 4 * l * a)) / (a + l)",
                "cinco": "0.167 * h * l^3",
                "seis": "0.5 * h * l * a^2",
                "siete": "0.0834 * h * l^2 * (6 * l + a)",
                "ocho": "h * pi * r^3",
                "nueve": "h * ((9 * l^4 + 2 * l^3 * (a + 2 * l)) / (3 * (a + 2 * l)))",
                "diez": "h * ((9 * l^4 + 2 * l^3 * (a + 2 * l)) / (3 * (a + 2 * l)))",
                "once": "0.167 * h * l^2 * (3 * a + l)",
                "doce": "0.167 * h * l^2 * (3 * a + l)"
            }

            momento_de_inercia = momentos_inercia_geometrias[self.geometria]
            ecuacion = momento_inercia_ecuaciones[self.geometria]

        return momento_de_inercia, ecuacion

    # Calcular momento de intercia polar en la soldadura (J)
    def calcular_momento_inercia_polar_sold(self):
        h = self.geometria_params.get("pierna", 0)
        l = self.geometria_params.get("largo", 0)
        a = self.geometria_params.get("ancho", 0)
        r = self.geometria_params.get("radio", 0)

        if l == 0 and a == 0:
            momento_de_inercia_polar = 1.414 * h * pi * r ** 3
            ecuacion = "1.414 * h * pi * r^3"
        else:
            momentos_inercia_polar_geometrias = {
                "uno": (0.059 * h * l ** 3),
                "dos": (0.059 * h * l ** 3),
                "tres": (0.059 * (h * ((a + l) ** 4 - 6 * a ** 2 * l ** 2)) / (a + l)),
                "cuatro": (0.059 * (h * ((a + l) ** 4 - 6 * a ** 2 * l ** 2)) / (a + l)),
                "cinco": (0.059 * h * l * (3 * a ** 2 + l ** 2)),
                "seis": (0.059 * h * l * (3 * a ** 2 + l ** 2)),
                "siete": (0.707 * h * (((a ** 3 + 6 * l * a ** 2 + 8 * l ** 3) / 12) - ((l ** 4) / (2 * l + a)))),
                "ocho": (1.414 * h * pi * r ** 3),
                "nueve": (0.707 * h * (((a ** 3 + 6 * l * a ** 2 + 8 * l ** 3) / 12) - ((l ** 4) / (2 * l + a)))),
                "diez": (0.707 * h * (((l ** 3 + 6 * a * l ** 2 + 8 * a ** 3) / 12) - ((a ** 4) / (2 * a + l)))),
                "once": (0.118 * h * (a + l) ** 3),
                "doce": (0.059 * h * (a ** 3 + 3 * a * l ** 2 + l ** 3))
            }

            momento_inercia_polar_ecuaciones = {
                "uno": "0.059 * h * l^3",
                "dos": "0.059 * h * l^3",
                "tres": "0.059 * (h * ((a + l)^4 - 6 * a ** 2 * l^2)) / (a + l)",
                "cuatro": "0.059 * (h * ((a + l)^4 - 6 * a^2 * l^2)) / (a + l)",
                "cinco": "0.059 * h * l * (3 * a^2 + l^2)",
                "seis": "0.059 * h * l * (3 * a^2 + l^2)",
                "siete": "0.707 * h * (((a^3 + 6 * l * a^2 + 8 * l^3) / 12) - ((l^4) / (2 * l + a)))",
                "ocho": "1.414 * h * pi * r^3",
                "nueve": "0.707 * h * (((a^3 + 6 * l * a^2 + 8 * l^3) / 12) - ((l^4) / (2 * l + a)))",
                "diez": "0.707 * h * (((l^3 + 6 * a * l^2 + 8 * a^3) / 12) - ((a^4) / (2 * a + l)))",
                "once": "0.118 * h * (a + l)^3",
                "doce": "0.059 * h * (a^3 + 3 * a * l^2 + l^3)"
            }

            momento_de_inercia_polar = momentos_inercia_polar_geometrias[self.geometria]
            ecuacion = momento_inercia_polar_ecuaciones[self.geometria]

        return momento_de_inercia_polar, ecuacion

    # Obtener las coordenadas del centroide (X barra, Y barra)
    def obtener_coordenadas_centroide(self):
        l = self.geometria_params.get("largo", 0)
        a = self.geometria_params.get("ancho", 0)

        if l == 0 and a == 0:
            x_barra, y_barra = 0, 0
        else:
            coordenadas_centroide_geometrias = {
                "uno": (0, l / 2),
                "dos": (l / 2, 0),
                "tres": ((a ** 2) / (2 * (a + l)), (l ** 2) / (2 * (l + a))),
                "cuatro": ((l ** 2) / (2 * (l + a)), (a ** 2) / (2 * (a + l))),
                "cinco": (a / 2, l / 2),
                "seis": (l / 2, a / 2),
                "siete": ((l ** 2) / (2 * l + a), a / 2),
                "ocho": (0, 0),
                "nueve": (a / 2, (l ** 2) / (2 * l + a)),
                "diez": (a / 2, (l ** 2) / (2 * l + a)),
                "once": (a / 2, l / 2),
                "doce": (a / 2, l / 2)
            }
            x_barra, y_barra = coordenadas_centroide_geometrias.get(self.geometria)

        return x_barra, y_barra

    # Obtener rx y ry para calcular el esfuerzo debido al par torsionante
    def obtener_rx_ry(self):
        l = self.geometria_params.get("largo", 0)
        a = self.geometria_params.get("ancho", 0)
        r = self.geometria_params.get("radio", 0)

        if l == 0 and a == 0:
            rx, ry = 0, r
            rx_ry_formulas = "0", "r"
        else:
            rx_ry_geometrias = {
                "uno": (0, l / 2),
                "dos": (l / 2, 0),
                "tres": ((a ** 2) / (2 * (a + l)), l - (l ** 2) / (2 * (l + a))),
                "cuatro": (l - (l ** 2) / (2 * (l + a)), (a ** 2) / (2 * (a + l))),
                "cinco": (a / 2, l / 2),
                "seis": (l / 2, a / 2),
                "siete": (l - (l ** 2) / (2 * l + a), a / 2),
                "ocho": (0, r),
                "nueve": (a / 2, l - (l ** 2) / (2 * l + a)),
                "diez": (0, l - (l ** 2) / (2 * l + a)),
                "once": (a / 2, l / 2),
                "doce": (a / 2, l / 2)
            }

            rx_ry_ecuaciones = {
                "uno": ("0", "l/2"),
                "dos": ("l/2", "0"),
                "tres": ("(a^2) / (2 * (a + l))", "l - (l^2) / (2 * (l + a))"),
                "cuatro": ("l - (l^2) / (2 * (l + a))", "(a^2) / (2 * (a + l))"),
                "cinco": ("a/2", "l/2"),
                "seis": ("l/2", "a/2"),
                "siete": ("l - (l^2) / (2 * l + a)", "a / 2"),
                "ocho": ("0", "r"),
                "nueve": ("a/2", "l - (l^2) / (2 * l + a)"),
                "diez": ("0", "l - (l^2) / (2 * l + a)"),
                "once": ("a/2", "l/2"),
                "doce": ("a/2", "l/2")
            }

            rx, ry = rx_ry_geometrias.get(self.geometria)
            rx_ry_formulas = rx_ry_ecuaciones[self.geometria]

        return rx, ry, rx_ry_formulas

    # Verificar el tamaño mínimo de la pierna del cordón de soldadura al terminar el diseño
    def verificar_tamano_minimo_pierna(self):
        sistema_unidades = self.sistema_unidades
        t_menor = self.espesor_menor_piezas
        h = self.geometria_params["pierna"]
        conclusion = ""

        if sistema_unidades == "Internacional":
            if t_menor <= 6:
                if 3 <= h <= t_menor:
                    conclusion = f"""Para un espesor e = {t_menor} mm, hmin = 3 mm.
        Como h = {h} mm, entonces cumple con la especificación de la norma AWS."""
                elif h < 3:
                    conclusion = f"""Para un espesor e = {t_menor} mm, hmin = 3 mm.
        Como h = {h} mm, entonces no cumple con la especificación de la norma AWS."""
                elif h > t_menor:
                    conclusion = f"""El valor de h no debe exceder el espesor de la pieza más delgada, e = {t_menor} mm.
        Como h = {h} mm, entonces no cumple con la especificación de la norma AWS."""
            elif 6 < t_menor <= 12:
                if 5 <= h <= t_menor:
                    conclusion = f"""Para un espesor e = {t_menor} mm, hmin = 5 mm.
        Como h = {h} mm, entonces cumple con la especificación de la norma AWS."""
                elif h < 5:
                    conclusion = f"""Para un espesor e = {t_menor} mm, hmin = 5 mm.
        Como h = {h} mm, entonces no cumple con la especificación de la norma AWS."""
                elif h > t_menor:
                    conclusion = f"""El valor de h no debe exceder el espesor de la pieza más delgada, e = {t_menor} mm.
        Como h = {h} mm, entonces no cumple con la especificación de la norma AWS."""
            elif 12 < t_menor <= 20:
                if 6 <= h <= t_menor:
                    conclusion = f"""Para un espesor e = {t_menor} mm, hmin = 6 mm.
        Como h = {h} mm, entonces cumple con la especificación de la norma AWS."""
                elif h < 6:
                    conclusion = f"""Para un espesor e = {t_menor} mm, hmin = 6 mm.
        Como h = {h} mm, entonces no cumple con la especificación de la norma AWS."""
                elif h > t_menor:
                    conclusion = f"""El valor de h no debe exceder el espesor de la pieza más delgada, e = {t_menor} mm.
        Como h = {h} mm, entonces no cumple con la especificación de la norma AWS."""
            elif t_menor > 20:
                if 8 <= h <= t_menor:
                    conclusion = f"""Para un espesor e = {t_menor} mm, hmin = 8 mm.
        Como h = {h} mm, entonces cumple con la especificación de la norma AWS."""
                elif h < 8:
                    conclusion = f"""Para un espesor e = {t_menor} mm, hmin = 8 mm.
        Como h = {h} mm, entonces no cumple con la especificación de la norma AWS."""
                elif h > t_menor:
                    conclusion = f"""El valor de h no debe exceder el espesor de la pieza más delgada, e = {t_menor} mm.
        Como h = {h} mm, entonces no cumple con la especificación de la norma AWS."""

        if sistema_unidades == "Inglés":
            if t_menor <= 1 / 4:
                if 1 / 8 <= h <= t_menor:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 1/8 pulg.
        Como h = {h} pulg, entonces cumple con la especificación de la norma AWS."""
                elif h < 1 / 8:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 1/8 pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
                elif h > t_menor:
                    conclusion = f"""El valor de h no debe exceder el espesor de la pieza más delgada, e = {t_menor} pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
            elif 1 / 4 < t_menor <= 1 / 2:
                if 3 / 16 <= h <= t_menor:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 3/16 pulg.
        Como h = {h} pulg, entonces cumple con la especificación de la norma AWS."""
                elif h < 3 / 16:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 3/16 pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
                elif h > t_menor:
                    conclusion = f"""El valor de h no debe exceder el espesor de la pieza más delgada, e = {t_menor} pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
            elif 1 / 2 < t_menor <= 3 / 4:
                if 1 / 4 <= h <= t_menor:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 1/4 pulg.
        Como h = {h} pulg, entonces cumple con la especificación de la norma AWS."""
                elif h < 1 / 4:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 1/4 pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
                elif h > t_menor:
                    conclusion = f"""El valor de h no debe exceder el espesor de la pieza más delgada, e = {t_menor} pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
            elif t_menor > 3 / 4:
                if 5 / 16 <= h <= t_menor:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 5/16 pulg.
        Como h = {h} pulg, entonces cumple con la especificación de la norma AWS."""
                elif h < 5 / 16:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 5/16 pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
                elif h > t_menor:
                    conclusion = f"""El valor de h no debe exceder el espesor de la pieza más delgada, e = {t_menor} pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""

        return conclusion

    ###################################################################################################################

    # DISEÑO POR FATIGA

    # Carga Paralela
    def carga_permisible_cp(self):

        # DISEÑO POR FATIGA

        # Obtener la relacion Fmax / Fmin
        relacion = self.relacion_cargas

        # Obtener la fuerza alternante y media en funcion de la relacion
        f_alt, f_med = obtener_carga_alt_y_med(relacion)

        # Factor de concentración de esfuerzo reducido, Kfs (Se considera carga paralela con unión intermedia)
        kfs = 2.7

        # Area de la soldadura
        area_sold = self.calcular_area_sold()

        # Determinar F en la soldadura

        # Obtener esfuerzo cortante alternante y medio en la soldadura (en función de F)
        tao_alt_sold = kfs * 1.414 * f_alt / area_sold
        tao_med_sold = 1.414 * f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar la carga F = Fmin de la ecuación de Gerber para FDmin_sold = 3.33
        f_sold = despejar_carga_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar F en la pieza 1

        # Obtener esfuerzo cortante alternante y medio en la pieza 1 (en función de F)
        tao_alt_pieza1 = kfs * f_alt / area_sold
        tao_med_pieza1 = f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia ultima al cortante del material base 1
        ssu_pieza1 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza1 = despejar_carga_ecuacion_gerber(tao_alt_pieza1, tao_med_pieza1, sse_pieza1, ssu_pieza1,
                                                  self.fd_min_pieza)

        # Determinar F en la pieza 2

        # Obtener esfuerzo cortante alternante y medio en la pieza 2 (en función de F)
        tao_alt_pieza2 = kfs * f_alt / area_sold
        tao_med_pieza2 = f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        sse_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular la resistencia ultima al cortante del material base 2
        ssu_pieza2 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza2)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza2 = despejar_carga_ecuacion_gerber(tao_alt_pieza2, tao_med_pieza2, sse_pieza2, ssu_pieza2,
                                                  self.fd_min_pieza)

        # Seleccionar el menor de los valores de carga F obtenidos
        f = min(f_sold, f_pieza1, f_pieza2)

        # Obtener el valor de Fmax a partir de F y la relacion Fmax/Fmin
        f_max = relacion * f

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraFilete(self.sistema_unidades, self.tipo_union,
                                                                 {"Fmax": f_max},
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria, self.geometria_params,
                                                                 self.espesor_menor_piezas)

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_cp()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna()

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.carga_permisible_estatica_cp()

        # Generar diccionario para informe de resultados
        resultados = {
            "relacion_cargas": relacion,
            "f_alt": f_alt,
            "f_med": f_med,
            "pierna": self.geometria_params["pierna"],
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "garganta": round(self.calcular_garganta(), 3),
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": round(area_sold, 3),
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_alt_sold": tao_alt_sold,
            "tao_med_sold": tao_med_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "f_sold": round(f_sold, 2),
            "tao_alt_pieza1": tao_alt_pieza1,
            "tao_med_pieza1": tao_med_pieza1,
            "tao_alt_pieza2": tao_alt_pieza2,
            "tao_med_pieza2": tao_med_pieza2,
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "sse_pieza2": round(sse_pieza2, 2),
            "ssu_pieza2": round(ssu_pieza2, 2),
            "f_pieza1": round(f_pieza1, 2),
            "f_pieza2": round(f_pieza2, 2),
            "f_min": round(f, 2),
            "f_max": round(f_max, 2),
            "conclusion_fperm": conclusion_fperm,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga,
            "verificacion_pierna": verificacion_pierna
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga Transversal
    def carga_permisible_ctrans(self):

        # DISEÑO POR FATIGA

        # Obtener la relacion Fmax / Fmin
        relacion = self.relacion_cargas

        # Obtener la fuerza alternante y media en funcion de la relacion
        f_alt, f_med = obtener_carga_alt_y_med(relacion)

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Intermedia": 1.5, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Area de la soldadura
        area_sold = self.calcular_area_sold()

        # Determinar F en la soldadura

        # Obtener esfuerzo cortante alternante y medio en la soldadura (en función de F)
        tao_alt_sold = kfs * 1.414 * f_alt / area_sold
        tao_med_sold = 1.414 * f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar la carga F = Fmin de la ecuación de Gerber para FDmin_sold = 3.33
        f_sold = despejar_carga_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar F en la pieza 1 (Pieza P)

        # Obtener esfuerzo cortante alternante y medio en la pieza 1 (en función de F)
        tao_p_alt = kfs * f_alt / area_sold
        tao_p_med = f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia ultima al cortante del material base 1
        ssu_pieza1 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza1 = despejar_carga_ecuacion_gerber(tao_p_alt, tao_p_med, sse_pieza1, ssu_pieza1,
                                                  self.fd_min_pieza)

        # Determinar F en la pieza 2 (Pieza T)

        # Obtener esfuerzo cortante alternante y medio en la pieza 2 (en función de F)
        sigma_t_alt = kfs * f_alt / area_sold
        sigma_t_med = f_med / area_sold

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza2 = despejar_carga_ecuacion_gerber(sigma_t_alt, sigma_t_med, se_pieza2, sut_pieza2,
                                                  self.fd_min_pieza)

        # Seleccionar el menor de los valores de carga F obtenidos
        f = min(f_sold, f_pieza1, f_pieza2)

        # Obtener el valor de Fmax a partir de F y la relacion Fmax/Fmin
        f_max = relacion * f

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraFilete(self.sistema_unidades, self.tipo_union,
                                                                 {"Fmax": f_max},
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria, self.geometria_params,
                                                                 self.espesor_menor_piezas)

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_ctrans()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna()

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.carga_permisible_estatica_ctrans()

        # Generar diccionario para informe de resultados
        resultados = {
            "relacion_cargas": relacion,
            "f_alt": f_alt,
            "f_med": f_med,
            "pierna": self.geometria_params["pierna"],
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "garganta": round(self.calcular_garganta(), 3),
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": round(area_sold, 3),
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_alt_sold": tao_alt_sold,
            "tao_med_sold": tao_med_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "f_sold": round(f_sold, 2),
            "tao_p_alt": tao_p_alt,
            "tao_p_med": tao_p_med,
            "sigma_t_alt": sigma_t_alt,
            "sigma_t_med": sigma_t_med,
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "f_pieza1": round(f_pieza1, 2),
            "f_pieza2": round(f_pieza2, 2),
            "f_min": round(f, 2),
            "f_max": round(f_max, 2),
            "conclusion_fperm": conclusion_fperm,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga,
            "verificacion_pierna": verificacion_pierna
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga de Flexión debido a una fuerza excéntrica
    def carga_permisible_cflex(self):

        # DISEÑO POR FATIGA

        # Obtener la relacion Fmax / Fmin
        relacion = self.relacion_cargas

        # Obtener el brazo (Distancia desde el pto de aplicación de la fuerza hasta el centroide)
        b = self.brazo

        # Obtener las cargas alternantes y medias en funcion de F
        f_alt, f_med = obtener_carga_alt_y_med(relacion)
        momento_flector_alt = f_alt * b
        momento_flector_med = f_med * b

        # Factor de concentración de esfuerzo reducido, Kfs (Se considera carga transversal y unión T)
        kfs = 2

        # Calculo de parámetros geométricos
        area_sold = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia_sold()
        i_pieza, i_pieza_ecuacion = self.calcular_momento_inercia_pieza()
        c = self.obtener_rx_ry()[1]
        c_ecuacion = self.obtener_rx_ry()[2][1]

        # Determinar F en la soldadura

        # Calcular esfuerzo cortante primario alternante y medio en la soldadura (En función de F)
        tao_primario_alt = kfs * 1.414 * f_alt / area_sold
        tao_primario_med = 1.414 * f_med / area_sold

        # Calcular esfuerzo cortante secundadario alternante y medio en la soldadura (En función de F)
        tao_secundario_alt = kfs * momento_flector_alt * c / i_sold
        tao_secundario_med = momento_flector_med * c / i_sold

        # Calcular el esfuerzo cortante resultante alternante y medio en la soldadura (En función de F)
        tao_alt_sold = sqrt(tao_primario_alt ** 2 + tao_secundario_alt ** 2)
        tao_med_sold = sqrt(tao_primario_med ** 2 + tao_secundario_med ** 2)

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar la carga F = Fmin de la ecuación de Gerber para FDmin_sold = 3.33
        f_sold = despejar_carga_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar F en la pieza 1 (Pieza P)

        # Calcular esfuerzo normal alternante y medio en la pieza 1 (En función de F)
        sigma_p_alt = kfs * momento_flector_alt * c / i_pieza
        sigma_p_med = momento_flector_med * c / i_pieza

        # Calcular esfuerzo cortante alternante y medio en la pieza 1 (En función de F)
        tao_p_alt = kfs * f_alt / area_sold
        tao_p_med = f_med / area_sold

        # Calcular el esfuerzo de Von Misses alternante y medio en la pieza 1 (En función de F)
        sigma_p_von_misses_alt = sqrt(sigma_p_alt ** 2 + 3 * tao_p_alt ** 2)
        sigma_p_von_misses_med = sqrt(sigma_p_med ** 2 + 3 * tao_p_med ** 2)

        # Calcular la resistencia a la fatiga del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza1 = despejar_carga_ecuacion_gerber(sigma_p_von_misses_alt, sigma_p_von_misses_med, se_pieza1, sut_pieza1,
                                                  self.fd_min_pieza)

        # Determinar F en la pieza 2 (Pieza T)

        # Calcular esfuerzo normal alternante y medio en la pieza 2 (En función de F)
        sigma_t_alt = tao_p_alt
        sigma_t_med = tao_p_med

        # Calcular esfuerzo cortante alternante y medio en la pieza 2 (En función de F)
        tao_t_alt = sigma_p_alt
        tao_t_med = sigma_p_med

        # Calcular el esfuerzo de Von Misses alternante y medio en la pieza 2 (En función de F)
        sigma_t_von_misses_alt = sqrt(sigma_t_alt ** 2 + 3 * tao_t_alt ** 2)
        sigma_t_von_misses_med = sqrt(sigma_t_med ** 2 + 3 * tao_t_med ** 2)

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza2 = despejar_carga_ecuacion_gerber(sigma_t_von_misses_alt, sigma_t_von_misses_med, se_pieza2, sut_pieza2,
                                                  self.fd_min_pieza)

        # Seleccionar el menor de los valores de carga F obtenidos
        f = min(f_sold, f_pieza1, f_pieza2)

        # Obtener el valor de Fmax a partir de F y la relacion Fmax/Fmin
        f_max = relacion * f

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraFilete(self.sistema_unidades, self.tipo_union,
                                                                 {"Fmax": f_max, "b": b},
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria, self.geometria_params,
                                                                 self.espesor_menor_piezas)

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_cflex()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna()

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.carga_permisible_estatica_cflex()

        # Generar diccionario para informe de resultados
        resultados = {
            "relacion_cargas": relacion,
            "b": b,
            "f_alt": f_alt,
            "f_med": f_med,
            "momento_flector_alt": momento_flector_alt,
            "momento_flector_med": momento_flector_med,
            "pierna": self.geometria_params["pierna"],
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "garganta": round(self.calcular_garganta(), 3),
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": round(area_sold, 3),
            "i_sold": round(i_sold, 2),
            "i_sold_ecuacion": i_sold_ecuacion,
            "i_pieza": round(i_pieza, 2),
            "i_pieza_ecuacion": i_pieza_ecuacion,
            "c": round(c, 3),
            "c_ecuacion": c_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_primario_alt": tao_primario_alt,
            "tao_primario_med": tao_primario_med,
            "tao_secundario_alt": tao_primario_alt,
            "tao_secundario_med": tao_secundario_med,
            "tao_alt_sold": tao_alt_sold,
            "tao_med_sold": tao_med_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "f_sold": round(f_sold, 2),
            "sigma_p_alt": sigma_p_alt,
            "sigma_p_med": sigma_p_med,
            "tao_p_alt": tao_p_alt,
            "tao_p_med": tao_p_med,
            "sigma_t_alt": sigma_t_alt,
            "sigma_t_med": sigma_t_med,
            "tao_t_alt": tao_t_alt,
            "tao_t_med": tao_t_med,
            "sigma_p_von_misses_alt": sigma_p_von_misses_alt,
            "sigma_p_von_misses_med": sigma_p_von_misses_med,
            "sigma_t_von_misses_alt": sigma_t_von_misses_alt,
            "sigma_t_von_misses_med": sigma_t_von_misses_med,
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "f_pieza1": round(f_pieza1, 2),
            "f_pieza2": round(f_pieza2, 2),
            "f_min": round(f, 2),
            "f_max": round(f_max, 2),
            "conclusion_fperm": conclusion_fperm,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga,
            "verificacion_pierna": verificacion_pierna
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga de Torsión debido a una fuerza excéntrica
    def carga_permisible_ctor(self):

        # DISEÑO POR FATIGA

        # Obtener la relacion Fmax / Fmin
        relacion = self.relacion_cargas

        # Obtener el brazo (Distancia desde el pto de aplicación de la fuerza hasta el centroide)
        b = self.brazo

        # Obtener las cargas alternantes y medias en funcion de F
        f_alt, f_med = obtener_carga_alt_y_med(relacion)
        momento_torsor_alt = f_alt * b
        momento_torsor_med = f_med * b

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Intermedia": 1.5, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Calculo de parámetros geométricos
        area_sold = self.calcular_area_sold()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar_sold()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion

        if self.geometria == "ocho":
            ry, rx, ry_rx_ecuacion = self.obtener_rx_ry()
            ry_ecuacion, rx_ecuacion = ry_rx_ecuacion

        # Determinar F en la soldadura

        # Calcular esfuerzo cortante primario alternante y medio en la soldadura (En función de F)
        tao_primario_alt = kfs * 1.414 * f_alt / area_sold
        tao_primario_med = 1.414 * f_med / area_sold

        # Calcular las componentes x e y del esfuerzo cortante secundadario alternante en la soldadura
        tao_secundario_alt_x = kfs * momento_torsor_alt * ry / j_sold
        tao_secundario_alt_y = kfs * momento_torsor_alt * rx / j_sold

        # Calcular las componentes x e y del esfuerzo cortante secundario medio en la soldadura
        tao_secundario_med_x = momento_torsor_med * ry / j_sold
        tao_secundario_med_y = momento_torsor_med * rx / j_sold

        # Calcular las componentes x e y del esfuerzo cortante alternante
        tao_alt_x = tao_secundario_alt_x
        tao_alt_y = tao_primario_alt + tao_secundario_alt_y

        # Calcular las componentes x e y del esfuerzo cortante medio
        tao_med_x = tao_secundario_med_x
        tao_med_y = tao_primario_med + tao_secundario_med_y

        # Calcular el esfuerzo cortante resultante alternante y medio en la soldadura (En función de F)
        tao_alt_sold = sqrt(tao_alt_x ** 2 + tao_alt_y ** 2)
        tao_med_sold = sqrt(tao_med_x ** 2 + tao_med_y ** 2)

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar la carga F = Fmin de la ecuación de Gerber para FDmin_sold = 3.33
        f_sold = despejar_carga_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar F en la pieza 1 (Pieza P)

        # Calcular esfuerzo cortante alternante y medio en la pieza 1 (En función de F)
        tao_p_alt = kfs * f_alt / area_sold
        tao_p_med = f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia última al cortante del material base 1
        ssu_pieza1 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza1 = despejar_carga_ecuacion_gerber(tao_p_alt, tao_p_med, sse_pieza1, ssu_pieza1, self.fd_min_pieza)

        # Determinar F en la pieza 2 (Pieza T)

        # Calcular esfuerzo normal alternante y medio en la pieza 2 (En función de F)
        sigma_t_alt = kfs * f_alt / area_sold
        sigma_t_med = f_med / area_sold

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza2 = despejar_carga_ecuacion_gerber(sigma_t_alt, sigma_t_med, se_pieza2, sut_pieza2,
                                                  self.fd_min_pieza)

        # Seleccionar el menor de los valores de carga F obtenidos
        f = min(f_sold, f_pieza1, f_pieza2)

        # Obtener el valor de Fmax a partir de F y la relacion Fmax/Fmin
        f_max = relacion * f

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraFilete(self.sistema_unidades, self.tipo_union,
                                                                 {"Fmax": f_max, "b": b},
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria, self.geometria_params,
                                                                 self.espesor_menor_piezas)

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_ctor()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna()

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.carga_permisible_estatica_ctor()

        # Generar diccionario para informe de resultados
        resultados = {
            "relacion_cargas": relacion,
            "b": b,
            "f_alt": f_alt,
            "f_med": f_med,
            "momento_torsor_alt": momento_torsor_alt,
            "momento_torsor_med": momento_torsor_med,
            "pierna": self.geometria_params["pierna"],
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "garganta": round(self.calcular_garganta(), 3),
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": round(area_sold, 3),
            "j_sold": round(j_sold, 2),
            "j_sold_ecuacion": j_sold_ecuacion,
            "rx": round(rx, 3),
            "ry": round(ry, 3),
            "rx_ecuacion": rx_ecuacion,
            "ry_ecuacion": ry_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_primario_alt": tao_primario_alt,
            "tao_primario_med": tao_primario_med,
            "tao_secundario_alt_x": tao_secundario_alt_x,
            "tao_secundario_alt_y": tao_secundario_alt_y,
            "tao_secundario_med_x": tao_secundario_med_x,
            "tao_secundario_med_y": tao_secundario_med_y,
            "tao_alt_x": tao_alt_x,
            "tao_alt_y": tao_alt_y,
            "tao_med_x": tao_med_y,
            "tao_med_y": tao_med_y,
            "tao_alt_sold": tao_alt_sold,
            "tao_med_sold": tao_med_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "f_sold": round(f_sold, 2),
            "tao_p_alt": tao_p_alt,
            "tao_p_med": tao_p_med,
            "sigma_t_alt": sigma_t_alt,
            "sigma_t_med": sigma_t_med,
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "f_pieza1": round(f_pieza1, 2),
            "f_pieza2": round(f_pieza2, 2),
            "f_min": round(f, 2),
            "f_max": round(f_max, 2),
            "conclusion_fperm": conclusion_fperm,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga,
            "verificacion_pierna": verificacion_pierna
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga Combinada debido a una carga excétrica
    def carga_permisible_ccomb(self):

        # DISEÑO POR FATIGA

        # Obtener la relacion Fmax / Fmin
        relacion = self.relacion_cargas

        # Obtener bl y bt (Distancia desde el pto de aplicación de la fuerza hasta el centroide, longitudinal y transv)
        bl = self.brazo["bl"]
        bt = self.brazo["bt"]

        # Obtener las cargas alternantes y medias en funcion de F
        f_alt, f_med = obtener_carga_alt_y_med(relacion)
        momento_flector_alt = f_alt * bl
        momento_flector_med = f_med * bl
        momento_torsor_alt = f_alt * bt
        momento_torsor_med = f_med * bt

        # Factor de concentración de esfuerzo reducido, Kfs (Se considera carga transversal y unión T)
        kfs = 2

        # Calculo de parámetros geométricos
        area_sold = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia_sold()
        i_pieza, i_pieza_ecuacion = self.calcular_momento_inercia_pieza()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar_sold()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        c = ry
        c_ecuacion = rx_ry_ecuacion[1]

        # Determinar F en la soldadura

        # Calcular esfuerzo cortante primario alternante y medio en la soldadura (En función de F)
        tao_primario_alt = kfs * 1.414 * f_alt / area_sold
        tao_primario_med = 1.414 * f_med / area_sold

        # Calcular esfuerzo cortante secundadario alternante y medio en la soldadura (En función de F)
        tao_secundario_alt = kfs * momento_flector_alt * c / i_sold
        tao_secundario_med = momento_flector_med * c / i_sold

        # Calcular las componentes x e y del esfuerzo cortante terciario alternante en la soldadura (En función de F)
        tao_terciario_alt_x = kfs * momento_torsor_alt * ry / j_sold
        tao_terciario_alt_y = kfs * momento_torsor_alt * rx / j_sold

        # Calcular las componentes x e y del esfuerzo cortante terciario medio en la soldadura (En función de F)
        tao_terciario_med_x = momento_torsor_med * ry / j_sold
        tao_terciario_med_y = momento_torsor_med * rx / j_sold

        # Calcular las componentes X, Y y Z del esfuerzo cortante alternante
        tao_alt_x = tao_terciario_alt_x
        tao_alt_y = tao_primario_alt + tao_terciario_alt_y
        tao_alt_z = tao_secundario_alt

        # Calcular las componentes X, Y y Z del esfuerzo cortante medio
        tao_med_x = tao_terciario_med_x
        tao_med_y = tao_primario_med + tao_terciario_med_y
        tao_med_z = tao_secundario_med

        # Calcular el esfuerzo cortante resultante alternante y medio en la soldadura (En función de F)
        tao_alt_sold = sqrt(tao_alt_x ** 2 + tao_alt_y ** 2 + tao_alt_z ** 2)
        tao_med_sold = sqrt(tao_med_x ** 2 + tao_med_y ** 2 + tao_med_z ** 2)

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar la carga F = Fmin de la ecuación de Gerber para FDmin_sold = 3.33
        f_sold = despejar_carga_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar F en la pieza 1 (Pieza P)

        # Calcular esfuerzo normal alternante y medio en la pieza 1 (En función de F)
        sigma_p_alt = kfs * momento_flector_alt * c / i_pieza
        sigma_p_med = momento_flector_med * c / i_pieza

        # Calcular esfuerzo cortante alternante y medio en la pieza 1 (En función de F)
        tao_p_alt = kfs * f_alt / area_sold
        tao_p_med = f_med / area_sold

        # Calcular el esfuerzo de Von Misses alternante y medio en la pieza 1 (En función de F)
        sigma_p_von_misses_alt = sqrt(sigma_p_alt ** 2 + 3 * tao_p_alt ** 2)
        sigma_p_von_misses_med = sqrt(sigma_p_med ** 2 + 3 * tao_p_med ** 2)

        # Calcular la resistencia a la fatiga del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza1 = despejar_carga_ecuacion_gerber(sigma_p_von_misses_alt, sigma_p_von_misses_med, se_pieza1, sut_pieza1,
                                                  self.fd_min_pieza)

        # Determinar F en la pieza 2 (Pieza T)

        # Calcular esfuerzo normal alternante y medio en la pieza 2 (En función de F)
        sigma_t_alt = tao_p_alt
        sigma_t_med = tao_p_med

        # Calcular esfuerzo cortante alternante y medio en la pieza 2 (En función de F)
        tao_t_alt = sigma_p_alt
        tao_t_med = sigma_p_med

        # Calcular el esfuerzo de Von Misses alternante y medio en la pieza 2 (En función de F)
        sigma_t_von_misses_alt = sqrt(sigma_t_alt ** 2 + 3 * tao_t_alt ** 2)
        sigma_t_von_misses_med = sqrt(sigma_t_med ** 2 + 3 * tao_t_med ** 2)

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza2 = despejar_carga_ecuacion_gerber(sigma_t_von_misses_alt, sigma_t_von_misses_med, se_pieza2, sut_pieza2,
                                                  self.fd_min_pieza)

        # Seleccionar el menor de los valores de carga F obtenidos
        f = min(f_sold, f_pieza1, f_pieza2)

        # Obtener el valor de Fmax a partir de F y la relacion Fmax/Fmin
        f_max = relacion * f

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraFilete(self.sistema_unidades, self.tipo_union,
                                                                 {"Fmax": f_max, "bl": bl, "bt": bt},
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria, self.geometria_params,
                                                                 self.espesor_menor_piezas)

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_ccomb()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna()

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.carga_permisible_estatica_ccomb()

        # Generar diccionario para informe de resultados
        resultados = {
            "relacion_cargas": relacion,
            "bl": bl,
            "bt": bt,
            "f_alt": f_alt,
            "f_med": f_med,
            "momento_flector_alt": momento_flector_alt,
            "momento_flector_med": momento_flector_med,
            "momento_torsor_alt": momento_torsor_alt,
            "momento_torsor_med": momento_torsor_med,
            "pierna": self.geometria_params["pierna"],
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "garganta": round(self.calcular_garganta(), 3),
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": round(area_sold, 3),
            "i_sold": round(i_sold, 2),
            "i_sold_ecuacion": i_sold_ecuacion,
            "i_pieza": round(i_pieza, 2),
            "i_pieza_ecuacion": i_pieza_ecuacion,
            "j_sold": round(j_sold, 2),
            "j_sold_ecuacion": j_sold_ecuacion,
            "rx": round(rx, 3),
            "ry": round(ry, 3),
            "rx_ecuacion": rx_ry_ecuacion[0],
            "ry_ecuacion": rx_ry_ecuacion[1],
            "c": round(c, 3),
            "c_ecuacion": c_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_primario_alt": tao_primario_alt,
            "tao_primario_med": tao_primario_med,
            "tao_secundario_alt": tao_primario_alt,
            "tao_secundario_med": tao_secundario_med,
            "tao_terciario_alt_x": tao_terciario_alt_x,
            "tao_terciario_alt_y": tao_terciario_alt_y,
            "tao_terciario_med_x": tao_terciario_med_x,
            "tao_terciario_med_y": tao_terciario_med_y,
            "tao_alt_x": tao_alt_x,
            "tao_alt_y": tao_alt_y,
            "tao_alt_z": tao_alt_z,
            "tao_med_x": tao_med_x,
            "tao_med_y": tao_med_y,
            "tao_med_z": tao_med_z,
            "tao_alt_sold": tao_alt_sold,
            "tao_med_sold": tao_med_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "f_sold": round(f_sold, 2),
            "sigma_p_alt": sigma_p_alt,
            "sigma_p_med": sigma_p_med,
            "tao_p_alt": tao_p_alt,
            "tao_p_med": tao_p_med,
            "sigma_t_alt": sigma_t_alt,
            "sigma_t_med": sigma_t_med,
            "tao_t_alt": tao_t_alt,
            "tao_t_med": tao_t_med,
            "sigma_p_von_misses_alt": sigma_p_von_misses_alt,
            "sigma_p_von_misses_med": sigma_p_von_misses_med,
            "sigma_t_von_misses_alt": sigma_t_von_misses_alt,
            "sigma_t_von_misses_med": sigma_t_von_misses_med,
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "f_pieza1": round(f_pieza1, 2),
            "f_pieza2": round(f_pieza2, 2),
            "f_min": round(f, 2),
            "f_max": round(f_max, 2),
            "conclusion_fperm": conclusion_fperm,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga,
            "verificacion_pierna": verificacion_pierna
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    ###################################################################################################################
    # DISEÑO POR CARGA ESTÁTICA

    # Carga Paralela
    def carga_permisible_estatica_cp(self):

        # DISEÑO POR CARGA ESTÁTICA

        # Definir Fmax
        f_max = symbols("F")

        # Calcular área de la soldadura
        area_sold = self.calcular_area_sold()

        # SOLDADURA

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)

        # Calcular esfuerzo aplicado en la soldadura
        tao_sold = 1.414 * f_max / area_sold

        # Despejar Fmax_sold de la ecuación de FD
        f_max_sold = despejar_carga_max_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao_sold)

        # PIEZA 1

        # Calcular la resistencia a la fluencia al cortante de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1

        # Calcular esfuerzo aplicado en la pieza1
        tao_pieza1 = f_max / area_sold

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza1 = despejar_carga_max_fd_estatica(self.fd_min_pieza, ssy_pieza1, tao_pieza1)

        # PIEZA 2

        # Calcular la resistencia a la fluencia al cortante de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]
        ssy_pieza2 = 0.577 * sy_pieza2

        # Calcular esfuerzo aplicado en la pieza2
        tao_pieza2 = f_max / area_sold

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza2 = despejar_carga_max_fd_estatica(self.fd_min_pieza, ssy_pieza2, tao_pieza2)

        f_max_estatica = min(f_max_sold, f_max_pieza1, f_max_pieza2)

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max_estatica)

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna()

        # Generar diccionario para informe de resultados
        resultados = {
            "tipo_union": self.tipo_union,
            "pierna": self.geometria_params["pierna"],
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "garganta": round(self.calcular_garganta(), 3),
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": round(area_sold, 3),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "tao_sold": tao_sold,
            "f_max_sold": "{:.2f}".format(f_max_sold),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "ssy_pieza1": round(ssy_pieza1, 2),
            "ssy_pieza2": round(ssy_pieza2, 2),
            "tao_pieza1": tao_pieza1,
            "tao_pieza2": tao_pieza2,
            "f_max_pieza1": "{:.2f}".format(f_max_pieza1),
            "f_max_pieza2": "{:.2f}".format(f_max_pieza2),
            "conclusion_fperm": conclusion_fperm,
            "verificacion_pierna": verificacion_pierna
        }
        return resultados

    # Carga Transversal
    def carga_permisible_estatica_ctrans(self):

        # Definir Fmax
        f_max = symbols("F")

        # Calcular área de la soldadura
        area_sold = self.calcular_area_sold()
        print(area_sold)

        # SOLDADURA

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)
        print(sut_sold)

        # Calcular esfuerzo aplicado en la soldadura
        tao_sold = 1.414 * f_max / area_sold
        print(tao_sold)

        # Despejar Fmax_sold de la ecuación de FD
        f_max_sold = despejar_carga_max_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao_sold)

        # PIEZA 1 (Pieza P)

        # Calcular la resistencia a la fluencia al cortante de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1

        # Calcular esfuerzo aplicado en la pieza1
        tao_pieza1 = f_max / area_sold
        print(tao_pieza1)

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza1 = despejar_carga_max_fd_estatica(self.fd_min_pieza, ssy_pieza1, tao_pieza1)
        print(f_max_pieza1)

        # PIEZA 2 (Pieza T)

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Calcular esfuerzo aplicado en la pieza2
        sigma_pieza2 = f_max / area_sold
        print(sigma_pieza2)

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza2 = despejar_carga_max_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma_pieza2)
        print(f_max_pieza2)

        f_max_estatica = min(f_max_sold, f_max_pieza1, f_max_pieza2)

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max_estatica)

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna()

        # Generar diccionario para informe de resultados
        resultados = {
            "tipo_union": self.tipo_union,
            "pierna": self.geometria_params["pierna"],
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "garganta": round(self.calcular_garganta(), 3),
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": round(area_sold, 3),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "tao_sold": tao_sold,
            "f_max_sold": "{:.2f}".format(f_max_sold),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "ssy_pieza1": round(ssy_pieza1, 2),
            "tao_pieza1": tao_pieza1,
            "sigma_pieza2": sigma_pieza2,
            "f_max_pieza1": "{:.2f}".format(f_max_pieza1),
            "f_max_pieza2": "{:.2f}".format(f_max_pieza2),
            "conclusion_fperm": conclusion_fperm,
            "verificacion_pierna": verificacion_pierna
        }
        return resultados

    # Carga de Flexión debido a una carga excéntrica
    def carga_permisible_estatica_cflex(self):

        # Definir Fmax
        f_max = symbols("F")

        # Obtener el valor del brazo (b) y calcular el momento flector
        b = self.brazo
        momento_flector = f_max * b

        # Cálculo de parámetros geométricos
        area_sold = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia_sold()
        i_pieza, i_pieza_ecuacion = self.calcular_momento_inercia_pieza()
        c = self.obtener_rx_ry()[1]
        c_ecuacion = self.obtener_rx_ry()[2][1]

        # SOLDADURA

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)

        # Calcular esfuerzo cortante primario (En función de F)
        tao_primario = 1.414 * f_max / area_sold

        # Calcular esfuerzo cortante secundario (En función de F)
        tao_secundario = momento_flector * c / i_sold

        # Calcular esfuerzo cortante resultante en la soldadura (En función de F)
        tao_sold = sqrt(tao_primario ** 2 + tao_secundario ** 2)

        # Despejar Fmax_sold de la ecuación de FD
        f_max_sold = despejar_carga_max_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao_sold)

        # PIEZA 1 (Pieza P)

        # Obtener la resistencia a la fluencia de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]

        # Calcular esfuerzo normal y esfuerzo cortante aplicado en la pieza1
        sigma_p = momento_flector * c / i_pieza
        tao_p = f_max / area_sold

        # Calcular esfuerzo de Von Misses en la pieza 1 (En función de F)
        sigma_von_misses_1 = sqrt(sigma_p ** 2 + 3 * tao_p ** 2)

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza1 = despejar_carga_max_fd_estatica(self.fd_min_pieza, sy_pieza1, sigma_von_misses_1)

        # PIEZA 2 (Pieza T)

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Calcular esfuerzo normal y esfuerzo cortante aplicado en la pieza 2
        sigma_t = f_max / area_sold
        tao_t = momento_flector * c / i_pieza

        # Calcular esfuerzo de Von Misses en la pieza 2 (En función de F)
        sigma_von_misses_2 = sqrt(sigma_t ** 2 + 3 * tao_t ** 2)

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza2 = despejar_carga_max_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma_von_misses_2)

        f_max_estatica = min(f_max_sold, f_max_pieza1, f_max_pieza2)

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max_estatica)

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna()

        # Generar diccionario para informe de resultados
        resultados = {
            "tipo_union": self.tipo_union,
            "pierna": self.geometria_params["pierna"],
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "garganta": round(self.calcular_garganta(), 3),
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": round(area_sold, 3),
            "i_sold": round(i_sold, 2),
            "i_sold_ecuacion": i_sold_ecuacion,
            "i_pieza": round(i_pieza, 2),
            "i_pieza_ecuacion": i_pieza_ecuacion,
            "c": round(c, 3),
            "c_ecuacion": c_ecuacion,
            "b": b,
            "momento_flector": momento_flector,
            "tao_primario": tao_primario,
            "tao_secundario": tao_secundario,
            "tao_sold": tao_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "f_max_sold": "{:.2f}".format(f_max_sold),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sigma_p": sigma_p,
            "tao_p": tao_p,
            "sigma_t": sigma_t,
            "tao_t": tao_t,
            "sigma_von_misses_1": sigma_von_misses_1,
            "sigma_von_misses_2": sigma_von_misses_2,
            "f_max_pieza1": "{:.2f}".format(f_max_pieza1),
            "f_max_pieza2": "{:.2f}".format(f_max_pieza2),
            "conclusion_fperm": conclusion_fperm,
            "verificacion_pierna": verificacion_pierna
        }
        return resultados

    # Carga de Torsión debido a una fuerza excéntrica
    def carga_permisible_estatica_ctor(self):

        # Definir Fmax
        f_max = symbols("F")

        # Obtener el valor del brazo (b) y calcular el momento torsor
        b = self.brazo
        momento_torsor = f_max * b

        # Cálculo de parámetros geométricos
        area_sold = self.calcular_area_sold()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar_sold()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion

        if self.geometria == "ocho":
            ry, rx, ry_rx_ecuacion = self.obtener_rx_ry()
            ry_ecuacion, rx_ecuacion = ry_rx_ecuacion

        # SOLDADURA

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)

        # Calcular esfuerzo cortante primario (En función de F)
        tao_primario = 1.414 * f_max / area_sold

        # Calcular componentes x e y del esfuerzo cortante secundario
        tao_secundario_x = momento_torsor * ry / j_sold
        tao_secundario_y = momento_torsor * rx / j_sold

        # Calcular componentes x e y del esfuerzo cortante
        tao_x = tao_secundario_x
        tao_y = tao_primario + tao_secundario_y

        # Calcular esfuerzo cortante resultante en la soldadura (En función de F)
        tao_sold = sqrt(tao_x ** 2 + tao_y ** 2)

        # Despejar Fmax_sold de la ecuación de FD
        f_max_sold = despejar_carga_max_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao_sold)

        # PIEZA 1 (Pieza P)

        # Calcular la resistencia a la fluencia al cortante de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1

        # Calcular esfuerzo cortante aplicado en la pieza1 (En función de F)
        tao_p = f_max / area_sold

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza1 = despejar_carga_max_fd_estatica(self.fd_min_pieza, ssy_pieza1, tao_p)

        # PIEZA 2 (Pieza T)

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Calcular esfuerzo normal aplicado en la pieza 2 (En función de F)
        sigma_t = f_max / area_sold

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza2 = despejar_carga_max_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma_t)

        f_max_estatica = min(f_max_sold, f_max_pieza1, f_max_pieza2)

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max_estatica)

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna()

        # Generar diccionario para informe de resultados
        resultados = {
            "tipo_union": self.tipo_union,
            "pierna": self.geometria_params["pierna"],
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "garganta": round(self.calcular_garganta(), 3),
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": round(area_sold, 3),
            "j_sold": round(j_sold, 2),
            "j_sold_ecuacion": j_sold_ecuacion,
            "rx": round(rx, 3),
            "ry": round(ry, 3),
            "rx_ecuacion": rx_ecuacion,
            "ry_ecuacion": ry_ecuacion,
            "b": b,
            "momento_torsor": momento_torsor,
            "tao_primario": tao_primario,
            "tao_secundario_x": tao_secundario_x,
            "tao_secundario_y": tao_secundario_y,
            "tao_x": tao_x,
            "tao_y": tao_y,
            "tao_sold": tao_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "f_max_sold": "{:.2f}".format(f_max_sold),
            "sy_pieza1": sy_pieza1,
            "ssy_pieza1": ssy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "tao_p": tao_p,
            "sigma_t": sigma_t,
            "f_max_pieza1": "{:.2f}".format(f_max_pieza1),
            "f_max_pieza2": "{:.2f}".format(f_max_pieza2),
            "conclusion_fperm": conclusion_fperm,
            "verificacion_pierna": verificacion_pierna
        }
        return resultados

    # Carga Combinada debido a una fuerza excéntrica
    def carga_permisible_estatica_ccomb(self):

        # Definir Fmax
        f_max = symbols("F")

        # Obtener el valor del brazo longitudinal (bl) y del brazo transversal (bt) y calcular los momentos
        bl = self.brazo["bl"]
        bt = self.brazo["bt"]
        momento_flector = f_max * bl
        momento_torsor = f_max * bt

        # Cálculo de parámetros geométricos
        area_sold = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia_sold()
        i_pieza, i_pieza_ecuacion = self.calcular_momento_inercia_pieza()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar_sold()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        c = ry
        c_ecuacion = rx_ry_ecuacion[1]

        # SOLDADURA

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)

        # Calcular esfuerzo cortante primario (En función de F)
        tao_primario = 1.414 * f_max / area_sold

        # Calcular esfuerzo cortante secundario (En función de F)
        tao_secundario = momento_flector * c / i_sold

        # Calcular componentes x e y del esfuerzo terciario (En función de F)
        tao_terciario_x = momento_torsor * ry / j_sold
        tao_terciario_y = momento_torsor * rx / j_sold

        # Calcular las componentes X, Y y Z del esfuerzo cortante en la soldadura (En función de F)
        tao_x = tao_terciario_x
        tao_y = tao_primario + tao_terciario_y
        tao_z = tao_secundario

        # Calcular el esfuerzo cortante resultante aplicado en la soldadura (En función de F)
        tao_sold = sqrt(tao_x ** 2 + tao_y ** 2 + tao_z ** 2)

        # Despejar Fmax_sold de la ecuación de FD
        f_max_sold = despejar_carga_max_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao_sold)

        # PIEZA 1 (Pieza P)

        # Obtener la resistencia a la fluencia de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]

        # Calcular esfuerzo normal y esfuerzo cortante aplicado en la pieza1
        sigma_p = momento_flector * c / i_pieza
        tao_p = f_max / area_sold

        # Calcular esfuerzo de Von Misses en la pieza 1 (En función de F)
        sigma_von_misses_1 = sqrt(sigma_p ** 2 + 3 * tao_p ** 2)

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza1 = despejar_carga_max_fd_estatica(self.fd_min_pieza, sy_pieza1, sigma_von_misses_1)

        # PIEZA 2 (Pieza T)

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Calcular esfuerzo normal y esfuerzo cortante aplicado en la pieza 2
        sigma_t = f_max / area_sold
        tao_t = momento_flector * c / i_pieza

        # Calcular esfuerzo de Von Misses en la pieza 2 (En función de F)
        sigma_von_misses_2 = sqrt(sigma_t ** 2 + 3 * tao_t ** 2)

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza2 = despejar_carga_max_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma_von_misses_2)

        f_max_estatica = min(f_max_sold, f_max_pieza1, f_max_pieza2)

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max_estatica)

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna()

        # Generar diccionario para informe de resultados
        resultados = {
            "tipo_union": self.tipo_union,
            "pierna": self.geometria_params["pierna"],
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "garganta": round(self.calcular_garganta(), 3),
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": round(area_sold, 3),
            "i_sold": round(i_sold, 2),
            "i_sold_ecuacion": i_sold_ecuacion,
            "i_pieza": round(i_pieza, 2),
            "i_pieza_ecuacion": i_pieza_ecuacion,
            "j_sold": round(j_sold, 2),
            "j_sold_ecuacion": j_sold_ecuacion,
            "rx": round(rx, 3),
            "ry": round(ry, 3),
            "rx_ecuacion": rx_ry_ecuacion[0],
            "ry_ecuacion": rx_ry_ecuacion[1],
            "c": round(c, 3),
            "c_ecuacion": c_ecuacion,
            "bl": bl,
            "bt": bt,
            "momento_flector": momento_flector,
            "momento_torsor": momento_torsor,
            "tao_primario": tao_primario,
            "tao_secundario": tao_secundario,
            "tao_terciario_x": tao_terciario_x,
            "tao_terciario_y": tao_terciario_y,
            "tao_x": tao_x,
            "tao_y": tao_y,
            "tao_z": tao_z,
            "tao_sold": tao_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "f_max_sold": "{:.2f}".format(f_max_sold),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sigma_p": sigma_p,
            "tao_p": tao_p,
            "sigma_t": sigma_t,
            "tao_t": tao_t,
            "sigma_von_misses_1": sigma_von_misses_1,
            "sigma_von_misses_2": sigma_von_misses_2,
            "f_max_pieza1": "{:.2f}".format(f_max_pieza1),
            "f_max_pieza2": "{:.2f}".format(f_max_pieza2),
            "conclusion_fperm": conclusion_fperm,
            "verificacion_pierna": verificacion_pierna
        }
        return resultados


#######################################################################################################################


# Clase para el cálculo de la pierna del cordón de soldadura
class DisenoPiernaFilete:
    # Factores de diseño mínimos
    fd_min_sold = 3.33
    fd_min_pieza = 2.5

    def __init__(self, sistema_unidades, tipo_union, carga, material_base_1, material_base_2,
                 electrodo, geometria, geometria_params, espesor_menor_piezas):
        self.sistema_unidades = sistema_unidades
        self.tipo_union = tipo_union
        self.carga = carga
        self.material_base_1 = material_base_1
        self.material_base_2 = material_base_2
        self.electrodo = electrodo
        self.geometria = geometria
        self.geometria_params = geometria_params
        self.espesor_menor_piezas = espesor_menor_piezas

    ###################################################################################################################

    # Verificar tamaño máximo de la pierna del cordón de soldadura
    def verificar_tamano_max_pierna(self, h_min):

        e_menor_piezas = self.espesor_menor_piezas

        if self.sistema_unidades == "Internacional":
            if h_min > e_menor_piezas:
                conclusion = f"""La pierna mínima necesaria para soportar las condiciones de carga de la junta es hmin = {h_min} mm. Como el espesor menor de las piezas ({e_menor_piezas} mm) < hmin ({h_min} mm), no cumple y se debe rediseñar. Considere cambiar la geometría del cordón, disminuir la carga aplicada en la junta, o modificar los materiales."""
                cumple = False
            else:
                conclusion = f"La pierna mínima necesaria en la junta es hmin = {h_min} mm"
                cumple = True
        else:
            if h_min > e_menor_piezas:
                conclusion = f"""La pierna mínima necesaria para soportar las condiciones de carga de la junta es hmin = {h_min} pulg. Como el espesor menor de las piezas ({e_menor_piezas} pulg) < hmin ({h_min} pulg), no cumple y se debe rediseñar. Considere cambiar la geometría del cordón, disminuir la carga aplicada en la junta, o modificar los materiales."""
                cumple = False
            else:
                conclusion = f"La pierna mínima necesaria en la junta es hmin = {h_min} pulg"
                cumple = True

        return cumple, conclusion

    # Verificar el tamaño mínimo de la pierna del cordón de soldadura
    def verificar_tamano_minimo_pierna(self, h):
        sistema_unidades = self.sistema_unidades
        e_menor = self.espesor_menor_piezas
        conclusion = ""

        if sistema_unidades == "Internacional":
            if e_menor <= 6:
                if h >= 3:
                    conclusion = f"""Para un espesor e = {e_menor} mm, hmin = 3 mm.
    Como h = {h} mm, entonces cumple con la especificación de la norma AWS."""
                else:
                    conclusion = f"""Para un espesor e = {e_menor} mm, hmin = 3 mm.
    Como h = {h} mm, entonces no cumple con la especificación de la norma AWS. Por lo tanto, se especifica h = 3 mm"""
            elif 6 < e_menor <= 12:
                if h >= 5:
                    conclusion = f"""Para un espesor e = {e_menor} mm, hmin = 5 mm.
    Como h = {h} mm, entonces cumple con la especificación de la norma AWS."""
                else:
                    conclusion = f"""Para un espesor e = {e_menor} mm, hmin = 5 mm.
    Como h = {h} mm, entonces no cumple con la especificación de la norma AWS. Por lo tanto, se especifica h = 5 mm"""
            elif 12 < e_menor <= 20:
                if h >= 6:
                    conclusion = f"""Para un espesor e = {e_menor} mm, hmin = 6 mm.
    Como h = {h} mm, entonces cumple con la especificación de la norma AWS."""
                else:
                    conclusion = f"""Para un espesor e = {e_menor} mm, hmin = 6 mm.
    Como h = {h} mm, entonces no cumple con la especificación de la norma AWS. Por lo tanto, se especifica h = 6 mm"""
            elif e_menor > 20:
                if h >= 8:
                    conclusion = f"""Para un espesor e = {e_menor} mm, hmin = 8 mm.
    Como h = {h} mm, entonces cumple con la especificación de la norma AWS."""
                else:
                    conclusion = f"""Para un espesor e = {e_menor} mm, hmin = 8 mm.
    Como h = {h} mm, entonces no cumple con la especificación de la norma AWS. Por lo tanto, se especifica h = 8 mm"""

        if sistema_unidades == "Inglés":
            if e_menor <= 1 / 4:
                if h >= 1 / 8:
                    conclusion = f"""Para un espesor e = {e_menor} pulg, hmin = 1/8 pulg.
    Como h = {h} pulg, entonces cumple con la especificación de la norma AWS."""
                else:
                    conclusion = f"""Para un espesor e = {e_menor} pulg, hmin = 1/8 pulg.
    Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS. Por lo tanto, se especifica h = 1/8 pulg"""
            elif 1 / 4 < e_menor <= 1 / 2:
                if h >= 3 / 16:
                    conclusion = f"""Para un espesor e = {e_menor} pulg, hmin = 3/16 pulg.
    Como h = {h} pulg, entonces cumple con la especificación de la norma AWS."""
                else:
                    conclusion = f"""Para un espesor e = {e_menor} pulg, hmin = 3/16 pulg.
    Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS. Por lo tanto, se especifica h = 3/16 pulg"""
            elif 1 / 2 < e_menor <= 3 / 4:
                if h >= 1 / 4:
                    conclusion = f"""Para un espesor e = {e_menor} pulg, hmin = 1/4 pulg.
    Como h = {h} pulg, entonces cumple con la especificación de la norma AWS."""
                else:
                    conclusion = f"""Para un espesor e = {e_menor} pulg, hmin = 1/4 pulg.
    Comoh = {h} pulg, entonces no cumple con la especificación de la norma AWS. Por lo tanto, se especifica h = 1/4 pulg"""
            elif e_menor > 3 / 4:
                if h >= 5 / 16:
                    conclusion = f"""Para un espesor e = {e_menor} pulg, hmin = 5/16 pulg.
    Como h = {h} pulg, entonces cumple con la especificación de la norma AWS."""
                else:
                    conclusion = f"""Para un espesor e = {e_menor} pulg, hmin = 5/16 pulg.
    Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS. Por lo tanto, se especifica h = 5/16 pulg"""

        return conclusion

    # Ajustar el tamaño mínimo de pierna necesario según la especificación de AWS
    def ajustar_tamano_pierna_aws(self, h_min_calculada):

        e_menor_piezas = self.espesor_menor_piezas
        h_min_modificada = h_min_calculada

        if self.sistema_unidades == "Internacional":

            if e_menor_piezas <= 6:
                if h_min_calculada < 3:
                    h_min_modificada = 3
            elif 6 < e_menor_piezas <= 12:
                if h_min_calculada < 5:
                    h_min_modificada = 5
            elif 12 < e_menor_piezas <= 20:
                if h_min_calculada < 6:
                    h_min_modificada = 6
            elif e_menor_piezas > 20:
                if h_min_calculada < 8:
                    h_min_modificada = 8

        if self.sistema_unidades == "Inglés":

            if e_menor_piezas <= 1 / 4:
                if h_min_calculada < 1 / 8:
                    h_min_modificada = 1 / 8
            elif 1 / 4 < e_menor_piezas <= 1 / 2:
                if h_min_calculada < 3 / 16:
                    h_min_modificada = 3 / 16
            elif 1 / 2 < e_menor_piezas <= 3 / 4:
                if h_min_calculada < 1 / 4:
                    h_min_modificada = 1 / 4
            elif e_menor_piezas > 3 / 4:
                if h_min_calculada < 5 / 16:
                    h_min_modificada = 5 / 16

        return h_min_modificada

    # GEOMETRIA

    # Calcular longitud total del cordón de soldadura
    def calcular_longitud_total(self):
        l = self.geometria_params.get("largo", 0)
        a = self.geometria_params.get("ancho", 0)
        r = self.geometria_params.get("radio", 0)

        geometrias_longitudes = {
            "uno": l,
            "dos": l,
            "tres": (l + a),
            "cuatro": (l + a),
            "cinco": (2 * l),
            "seis": (2 * l),
            "siete": (2 * l + a),
            "ocho": (2 * pi * r),
            "nueve": 2 * l + a,
            "diez": 2 * l + a,
            "once": 2 * l + 2 * a,
            "doce": 2 * l + 2 * a
        }

        lt_ecuaciones = {
            "uno": 'l',
            "dos": 'l',
            "tres": 'l + a',
            "cuatro": 'l + a',
            "cinco": '2 * l',
            "seis": '2 * l',
            "siete": '2 * l + a',
            "ocho": '2 * pi * r',
            "nueve": '2 * l + a',
            "diez": '2 * l + a',
            "once": '2 * l + 2 * a',
            "doce": '2 * l + 2 * a'
        }

        longitud_total = geometrias_longitudes[self.geometria]
        ecuacion = lt_ecuaciones[self.geometria]
        return longitud_total, ecuacion

    # Realizar cálculo del área de la pierna del cordón de soldadura (En función de h)
    def calcular_area_sold(self):
        h = symbols("h")
        longitud_total = self.calcular_longitud_total()[0]
        area_sold = h * longitud_total
        return area_sold

    # Calcular momento de inercia en la soldadura (I) (En función de h)
    def calcular_momento_inercia_sold(self):
        h = symbols("h")
        l = self.geometria_params.get("largo", 0)
        a = self.geometria_params.get("ancho", 0)
        r = self.geometria_params.get("radio", 0)

        if l == 0 and a == 0:
            momento_de_inercia = 0.707 * h * pi * r ** 3
            ecuacion = "0.707 * h * pi * r^3"
        else:
            momentos_inercia_geometrias = {
                "uno": (0.059 * h * l ** 3),
                "dos": (0.059 * h ** 3 * l),
                "tres": (0.059 * (h * l ** 2 * (l ** 2 + 4 * a * l)) / (l + a)),
                "cuatro": (0.059 * (h * a ** 2 * (a ** 2 + 4 * l * a)) / (a + l)),
                "cinco": (0.118 * h * l ** 3),
                "seis": (0.354 * h * l * a ** 2),
                "siete": (0.059 * h * l ** 2 * (6 * l + a)),
                "ocho": (0.707 * h * pi * r ** 3),
                "nueve": (0.707 * h * ((9 * l ** 4 + 2 * l ** 3 * (a + 2 * l)) / (3 * (a + 2 * l)))),
                "diez": (0.707 * h * ((9 * l ** 4 + 2 * l ** 3 * (a + 2 * l)) / (3 * (a + 2 * l)))),
                "once": (0.118 * h * l ** 2 * (3 * a + l)),
                "doce": (0.118 * h * l ** 2 * (3 * a + l))
            }

            momento_inercia_ecuaciones = {
                "uno": "0.059 * h * l^3",
                "dos": "0.059 * h^3 * l",
                "tres": "0.059 * (h * l^2 * (l^2 + 4 * a * l)) / (l + a)",
                "cuatro": "0.059 * (h * a^2 * (a^2 + 4 * l * a)) / (a + l)",
                "cinco": "0.118 * h * l^3",
                "seis": "0.354 * h * l * a^2",
                "siete": "0.059 * h * l^2 * (6 * l + a)",
                "ocho": "0.707 * h * pi * r^3",
                "nueve": "0.707 * h * ((9 * l^4 + 2 * l^3 * (a + 2 * l)) / (3 * (a + 2 * l)))",
                "diez": "0.707 * h * ((9 * l^4 + 2 * l^3 * (a + 2 * l)) / (3 * (a + 2 * l)))",
                "once": "0.118 * h * l^2 * (3 * a + l)",
                "doce": "0.118 * h * l^2 * (3 * a + l)"
            }

            momento_de_inercia = momentos_inercia_geometrias[self.geometria]
            ecuacion = momento_inercia_ecuaciones[self.geometria]

        return momento_de_inercia, ecuacion

    # Calcular momento de inercia en la pieza (I)
    def calcular_momento_inercia_pieza(self):
        h = symbols("h")
        l = self.geometria_params.get("largo", 0)
        a = self.geometria_params.get("ancho", 0)
        r = self.geometria_params.get("radio", 0)

        if l == 0 and a == 0:
            momento_de_inercia = h * pi * r ** 3
            ecuacion = "h * pi * r^3"
        else:
            momentos_inercia_geometrias = {
                "uno": (0.0834 * h * l ** 3),
                "dos": (0.0834 * h ** 3 * l),
                "tres": (0.084 * (h * l ** 2 * (l ** 2 + 4 * a * l)) / (l + a)),
                "cuatro": (0.084 * (h * a ** 2 * (a ** 2 + 4 * l * a)) / (a + l)),
                "cinco": (0.167 * h * l ** 3),
                "seis": (0.5 * h * l * a ** 2),
                "siete": (0.0834 * h * l ** 2 * (6 * l + a)),
                "ocho": (h * pi * r ** 3),
                "nueve": (h * ((9 * l ** 4 + 2 * l ** 3 * (a + 2 * l)) / (3 * (a + 2 * l)))),
                "diez": (h * ((9 * l ** 4 + 2 * l ** 3 * (a + 2 * l)) / (3 * (a + 2 * l)))),
                "once": (0.167 * h * l ** 2 * (3 * a + l)),
                "doce": (0.167 * h * l ** 2 * (3 * a + l))
            }

            momento_inercia_ecuaciones = {
                "uno": "0.0834 * h * l^3",
                "dos": "0.0834 * h^3 * l",
                "tres": "0.084 * (h * l^2 * (l^2 + 4 * a * l)) / (l + a)",
                "cuatro": "0.084 * (h * a^2 * (a ** 2 + 4 * l * a)) / (a + l)",
                "cinco": "0.167 * h * l^3",
                "seis": "0.5 * h * l * a^2",
                "siete": "0.0834 * h * l^2 * (6 * l + a)",
                "ocho": "h * pi * r^3",
                "nueve": "h * ((9 * l^4 + 2 * l^3 * (a + 2 * l)) / (3 * (a + 2 * l)))",
                "diez": "h * ((9 * l^4 + 2 * l^3 * (a + 2 * l)) / (3 * (a + 2 * l)))",
                "once": "0.167 * h * l^2 * (3 * a + l)",
                "doce": "0.167 * h * l^2 * (3 * a + l)"
            }

            momento_de_inercia = momentos_inercia_geometrias[self.geometria]
            ecuacion = momento_inercia_ecuaciones[self.geometria]

        return momento_de_inercia, ecuacion

    # Calcular momento de intercia polar en la soldadura (J)
    def calcular_momento_inercia_polar_sold(self):
        h = symbols("h")
        l = self.geometria_params.get("largo", 0)
        a = self.geometria_params.get("ancho", 0)
        r = self.geometria_params.get("radio", 0)

        if l == 0 and a == 0:
            momento_de_inercia_polar = 1.414 * h * pi * r ** 3
            ecuacion = "1.414 * h * pi * r^3"
        else:
            momentos_inercia_polar_geometrias = {
                "uno": (0.059 * h * l ** 3),
                "dos": (0.059 * h * l ** 3),
                "tres": (0.059 * (h * ((a + l) ** 4 - 6 * a ** 2 * l ** 2)) / (a + l)),
                "cuatro": (0.059 * (h * ((a + l) ** 4 - 6 * a ** 2 * l ** 2)) / (a + l)),
                "cinco": (0.059 * h * l * (3 * a ** 2 + l ** 2)),
                "seis": (0.059 * h * l * (3 * a ** 2 + l ** 2)),
                "siete": (0.707 * h * (((a ** 3 + 6 * l * a ** 2 + 8 * l ** 3) / 12) - ((l ** 4) / (2 * l + a)))),
                "ocho": (1.414 * h * pi * r ** 3),
                "nueve": (0.707 * h * (((a ** 3 + 6 * l * a ** 2 + 8 * l ** 3) / 12) - ((l ** 4) / (2 * l + a)))),
                "diez": (0.707 * h * (((l ** 3 + 6 * a * l ** 2 + 8 * a ** 3) / 12) - ((a ** 4) / (2 * a + l)))),
                "once": (0.118 * h * (a + l) ** 3),
                "doce": (0.059 * h * (a ** 3 + 3 * a * l ** 2 + l ** 3))
            }

            momento_inercia_polar_ecuaciones = {
                "uno": "0.059 * h * l^3",
                "dos": "0.059 * h * l^3",
                "tres": "0.059 * (h * ((a + l)^4 - 6 * a ** 2 * l^2)) / (a + l)",
                "cuatro": "0.059 * (h * ((a + l)^4 - 6 * a^2 * l^2)) / (a + l)",
                "cinco": "0.059 * h * l * (3 * a^2 + l^2)",
                "seis": "0.059 * h * l * (3 * a^2 + l^2)",
                "siete": "0.707 * h * (((a^3 + 6 * l * a^2 + 8 * l^3) / 12) - ((l^4) / (2 * l + a)))",
                "ocho": "1.414 * h * pi * r^3",
                "nueve": "0.707 * h * (((a^3 + 6 * l * a^2 + 8 * l^3) / 12) - ((l^4) / (2 * l + a)))",
                "diez": "0.707 * h * (((l^3 + 6 * a * l^2 + 8 * a^3) / 12) - ((a^4) / (2 * a + l)))",
                "once": "0.118 * h * (a + l)^3",
                "doce": "0.059 * h * (a^3 + 3 * a * l^2 + l^3)"
            }

            momento_de_inercia_polar = momentos_inercia_polar_geometrias[self.geometria]
            ecuacion = momento_inercia_polar_ecuaciones[self.geometria]

        return momento_de_inercia_polar, ecuacion

    # Obtener las coordenadas del centroide (X barra, Y barra)
    def obtener_coordenadas_centroide(self):
        l = self.geometria_params.get("largo", 0)
        a = self.geometria_params.get("ancho", 0)

        if l == 0 and a == 0:
            x_barra, y_barra = 0, 0
        else:
            coordenadas_centroide_geometrias = {
                "uno": (0, l / 2),
                "dos": (l / 2, 0),
                "tres": ((a ** 2) / (2 * (a + l)), (l ** 2) / (2 * (l + a))),
                "cuatro": ((l ** 2) / (2 * (l + a)), (a ** 2) / (2 * (a + l))),
                "cinco": (a / 2, l / 2),
                "seis": (l / 2, a / 2),
                "siete": ((l ** 2) / (2 * l + a), a / 2),
                "ocho": (0, 0),
                "nueve": (a / 2, (l ** 2) / (2 * l + a)),
                "diez": (a / 2, (l ** 2) / (2 * l + a)),
                "once": (a / 2, l / 2),
                "doce": (a / 2, l / 2)
            }
            x_barra, y_barra = coordenadas_centroide_geometrias.get(self.geometria)

        return x_barra, y_barra

    # Obtener rx y ry para calcular el esfuerzo debido al par torsionante
    def obtener_rx_ry(self):
        l = self.geometria_params.get("largo", 0)
        a = self.geometria_params.get("ancho", 0)
        r = self.geometria_params.get("radio", 0)

        if l == 0 and a == 0:
            rx, ry = 0, r
            rx_ry_formulas = "0", "r"
        else:
            rx_ry_geometrias = {
                "uno": (0, l / 2),
                "dos": (l / 2, 0),
                "tres": ((a ** 2) / (2 * (a + l)), l - (l ** 2) / (2 * (l + a))),
                "cuatro": (l - (l ** 2) / (2 * (l + a)), (a ** 2) / (2 * (a + l))),
                "cinco": (a / 2, l / 2),
                "seis": (l / 2, a / 2),
                "siete": (l - (l ** 2) / (2 * l + a), a / 2),
                "ocho": (0, r),
                "nueve": (a / 2, l - (l ** 2) / (2 * l + a)),
                "diez": (0, l - (l ** 2) / (2 * l + a)),
                "once": (a / 2, l / 2),
                "doce": (a / 2, l / 2)
            }

            rx_ry_ecuaciones = {
                "uno": ("0", "l/2"),
                "dos": ("l/2", "0"),
                "tres": ("(a^2) / (2 * (a + l))", "l - (l^2) / (2 * (l + a))"),
                "cuatro": ("l - (l^2) / (2 * (l + a))", "(a^2) / (2 * (a + l))"),
                "cinco": ("a/2", "l/2"),
                "seis": ("l/2", "a/2"),
                "siete": ("l - (l^2) / (2 * l + a)", "a / 2"),
                "ocho": ("0", "r"),
                "nueve": ("a/2", "l - (l^2) / (2 * l + a)"),
                "diez": ("0", "l - (l^2) / (2 * l + a)"),
                "once": ("a/2", "l/2"),
                "doce": ("a/2", "l/2")
            }

            rx, ry = rx_ry_geometrias.get(self.geometria)
            rx_ry_formulas = rx_ry_ecuaciones[self.geometria]

        return rx, ry, rx_ry_formulas

    ###################################################################################################################
    # DISEÑO POR FATIGA

    # Carga Paralela
    def pierna_cp(self):

        # DISEÑO POR FATIGA

        # Obtener cargas max y min
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]

        # Calcular cargas alternantes y medias
        f_alt, f_med = analisis.calcular_carga_alt_y_med(f_max, f_min)

        # Factor de concentración de esfuerzo reducido, Kfs (Se considera carga paralela con unión intermedia)
        kfs = 2.7

        # Area de la soldadura
        area_sold = self.calcular_area_sold()

        # Determinar h en la soldadura

        # Calcular esfuerzo cortante alternante y medio en la soldadura
        tao_alt_sold = kfs * 1.414 * f_alt / area_sold
        tao_med_sold = 1.414 * f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_sold = 3.33
        h_sold = despejar_pierna_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar h en la pieza 1

        # Obtener esfuerzo cortante alternante y medio en la pieza 1 (en función de h)
        tao_alt_pieza1 = kfs * f_alt / area_sold
        tao_med_pieza1 = f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia ultima al cortante del material base 1
        ssu_pieza1 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_pieza = 2.5
        h_pieza1 = despejar_pierna_ecuacion_gerber(tao_alt_pieza1, tao_med_pieza1, sse_pieza1, ssu_pieza1,
                                                   self.fd_min_pieza)

        # Determinar h en la pieza 2

        # Obtener esfuerzo cortante alternante y medio en la pieza 2 (en función de h)
        tao_alt_pieza2 = kfs * f_alt / area_sold
        tao_med_pieza2 = f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        sse_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular la resistencia ultima al cortante del material base 2
        ssu_pieza2 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza2)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_pieza = 2.5
        h_pieza2 = despejar_pierna_ecuacion_gerber(tao_alt_pieza2, tao_med_pieza2, sse_pieza2, ssu_pieza2,
                                                   self.fd_min_pieza)

        # Seleccionar el mayor de los valores para la pierna h obtenidos
        h_min = round(max(h_sold, h_pieza1, h_pieza2), 3 if self.sistema_unidades == "Internacional" else 4)

        # Mensaje con la pierna mínima (hmin) obtenida
        conclusion_h_min = conclusion_pierna_min(self.sistema_unidades, h_min)

        # Verificar que la pierna calculada no exceda el tamaño máximo y generar mensaje sobre la verificacion
        cumple_h_max, verificacion_h_max = self.verificar_tamano_max_pierna(h_min)

        if not cumple_h_max:
            verificacion_h_min = "N/A"
            valores_comprobacion_estatica = None
            rediseno_estatica = None
            conclusion_diseno_fatiga = "N/A"

        else:
            # Si no excede el tamaño máximo, se verifica que no esté por debajo del tamaño mínimo
            verificacion_h_min = self.verificar_tamano_minimo_pierna(h_min)

            # Si es neceario, ajustar el valor de h_min según la especificación de la AWS
            h_min = self.ajustar_tamano_pierna_aws(h_min)

            # Analizar por carga estática partiendo del resultado obtenido
            comprobacion_estatica = analisis.AnalisisSoldaduraFilete(self.sistema_unidades, self.tipo_union, self.carga,
                                                                     self.material_base_1, self.material_base_2,
                                                                     self.electrodo, self.geometria,
                                                                     {"pierna": h_min,
                                                                      "largo": self.geometria_params.get("largo", 0),
                                                                      "ancho": self.geometria_params.get("ancho", 0)},
                                                                     self.espesor_menor_piezas)

            # Verificar si se presentó la falla por carga estática y obtener valores para informe
            falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_cp()

            # Mensaje de conclusion de diseño por fatiga
            conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

            if not falla_estatica:
                rediseno_estatica = None
            else:
                # DISEÑO POR CARGA ESTÁTICA
                rediseno_estatica = self.pierna_cp_estatica()

        # Generar diccionario para informe de resultados del diseño por fatiga
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": area_sold,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_alt_sold": tao_alt_sold,
            "tao_med_sold": tao_med_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "h_sold": round(h_sold, 3 if self.sistema_unidades == "Internacional" else 4),
            "tao_alt_pieza1": tao_alt_pieza1,
            "tao_med_pieza1": tao_med_pieza1,
            "tao_alt_pieza2": tao_alt_pieza2,
            "tao_med_pieza2": tao_med_pieza2,
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "sse_pieza2": round(sse_pieza2, 2),
            "ssu_pieza2": round(ssu_pieza2, 2),
            "h_pieza1": round(h_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_pieza2": round(h_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min": h_min,
            "conclusion_h_min": conclusion_h_min,
            "verificacion_h_max": verificacion_h_max,
            "verificacion_h_min": verificacion_h_min,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga Trasversal
    def pierna_ctrans(self):

        # DISEÑO POR FATIGA

        # Obtener cargas max y min
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]

        # Calcular cargas alternantes y medias
        f_alt, f_med = analisis.calcular_carga_alt_y_med(f_max, f_min)

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Intermedia": 1.5, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Area de la soldadura
        area_sold = self.calcular_area_sold()

        # Determinar h en la soldadura

        # Calcular esfuerzo cortante alternante y medio en la soldadura
        tao_alt_sold = kfs * 1.414 * f_alt / area_sold
        tao_med_sold = 1.414 * f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_sold = 3.33
        h_sold = despejar_pierna_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar h en la pieza 1 (Pieza P)

        # Obtener esfuerzo cortante alternante y medio en la pieza 1 (en función de h)
        tao_p_alt = kfs * f_alt / area_sold
        tao_p_med = f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia ultima al cortante del material base 1
        ssu_pieza1 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_pieza = 2.5
        h_pieza1 = despejar_pierna_ecuacion_gerber(tao_p_alt, tao_p_med, sse_pieza1, ssu_pieza1,
                                                   self.fd_min_pieza)

        # Determinar h en la pieza 2 (Pieza T)

        # Obtener esfuerzo cortante alternante y medio en la pieza 2 (en función de h)
        sigma_t_alt = kfs * f_alt / area_sold
        sigma_t_med = f_med / area_sold

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_pieza = 2.5
        h_pieza2 = despejar_pierna_ecuacion_gerber(sigma_t_alt, sigma_t_med, se_pieza2, sut_pieza2,
                                                   self.fd_min_pieza)

        # Seleccionar el mayor de los valores para la pierna h obtenidos
        h_min = round(max(h_sold, h_pieza1, h_pieza2), 3 if self.sistema_unidades == "Internacional" else 4)

        # Mensaje con la pierna mínima (hmin) obtenida
        conclusion_h_min = conclusion_pierna_min(self.sistema_unidades, h_min)

        # Verificar que la pierna calculada no exceda el tamaño máximo y generar mensaje sobre la verificacion
        cumple_h_max, verificacion_h_max = self.verificar_tamano_max_pierna(h_min)

        if not cumple_h_max:
            verificacion_h_min = "N/A"
            valores_comprobacion_estatica = None
            rediseno_estatica = None
            conclusion_diseno_fatiga = "N/A"

        else:
            # Si no excede el tamaño máximo, se verifica que no esté por debajo del tamaño mínimo
            verificacion_h_min = self.verificar_tamano_minimo_pierna(h_min)

            # Si es neceario, ajustar el valor de h_min según la especificación de la AWS
            h_min = self.ajustar_tamano_pierna_aws(h_min)

            # Analizar por carga estática partiendo del resultado obtenido
            comprobacion_estatica = analisis.AnalisisSoldaduraFilete(self.sistema_unidades, self.tipo_union, self.carga,
                                                                     self.material_base_1, self.material_base_2,
                                                                     self.electrodo, self.geometria,
                                                                     {"pierna": h_min,
                                                                      "largo": self.geometria_params.get("largo", 0),
                                                                      "ancho": self.geometria_params.get("ancho", 0),
                                                                      "radio": self.geometria_params.get("radio", 0)},
                                                                     self.espesor_menor_piezas)

            # Verificar si se presentó la falla por carga estática y obtener valores para informe
            falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_ctrans()

            # Mensaje de conclusion de diseño por fatiga
            conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

            if not falla_estatica:
                rediseno_estatica = None

            else:
                # DISEÑO POR CARGA ESTÁTICA
                rediseno_estatica = self.pierna_ctrans_estatica()

        # Generar diccionario para informe de resultados del diseño por fatiga
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": area_sold,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_alt_sold": tao_alt_sold,
            "tao_med_sold": tao_med_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "h_sold": round(h_sold, 3 if self.sistema_unidades == "Internacional" else 4),
            "tao_p_alt": tao_p_alt,
            "tao_p_med": tao_p_med,
            "sigma_t_alt": sigma_t_alt,
            "sigma_t_med": sigma_t_med,
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "ssu_pieza1": ssu_pieza1,
            "sse_pieza1": round(sse_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "h_pieza1": round(h_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_pieza2": round(h_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min": h_min,
            "conclusion_h_min": conclusion_h_min,
            "verificacion_h_max": verificacion_h_max,
            "verificacion_h_min": verificacion_h_min,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga de Flexión debido a una fuerza excéntrica
    def pierna_cflex(self):

        # DISEÑO POR FATIGA

        # Obtener cargas max y min, y el brazo (b)
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]
        b = self.carga["b"]
        momento_flector_max, momento_flector_min = analisis.calcular_momento_max_y_min(f_max, f_min, b)

        # Calcular cargas alternantes y medias
        f_alt, f_med = analisis.calcular_carga_alt_y_med(f_max, f_min)
        momento_flector_alt, momento_flector_med = analisis.calcular_carga_alt_y_med(momento_flector_max,
                                                                                     momento_flector_min)

        # Factor de concentración de esfuerzo reducido, Kfs (Se considera carga transversal y unión T)
        kfs = 2

        # Calculo de parámetros geométricos
        area_sold = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia_sold()
        i_pieza, i_pieza_ecuacion = self.calcular_momento_inercia_pieza()
        c = self.obtener_rx_ry()[1]
        c_ecuacion = self.obtener_rx_ry()[2][1]

        # Determinar h en la soldadura

        # Calcular esfuerzo cortante primario alternante y medio en la soldadura (En función de h)
        tao_primario_alt = kfs * 1.414 * f_alt / area_sold
        tao_primario_med = 1.414 * f_med / area_sold

        # Calcular esfuerzo cortante secundadario alternante y medio en la soldadura (En función de h)
        tao_secundario_alt = kfs * momento_flector_alt * c / i_sold
        tao_secundario_med = momento_flector_med * c / i_sold

        # Calcular el esfuerzo cortante resultante alternante y medio en la soldadura (En función de h)
        tao_alt_sold = sqrt(tao_primario_alt ** 2 + tao_secundario_alt ** 2)
        tao_med_sold = sqrt(tao_primario_med ** 2 + tao_secundario_med ** 2)

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_sold = 3.33
        h_sold = despejar_pierna_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar h en la pieza 1 (Pieza P)

        # Calcular esfuerzo normal alternante y medio en la pieza 1 (En función de h)
        sigma_p_alt = kfs * momento_flector_alt * c / i_pieza
        sigma_p_med = momento_flector_med * c / i_pieza

        # Calcular esfuerzo cortante alternante y medio en la pieza 1 (En función de h)
        tao_p_alt = kfs * f_alt / area_sold
        tao_p_med = f_med / area_sold

        # Calcular el esfuerzo de Von Misses alternante y medio en la pieza 1 (En función de h)
        sigma_p_von_misses_alt = sqrt(sigma_p_alt ** 2 + 3 * tao_p_alt ** 2)
        sigma_p_von_misses_med = sqrt(sigma_p_med ** 2 + 3 * tao_p_med ** 2)

        # Calcular la resistencia a la fatiga del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_pieza = 2.5
        h_pieza1 = despejar_pierna_ecuacion_gerber(sigma_p_von_misses_alt, sigma_p_von_misses_med, se_pieza1,
                                                   sut_pieza1,
                                                   self.fd_min_pieza)

        # Determinar h en la pieza 2 (Pieza T)

        # Calcular esfuerzo normal alternante y medio en la pieza 2 (En función de h)
        sigma_t_alt = tao_p_alt
        sigma_t_med = tao_p_med

        # Calcular esfuerzo cortante alternante y medio en la pieza 2 (En función de h)
        tao_t_alt = sigma_p_alt
        tao_t_med = sigma_p_med

        # Calcular el esfuerzo de Von Misses alternante y medio en la pieza 2 (En función de h)
        sigma_t_von_misses_alt = sqrt(sigma_t_alt ** 2 + 3 * tao_t_alt ** 2)
        sigma_t_von_misses_med = sqrt(sigma_t_med ** 2 + 3 * tao_t_med ** 2)

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_pieza = 2.5
        h_pieza2 = despejar_pierna_ecuacion_gerber(sigma_t_von_misses_alt, sigma_t_von_misses_med, se_pieza2,
                                                   sut_pieza2, self.fd_min_pieza)

        # Seleccionar el mayor de los valores para la pierna h obtenidos
        h_min = round(max(h_sold, h_pieza1, h_pieza2), 3 if self.sistema_unidades == "Internacional" else 4)

        # Mensaje con la pierna mínima (hmin) obtenida
        conclusion_h_min = conclusion_pierna_min(self.sistema_unidades, h_min)

        # Verificar que la pierna calculada no exceda el tamaño máximo y generar mensaje sobre la verificacion
        cumple_h_max, verificacion_h_max = self.verificar_tamano_max_pierna(h_min)

        if not cumple_h_max:
            verificacion_h_min = "N/A"
            valores_comprobacion_estatica = None
            rediseno_estatica = None
            conclusion_diseno_fatiga = "N/A"

        else:
            # Si no excede el tamaño máximo, se verifica que no esté por debajo del tamaño mínimo
            verificacion_h_min = self.verificar_tamano_minimo_pierna(h_min)

            # Si es neceario, ajustar el valor de h_min según la especificación de la AWS
            h_min = self.ajustar_tamano_pierna_aws(h_min)

            # Analizar por carga estática partiendo del resultado obtenido
            comprobacion_estatica = analisis.AnalisisSoldaduraFilete(self.sistema_unidades, self.tipo_union, self.carga,
                                                                     self.material_base_1, self.material_base_2,
                                                                     self.electrodo, self.geometria,
                                                                     {"pierna": h_min,
                                                                      "largo": self.geometria_params.get("largo", 0),
                                                                      "ancho": self.geometria_params.get("ancho", 0),
                                                                      "radio": self.geometria_params.get("radio", 0)},
                                                                     self.espesor_menor_piezas)

            # Verificar si se presentó la falla por carga estática y obtener valores para informe
            falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_cflex()

            # Mensaje de conclusion de diseño por fatiga
            conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

            if not falla_estatica:
                rediseno_estatica = None
            else:
                # DISEÑO POR CARGA ESTÁTICA
                rediseno_estatica = self.pierna_cflex_estatica()

            # Generar diccionario para informe de resultados del diseño por fatiga
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "b": b,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "momento_flector_alt": round(momento_flector_alt, 2),
            "momento_flector_med": round(momento_flector_med, 2),
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": area_sold,
            "i_sold": i_sold,
            "i_sold_ecuacion": i_sold_ecuacion,
            "i_pieza": i_pieza,
            "i_pieza_ecuacion": i_pieza_ecuacion,
            "c": round(c, 3),
            "c_ecuacion": c_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_primario_alt": tao_primario_alt,
            "tao_primario_med": tao_primario_med,
            "tao_secundario_alt": tao_secundario_alt,
            "tao_secundario_med": tao_secundario_med,
            "tao_alt_sold": tao_alt_sold,
            "tao_med_sold": tao_med_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "h_sold": round(h_sold, 3 if self.sistema_unidades == "Internacional" else 4),
            "sigma_p_alt": sigma_p_alt,
            "sigma_p_med": sigma_p_med,
            "tao_p_alt": tao_p_alt,
            "tao_p_med": tao_p_med,
            "sigma_t_alt": sigma_t_alt,
            "sigma_t_med": sigma_t_med,
            "tao_t_alt": tao_t_alt,
            "tao_t_med": tao_t_med,
            "sigma_p_von_misses_alt": sigma_p_von_misses_alt,
            "sigma_p_von_misses_med": sigma_p_von_misses_med,
            "sigma_t_von_misses_alt": sigma_t_von_misses_alt,
            "sigma_t_von_misses_med": sigma_t_von_misses_med,
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "h_pieza1": round(h_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_pieza2": round(h_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min": h_min,
            "conclusion_h_min": conclusion_h_min,
            "verificacion_h_max": verificacion_h_max,
            "verificacion_h_min": verificacion_h_min,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga de Torsión debido a una fuerza excéntrica
    def pierna_ctor(self):

        # DISEÑO POR FATIGA

        # Obtener cargas max y min, y el brazo (b)
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]
        b = self.carga["b"]
        momento_torsor_max, momento_torsor_min = analisis.calcular_momento_max_y_min(f_max, f_min, b)

        # Calcular cargas alternantes y medias
        f_alt, f_med = analisis.calcular_carga_alt_y_med(f_max, f_min)
        momento_torsor_alt, momento_torsor_med = analisis.calcular_carga_alt_y_med(momento_torsor_max,
                                                                                   momento_torsor_min)

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Intermedia": 1.5, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Cálculo de parámetros geométricos
        area_sold = self.calcular_area_sold()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar_sold()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion

        if self.geometria == "ocho":
            ry, rx, ry_rx_ecuacion = self.obtener_rx_ry()
            ry_ecuacion, rx_ecuacion = ry_rx_ecuacion

        # Determinar h en la soldadura

        # Calcular esfuerzo cortante primario alternante y medio en la soldadura (En función de h)
        tao_primario_alt = kfs * 1.414 * f_alt / area_sold
        tao_primario_med = 1.414 * f_med / area_sold

        # Calcular las componentes x e y del esfuerzo cortante secundadario alternante en la soldadura (En función de h)
        tao_secundario_alt_x = kfs * momento_torsor_alt * ry / j_sold
        tao_secundario_alt_y = kfs * momento_torsor_alt * rx / j_sold

        # Calcular las componentes x e y del esfuerzo cortante secundario medio en la soldadura (En función de h)
        tao_secundario_med_x = momento_torsor_med * ry / j_sold
        tao_secundario_med_y = momento_torsor_med * rx / j_sold

        # Calcular las componentes x e y del esfuerzo cortante alternante (En función de h)
        tao_alt_x = tao_secundario_alt_x
        tao_alt_y = tao_primario_alt + tao_secundario_alt_y

        # Calcular las componentes x e y del esfuerzo cortante medio (En función de h)
        tao_med_x = tao_secundario_med_x
        tao_med_y = tao_primario_med + tao_secundario_med_y

        # Calcular el esfuerzo cortante resultante alternante y medio en la soldadura (En función de h)
        tao_alt_sold = sqrt(tao_alt_x ** 2 + tao_alt_y ** 2)
        tao_med_sold = sqrt(tao_med_x ** 2 + tao_med_y ** 2)

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_sold = 3.33
        h_sold = despejar_pierna_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar h en la pieza 1 (Pieza P)

        # Calcular esfuerzo cortante alternante y medio en la pieza 1 (En función de h)
        tao_p_alt = kfs * f_alt / area_sold
        tao_p_med = f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia última al cortante del material base 1
        ssu_pieza1 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_pieza = 2.5
        h_pieza1 = despejar_pierna_ecuacion_gerber(tao_p_alt, tao_p_med, sse_pieza1, ssu_pieza1, self.fd_min_pieza)

        # Determinar h en la pieza 2 (Pieza T)

        # Calcular esfuerzo normal alternante y medio en la pieza 2 (En función de h)
        sigma_t_alt = kfs * f_alt / area_sold
        sigma_t_med = f_med / area_sold

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_pieza = 2.5
        h_pieza2 = despejar_pierna_ecuacion_gerber(sigma_t_alt, sigma_t_med, se_pieza2, sut_pieza2, self.fd_min_pieza)

        # Seleccionar el mayor de los valores para la pierna h obtenidos
        h_min = round(max(h_sold, h_pieza1, h_pieza2), 3 if self.sistema_unidades == "Internacional" else 4)

        # Mensaje con la pierna mínima (hmin) obtenida
        conclusion_h_min = conclusion_pierna_min(self.sistema_unidades, h_min)

        # Verificar que la pierna calculada no exceda el tamaño máximo y generar mensaje sobre la verificacion
        cumple_h_max, verificacion_h_max = self.verificar_tamano_max_pierna(h_min)

        if not cumple_h_max:
            verificacion_h_min = "N/A"
            valores_comprobacion_estatica = None
            rediseno_estatica = None
            conclusion_diseno_fatiga = "N/A"

        else:
            # Si no excede el tamaño máximo, se verifica que no esté por debajo del tamaño mínimo
            verificacion_h_min = self.verificar_tamano_minimo_pierna(h_min)

            # Si es neceario, ajustar el valor de h_min según la especificación de la AWS
            h_min = self.ajustar_tamano_pierna_aws(h_min)

            # Analizar por carga estática partiendo del resultado obtenido
            comprobacion_estatica = analisis.AnalisisSoldaduraFilete(self.sistema_unidades, self.tipo_union, self.carga,
                                                                     self.material_base_1, self.material_base_2,
                                                                     self.electrodo, self.geometria,
                                                                     {"pierna": h_min,
                                                                      "largo": self.geometria_params.get("largo", 0),
                                                                      "ancho": self.geometria_params.get("ancho", 0),
                                                                      "radio": self.geometria_params.get("radio", 0)},
                                                                     self.espesor_menor_piezas)

            # Verificar si se presentó la falla por carga estática y obtener valores para informe
            falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_ctor()

            # Mensaje de conclusion de diseño por fatiga
            conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

            if not falla_estatica:
                rediseno_estatica = None
            else:
                # DISEÑO POR CARGA ESTÁTICA
                rediseno_estatica = self.pierna_ctor_estatica()

        # Generar diccionario para informe de resultados del diseño por fatiga
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "b": b,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "momento_torsor_alt": round(momento_torsor_alt, 2),
            "momento_torsor_med": round(momento_torsor_med, 2),
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": area_sold,
            "j_sold": j_sold,
            "j_sold_ecuacion": j_sold_ecuacion,
            "rx": round(rx, 3),
            "ry": round(ry, 3),
            "rx_ecuacion": rx_ecuacion,
            "ry_ecuacion": ry_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_primario_alt": tao_primario_alt,
            "tao_primario_med": tao_primario_med,
            "tao_secundario_alt_x": tao_secundario_alt_x,
            "tao_secundario_alt_y": tao_secundario_alt_y,
            "tao_secundario_med_x": tao_secundario_med_x,
            "tao_secundario_med_y": tao_secundario_med_y,
            "tao_alt_x": tao_alt_x,
            "tao_alt_y": tao_alt_y,
            "tao_med_x": tao_med_x,
            "tao_med_y": tao_med_y,
            "tao_alt_sold": tao_alt_sold,
            "tao_med_sold": tao_med_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "h_sold": round(h_sold, 3),
            "tao_p_alt": tao_p_alt,
            "tao_p_med": tao_p_med,
            "sigma_t_alt": sigma_t_alt,
            "sigma_t_med": sigma_t_med,
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "h_pieza1": round(h_pieza1, 3),
            "h_pieza2": round(h_pieza2, 3),
            "h_min": h_min,
            "conclusion_h_min": conclusion_h_min,
            "verificacion_h_max": verificacion_h_max,
            "verificacion_h_min": verificacion_h_min,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga Combinada debido a una fuerza excéntrica
    def pierna_ccomb(self):

        # DISEÑO POR FATIGA

        # Obtener cargas max y min, el brazo longitudinal (bl) y el brazo transversal (bt)
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]
        bl = self.carga["bl"]
        bt = self.carga["bt"]
        momento_flector_max, momento_flector_min = analisis.calcular_momento_max_y_min(f_max, f_min, bl)
        momento_torsor_max, momento_torsor_min = analisis.calcular_momento_max_y_min(f_max, f_min, bt)

        # Calcular cargas alternantes y medias
        f_alt, f_med = analisis.calcular_carga_alt_y_med(f_max, f_min)
        momento_flector_alt, momento_flector_med = analisis.calcular_carga_alt_y_med(momento_flector_max,
                                                                                     momento_flector_min)
        momento_torsor_alt, momento_torsor_med = analisis.calcular_carga_alt_y_med(momento_torsor_max,
                                                                                   momento_torsor_min)

        # Factor de concentración de esfuerzo reducido, Kfs (Se considera carga transversal y unión T)
        kfs = 2

        # Cálculo de parámetros geométricos
        area_sold = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia_sold()
        i_pieza, i_pieza_ecuacion = self.calcular_momento_inercia_pieza()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar_sold()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        c = ry
        c_ecuacion = rx_ry_ecuacion[1]

        # Determinar h en la soldadura

        # Calcular esfuerzo cortante primario alternante y medio en la soldadura (En función de h)
        tao_primario_alt = kfs * 1.414 * f_alt / area_sold
        tao_primario_med = 1.414 * f_med / area_sold

        # Calcular esfuerzo cortante secundario alternante y medio en la soldadura (En función de h)
        tao_secundario_alt = kfs * momento_flector_alt * c / i_sold
        tao_secundario_med = momento_flector_med * c / i_sold

        # Calcular las componentes x e y del esfuerzo cortante terciario alternante en la soldadura (En función de h)
        tao_terciario_alt_x = kfs * momento_torsor_alt * ry / j_sold
        tao_terciario_alt_y = kfs * momento_torsor_alt * rx / j_sold

        # Calcular las componentes x e y del esfuerzo cortante terciario medio en la soldadura (En función de h)
        tao_terciario_med_x = momento_torsor_med * ry / j_sold
        tao_terciario_med_y = momento_torsor_med * rx / j_sold

        # Calcular las componentes X, Y y Z del esfuerzo cortante alternante (En función de h)
        tao_alt_x = tao_terciario_alt_x
        tao_alt_y = tao_primario_alt + tao_terciario_alt_y
        tao_alt_z = tao_secundario_alt

        # Calcular las componentes X, Y y Z del esfuerzo cortante medio (En función de h)
        tao_med_x = tao_terciario_med_x
        tao_med_y = tao_primario_med + tao_terciario_med_y
        tao_med_z = tao_secundario_med

        # Calcular el esfuerzo cortante resultante alternante y medio en la soldadura (En función de h)
        tao_alt_sold = sqrt(tao_alt_x ** 2 + tao_alt_y ** 2 + tao_alt_z ** 2)
        tao_med_sold = sqrt(tao_med_x ** 2 + tao_med_y ** 2 + tao_med_z ** 2)

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_sold = 3.33
        h_sold = despejar_pierna_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar h en la pieza 1 (Pieza P)

        # Calcular esfuerzo normal alternante y medio en la pieza 1 (En función de h)
        sigma_p_alt = kfs * momento_flector_alt * c / i_pieza
        sigma_p_med = momento_flector_med * c / i_pieza

        # Calcular esfuerzo cortante alternante y medio en la pieza 1 (En función de h)
        tao_p_alt = kfs * f_alt / area_sold
        tao_p_med = f_med / area_sold

        # Calcular el esfuerzo de Von Misses alternante y medio en la pieza 1 (En función de h)
        sigma_p_von_misses_alt = sqrt(sigma_p_alt ** 2 + 3 * tao_p_alt ** 2)
        sigma_p_von_misses_med = sqrt(sigma_p_med ** 2 + 3 * tao_p_med ** 2)

        # Calcular la resistencia a la fatiga del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_pieza = 2.5
        h_pieza1 = despejar_pierna_ecuacion_gerber(sigma_p_von_misses_alt, sigma_p_von_misses_med, se_pieza1,
                                                   sut_pieza1, self.fd_min_pieza)

        # Determinar h en la pieza 2 (Pieza T)

        # Calcular esfuerzo normal alternante y medio en la pieza 2 (En función de h)
        sigma_t_alt = tao_p_alt
        sigma_t_med = tao_p_med

        # Calcular esfuerzo cortante alternante y medio en la pieza 2 (En función de h)
        tao_t_alt = sigma_p_alt
        tao_t_med = sigma_p_med

        # Calcular el esfuerzo de Von Misses alternante y medio en la pieza 2 (En función de h)
        sigma_t_von_misses_alt = sqrt(sigma_t_alt ** 2 + 3 * tao_t_alt ** 2)
        sigma_t_von_misses_med = sqrt(sigma_t_med ** 2 + 3 * tao_t_med ** 2)

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar la pierna (h) de la ecuación de Gerber para FDmin_pieza = 2.5
        h_pieza2 = despejar_pierna_ecuacion_gerber(sigma_t_von_misses_alt, sigma_t_von_misses_med, se_pieza2,
                                                   sut_pieza2, self.fd_min_pieza)

        # Seleccionar el mayor de los valores para la pierna h obtenidos
        h_min = round(max(h_sold, h_pieza1, h_pieza2), 3 if self.sistema_unidades == "Internacional" else 4)

        # Mensaje con la pierna mínima (hmin) obtenida
        conclusion_h_min = conclusion_pierna_min(self.sistema_unidades, h_min)

        # Verificar que la pierna calculada no exceda el tamaño máximo y generar mensaje sobre la verificacion
        cumple_h_max, verificacion_h_max = self.verificar_tamano_max_pierna(h_min)

        if not cumple_h_max:
            verificacion_h_min = "N/A"
            valores_comprobacion_estatica = None
            rediseno_estatica = None
            conclusion_diseno_fatiga = "N/A"

        else:
            # Si no excede el tamaño máximo, se verifica que no esté por debajo del tamaño mínimo
            verificacion_h_min = self.verificar_tamano_minimo_pierna(h_min)

            # Si es neceario, ajustar el valor de h_min según la especificación de la AWS
            h_min = self.ajustar_tamano_pierna_aws(h_min)

            # Analizar por carga estática partiendo del resultado obtenido
            comprobacion_estatica = analisis.AnalisisSoldaduraFilete(self.sistema_unidades, self.tipo_union, self.carga,
                                                                     self.material_base_1, self.material_base_2,
                                                                     self.electrodo, self.geometria,
                                                                     {"pierna": h_min,
                                                                      "largo": self.geometria_params.get("largo", 0),
                                                                      "ancho": self.geometria_params.get("ancho", 0),
                                                                      "radio": self.geometria_params.get("radio", 0)},
                                                                     self.espesor_menor_piezas)

            # Verificar si se presentó la falla por carga estática y obtener valores para informe
            falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_ccomb()

            # Mensaje de conclusion de diseño por fatiga
            conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

            if not falla_estatica:
                rediseno_estatica = None
            else:
                # DISEÑO POR CARGA ESTÁTICA
                rediseno_estatica = self.pierna_ccomb_estatica()

        # Generar diccionario para informe de resultados del diseño por fatiga
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "bl": bl,
            "bt": bt,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "momento_flector_alt": round(momento_flector_alt, 2),
            "momento_flector_med": round(momento_flector_med, 2),
            "momento_torsor_alt": round(momento_torsor_alt, 2),
            "momento_torsor_med": round(momento_torsor_med, 2),
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": area_sold,
            "i_sold": i_sold,
            "i_sold_ecuacion": i_sold_ecuacion,
            "i_pieza": i_pieza,
            "i_pieza_ecuacion": i_pieza_ecuacion,
            "j_sold": j_sold,
            "j_sold_ecuacion": j_sold_ecuacion,
            "rx": round(rx, 3),
            "ry": round(ry, 3),
            "rx_ecuacion": rx_ry_ecuacion[0],
            "ry_ecuacion": rx_ry_ecuacion[1],
            "c": round(c, 3),
            "c_ecuacion": c_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_primario_alt": tao_primario_alt,
            "tao_primario_med": tao_primario_med,
            "tao_secundario_alt": tao_secundario_alt,
            "tao_secundario_med": tao_secundario_med,
            "tao_terciario_alt_x": tao_terciario_alt_x,
            "tao_terciario_alt_y": tao_terciario_alt_y,
            "tao_terciario_med_x": tao_terciario_med_x,
            "tao_terciario_med_y": tao_terciario_med_y,
            "tao_alt_x": tao_alt_x,
            "tao_alt_y": tao_alt_y,
            "tao_alt_z": tao_alt_z,
            "tao_med_x": tao_med_x,
            "tao_med_y": tao_med_y,
            "tao_med_z": tao_med_z,
            "tao_alt_sold": tao_alt_sold,
            "tao_med_sold": tao_med_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "h_sold": round(h_sold, 3),
            "sigma_p_alt": sigma_p_alt,
            "sigma_p_med": sigma_p_med,
            "tao_p_alt": tao_p_alt,
            "tao_p_med": tao_p_med,
            "sigma_t_alt": sigma_t_alt,
            "sigma_t_med": sigma_t_med,
            "tao_t_alt": tao_t_alt,
            "tao_t_med": tao_t_med,
            "sigma_p_von_misses_alt": sigma_p_von_misses_alt,
            "sigma_p_von_misses_med": sigma_p_von_misses_med,
            "sigma_t_von_misses_alt": sigma_t_von_misses_alt,
            "sigma_t_von_misses_med": sigma_t_von_misses_med,
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "h_pieza1": round(h_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_pieza2": round(h_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min": h_min,
            "conclusion_h_min": conclusion_h_min,
            "verificacion_h_max": verificacion_h_max,
            "verificacion_h_min": verificacion_h_min,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    ###################################################################################################################
    # DISEÑO POR CARGA ESTÁTICA

    # Carga Paralela
    def pierna_cp_estatica(self):

        f_max = self.carga["Fmax"]

        # Calcular área de la soldadura
        area_sold = self.calcular_area_sold()

        # SOLDADURA

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)

        # Calcular esfuerzo applicado en la soldadura
        tao_sold = 1.414 * f_max / area_sold

        # Despejar hmin_sold de la ecuación de FD
        h_min_sold = despejar_h_min_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao_sold)

        # PIEZA 1

        # Calcular la resistencia a la fluencia al cortante de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1

        # Calcular esfuerzo aplicado en la pieza1
        tao_pieza1 = f_max / area_sold

        # Despejar hmin_pieza1 de la ecuación de FD
        h_min_pieza1 = despejar_h_min_fd_estatica(self.fd_min_pieza, ssy_pieza1, tao_pieza1)

        # PIEZA 2

        # Calcular la resistencia a la fluencia al cortante de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]
        ssy_pieza2 = 0.577 * sy_pieza2

        # Calcular esfuerzo aplicado en la pieza2
        tao_pieza2 = f_max / area_sold

        # Despejar hmin_pieza2 de la ecuación de FD
        h_min_pieza2 = despejar_h_min_fd_estatica(self.fd_min_pieza, ssy_pieza2, tao_pieza2)

        # Seleccionar el mayor de los valores para la pierna h obtenidos por estática
        h_min_estatica = round(max(h_min_sold, h_min_pieza1, h_min_pieza2),
                               3 if self.sistema_unidades == "Internacional" else 4)

        # Verificar que la pierna calculada no exceda el tamaño máximo y generar mensaje sobre la verificacion
        cumple_h_max, conclusion_h_max = self.verificar_tamano_max_pierna(h_min_estatica)

        if cumple_h_max:
            # Si no excede el tamaño máximo, se verifica que no esté por debajo del tamaño mínimo
            verificacion_h_min = self.verificar_tamano_minimo_pierna(h_min_estatica)
        else:
            verificacion_h_min = "N/A"

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "tipo_union": self.tipo_union,
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": area_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "tao_sold": tao_sold,
            "h_min_sold": round(h_min_sold, 3 if self.sistema_unidades == "Internacional" else 4),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "ssy_pieza1": round(ssy_pieza1, 2),
            "ssy_pieza2": round(ssy_pieza2, 2),
            "tao_pieza1": tao_pieza1,
            "tao_pieza2": tao_pieza2,
            "h_min_pieza1": round(h_min_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min_pieza2": round(h_min_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min": h_min_estatica,
            "verificacion_h_max": conclusion_h_max,
            "verificacion_h_min": verificacion_h_min,
        }

        return resultados

    # Carga Transversal
    def pierna_ctrans_estatica(self):

        f_max = self.carga["Fmax"]

        # Calcular área de la soldadura
        area_sold = self.calcular_area_sold()

        # SOLDADURA

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)

        # Calcular esfuerzo applicado en la soldadura
        tao_sold = 1.414 * f_max / area_sold

        # Despejar hmin_sold de la ecuación de FD
        h_min_sold = despejar_h_min_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao_sold)

        # PIEZA 1

        # Calcular la resistencia a la fluencia al cortante de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1

        # Calcular esfuerzo aplicado en la pieza1
        tao_pieza1 = f_max / area_sold

        # Despejar hmin_pieza1 de la ecuación de FD
        h_min_pieza1 = despejar_h_min_fd_estatica(self.fd_min_pieza, ssy_pieza1, tao_pieza1)

        # PIEZA 2

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Calcular esfuerzo aplicado en la pieza2
        sigma_pieza2 = f_max / area_sold

        # Despejar hmin_pieza2 de la ecuación de FD
        h_min_pieza2 = despejar_h_min_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma_pieza2)

        # Seleccionar el mayor de los valores para la pierna h obtenidos por estática
        h_min_estatica = round(max(h_min_sold, h_min_pieza1, h_min_pieza2),
                               3 if self.sistema_unidades == "Internacional" else 4)

        # Verificar que la pierna calculada no exceda el tamaño máximo y generar mensaje sobre la verificacion
        cumple_h_max, conclusion_h_max = self.verificar_tamano_max_pierna(h_min_estatica)

        if cumple_h_max:
            # Si no excede el tamaño máximo, se verifica que no esté por debajo del tamaño mínimo
            verificacion_h_min = self.verificar_tamano_minimo_pierna(h_min_estatica)
        else:
            verificacion_h_min = "N/A"

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "tipo_union": self.tipo_union,
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": area_sold,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "tao_sold": tao_sold,
            "h_min_sold": round(h_min_sold, 3 if self.sistema_unidades == "Internacional" else 4),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "ssy_pieza1": round(ssy_pieza1, 2),
            "tao_pieza1": tao_pieza1,
            "sigma_pieza2": sigma_pieza2,
            "h_min_pieza1": round(h_min_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min_pieza2": round(h_min_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min": h_min_estatica,
            "verificacion_h_max": conclusion_h_max,
            "verificacion_h_min": verificacion_h_min,
        }

        return resultados

    # Carga de Flexión debido a una fuerza excéntrica
    def pierna_cflex_estatica(self):

        f_max = self.carga["Fmax"]
        b = self.carga["b"]

        # Cálculo de parámetros geométricos
        area_sold = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia_sold()
        i_pieza, i_pieza_ecuacion = self.calcular_momento_inercia_pieza()
        c = self.obtener_rx_ry()[1]
        c_ecuacion = self.obtener_rx_ry()[2][1]

        # Cálculo del momento flector estático
        momento_flector = f_max * b

        # SOLDADURA

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)

        # Calcular esfuerzo cortante primario (En función de F)
        tao_primario = 1.414 * f_max / area_sold

        # Calcular esfuerzo cortante secundario (En función de F)
        tao_secundario = momento_flector * c / i_sold

        # Calcular esfuerzo cortante resultante en la soldadura (En función de F)
        tao_sold = sqrt(tao_primario ** 2 + tao_secundario ** 2)

        # Despejar hmin_sold de la ecuación de FD
        h_min_sold = despejar_h_min_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao_sold)

        # PIEZA 1 (Pieza P)

        # Obtener la resistencia a la fluencia de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]

        # Calcular esfuerzo normal y esfuerzo cortante aplicado en la pieza 1 (En función de h)
        sigma_p = momento_flector * c / i_pieza
        tao_p = f_max / area_sold

        # Calcular esfuerzo de Von Misses en la pieza 1 (En función de h)
        sigma_von_misses_1 = sqrt(sigma_p ** 2 + 3 * tao_p ** 2)

        # Despejar hmin_pieza1 de la ecuación de FD
        h_min_pieza1 = despejar_h_min_fd_estatica(self.fd_min_pieza, sy_pieza1, sigma_von_misses_1)

        # PIEZA 2 (Pieza T)

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Calcular esfuerzo normal y esfuerzo cortante aplicado en la pieza 2
        sigma_t = f_max / area_sold
        tao_t = momento_flector * c / i_pieza

        # Calcular esfuerzo de Von Misses en la pieza 2 (En función de F)
        sigma_von_misses_2 = sqrt(sigma_t ** 2 + 3 * tao_t ** 2)

        # Despejar hmin_pieza2 de la ecuación de FD
        h_min_pieza2 = despejar_h_min_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma_von_misses_2)

        # Seleccionar el mayor de los valores para la pierna h obtenidos por estática
        h_min_estatica = round(max(h_min_sold, h_min_pieza1, h_min_pieza2),
                               3 if self.sistema_unidades == "Internacional" else 4)

        # Verificar que la pierna calculada no exceda el tamaño máximo y generar mensaje sobre la verificacion
        cumple_h_max, conclusion_h_max = self.verificar_tamano_max_pierna(h_min_estatica)

        if cumple_h_max:
            # Si no excede el tamaño máximo, se verifica que no esté por debajo del tamaño mínimo
            verificacion_h_min = self.verificar_tamano_minimo_pierna(h_min_estatica)
        else:
            verificacion_h_min = "N/A"

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "b": b,
            "momento_flector": round(momento_flector, 2),
            "tipo_union": self.tipo_union,
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": area_sold,
            "i_sold": i_sold,
            "i_sold_ecuacion": i_sold_ecuacion,
            "i_pieza": i_pieza,
            "i_pieza_ecuacion": i_pieza_ecuacion,
            "c": round(c, 3),
            "c_ecuacion": c_ecuacion,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "tao_primario": tao_primario,
            "tao_secundario": tao_secundario,
            "tao_sold": tao_sold,
            "h_min_sold": round(h_min_sold, 3 if self.sistema_unidades == "Internacional" else 4),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sigma_p": sigma_p,
            "tao_p": tao_p,
            "sigma_t": sigma_t,
            "tao_t": tao_t,
            "sigma_von_misses_1": sigma_von_misses_1,
            "sigma_von_misses_2": sigma_von_misses_2,
            "h_min_pieza1": round(h_min_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min_pieza2": round(h_min_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min": h_min_estatica,
            "verificacion_h_max": conclusion_h_max,
            "verificacion_h_min": verificacion_h_min,
        }

        return resultados

    # Carga de Torsión debido a una fuerza excéntrica
    def pierna_ctor_estatica(self):

        f_max = self.carga["Fmax"]
        b = self.carga["b"]

        # Cálculo de parámetros geométricos
        area_sold = self.calcular_area_sold()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar_sold()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion

        if self.geometria == "ocho":
            ry, rx, ry_rx_ecuacion = self.obtener_rx_ry()
            ry_ecuacion, rx_ecuacion = ry_rx_ecuacion

        # Calculo del momento flector estático
        momento_torsor = f_max * b

        # SOLDADURA

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)

        # Calcular esfuerzo cortante primario (En función de h)
        tao_primario = 1.414 * f_max / area_sold

        # Calcular componentes x e y del esfuerzo cortante secundario
        tao_secundario_x = momento_torsor * ry / j_sold
        tao_secundario_y = momento_torsor * rx / j_sold

        # Calcular componentes x e y del esfuerzo cortante
        tao_x = tao_secundario_x
        tao_y = tao_primario + tao_secundario_y

        # Calcular esfuerzo cortante resultante en la soldadura (En función de h)
        tao_sold = sqrt(tao_x ** 2 + tao_y ** 2)

        # Despejar hmin_sold de la ecuación de FD
        h_min_sold = despejar_h_min_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao_sold)

        # PIEZA 1 (Pieza P)

        # Calcular la resistencia a la fluencia al cortante de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1

        # Calcular esfuerzo cortante aplicado en la pieza1 (En función de h)
        tao_p = f_max / area_sold

        # Despejar hmin_pieza1 de la ecuación de FD
        h_min_pieza1 = despejar_h_min_fd_estatica(self.fd_min_pieza, ssy_pieza1, tao_p)

        # PIEZA 2 (Pieza T)

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Calcular esfuerzo normal aplicado en la pieza 2 (En función de h)
        sigma_t = f_max / area_sold

        # Despejar hmin_pieza2 de la ecuación de FD
        h_min_pieza2 = despejar_h_min_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma_t)

        # Seleccionar el mayor de los valores para la pierna h obtenidos por estática
        h_min_estatica = round(max(h_min_sold, h_min_pieza1, h_min_pieza2),
                               3 if self.sistema_unidades == "Internacional" else 4)

        # Verificar que la pierna calculada no exceda el tamaño máximo y generar mensaje sobre la verificacion
        cumple_h_max, conclusion_h_max = self.verificar_tamano_max_pierna(h_min_estatica)

        if cumple_h_max:
            # Si no excede el tamaño máximo, se verifica que no esté por debajo del tamaño mínimo
            verificacion_h_min = self.verificar_tamano_minimo_pierna(h_min_estatica)
        else:
            verificacion_h_min = "N/A"

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "b": b,
            "momento_torsor": round(momento_torsor, 2),
            "tipo_union": self.tipo_union,
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": area_sold,
            "j_sold": j_sold,
            "j_sold_ecuacion": j_sold_ecuacion,
            "rx": round(rx, 3),
            "ry": round(ry, 3),
            "rx_ecuacion": rx_ecuacion,
            "ry_ecuacion": ry_ecuacion,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "tao_primario": tao_primario,
            "tao_secundario_x": tao_secundario_x,
            "tao_secundario_y": tao_secundario_y,
            "tao_x": tao_x,
            "tao_y": tao_y,
            "tao_sold": tao_sold,
            "h_min_sold": round(h_min_sold, 3 if self.sistema_unidades == "Internacional" else 4),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "ssy_pieza1": ssy_pieza1,
            "tao_p": tao_p,
            "sigma_t": sigma_t,
            "h_min_pieza1": round(h_min_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min_pieza2": round(h_min_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min": h_min_estatica,
            "verificacion_h_max": conclusion_h_max,
            "verificacion_h_min": verificacion_h_min,
        }

        return resultados

    # Carga Combinada debido a una fuerza excéntrica
    def pierna_ccomb_estatica(self):

        f_max = self.carga["Fmax"]
        bl = self.carga["bl"]
        bt = self.carga["bt"]

        # Cálculo de parámetros geométricos
        area_sold = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia_sold()
        i_pieza, i_pieza_ecuacion = self.calcular_momento_inercia_pieza()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar_sold()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        c = ry
        c_ecuacion = rx_ry_ecuacion[1]

        # Calculo del momento flector y mommento torsor estático
        momento_flector = f_max * bl
        momento_torsor = f_max * bt

        # SOLDADURA

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)

        # Calcular esfuerzo cortante primario (En función de h)
        tao_primario = 1.414 * f_max / area_sold

        # Calcular esfuerzo cortante secundario (En función de h)
        tao_secundario = momento_flector * c / i_sold

        # Calcular componentes x e y del esfuerzo cortante terciario (En función de h)
        tao_terciario_x = momento_torsor * ry / j_sold
        tao_terciario_y = momento_torsor * rx / j_sold

        # Calcular componentes X, Y y Z del esfuerzo cortante (En función de h)
        tao_x = tao_terciario_x
        tao_y = tao_primario + tao_terciario_y
        tao_z = tao_secundario

        # Calcular esfuerzo cortante resultante en la soldadura (En función de h)
        tao_sold = sqrt(tao_x ** 2 + tao_y ** 2 + tao_z ** 2)

        # Despejar hmin_sold de la ecuación de FD
        h_min_sold = despejar_h_min_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao_sold)

        # PIEZA 1 (Pieza P)

        # Obtener la resistencia a la fluencia de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]

        # Calcular esfuerzo normal y esfuerzo cortante aplicado en la pieza 1 (En función de h)
        sigma_p = momento_flector * c / i_pieza
        tao_p = f_max / area_sold

        # Calcular esfuerzo de Von Misses en la pieza 1 (En función de h)
        sigma_von_misses_1 = sqrt(sigma_p ** 2 + 3 * tao_p ** 2)

        # Despejar hmin_pieza1 de la ecuación de FD
        h_min_pieza1 = despejar_h_min_fd_estatica(self.fd_min_pieza, sy_pieza1, sigma_von_misses_1)

        # PIEZA 2 (Pieza T)

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Calcular esfuerzo normal y esfuerzo cortante aplicado en la pieza 2
        sigma_t = f_max / area_sold
        tao_t = momento_flector * c / i_pieza

        # Calcular esfuerzo de Von Misses en la pieza 2 (En función de F)
        sigma_von_misses_2 = sqrt(sigma_t ** 2 + 3 * tao_t ** 2)

        # Despejar hmin_pieza2 de la ecuación de FD
        h_min_pieza2 = despejar_h_min_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma_von_misses_2)

        # Seleccionar el mayor de los valores para la pierna h obtenidos por estática
        h_min_estatica = round(max(h_min_sold, h_min_pieza1, h_min_pieza2),
                               3 if self.sistema_unidades == "Internacional" else 4)

        # Redondear el valor de h a 3 decimales para mostrar en pantalla
        resultado_h = round(h_min_estatica, 3)

        # Verificar que la pierna calculada no exceda el tamaño máximo y generar mensaje sobre la verificacion
        cumple_h_max, conclusion_h_max = self.verificar_tamano_max_pierna(resultado_h)

        if cumple_h_max:
            # Si no excede el tamaño máximo, se verifica que no esté por debajo del tamaño mínimo
            verificacion_h_min = self.verificar_tamano_minimo_pierna(resultado_h)
        else:
            verificacion_h_min = "N/A"

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "bl": bl,
            "bt": bt,
            "momento_flector": round(momento_flector, 2),
            "momento_torsor": round(momento_torsor, 2),
            "tipo_union": self.tipo_union,
            "largo": self.geometria_params["largo"],
            "ancho": self.geometria_params["ancho"],
            "radio": self.geometria_params["radio"],
            "espesor_menor_piezas": self.espesor_menor_piezas,
            "longitud_total": round(self.calcular_longitud_total()[0], 2),
            "lt_ecuacion": self.calcular_longitud_total()[1],
            "area_sold": area_sold,
            "i_sold": i_sold,
            "i_sold_ecuacion": i_sold_ecuacion,
            "i_pieza": i_pieza,
            "i_pieza_ecuacion": i_pieza_ecuacion,
            "j_sold": j_sold,
            "j_sold_ecuacion": j_sold_ecuacion,
            "rx": round(rx, 3),
            "ry": round(ry, 3),
            "rx_ecuacion": rx_ry_ecuacion[0],
            "ry_ecuacion": rx_ry_ecuacion[1],
            "c": round(c, 3),
            "c_ecuacion": c_ecuacion,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "tao_primario": tao_primario,
            "tao_secundario": tao_secundario,
            "tao_terciario_x": tao_terciario_x,
            "tao_terciario_y": tao_terciario_y,
            "tao_x": tao_x,
            "tao_y": tao_y,
            "tao_z": tao_z,
            "tao_sold": tao_sold,
            "h_min_sold": round(h_min_sold, 3 if self.sistema_unidades == "Internacional" else 4),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sigma_p": sigma_p,
            "tao_p": tao_p,
            "sigma_t": sigma_t,
            "tao_t": tao_t,
            "sigma_von_misses_1": sigma_von_misses_1,
            "sigma_von_misses_2": sigma_von_misses_2,
            "h_min_pieza1": round(h_min_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min_pieza2": round(h_min_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "h_min": resultado_h,
            "verificacion_h_max": conclusion_h_max,
            "verificacion_h_min": verificacion_h_min,
        }

        return resultados


#######################################################################################################################
# SOLDADURA DE RANURA

# Clase para el cálculo de la carga permisible en la junta
class DisenoCargaPermisibleRanura:
    # Factores de diseño mínimo
    fd_min_sold = 3.33
    fd_min_pieza = 2.5

    def __init__(self, sistema_unidades, tipo_union, relacion_cargas, brazo, material_base_1, material_base_2,
                 electrodo, geometria, geometria_params):
        self.sistema_unidades = sistema_unidades
        self.tipo_union = tipo_union
        self.relacion_cargas = relacion_cargas
        self.brazo = brazo
        self.material_base_1 = material_base_1
        self.material_base_2 = material_base_2
        self.electrodo = electrodo
        self.geometria = geometria
        self.geometria_params = geometria_params

    ###################################################################################################################
    # GEOMETRIA

    # Calcular el área de la garganta de la soldadura
    def calcular_area_sold(self):
        t = self.geometria_params.get("espesor", 0)
        l = self.geometria_params.get("largo", 0)
        r_ext = self.geometria_params.get("radio exterior", 0)

        if r_ext > 0:
            r_int = r_ext - t
        else:
            r_int = 0

        areas_geometrias = {
            "uno": (l * t),
            "dos": (l * t),
            "tres": pi * (r_ext ** 2 - r_int ** 2)
        }

        areas_formulas = {
            "uno": "l * t",
            "dos": "l * t",
            "tres": "pi * ((r ext)^2 - (r int)^2)"
        }

        area_sold = areas_geometrias.get(self.geometria, 0)
        area_sold_ecuacion = areas_formulas[self.geometria]

        if self.geometria == "tres" and r_ext <= t:
            area_sold = 1 / 0

        return area_sold, area_sold_ecuacion

    # Calcular el momento de inercia
    def calcular_momento_inercia(self):
        t = self.geometria_params.get("espesor", 0)
        l = self.geometria_params.get("largo", 0)
        r_ext = self.geometria_params.get("radio exterior", 0)

        if r_ext > 0:
            r_int = r_ext - t
        else:
            r_int = 0

        momentos_inercia_geometrias = {
            "uno": (0.0834 * t * l ** 3),
            "dos": (0.0834 * t ** 3 * l),
            "tres": (0.25 * pi * (r_ext ** 4 - r_int ** 4)),
        }

        momentos_inercia_formulas = {
            "uno": "0.0834 * t * l^3",
            "dos": "0.0834 * t^3 * l",
            "tres": "0.25 * pi * ((r ext)^4 - (r int)^4)",
        }

        momento_de_inercia = momentos_inercia_geometrias.get(self.geometria)
        momento_de_inercia_ecuacion = momentos_inercia_formulas[self.geometria]
        return momento_de_inercia, momento_de_inercia_ecuacion

    # Calcular el momento de inercia polar
    def calcular_momento_inercia_polar(self):
        t = self.geometria_params.get("espesor", 0)
        l = self.geometria_params.get("largo", 0)
        r_ext = self.geometria_params.get("radio exterior", 0)

        if r_ext > 0:
            r_int = r_ext - t
        else:
            r_int = 0

        momentos_inercia_polar_geometrias = {
            "uno": (t * l ** 3 / 12),
            "dos": (t * l ** 3 / 12),
            "tres": (0.5 * pi * (r_ext ** 4 - r_int ** 4)),
        }

        momentos_inercia_polar_formulas = {
            "uno": "t * l^3 / 12",
            "dos": "t * l^3 / 12",
            "tres": "0.5 * pi * ((r ext)^4 - (r int)^4)",
        }

        momento_de_inercia_polar = momentos_inercia_polar_geometrias.get(self.geometria)
        momento_de_inercia_polar_ecuacion = momentos_inercia_polar_formulas[self.geometria]
        return momento_de_inercia_polar, momento_de_inercia_polar_ecuacion

    # Obtener las coordenadas del centroide (X barra, Y barra)
    def obtener_coordenadas_centroide(self):
        l = self.geometria_params.get("largo", 0)
        coordenadas_centroide_geometrias = {
            "uno": (0, l / 2),
            "dos": (l / 2, 0),
            "tres": (0, 0)
        }
        x_barra, y_barra = coordenadas_centroide_geometrias.get(self.geometria)
        return x_barra, y_barra

    # Obtener rx y ry para calcular el esfuerzo debido al par torsionante
    def obtener_rx_ry(self):
        t = self.geometria_params.get("espesor", 0)
        l = self.geometria_params.get("largo", 0)
        r_ext = self.geometria_params.get("radio exterior", 0)

        rx_ry_geometrias = {
            "uno": (t / 2, l / 2),
            "dos": (l / 2, t / 2),
            "tres": (0, r_ext),
        }

        rx_ry_formulas = {
            "uno": ("t/2", "l/2"),
            "dos": ("l/2", "t/2"),
            "tres": ("0", "r ext"),
        }
        rx, ry = rx_ry_geometrias.get(self.geometria)
        rx_ry_ecuacion = rx_ry_formulas[self.geometria]
        return rx, ry, rx_ry_ecuacion

    ###################################################################################################################
    # DISEÑO POR FATIGA

    # Carga Paralela
    def carga_permisible_cp(self):

        # DISEÑO POR FATIGA

        # Obtener la relacion Fmax / Fmin
        relacion = self.relacion_cargas

        # Obtener la fuerza alternante y media en funcion de la relacion
        f_alt, f_med = obtener_carga_alt_y_med(relacion)

        # Factor de concentración de esfuerzo reducido, Kfs (Se considera carga paralela con unión tope)
        kfs = 1.2

        # Area de la soldadura
        area_sold, area_sold_ecuacion = self.calcular_area_sold()

        # Obtener esfuerzo cortante alternante y medio (en función de F)
        tao_alt = kfs * f_alt / area_sold
        tao_med = f_med / area_sold

        # Determinar F en la soldadura

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar la carga F = Fmin de la ecuación de Gerber para FDmin_sold = 3.33
        f_sold = despejar_carga_ecuacion_gerber(tao_alt, tao_med, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar F en la pieza 1

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia ultima al cortante del material base 1
        ssu_pieza1 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza1 = despejar_carga_ecuacion_gerber(tao_alt, tao_med, sse_pieza1, ssu_pieza1,
                                                  self.fd_min_pieza)

        # Determinar F en la pieza 2

        # Calcular la resistencia a la fatiga al cortante del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        sse_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular la resistencia ultima al cortante del material base 2
        ssu_pieza2 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza2)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza2 = despejar_carga_ecuacion_gerber(tao_alt, tao_med, sse_pieza2, ssu_pieza2,
                                                  self.fd_min_pieza)

        # Seleccionar el menor de los valores de carga F obtenidos
        f = min(f_sold, f_pieza1, f_pieza2)

        # Obtener el valor de Fmax a partir de F y la relacion Fmax/Fmin
        f_max = relacion * f

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraRanura(self.sistema_unidades, self.tipo_union,
                                                                 {"Fmax": f_max},
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria, self.geometria_params)

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_cp()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.carga_permisible_estatica_cp()

        # Generar diccionario para informe de resultados
        resultados = {
            "relacion_cargas": relacion,
            "f_alt": f_alt,
            "f_med": f_med,
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "area_sold": round(area_sold, 3),
            "area_sold_ecuacion": area_sold_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_alt": tao_alt,
            "tao_med": tao_med,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "f_sold": round(f_sold, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "sse_pieza2": round(sse_pieza2, 2),
            "ssu_pieza2": round(ssu_pieza2, 2),
            "f_pieza1": round(f_pieza1, 2),
            "f_pieza2": round(f_pieza2, 2),
            "f_min": round(f, 2),
            "f_max": round(f_max, 2),
            "conclusion_fperm": conclusion_fperm,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga Transversal
    def carga_permisible_ctrans(self):

        # DISEÑO POR FATIGA

        # Obtener la relacion Fmax / Fmin
        relacion = self.relacion_cargas

        # Obtener la fuerza alternante y media en funcion de la relacion
        f_alt, f_med = obtener_carga_alt_y_med(relacion)

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Tope": 1.2, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Area de la soldadura
        area_sold, area_sold_ecuacion = self.calcular_area_sold()

        # Obtener esfuerzo normal alternante y medio (en función de F)
        sigma_alt = kfs * f_alt / area_sold
        sigma_med = f_med / area_sold

        # Determinar F en la soldadura

        # Calcular la resistencia a la fatiga del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        se_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Despejar la carga F = Fmin de la ecuación de Gerber para FDmin_sold = 3.33
        f_sold = despejar_carga_ecuacion_gerber(sigma_alt, sigma_med, se_sold, sut_sold, self.fd_min_sold)

        # Determinar F en la pieza 1 (Pieza P)

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza1 = despejar_carga_ecuacion_gerber(sigma_alt, sigma_med, se_pieza1, sut_pieza1, self.fd_min_pieza)

        # Determinar F en la pieza 2 (Pieza T)

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza2 = despejar_carga_ecuacion_gerber(sigma_alt, sigma_med, se_pieza2, sut_pieza2, self.fd_min_pieza)

        # Seleccionar el menor de los valores de carga F obtenidos
        f = min(f_sold, f_pieza1, f_pieza2)

        # Obtener el valor de Fmax a partir de F y la relacion Fmax/Fmin
        f_max = relacion * f

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraRanura(self.sistema_unidades, self.tipo_union,
                                                                 {"Fmax": f_max},
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria, self.geometria_params)

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_ctrans()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.carga_permisible_estatica_ctrans()

        # Generar diccionario para informe de resultados
        resultados = {
            "relacion_cargas": relacion,
            "f_alt": f_alt,
            "f_med": f_med,
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "r_ext": self.geometria_params["radio exterior"],
            "area_sold": round(area_sold, 3),
            "area_sold_ecuacion": area_sold_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "sigma_alt": sigma_alt,
            "sigma_med": sigma_med,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "se_sold": round(se_sold, 2),
            "f_sold": round(f_sold, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "f_pieza1": round(f_pieza1, 2),
            "f_pieza2": round(f_pieza2, 2),
            "f_min": round(f, 2),
            "f_max": round(f_max, 2),
            "conclusion_fperm": conclusion_fperm,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga de Flexión debido a una fuerza excéntrica
    def carga_permisible_cflex(self):

        # DISEÑO POR FATIGA

        # Obtener la relacion Fmax / Fmin
        relacion = self.relacion_cargas

        # Obtener el brazo (Distancia desde el pto de aplicación de la fuerza hasta el centroide)
        b = self.brazo

        # Obtener las cargas alternantes y medias en funcion de F
        f_alt, f_med = obtener_carga_alt_y_med(relacion)
        momento_flector_alt = f_alt * b
        momento_flector_med = f_med * b

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Tope": 1.2, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Cálculo de parámetros geométricos
        area_sold, area_sold_ecuacion = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia()
        c = self.obtener_rx_ry()[1]
        c_ecuacion = self.obtener_rx_ry()[2][1]

        # Calcular esfuerzo cortante alternante y medio (En función de F)
        tao_alt = kfs * f_alt / area_sold
        tao_med = f_med / area_sold

        # Calcular esfuerzo normal alternante y medio (En función de F)
        sigma_alt = kfs * momento_flector_alt * c / i_sold
        sigma_med = momento_flector_med * c / i_sold

        # Calcular el esfuerzo de Von Misses alternante y medio (En función de F)
        sigma_von_misses_alt = sqrt(sigma_alt ** 2 + 3 * tao_alt ** 2)
        sigma_von_misses_med = sqrt(sigma_med ** 2 + 3 * tao_med ** 2)

        # Determinar F en la soldadura

        # Calcular la resistencia a la fatiga del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        se_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Despejar la carga F = Fmin de la ecuación de Gerber para FDmin_sold = 3.33
        f_sold = despejar_carga_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_sold, sut_sold,
                                                self.fd_min_sold)

        # Determinar F en la pieza 1 (Pieza P)

        # Calcular la resistencia a la fatiga del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza1 = despejar_carga_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_pieza1, sut_pieza1,
                                                  self.fd_min_pieza)

        # Determinar F en la pieza 2 (Pieza T)

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza2 = despejar_carga_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_pieza2, sut_pieza2,
                                                  self.fd_min_pieza)

        # Seleccionar el menor de los valores de carga F obtenidos
        f = min(f_sold, f_pieza1, f_pieza2)

        # Obtener el valor de Fmax a partir de F y la relacion Fmax/Fmin
        f_max = relacion * f

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraRanura(self.sistema_unidades, self.tipo_union,
                                                                 {"Fmax": f_max, "b": b},
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria,
                                                                 self.geometria_params)

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_cflex()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.carga_permisible_estatica_cflex()

        # Generar diccionario para informe de resultados
        resultados = {
            "relacion_cargas": relacion,
            "b": b,
            "f_alt": f_alt,
            "f_med": f_med,
            "momento_flector_alt": momento_flector_alt,
            "momento_flector_med": momento_flector_med,
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "r_ext": self.geometria_params["radio exterior"],
            "area_sold": round(area_sold, 3),
            "area_sold_ecuacion": area_sold_ecuacion,
            "i_sold": round(i_sold, 2),
            "i_sold_ecuacion": i_sold_ecuacion,
            "c": round(c, 3),
            "c_ecuacion": c_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_alt": tao_alt,
            "tao_med": tao_med,
            "sigma_alt": sigma_alt,
            "sigma_med": sigma_med,
            "sigma_von_misses_alt": sigma_von_misses_alt,
            "sigma_von_misses_med": sigma_von_misses_med,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "se_sold": round(se_sold, 2),
            "f_sold": round(f_sold, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "f_pieza1": round(f_pieza1, 2),
            "f_pieza2": round(f_pieza2, 2),
            "f_min": round(f, 2),
            "f_max": round(f_max, 2),
            "conclusion_fperm": conclusion_fperm,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga de Torsión
    def carga_permisible_ctor(self):

        # DISEÑO POR FATIGA

        # Obtener la relacion Tmax / Tmin
        relacion = self.relacion_cargas

        # Obtener carga alternante y media (En función de T)
        momento_torsor_alt, momento_torsor_med = obtener_torque_alt_y_med(relacion)

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Tope": 1.2, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Cálculo de parámetros geométricos
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion
        r = sqrt(rx ** 2 + ry ** 2)

        # Calcular el esfuerzo cortante resultante alternante y medio (En función de T)
        tao_alt = kfs * momento_torsor_alt * r / j_sold
        tao_med = momento_torsor_med * r / j_sold

        # Determinar T en la soldadura

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar el momento torsor T = Tmin de la ecuación de Gerber para FDmin_sold = 3.33
        momento_torsor_sold = despejar_torque_ecuacion_gerber(tao_alt, tao_med, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar T en la pieza 1

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia última al cortante del material base 1
        ssu_pieza1 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Despejar el momento torsor T = Tmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        momento_torsor_pieza1 = despejar_torque_ecuacion_gerber(tao_alt, tao_med, sse_pieza1, ssu_pieza1,
                                                                self.fd_min_pieza)

        # Determinar T en la pieza 2

        # Calcular la resistencia a la fatiga al cortante del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        sse_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular la resistencia ultima al cortante de la pieza 2
        ssu_pieza2 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza2)

        # Despejar el momento torsor T = Tmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        momento_torsor_pieza2 = despejar_torque_ecuacion_gerber(tao_alt, tao_med, sse_pieza2, ssu_pieza2,
                                                                self.fd_min_pieza)

        # Seleccionar el menor de los valores del momento torsor T = Tmin obtenidos
        momento_torsor = min(momento_torsor_sold, momento_torsor_pieza1, momento_torsor_pieza2)

        # Obtener el valor de Tmax a partir del momento torsor T = Tmin calculado y la relacion Tmax/Tmin
        momento_torsor_max = relacion * momento_torsor

        # Generar mensaje con el torque permisible obtenido
        conclusion_tperm = conclusion_torque_permisible(self.sistema_unidades, momento_torsor_max)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraRanura(self.sistema_unidades, self.tipo_union,
                                                                 {
                                                                     "Tmax": momento_torsor_max / 1000 if self.sistema_unidades == "Internacional" else momento_torsor_max},
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria, self.geometria_params)

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_ctor()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.carga_permisible_estatica_ctor()

        # Generar diccionario para informe de resultados
        resultados = {
            "relacion_cargas": relacion,
            "tipo_union": self.tipo_union,
            "momento_torsor_alt": momento_torsor_alt,
            "momento_torsor_med": momento_torsor_med,
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "r_ext": self.geometria_params["radio exterior"],
            "area_sold": round(self.calcular_area_sold()[0], 3),
            "area_sold_ecuacion": self.calcular_area_sold()[1],
            "j_sold": round(j_sold, 2),
            "j_sold_ecuacion": j_sold_ecuacion,
            "r": round(r, 3),
            "rx_ecuacion": rx_ecuacion,
            "ry_ecuacion": ry_ecuacion,
            "kfs": kfs,
            "tao_alt": tao_alt,
            "tao_med": tao_med,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "t_sold": round(momento_torsor_sold, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "sse_pieza2": round(sse_pieza2, 2),
            "ssu_pieza2": round(ssu_pieza2, 2),
            "t_pieza1": round(momento_torsor_pieza1, 2),
            "t_pieza2": round(momento_torsor_pieza2, 2),
            "t_min": round(momento_torsor, 2),
            "t_max": round(momento_torsor_max, 2),
            "conclusion_tperm": conclusion_tperm,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }
        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga Combinada debido a una carga excétrica
    def carga_permisible_ccomb(self):

        # DISEÑO POR FATIGA

        # Obtener la relacion Fmax / Fmin
        relacion = self.relacion_cargas

        # Obtener bl y bt (Distancia desde el pto de aplicación de la fuerza hasta el centroide, longitudinal y transv)
        bl = self.brazo["bl"]
        bt = self.brazo["bt"]

        # Obtener las cargas alternantes y medias en funcion de F
        f_alt, f_med = obtener_carga_alt_y_med(relacion)
        momento_flector_alt = f_alt * bl
        momento_flector_med = f_med * bl
        momento_torsor_alt = f_alt * bt
        momento_torsor_med = f_med * bt

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Tope": 1.2, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Cálculo de parámetros geométricos
        area_sold, area_sold_ecuacion = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion
        c = ry
        c_ecuacion = ry_ecuacion

        # Calcular esfuerzo cortante primario alternante y medio
        tao_primario_alt = kfs * f_alt / area_sold
        tao_primario_med = f_med / area_sold

        # Calcular las componentes x e y del esfuerzo cortante secundario alternante
        tao_secundario_alt_x = kfs * momento_torsor_alt * ry / j_sold
        tao_secundario_alt_y = kfs * momento_torsor_alt * rx / j_sold

        # Calcular las componentes x e y del esfuerzo cortante secundario medio
        tao_secundario_med_x = momento_torsor_med * ry / j_sold
        tao_secundario_med_y = momento_torsor_med * rx / j_sold

        # Calcular las componentes x e y del esfuerzo cortante alternante
        tao_alt_x = tao_secundario_alt_x
        tao_alt_y = tao_primario_alt + tao_secundario_alt_y

        # Calcular las componentes x e y del esfuerzo cortante medio
        tao_med_x = tao_secundario_med_x
        tao_med_y = tao_primario_med + tao_secundario_med_y

        # Calcular el esfuerzo cortante resultante alternante y medio
        tao_alt = sqrt(tao_alt_x ** 2 + tao_alt_y ** 2)
        tao_med = sqrt(tao_med_x ** 2 + tao_med_y ** 2)

        # Calcular esfuerzo normal alternante y medio
        sigma_alt = kfs * momento_flector_alt * c / i_sold
        sigma_med = momento_flector_med * c / i_sold

        # Calcular el esfuerzo de Von Misses alternante y medio (En función de F)
        sigma_von_misses_alt = sqrt(sigma_alt ** 2 + 3 * tao_alt ** 2)
        sigma_von_misses_med = sqrt(sigma_med ** 2 + 3 * tao_med ** 2)

        # Determinar F en la soldadura

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        se_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Despejar la carga F = Fmin de la ecuación de Gerber para FDmin_sold = 3.33
        f_sold = despejar_carga_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_sold, sut_sold,
                                                self.fd_min_sold)

        # Determinar F en la pieza 1

        # Calcular la resistencia a la fatiga del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza1 = despejar_carga_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_pieza1, sut_pieza1,
                                                  self.fd_min_pieza)

        # Determinar F en la pieza 2

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar la carga F = Fmin de la ecuación de Gerber para un FDmin_pieza = 2.5
        f_pieza2 = despejar_carga_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_pieza2, sut_pieza2,
                                                  self.fd_min_pieza)

        # Seleccionar el menor de los valores de carga F obtenidos
        f = min(f_sold, f_pieza1, f_pieza2)

        # Obtener el valor de Fmax a partir de F y la relacion Fmax/Fmin
        f_max = relacion * f

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraRanura(self.sistema_unidades, self.tipo_union,
                                                                 {"Fmax": f_max, "bl": bl, "bt": bt},
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria, self.geometria_params)

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_ccomb()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.carga_permisible_estatica_ccomb()

        # Generar diccionario para informe de resultados
        resultados = {
            "relacion_cargas": relacion,
            "bl": bl,
            "bt": bt,
            "f_alt": f_alt,
            "f_med": f_med,
            "momento_flector_alt": momento_flector_alt,
            "momento_flector_med": momento_flector_med,
            "momento_torsor_alt": momento_torsor_alt,
            "momento_torsor_med": momento_torsor_med,
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "r_ext": self.geometria_params["radio exterior"],
            "area_sold": round(area_sold, 3),
            "area_sold_ecuacion": area_sold_ecuacion,
            "i_sold": round(i_sold, 2),
            "j_sold": round(j_sold, 2),
            "rx": round(rx, 3),
            "ry": round(ry, 3),
            "c": round(c, 3),
            "i_sold_ecuacion": i_sold_ecuacion,
            "j_sold_ecuacion": j_sold_ecuacion,
            "rx_ecuacion": rx_ecuacion,
            "ry_ecuacion": ry_ecuacion,
            "c_ecuacion": c_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_primario_alt": tao_primario_alt,
            "tao_primario_med": tao_primario_med,
            "tao_secundario_alt_x": tao_secundario_alt_x,
            "tao_secundario_alt_y": tao_secundario_alt_y,
            "tao_secundario_med_x": tao_secundario_med_x,
            "tao_secundario_med_y": tao_secundario_med_y,
            "tao_alt_x": tao_alt_x,
            "tao_alt_y": tao_alt_y,
            "tao_med_x": tao_med_x,
            "tao_med_y": tao_med_y,
            "tao_alt": tao_alt,
            "tao_med": tao_med,
            "sigma_alt": sigma_alt,
            "sigma_med": sigma_med,
            "sigma_von_misses_alt": sigma_von_misses_alt,
            "sigma_von_misses_med": sigma_von_misses_med,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "se_sold": round(se_sold, 2),
            "f_sold": round(f_sold, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "f_pieza1": round(f_pieza1, 2),
            "f_pieza2": round(f_pieza2, 2),
            "f_min": round(f, 2),
            "f_max": round(f_max, 2),
            "conclusion_fperm": conclusion_fperm,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    ###################################################################################################################

    # DISEÑO POR CARGA ESTÁTICA

    # Carga Paralela
    def carga_permisible_estatica_cp(self):

        # Definir Fmax
        f_max = symbols("F")

        # Calcular área de la soldadura
        area_sold, area_sold_ecuacion = self.calcular_area_sold()

        # Calcular esfuerzo aplicado en la junta
        tao = f_max / area_sold

        # SOLDADURA

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)

        # Despejar Fmax_sold de la ecuación de FD
        f_max_sold = despejar_carga_max_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao)

        # PIEZA 1

        # Calcular la resistencia a la fluencia al cortante de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza1 = despejar_carga_max_fd_estatica(self.fd_min_pieza, ssy_pieza1, tao)

        # PIEZA 2

        # Calcular la resistencia a la fluencia al cortante de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]
        ssy_pieza2 = 0.577 * sy_pieza2

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza2 = despejar_carga_max_fd_estatica(self.fd_min_pieza, ssy_pieza2, tao)

        f_max_estatica = min(f_max_sold, f_max_pieza1, f_max_pieza2)

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max_estatica)

        # Generar diccionario para informe de resultados
        resultados = {
            "tipo_union": self.tipo_union,
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "area_sold": round(area_sold, 3),
            "area_sold_ecuacion": area_sold_ecuacion,
            "tao": tao,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "f_max_sold": "{:.2f}".format(f_max_sold),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "ssy_pieza1": round(ssy_pieza1, 2),
            "ssy_pieza2": round(ssy_pieza2, 2),
            "f_max_pieza1": "{:.2f}".format(f_max_pieza1),
            "f_max_pieza2": "{:.2f}".format(f_max_pieza2),
            "conclusion_fperm": conclusion_fperm
        }
        return resultados

    # Carga Transversal
    def carga_permisible_estatica_ctrans(self):

        # Definir Fmax
        f_max = symbols("F")

        # Calcular área de la soldadura
        area_sold, area_sold_ecuacion = self.calcular_area_sold()

        # Calcular esfuerzo aplicado en la junta
        sigma = f_max / area_sold

        # SOLDADURA

        # Obtener la resistencia a la fluencia del material de aporte (soldadura)
        sy_sold = self.electrodo["Sy"]

        # Despejar Fmax_sold de la ecuación de FD
        f_max_sold = despejar_carga_max_fd_estatica(self.fd_min_sold, sy_sold, sigma)

        # PIEZA 1 (Pieza P)

        # Obtener la resistencia a la fluencia al cortante de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza1 = despejar_carga_max_fd_estatica(self.fd_min_pieza, sy_pieza1, sigma)

        # PIEZA 2 (Pieza T)

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza2 = despejar_carga_max_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma)

        f_max_estatica = min(f_max_sold, f_max_pieza1, f_max_pieza2)

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max_estatica)

        # Generar diccionario para informe de resultados
        resultados = {
            "tipo_union": self.tipo_union,
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "r_ext": self.geometria_params["radio exterior"],
            "area_sold": round(area_sold, 3),
            "area_sold_ecuacion": area_sold_ecuacion,
            "sigma": sigma,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "f_max_sold": "{:.2f}".format(f_max_sold),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "f_max_pieza1": "{:.2f}".format(f_max_pieza1),
            "f_max_pieza2": "{:.2f}".format(f_max_pieza2),
            "conclusion_fperm": conclusion_fperm
        }
        return resultados

    # Carga de Flexión debido a una fuerza excéntrica
    def carga_permisible_estatica_cflex(self):

        # Definir Fmax
        f_max = symbols("F")

        # Obtener el valor del brazo (b) y calcular el momento flector
        b = self.brazo
        momento_flector = f_max * b

        # Cálculo de parámetros geométricos
        area_sold, area_sold_ecuacion = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia()
        c = self.obtener_rx_ry()[1]
        c_ecuacion = self.obtener_rx_ry()[2][1]

        # Calcular los esfuerzos aplicados en la junta (En función de F)
        tao = f_max / area_sold
        sigma = momento_flector * c / i_sold
        sigma_von_misses = sqrt(sigma ** 2 + 3 * tao ** 2)

        # SOLDADURA

        # Obtener la resistencia a la fluencia del material de aporte (soldadura)
        sy_sold = self.electrodo["Sy"]

        # Despejar Fmax_sold de la ecuación de FD
        f_max_sold = despejar_carga_max_fd_estatica(self.fd_min_sold, sy_sold, sigma_von_misses)

        # PIEZA 1 (Pieza P)

        # Obtener la resistencia a la fluencia de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza1 = despejar_carga_max_fd_estatica(self.fd_min_pieza, sy_pieza1, sigma_von_misses)

        # PIEZA 2 (Pieza T)

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza2 = despejar_carga_max_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma_von_misses)

        f_max_estatica = min(f_max_sold, f_max_pieza1, f_max_pieza2)

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max_estatica)

        # Generar diccionario para informe de resultados
        resultados = {
            "tipo_union": self.tipo_union,
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "r_ext": self.geometria_params["radio exterior"],
            "area_sold": round(area_sold, 3),
            "area_sold_ecuacion": area_sold_ecuacion,
            "i_sold": round(i_sold, 2),
            "i_sold_ecuacion": i_sold_ecuacion,
            "c": round(c, 3),
            "c_ecuacion": c_ecuacion,
            "b": b,
            "momento_flector": momento_flector,
            "sigma": sigma,
            "tao": tao,
            "sigma_von_misses": sigma_von_misses,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "f_max_sold": "{:.2f}".format(f_max_sold),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "f_max_pieza1": "{:.2f}".format(f_max_pieza1),
            "f_max_pieza2": "{:.2f}".format(f_max_pieza2),
            "conclusion_fperm": conclusion_fperm
        }
        return resultados

    # Carga de Torsión
    def carga_permisible_estatica_ctor(self):

        # Definir Tmax
        momento_torsor_max = symbols("T")

        # Cálculo de parámetros geométricos
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion
        r = sqrt(rx ** 2 + ry ** 2)

        # Calcular esfuerzo cortante aplicado en la junta (En función de T)
        tao = momento_torsor_max * r / j_sold

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)

        # Despejar Tmax_sold de la ecuación de FD
        momento_torsor_max_sold = despejar_torque_max_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao)

        # PIEZA 1

        # Calcular la resistencia a la fluencia al cortante de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1

        # Despejar Tmax_pieza1 de la ecuación de FD
        momento_torsor_max_pieza1 = despejar_torque_max_fd_estatica(self.fd_min_pieza, ssy_pieza1, tao)

        # PIEZA 2

        # Calcular la resistencia a la fluencia al cortante de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]
        ssy_pieza2 = 0.577 * sy_pieza2

        # Despejar Tmax_pieza2 de la ecuación de FD
        momento_torsor_max_pieza2 = despejar_torque_max_fd_estatica(self.fd_min_pieza, ssy_pieza2, tao)

        momento_torsor_max_estatica = min(momento_torsor_max_sold, momento_torsor_max_pieza1,
                                          momento_torsor_max_pieza2)

        # Generar mensaje con el torque permisible obtenido
        conclusion_tperm = conclusion_torque_permisible(self.sistema_unidades, momento_torsor_max_estatica)

        # Generar diccionario para informe de resultados
        resultados = {
            "tipo_union": self.tipo_union,
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "r_ext": self.geometria_params["radio exterior"],
            "area_sold": round(self.calcular_area_sold()[0], 3),
            "area_sold_ecuacion": self.calcular_area_sold()[1],
            "j_sold": round(j_sold, 2),
            "j_sold_ecuacion": j_sold_ecuacion,
            "r": round(r, 3),
            "rx_ecuacion": rx_ecuacion,
            "ry_ecuacion": ry_ecuacion,
            "tao": tao,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": "{:.2f}".format(tao_admisible_sold),
            "t_max_sold": round(momento_torsor_max_sold, 2),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "ssy_pieza1": ssy_pieza1,
            "ssy_pieza2": ssy_pieza2,
            "t_max_pieza1": "{:.2f}".format(momento_torsor_max_pieza1),
            "t_max_pieza2": "{:.2f}".format(momento_torsor_max_pieza2),
            "conclusion_tperm": conclusion_tperm
        }
        return resultados

    # Carga Combinada debido a una carga excétrica
    def carga_permisible_estatica_ccomb(self):

        # Definir Fmax
        f_max = symbols("F")

        # Obtener el valor del brazo longitudinal (bl) y del brazo transversal (bt) y calcular los momentos
        bl = self.brazo["bl"]
        bt = self.brazo["bt"]
        momento_flector = f_max * bl
        momento_torsor = f_max * bt

        # Cálculo de parámetros geométricos
        area_sold, area_sold_ecuacion = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion
        c = ry
        c_ecuacion = ry_ecuacion

        # Calcular esfuerzo normal aplicado en la junta (En función de F)
        sigma = momento_flector * c / i_sold

        # Calcular esfuerzo cortante en la soldadura (En función de F)
        tao_primario = f_max / area_sold
        tao_secundario_x = momento_torsor * ry / j_sold
        tao_secundario_y = momento_torsor * rx / j_sold
        tao_x = tao_secundario_x
        tao_y = tao_primario + tao_secundario_y
        tao = sqrt(tao_x ** 2 + tao_y ** 2)

        # Calcular el esfuerzo Von Misses aplicado en la soldadura (En función de F)
        sigma_von_misses = sqrt(sigma ** 2 + 3 * tao ** 2)

        # SOLDADURA

        # Obtener resistencia a la fluencia del material de aporte (soldadura)
        sy_sold = self.electrodo["Sy"]

        # Despejar Fmax_sold de la ecuación de FD
        f_max_sold = despejar_carga_max_fd_estatica(self.fd_min_sold, sy_sold, sigma_von_misses)

        # PIEZA 1

        # Obtener la resistencia a la fluencia de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza1 = despejar_carga_max_fd_estatica(self.fd_min_pieza, sy_pieza1, sigma_von_misses)

        # PIEZA 2

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Despejar Fmax_pieza1 de la ecuación de FD
        f_max_pieza2 = despejar_carga_max_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma_von_misses)

        f_max_estatica = min(f_max_sold, f_max_pieza1, f_max_pieza2)

        # Generar mensaje con la fuerza permisible obtenida
        conclusion_fperm = conclusion_fuerza_permisible(self.sistema_unidades, f_max_estatica)

        # Generar diccionario para informe de resultados
        resultados = {
            "tipo_union": self.tipo_union,
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "r_ext": self.geometria_params["radio exterior"],
            "area_sold": round(area_sold, 3),
            "area_sold_ecuacion": area_sold_ecuacion,
            "i_sold": round(i_sold, 2),
            "j_sold": round(j_sold, 2),
            "rx": round(rx, 3),
            "ry": round(ry, 3),
            "c": round(c, 3),
            "i_sold_ecuacion": i_sold_ecuacion,
            "j_sold_ecuacion": j_sold_ecuacion,
            "rx_ecuacion": rx_ecuacion,
            "ry_ecuacion": ry_ecuacion,
            "c_ecuacion": c_ecuacion,
            "bl": bl,
            "bt": bt,
            "momento_flector": momento_flector,
            "momento_torsor": momento_torsor,
            "sigma": sigma,
            "tao_primario": tao_primario,
            "tao_secundario_x": tao_secundario_x,
            "tao_secundario_y": tao_secundario_y,
            "tao_x": tao_x,
            "tao_y": tao_y,
            "tao": tao,
            "sigma_von_misses": sigma_von_misses,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "f_max_sold": "{:.2f}".format(f_max_sold),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "f_max_pieza1": "{:.2f}".format(f_max_pieza1),
            "f_max_pieza2": "{:.2f}".format(f_max_pieza2),
            "conclusion_fperm": conclusion_fperm
        }
        return resultados


# Clase para el cálculo del espesor mínimo necesario en la junta
class DisenoEspesorRanura:
    # Factores de diseño mínimo
    fd_min_sold = 3.33
    fd_min_pieza = 2.5

    def __init__(self, sistema_unidades, tipo_union, carga, material_base_1, material_base_2,
                 electrodo, geometria, geometria_params):
        self.sistema_unidades = sistema_unidades
        self.tipo_union = tipo_union
        self.carga = carga
        self.material_base_1 = material_base_1
        self.material_base_2 = material_base_2
        self.electrodo = electrodo
        self.geometria = geometria
        self.geometria_params = geometria_params

    ###################################################################################################################
    # GEOMETRIA

    # Calcular el área de la garganta de la soldadura
    def calcular_area_sold(self):

        t = symbols("t")
        l = self.geometria_params.get("largo", 0)
        r_ext = self.geometria_params.get("radio exterior", 0)

        if r_ext > 0:
            r_int = r_ext - t
        else:
            r_int = 0

        areas_geometrias = {
            "uno": (l * t),
            "dos": (l * t),
            "tres": pi * (r_ext ** 2 - r_int ** 2)
        }

        areas_formulas = {
            "uno": "l * t",
            "dos": "l * t",
            "tres": "pi * ((r ext)^2 - (r int)^2)"
        }

        area_sold = areas_geometrias.get(self.geometria, 0)
        area_sold_ecuacion = areas_formulas[self.geometria]
        return area_sold, area_sold_ecuacion

    # Calcular el momento de inercia
    def calcular_momento_inercia(self):

        t = symbols("t")
        l = self.geometria_params.get("largo", 0)
        r_ext = self.geometria_params.get("radio exterior", 0)

        if r_ext > 0:
            r_int = r_ext - t
        else:
            r_int = 0

        momentos_inercia_geometrias = {
            "uno": (0.0834 * t * l ** 3),
            "dos": (0.0834 * t ** 3 * l),
            "tres": (0.25 * pi * (r_ext ** 4 - r_int ** 4)),
        }

        momentos_inercia_formulas = {
            "uno": "0.0834 * t * l^3",
            "dos": "0.0834 * t^3 * l",
            "tres": "0.25 * pi * ((r ext)^4 - (r int)^4)",
        }

        momento_de_inercia = momentos_inercia_geometrias.get(self.geometria)
        momento_de_inercia_ecuacion = momentos_inercia_formulas[self.geometria]
        return momento_de_inercia, momento_de_inercia_ecuacion

    # Calcular el momento de inercia polar
    def calcular_momento_inercia_polar(self):

        t = symbols("t")
        l = self.geometria_params.get("largo", 0)
        r_ext = self.geometria_params.get("radio exterior", 0)

        if r_ext > 0:
            r_int = r_ext - t
        else:
            r_int = 0

        momentos_inercia_polar_geometrias = {
            "uno": (t * l ** 3 / 12),
            "dos": (t * l ** 3 / 12),
            "tres": (0.5 * pi * (r_ext ** 4 - r_int ** 4)),
        }

        momentos_inercia_polar_formulas = {
            "uno": "t * l^3 / 12",
            "dos": "t * l^3 / 12",
            "tres": "0.5 * pi * ((r ext)^4 - (r int)^4)",
        }

        momento_de_inercia_polar = momentos_inercia_polar_geometrias.get(self.geometria)
        momento_de_inercia_polar_ecuacion = momentos_inercia_polar_formulas[self.geometria]
        return momento_de_inercia_polar, momento_de_inercia_polar_ecuacion

    # Obtener las coordenadas del centroide (X barra, Y barra)
    def obtener_coordenadas_centroide(self):

        l = self.geometria_params.get("largo", 0)
        coordenadas_centroide_geometrias = {
            "uno": (0, l / 2),
            "dos": (l / 2, 0),
            "tres": (0, 0)
        }
        x_barra, y_barra = coordenadas_centroide_geometrias.get(self.geometria)
        return x_barra, y_barra

    # Obtener rx y ry para calcular el esfuerzo debido al par torsionante
    def obtener_rx_ry(self):

        t = symbols("t")
        l = self.geometria_params.get("largo", 0)
        r_ext = self.geometria_params.get("radio exterior", 0)

        rx_ry_geometrias = {
            "uno": (t / 2, l / 2),
            "dos": (l / 2, t / 2),
            "tres": (0, r_ext),
        }

        rx_ry_formulas = {
            "uno": ("t/2", "l/2"),
            "dos": ("l/2", "t/2"),
            "tres": ("0", "r ext"),
        }
        rx, ry = rx_ry_geometrias.get(self.geometria)
        rx_ry_ecuacion = rx_ry_formulas[self.geometria]
        return rx, ry, rx_ry_ecuacion

    # OTROS

    @staticmethod
    # Despejar el espesor tmin de la ecuación del FD por carga estática
    def despejar_espesor_min_fd_estatica(fd, resistencia, esfuerzo_soportado):

        """# Definir la variable a calcular
        t = symbols("t")

        # Definir la ecuación (Despejada igual a cero)
        ecuacion_fd_estatica = fd - resistencia / esfuerzo_soportado

        # Despejar Fmax
        soluciones_espesor = solve(ecuacion_fd_estatica, t)

        soluciones_reales = []

        # Seleccionar la solución positiva de la ecuación
        for solucion in soluciones_espesor:
            if solucion.is_real and solucion > 0:
                soluciones_reales.append(solucion)

        sol_definitiva = min(soluciones_reales)

        return sol_definitiva"""

        t = symbols('t')

        ecuacion_fd_estatica = fd - resistencia / esfuerzo_soportado

        f_func = lambdify(t, ecuacion_fd_estatica, 'scipy')

        # Definir el rango de búsqueda
        rango_inicial = 0.05  # Puedes ajustar el valor inicial según tus necesidades
        rango_final = 10

        # Inicializar la variable solucion fuera del bucle
        solucion = None

        # Iterar a través de valores en el rango
        for valor_inicial in np.arange(rango_inicial, rango_final, 0.01):  # Ajusta el rango según tus necesidades
            try:
                solucion = newton(f_func, x0=valor_inicial, tol=1e-8, maxiter=100000)
                if solucion > 0:
                    print("Primera solución real y positiva encontrada:", solucion)
                    break  # Salir del bucle una vez que encuentres la solución
            except RuntimeError:
                # Capturar excepción por si newton no converge en este punto
                continue

        # Verificar si se encontró alguna solución
        if solucion is not None and solucion > 0:
            return solucion
        else:
            # Manejar el caso donde no se encontró ninguna solución
            print("No se encontró ninguna solución real y positiva en el rango especificado.")
            return None

    @staticmethod
    # Despejar el espesor tmin del cordón de soldadura de la ecuación de Gerber
    def despejar_espesor_ecuacion_gerber(esfuerzo_alternante, esfuerzo_medio, resistencia_fatiga, resistencia_ultima,
                                         fd):

        """# Definir la ecuación
        ecuacion_gerber = lambda t: (
               (fd * esfuerzo_medio / resistencia_ultima) ** 2 + (fd * esfuerzo_alternante / resistencia_fatiga) - 1
        )

        # Definir el rango de búsqueda
        rango_inicial = 0.01  # Puedes ajustar el valor inicial según tus necesidades

        # Inicializar la variable solucion fuera del bucle
        solucion = None

        # Iterar a través de valores en el rango
        for valor_inicial in np.arange(rango_inicial, 200.0, 0.1):  # Ajusta el rango según tus necesidades
            try:
                solucion = newton(ecuacion_gerber, x0=valor_inicial, tol=1e-3, maxiter=100000)
                if solucion > 0:
                    solucion = solucion
                    break  # Salir del bucle una vez que encuentres la solución
            except RuntimeError:
                # Capturar excepción por si newton no converge en este punto
                continue

        # Verificar si se encontró alguna solución
        if solucion is not None:
            return solucion
        else:
            # Manejar el caso donde no se encontró ninguna solución
            print("No se encontró solución real")
            return None"""

        t = symbols('t')

        ecuacion_gerber = (fd * esfuerzo_medio / resistencia_ultima) ** 2 + (
                    fd * esfuerzo_alternante / resistencia_fatiga) - 1
        print(ecuacion_gerber)
        f_func = lambdify(t, ecuacion_gerber, 'scipy')

        # Definir el rango de búsqueda
        rango_inicial = 0.02  # Puedes ajustar el valor inicial según tus necesidades
        rango_final = 10

        # Inicializar la variable solucion fuera del bucle
        solucion = None

        # Iterar a través de valores en el rango
        for valor_inicial in np.arange(rango_inicial, rango_final, 0.01):  # Ajusta el rango según tus necesidades
            try:
                solucion = newton(f_func, x0=valor_inicial, tol=1e-8, maxiter=100000)
                if solucion > 0:
                    print("Primera solución real y positiva encontrada:", solucion)
                    break  # Salir del bucle una vez que encuentres la solución
            except RuntimeError:
                # Capturar excepción por si newton no converge en este punto
                continue

        # Verificar si se encontró alguna solución
        if solucion is not None and solucion > 0:
            return solucion
        else:
            # Manejar el caso donde no se encontró ninguna solución
            print("No se encontró ninguna solución real y positiva en el rango especificado.")
            return None

    # Mensaje con el espesor minimo (tmin necesario en la junta)
    def conclusion_espesor_min(self, t_min_calculado):

        sistema_unidades = self.sistema_unidades

        if sistema_unidades == "Internacional":
            conclusion = f"El espesor mínimo necesario en la junta es tmin = {t_min_calculado} mm"
        else:
            conclusion = f"El espesor mínimo necesario en la junta es tmin = {t_min_calculado} pulg"

        return conclusion

    # Validar que para la geometría tubular la respuesta no sea absurda
    def validar_espesor_calculado_tubular(self, t_min):

        t_min = float(t_min)
        error = None
        if self.geometria == "tres":
            r_ext = self.geometria_params["radio exterior"]
            if r_ext <= t_min:
                # Forzar TypeError
                error = r_ext + ""
        return error

    ###################################################################################################################
    # DISEÑO POR FATIGA

    # Carga Paralela
    def espesor_cp(self):

        # DISEÑO POR FATIGA

        # Obtener cargas max y min
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]

        # Calcular cargas alternantes y medias
        f_alt, f_med = analisis.calcular_carga_alt_y_med(f_max, f_min)

        # Factor de concentración de esfuerzo reducido, Kfs (Se considera carga paralela con unión tope)
        kfs = 1.2

        # Area de la soldadura
        area_sold, area_sold_ecuacion = self.calcular_area_sold()

        # Obtener esfuerzo cortante alternante y medio (en función de t)
        tao_alt = kfs * f_alt / area_sold
        tao_med = f_med / area_sold

        # Determinar t en la soldadura

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar el espesor (t) de la ecuación de Gerber para FDmin_sold = 3.33
        t_sold = self.despejar_espesor_ecuacion_gerber(tao_alt, tao_med, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar t en la pieza 1

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia ultima al cortante del material base 1
        ssu_pieza1 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Despejar el espesor (t) de la ecuación de Gerber para un FDmin_pieza = 2.5
        t_pieza1 = self.despejar_espesor_ecuacion_gerber(tao_alt, tao_med, sse_pieza1, ssu_pieza1, self.fd_min_pieza)

        # Determinar t en la pieza 2

        # Calcular la resistencia a la fatiga al cortante del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        sse_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular la resistencia ultima al cortante del material base 2
        ssu_pieza2 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza2)

        # Despejar el espesor (t) de la ecuación de Gerber para un FDmin_pieza = 2.5
        t_pieza2 = self.despejar_espesor_ecuacion_gerber(tao_alt, tao_med, sse_pieza2, ssu_pieza2, self.fd_min_pieza)

        # Se selecciona el mayor de los espesores calculados
        t_min = round(max(t_sold, t_pieza1, t_pieza2), 3 if self.sistema_unidades == "Internacional" else 4)

        # Generar mensaje con el espesor minimo obtenido
        conclusion_tmin = self.conclusion_espesor_min(t_min)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraRanura(self.sistema_unidades, self.tipo_union, self.carga,
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria,
                                                                 {"espesor": t_min,
                                                                  "largo": self.geometria_params.get("largo", 0)})

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_cp()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.espesor_cp_estatica()

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "largo": self.geometria_params["largo"],
            "area_sold": area_sold,
            "area_sold_ecuacion": area_sold_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_alt": tao_alt,
            "tao_med": tao_med,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "t_sold": round(t_sold, 3 if self.sistema_unidades == "Internacional" else 4),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "sse_pieza2": round(sse_pieza2, 2),
            "ssu_pieza2": round(ssu_pieza2, 2),
            "t_pieza1": round(t_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "t_pieza2": round(t_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "t_min": t_min,
            "conclusion_tmin": conclusion_tmin,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga Transversal
    def espesor_ctrans(self):

        # DISEÑO POR FATIGA

        # Obtener cargas max y min
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]

        # Calcular cargas alternantes y medias
        f_alt, f_med = analisis.calcular_carga_alt_y_med(f_max, f_min)

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Tope": 1.2, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Area de la soldadura
        area_sold, area_sold_ecuacion = self.calcular_area_sold()

        # Obtener esfuerzo normal alternante y medio (en función de t)
        sigma_alt = kfs * f_alt / area_sold
        sigma_med = f_med / area_sold

        # Determinar t en la soldadura

        # Calcular la resistencia a la fatiga del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        se_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Despejar el espesor (t) de la ecuación de Gerber para FDmin_sold = 3.33
        t_sold = self.despejar_espesor_ecuacion_gerber(sigma_alt, sigma_med, se_sold, sut_sold, self.fd_min_sold)

        # Determinar t en la pieza 1

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Despejar el espesor (t) de la ecuación de Gerber para un FDmin_pieza = 2.5
        t_pieza1 = self.despejar_espesor_ecuacion_gerber(sigma_alt, sigma_med, se_pieza1, sut_pieza1, self.fd_min_pieza)

        # Determinar F en la pieza 2

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar el espesor (t) de la ecuación de Gerber para un FDmin_pieza = 2.5
        t_pieza2 = self.despejar_espesor_ecuacion_gerber(sigma_alt, sigma_med, se_pieza2, sut_pieza2, self.fd_min_pieza)

        # Se selecciona el mayor de los espesores calculados
        t_min = round(max(t_sold, t_pieza1, t_pieza2), 3 if self.sistema_unidades == "Internacional" else 4)

        # Validar que para la geometría tubular la respuesta no sea absurda
        self.validar_espesor_calculado_tubular(t_min)

        # Generar mensaje con el espesor minimo obtenido
        conclusion_tmin = self.conclusion_espesor_min(t_min)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraRanura(self.sistema_unidades, self.tipo_union, self.carga,
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria,
                                                                 {"espesor": t_min,
                                                                  "largo": self.geometria_params.get("largo", 0),
                                                                  "radio exterior": self.geometria_params.get(
                                                                      "radio exterior", 0)})

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_ctrans()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.espesor_ctrans_estatica()

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "largo": self.geometria_params["largo"],
            "area_sold": area_sold,
            "area_sold_ecuacion": area_sold_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "sigma_alt": sigma_alt,
            "sigma_med": sigma_med,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "se_sold": round(se_sold, 2),
            "t_sold": round(t_sold, 3 if self.sistema_unidades == "Internacional" else 4),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "t_pieza1": round(t_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "t_pieza2": round(t_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "t_min": t_min,
            "conclusion_tmin": conclusion_tmin,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga de Flexión debido a una fuerza excéntrica
    def espesor_cflex(self):

        # DISEÑO POR FATIGA

        # Obtener cargas max y min, y el brazo (b)
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]
        b = self.carga["b"]
        momento_flector_max, momento_flector_min = analisis.calcular_momento_max_y_min(f_max, f_min, b)

        # Calcular cargas alternantes y medias
        f_alt, f_med = analisis.calcular_carga_alt_y_med(f_max, f_min)
        momento_flector_alt, momento_flector_med = analisis.calcular_carga_alt_y_med(momento_flector_max,
                                                                                     momento_flector_min)

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Tope": 1.2, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Cálculo de parámetros geométricos
        area_sold, area_sold_ecuacion = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia()
        c = self.obtener_rx_ry()[1]
        c_ecuacion = self.obtener_rx_ry()[2][1]

        # Calcular esfuerzo cortante alternante y medio (En función de t)
        tao_alt = kfs * f_alt / area_sold
        tao_med = f_med / area_sold

        # Calcular esfuerzo normal alternante y medio (En función de t)
        sigma_alt = kfs * momento_flector_alt * c / i_sold
        sigma_med = momento_flector_med * c / i_sold

        # Calcular el esfuerzo de Von Misses alternante y medio (En función de t)
        sigma_von_misses_alt = sqrt(sigma_alt ** 2 + 3 * tao_alt ** 2)
        sigma_von_misses_med = sqrt(sigma_med ** 2 + 3 * tao_med ** 2)

        # Determinar t en la soldadura

        # Calcular la resistencia a la fatiga del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        se_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Despejar el espesor (t) de la ecuación de Gerber para FDmin_sold = 3.33
        t_sold = self.despejar_espesor_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_sold, sut_sold,
                                                       self.fd_min_sold)

        # Determinar t en la pieza 1

        # Calcular la resistencia a la fatiga del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Despejar el espesor (t) de la ecuación de Gerber para un FDmin_pieza = 2.5
        t_pieza1 = self.despejar_espesor_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_pieza1,
                                                         sut_pieza1, self.fd_min_pieza)

        # Determinar t en la pieza 2

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar el espesor (t) de la ecuación de Gerber para un FDmin_pieza = 2.5
        t_pieza2 = self.despejar_espesor_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_pieza2,
                                                         sut_pieza2, self.fd_min_pieza)

        # Se selecciona el mayor de los espesores calculados
        t_min = round(max(t_sold, t_pieza1, t_pieza2), 3 if self.sistema_unidades == "Internacional" else 4)

        # Validar que para la geometría tubular la respuesta no sea absurda
        self.validar_espesor_calculado_tubular(t_min)

        # Generar mensaje con el espesor minimo obtenido
        conclusion_tmin = self.conclusion_espesor_min(t_min)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraRanura(self.sistema_unidades, self.tipo_union, self.carga,
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria,
                                                                 {"espesor": t_min,
                                                                  "largo": self.geometria_params.get("largo", 0),
                                                                  "radio exterior": self.geometria_params.get(
                                                                      "radio exterior", 0)})

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_cflex()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.espesor_cflex_estatica()

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "b": b,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "momento_flector_alt": momento_flector_alt,
            "momento_flector_med": momento_flector_med,
            "largo": self.geometria_params["largo"],
            "area_sold": area_sold,
            "area_sold_ecuacion": area_sold_ecuacion,
            "i_sold": i_sold,
            "i_sold_ecuacion": i_sold_ecuacion,
            "c": c,
            "c_ecuacion": c_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_alt": tao_alt,
            "tao_med": tao_med,
            "sigma_alt": sigma_alt,
            "sigma_med": sigma_med,
            "sigma_von_misses_alt": sigma_von_misses_alt,
            "sigma_von_misses_med": sigma_von_misses_med,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "se_sold": round(se_sold, 2),
            "t_sold": round(t_sold, 3 if self.sistema_unidades == "Internacional" else 4),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "t_pieza1": round(t_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "t_pieza2": round(t_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "t_min": t_min,
            "conclusion_tmin": conclusion_tmin,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga de Torsión
    def espesor_ctor(self):

        # DISEÑO POR FATIGA

        # Obtener momento torsor max y min
        momento_torsor_max = self.carga.get("Tmax", 0)
        momento_torsor_min = self.carga.get("Tmin", 0)

        if self.sistema_unidades == "Internacional":
            momento_torsor_max = momento_torsor_max * 1000
            momento_torsor_min = momento_torsor_min * 1000

        # Calcular carga alternante y media
        momento_torsor_alt, momento_torsor_med = analisis.calcular_carga_alt_y_med(momento_torsor_max,
                                                                                   momento_torsor_min)

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Tope": 1.2, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Cálculo de parámetros geométricos
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion
        r = sqrt(rx ** 2 + ry ** 2)

        # Calcular el esfuerzo cortante resultante alternante y medio (En función de t)
        tao_alt = kfs * momento_torsor_alt * r / j_sold
        tao_med = momento_torsor_med * r / j_sold

        # Determinar T en la soldadura

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = analisis.calcular_resistencia_ultima_al_cortante(sut_sold)

        # Despejar el espesor (t) de la ecuación de Gerber para FDmin_sold = 3.33
        t_sold = self.despejar_espesor_ecuacion_gerber(tao_alt, tao_med, sse_sold, ssu_sold, self.fd_min_sold)

        # Determinar T en la pieza 1

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia última al cortante del material base 1
        ssu_pieza1 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Despejar el espesor (t) de la ecuación de Gerber para un FDmin_pieza = 2.5
        t_pieza1 = self.despejar_espesor_ecuacion_gerber(tao_alt, tao_med, sse_pieza1, ssu_pieza1, self.fd_min_pieza)

        # Determinar T en la pieza 2

        # Calcular la resistencia a la fatiga al cortante del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        sse_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular la resistencia ultima al cortante de la pieza 2
        ssu_pieza2 = analisis.calcular_resistencia_ultima_al_cortante(sut_pieza2)

        # Despejar el espesor (t) de la ecuación de Gerber para un FDmin_pieza = 2.5
        t_pieza2 = self.despejar_espesor_ecuacion_gerber(tao_alt, tao_med, sse_pieza2, ssu_pieza2, self.fd_min_pieza)

        # Se selecciona el mayor de los espesores calculados
        t_min = round(max(t_sold, t_pieza1, t_pieza2), 3 if self.sistema_unidades == "Internacional" else 4)

        # Validar que para la geometría tubular la respuesta no sea absurda
        self.validar_espesor_calculado_tubular(t_min)

        # Generar mensaje con el espesor minimo obtenido
        conclusion_tmin = self.conclusion_espesor_min(t_min)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraRanura(self.sistema_unidades, self.tipo_union, self.carga,
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria,
                                                                 {"espesor": t_min,
                                                                  "largo": self.geometria_params.get("largo", 0),
                                                                  "radio exterior": self.geometria_params.get(
                                                                      "radio exterior", 0)})

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_ctor()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.espesor_ctor_estatica()

        # Generar diccionario para informe de resultados
        resultados = {
            "Tmax": momento_torsor_max,
            "Tmin": momento_torsor_min,
            "Talt": round(momento_torsor_alt, 2),
            "Tmed": round(momento_torsor_med, 2),
            "tipo_union": self.tipo_union,
            "momento_torsor_alt": momento_torsor_alt,
            "momento_torsor_med": momento_torsor_med,
            "largo": self.geometria_params["largo"],
            "area_sold": self.calcular_area_sold()[0],
            "area_sold_ecuacion": self.calcular_area_sold()[1],
            "j_sold": j_sold,
            "j_sold_ecuacion": j_sold_ecuacion,
            "r": r,
            "rx_ecuacion": rx_ecuacion,
            "ry_ecuacion": ry_ecuacion,
            "kfs": kfs,
            "tao_alt": tao_alt,
            "tao_med": tao_med,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "t_sold": round(t_sold, 3 if self.sistema_unidades == "Internacional" else 4),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "sse_pieza2": round(sse_pieza2, 2),
            "ssu_pieza2": round(ssu_pieza2, 2),
            "t_pieza1": round(t_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "t_pieza2": round(t_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "t_min": t_min,
            "conclusion_tmin": conclusion_tmin,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }
        return resultados, valores_comprobacion_estatica, rediseno_estatica

    # Carga Combinada debido a una carga excétrica
    def espesor_ccomb(self):

        # DISEÑO POR FATIGA

        # Obtener cargas max y min, el brazo longitudinal (bl) y el brazo transversal (bt)
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]
        bl = self.carga["bl"]
        bt = self.carga["bt"]
        momento_flector_max, momento_flector_min = analisis.calcular_momento_max_y_min(f_max, f_min, bl)
        momento_torsor_max, momento_torsor_min = analisis.calcular_momento_max_y_min(f_max, f_min, bt)

        # Calcular cargas alternantes y medias
        f_alt, f_med = analisis.calcular_carga_alt_y_med(f_max, f_min)
        momento_flector_alt, momento_flector_med = analisis.calcular_carga_alt_y_med(momento_flector_max,
                                                                                     momento_flector_min)
        momento_torsor_alt, momento_torsor_med = analisis.calcular_carga_alt_y_med(momento_torsor_max,
                                                                                   momento_torsor_min)

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Tope": 1.2, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Cálculo de parámetros geométricos
        area_sold, area_sold_ecuacion = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion
        c = ry
        c_ecuacion = ry_ecuacion

        # Calcular esfuerzo cortante primario alternante y medio
        tao_primario_alt = kfs * f_alt / area_sold
        tao_primario_med = f_med / area_sold

        # Calcular las componentes x e y del esfuerzo cortante secundario alternante
        tao_secundario_alt_x = kfs * momento_torsor_alt * ry / j_sold
        tao_secundario_alt_y = kfs * momento_torsor_alt * rx / j_sold

        # Calcular las componentes x e y del esfuerzo cortante secundario medio
        tao_secundario_med_x = momento_torsor_med * ry / j_sold
        tao_secundario_med_y = momento_torsor_med * rx / j_sold

        # Calcular las componentes x e y del esfuerzo cortante alternante
        tao_alt_x = tao_secundario_alt_x
        tao_alt_y = tao_primario_alt + tao_secundario_alt_y

        # Calcular las componentes x e y del esfuerzo cortante medio
        tao_med_x = tao_secundario_med_x
        tao_med_y = tao_primario_med + tao_secundario_med_y

        # Calcular el esfuerzo cortante resultante alternante y medio
        tao_alt = sqrt(tao_alt_x ** 2 + tao_alt_y ** 2)
        tao_med = sqrt(tao_med_x ** 2 + tao_med_y ** 2)

        # Calcular esfuerzo normal alternante y medio
        sigma_alt = kfs * momento_flector_alt * c / i_sold
        sigma_med = momento_flector_med * c / i_sold

        # Calcular el esfuerzo de Von Misses alternante y medio (En función de F)
        sigma_von_misses_alt = sqrt(sigma_alt ** 2 + 3 * tao_alt ** 2)
        sigma_von_misses_med = sqrt(sigma_med ** 2 + 3 * tao_med ** 2)

        # Determinar t en la soldadura

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        se_sold = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Despejar el espesor (t) de la ecuación de Gerber para FDmin_sold = 3.33
        t_sold = self.despejar_espesor_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_sold, sut_sold,
                                                       self.fd_min_sold)

        # Determinar t en la pieza 1

        # Calcular la resistencia a la fatiga del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Despejar el espesor (t) de la ecuación de Gerber para un FDmin_pieza = 2.5
        t_pieza1 = self.despejar_espesor_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_pieza1,
                                                         sut_pieza1, self.fd_min_pieza)

        # Determinar t en la pieza 2

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = analisis.calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Despejar el espesor (t) de la ecuación de Gerber para un FDmin_pieza = 2.5
        t_pieza2 = self.despejar_espesor_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_pieza2,
                                                         sut_pieza2, self.fd_min_pieza)

        # Se selecciona el mayor de los espesores calculados
        t_min = round(max(t_sold, t_pieza1, t_pieza2), 3 if self.sistema_unidades == "Internacional" else 4)

        # Validar que para la geometría tubular la respuesta no sea absurda
        self.validar_espesor_calculado_tubular(t_min)

        # Generar mensaje con el espesor minimo obtenido
        conclusion_tmin = self.conclusion_espesor_min(t_min)

        # Analizar por carga estática partiendo del resultado obtenido
        comprobacion_estatica = analisis.AnalisisSoldaduraRanura(self.sistema_unidades, self.tipo_union, self.carga,
                                                                 self.material_base_1, self.material_base_2,
                                                                 self.electrodo, self.geometria,
                                                                 {"espesor": t_min,
                                                                  "largo": self.geometria_params.get("largo", 0),
                                                                  "radio exterior": self.geometria_params.get(
                                                                      "radio exterior", 0)})

        # Verificar si se presentó la falla por carga estática y obtener valores para informe
        falla_estatica, valores_comprobacion_estatica = comprobacion_estatica.analisis_estatico_ccomb()

        # Mensaje de conclusion de diseño por fatiga
        conclusion_diseno_fatiga = generar_conclusion_diseno_fatiga(falla_estatica)

        if not falla_estatica:
            rediseno_estatica = None
        else:
            # DISEÑO POR CARGA ESTÁTICA
            rediseno_estatica = self.espesor_ccomb_estatica()

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "bl": bl,
            "bt": bt,
            "momento_flector_alt": round(momento_flector_alt, 2),
            "momento_flector_med": round(momento_flector_med, 2),
            "momento_torsor_alt": round(momento_torsor_alt, 2),
            "momento_torsor_med": round(momento_torsor_med, 2),
            "largo": self.geometria_params["largo"],
            "area_sold": area_sold,
            "area_sold_ecuacion": area_sold_ecuacion,
            "i_sold": i_sold,
            "j_sold": j_sold,
            "rx": rx,
            "ry": ry,
            "c": c,
            "i_sold_ecuacion": i_sold_ecuacion,
            "j_sold_ecuacion": j_sold_ecuacion,
            "rx_ecuacion": rx_ecuacion,
            "ry_ecuacion": ry_ecuacion,
            "c_ecuacion": c_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_primario_alt": tao_primario_alt,
            "tao_primario_med": tao_primario_med,
            "tao_secundario_alt_x": tao_secundario_alt_x,
            "tao_secundario_alt_y": tao_secundario_alt_y,
            "tao_secundario_med_x": tao_secundario_med_x,
            "tao_secundario_med_y": tao_secundario_med_y,
            "tao_alt_x": tao_alt_x,
            "tao_alt_y": tao_alt_y,
            "tao_med_x": tao_med_x,
            "tao_med_y": tao_med_y,
            "tao_alt": tao_alt,
            "tao_med": tao_med,
            "sigma_alt": sigma_alt,
            "sigma_med": sigma_med,
            "sigma_von_misses_alt": sigma_von_misses_alt,
            "sigma_von_misses_med": sigma_von_misses_med,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "se_sold": round(se_sold, 2),
            "t_sold": round(t_sold, 3 if self.sistema_unidades == "Internacional" else 4),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": sut_pieza1,
            "sut_pieza2": sut_pieza2,
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "t_pieza1": round(t_pieza1, 3 if self.sistema_unidades == "Internacional" else 4),
            "t_pieza2": round(t_pieza2, 3 if self.sistema_unidades == "Internacional" else 4),
            "t_min": t_min,
            "conclusion_tmin": conclusion_tmin,
            "conclusion_diseno_fatiga": conclusion_diseno_fatiga
        }

        return resultados, valores_comprobacion_estatica, rediseno_estatica

    ###################################################################################################################

    # DISEÑO POR CARGA ESTÁTICA

    # Carga Paralela
    def espesor_cp_estatica(self):

        # Obtener Fmax
        f_max = self.carga["Fmax"]

        # Calcular área de la soldadura
        area_sold, area_sold_ecuacion = self.calcular_area_sold()

        # Calcular esfuerzo aplicado en la junta
        tao = f_max / area_sold

        # SOLDADURA

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)

        # Despejar tmin_sold de la ecuación de FD
        t_min_sold = self.despejar_espesor_min_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao)

        # PIEZA 1

        # Calcular la resistencia a la fluencia al cortante de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1

        # Despejar tmin_pieza1 de la ecuación de FD
        t_min_pieza1 = self.despejar_espesor_min_fd_estatica(self.fd_min_pieza, ssy_pieza1, tao)

        # PIEZA 2

        # Calcular la resistencia a la fluencia al cortante de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]
        ssy_pieza2 = 0.577 * sy_pieza2

        # Despejar tmin_pieza1 de la ecuación de FD
        t_min_pieza2 = self.despejar_espesor_min_fd_estatica(self.fd_min_pieza, ssy_pieza2, tao)

        # Se selecciona el mayor de los espesores calculados
        t_min_estatica = format(max(t_min_sold, t_min_pieza1, t_min_pieza2),
                                '.3f' if self.sistema_unidades == "Internacional" else '.4f')

        # Generar mensaje con el espesor minimo obtenido
        conclusion_tmin = self.conclusion_espesor_min(t_min_estatica)

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "tipo_union": self.tipo_union,
            "largo": self.geometria_params["largo"],
            "area_sold": area_sold,
            "area_sold_ecuacion": area_sold_ecuacion,
            "tao": tao,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "t_min_sold": format(t_min_sold, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "ssy_pieza1": round(ssy_pieza1, 2),
            "ssy_pieza2": round(ssy_pieza2, 2),
            "t_min_pieza1": format(t_min_pieza1, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "t_min_pieza2": format(t_min_pieza2, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "t_min": t_min_estatica,
            "conclusion_tmin": conclusion_tmin
        }
        return resultados

    # Carga Transversal
    def espesor_ctrans_estatica(self):

        # Obtener Fmax
        f_max = self.carga["Fmax"]

        # Calcular área de la soldadura
        area_sold, area_sold_ecuacion = self.calcular_area_sold()

        # Calcular esfuerzo aplicado en la junta
        sigma = f_max / area_sold

        # SOLDADURA

        # Obtener la resistencia a la fluencia del material de aporte (soldadura)
        sy_sold = self.electrodo["Sy"]

        # Despejar tmin_sold de la ecuación de FD
        t_min_sold = self.despejar_espesor_min_fd_estatica(self.fd_min_sold, sy_sold, sigma)

        # PIEZA 1

        # Obtener la resistencia a la fluencia al cortante de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]

        # Despejar tmin_pieza1 de la ecuación de FD
        t_min_pieza1 = self.despejar_espesor_min_fd_estatica(self.fd_min_pieza, sy_pieza1, sigma)

        # PIEZA 2

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Despejar tmin_pieza1 de la ecuación de FD
        t_min_pieza2 = self.despejar_espesor_min_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma)

        # Se selecciona el mayor de los espesores calculados
        t_min_estatica = format(max(t_min_sold, t_min_pieza1, t_min_pieza2),
                                '.3f' if self.sistema_unidades == "Internacional" else '.4f')

        # Validar que para la geometría tubular la respuesta no sea absurda
        self.validar_espesor_calculado_tubular(t_min_estatica)

        # Generar mensaje con el espesor minimo obtenido
        conclusion_tmin = self.conclusion_espesor_min(t_min_estatica)

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "tipo_union": self.tipo_union,
            "largo": self.geometria_params["largo"],
            "area_sold": area_sold,
            "area_sold_ecuacion": area_sold_ecuacion,
            "sigma": sigma,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "t_min_sold": format(t_min_sold, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "t_min_pieza1": format(t_min_pieza1, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "t_min_pieza2": format(t_min_pieza2, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "t_min": t_min_estatica,
            "conclusion_tmin": conclusion_tmin
        }
        return resultados

    # Carga de Flexión debido a una fuerza excéntrica
    def espesor_cflex_estatica(self):

        # Obtener Fmax y el brazo
        f_max = self.carga["Fmax"]
        brazo = self.carga["b"]

        # Calcular el momento flector debido a la fuerza externa
        momento_flector = f_max * brazo

        # Cálculo de parámetros geométricos
        area_sold, area_sold_ecuacion = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia()
        c = self.obtener_rx_ry()[1]
        c_ecuacion = self.obtener_rx_ry()[2][1]

        # Calcular los esfuerzos aplicados en la junta (En función de t)
        tao = f_max / area_sold
        sigma = momento_flector * c / i_sold
        sigma_von_misses = sqrt(sigma ** 2 + 3 * tao ** 2)

        # SOLDADURA

        # Obtener la resistencia a la fluencia del material de aporte (soldadura)
        sy_sold = self.electrodo["Sy"]

        # Despejar tmin_sold de la ecuación de FD
        t_min_sold = self.despejar_espesor_min_fd_estatica(self.fd_min_sold, sy_sold, sigma_von_misses)

        # PIEZA 1

        # Obtener la resistencia a la fluencia de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]

        # Despejar tmin_pieza1 de la ecuación de FD
        t_min_pieza1 = self.despejar_espesor_min_fd_estatica(self.fd_min_pieza, sy_pieza1, sigma_von_misses)

        # PIEZA 2

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Despejar tmin_pieza1 de la ecuación de FD
        t_min_pieza2 = self.despejar_espesor_min_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma_von_misses)

        # Se selecciona el mayor de los espesores calculados
        t_min_estatica = format(max(t_min_sold, t_min_pieza1, t_min_pieza2),
                                '.3f' if self.sistema_unidades == "Internacional" else '.4f')

        # Validar que para la geometría tubular la respuesta no sea absurda
        self.validar_espesor_calculado_tubular(t_min_estatica)

        # Generar mensaje con el espesor minimo obtenido
        conclusion_tmin = self.conclusion_espesor_min(t_min_estatica)

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "tipo_union": self.tipo_union,
            "largo": self.geometria_params["largo"],
            "area_sold": area_sold,
            "area_sold_ecuacion": area_sold_ecuacion,
            "i_sold": i_sold,
            "i_sold_ecuacion": i_sold_ecuacion,
            "c": c,
            "c_ecuacion": c_ecuacion,
            "b": brazo,
            "momento_flector": momento_flector,
            "sigma": sigma,
            "tao": tao,
            "sigma_von_misses": sigma_von_misses,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "t_min_sold": format(t_min_sold, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "t_min_pieza1": format(t_min_pieza1, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "t_min_pieza2": format(t_min_pieza2, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "t_min": t_min_estatica,
            "conclusion_tmin": conclusion_tmin
        }
        return resultados

    # Carga de Torsión
    def espesor_ctor_estatica(self):

        # Obtener el momento torsor max
        momento_torsor = self.carga["Tmax"]

        if self.sistema_unidades == "Internacional":
            momento_torsor = momento_torsor * 1000

        # Cálculo de parámetros geométricos
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion
        r = sqrt(rx ** 2 + ry ** 2)

        # Calcular esfuerzo cortante aplicado en la junta (En función de t)
        tao = momento_torsor * r / j_sold

        # Calcular esfuerzo admisible del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = analisis.calcular_tao_adm_ma(sut_sold)

        # Despejar tmin_sold de la ecuación de FD
        t_min_sold = self.despejar_espesor_min_fd_estatica(self.fd_min_sold, tao_admisible_sold, tao)

        # PIEZA 1

        # Calcular la resistencia a la fluencia al cortante de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1

        # Despejar tmin_pieza1 de la ecuación de FD
        t_min_pieza1 = self.despejar_espesor_min_fd_estatica(self.fd_min_pieza, ssy_pieza1, tao)

        # PIEZA 2

        # Calcular la resistencia a la fluencia al cortante de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]
        ssy_pieza2 = 0.577 * sy_pieza2

        # Despejar tmin_pieza1 de la ecuación de FD
        t_min_pieza2 = self.despejar_espesor_min_fd_estatica(self.fd_min_pieza, ssy_pieza2, tao)

        # Se selecciona el mayor de los espesores calculados
        t_min_estatica = format(max(t_min_sold, t_min_pieza1, t_min_pieza2),
                                '.3f' if self.sistema_unidades == "Internacional" else '.4f')

        # Validar que para la geometría tubular la respuesta no sea absurda
        self.validar_espesor_calculado_tubular(t_min_estatica)

        # Generar mensaje con el espesor minimo obtenido
        conclusion_tmin = self.conclusion_espesor_min(t_min_estatica)

        # Generar diccionario para informe de resultados
        resultados = {
            "Tmax": momento_torsor,
            "tipo_union": self.tipo_union,
            "largo": self.geometria_params["largo"],
            "area_sold": self.calcular_area_sold()[0],
            "area_sold_ecuacion": self.calcular_area_sold()[1],
            "j_sold": j_sold,
            "j_sold_ecuacion": j_sold_ecuacion,
            "r": r,
            "rx_ecuacion": rx_ecuacion,
            "ry_ecuacion": ry_ecuacion,
            "tao": tao,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "t_min_sold": format(t_min_sold, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "ssy_pieza1": ssy_pieza1,
            "ssy_pieza2": ssy_pieza2,
            "t_min_pieza1": format(t_min_pieza1, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "t_min_pieza2": format(t_min_pieza2, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "t_min": t_min_estatica,
            "conclusion_tmin": conclusion_tmin
        }
        return resultados

    # Carga Combinada debido a una carga excétrica
    def espesor_ccomb_estatica(self):

        # Obtener Fmax, el brazo longitudinal (bl) y el brazo transversal (bt)
        f_max = self.carga["Fmax"]
        bl = self.carga["bl"]
        bt = self.carga["bt"]

        # Calcular los momentos producidos por la fuerza externa
        momento_flector = f_max * bl
        momento_torsor = f_max * bt

        # Cálculo de parámetros geométricos
        area_sold, area_sold_ecuacion = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion
        c = ry
        c_ecuacion = ry_ecuacion

        # Calcular esfuerzo normal aplicado en la junta (En función de t)
        sigma = momento_flector * c / i_sold

        # Calcular esfuerzo cortante en la junta(En función de t)
        tao_primario = f_max / area_sold
        tao_secundario_x = momento_torsor * ry / j_sold
        tao_secundario_y = momento_torsor * rx / j_sold
        tao_x = tao_secundario_x
        tao_y = tao_primario + tao_secundario_y
        tao = sqrt(tao_x ** 2 + tao_y ** 2)
        print(type(tao_secundario_y))
        print(type(tao_secundario_x))

        # Calcular el esfuerzo Von Misses aplicado en la junta (En función de t)
        sigma_von_misses = sqrt(sigma ** 2 + 3 * tao ** 2)

        # SOLDADURA

        # Obtener resistencia a la fluencia del material de aporte (soldadura)
        sy_sold = self.electrodo["Sy"]

        # Despejar tmin_sold de la ecuación de FD
        t_min_sold = self.despejar_espesor_min_fd_estatica(self.fd_min_sold, sy_sold, sigma_von_misses)

        # PIEZA 1

        # Obtener la resistencia a la fluencia de la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]

        # Despejar tmin_pieza1 de la ecuación de FD
        t_min_pieza1 = self.despejar_espesor_min_fd_estatica(self.fd_min_pieza, sy_pieza1, sigma_von_misses)

        # PIEZA 2

        # Obtener la resistencia a la fluencia de la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]

        # Despejar tmin_pieza1 de la ecuación de FD
        t_min_pieza2 = self.despejar_espesor_min_fd_estatica(self.fd_min_pieza, sy_pieza2, sigma_von_misses)

        # Se selecciona el mayor de los espesores calculados
        t_min_estatica = format(max(t_min_sold, t_min_pieza1, t_min_pieza2),
                                '.3f' if self.sistema_unidades == "Internacional" else '.4f')

        # Validar que para la geometría tubular la respuesta no sea absurda
        self.validar_espesor_calculado_tubular(t_min_estatica)

        # Generar mensaje con el espesor minimo obtenido
        conclusion_tmin = self.conclusion_espesor_min(t_min_estatica)

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "bl": bl,
            "bt": bt,
            "tipo_union": self.tipo_union,
            "largo": self.geometria_params["largo"],
            "area_sold": area_sold,
            "area_sold_ecuacion": area_sold_ecuacion,
            "i_sold": i_sold,
            "j_sold": j_sold,
            "rx": rx,
            "ry": ry,
            "c": c,
            "i_sold_ecuacion": i_sold_ecuacion,
            "j_sold_ecuacion": j_sold_ecuacion,
            "rx_ecuacion": rx_ecuacion,
            "ry_ecuacion": ry_ecuacion,
            "c_ecuacion": c_ecuacion,
            "momento_flector": momento_flector,
            "momento_torsor": momento_torsor,
            "sigma": sigma,
            "tao_primario": tao_primario,
            "tao_secundario_x": tao_secundario_x,
            "tao_secundario_y": tao_secundario_y,
            "tao_x": tao_x,
            "tao_y": tao_y,
            "tao": tao,
            "sigma_von_misses": sigma_von_misses,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "t_min_sold": format(t_min_sold, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "t_min_pieza1": format(t_min_pieza1, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "t_min_pieza2": format(t_min_pieza2, '.3f' if self.sistema_unidades == "Internacional" else '.4f'),
            "t_min": t_min_estatica,
            "conclusion_tmin": conclusion_tmin
        }
        return resultados
#######################################################################################################################
