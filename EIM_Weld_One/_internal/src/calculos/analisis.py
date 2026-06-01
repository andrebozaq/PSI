"""
En este módulo se le darán forma a las funciones necesarias para ejecutar los cálculos de análisis
"""
from math import pi, sqrt
from sympy import symbols, solve


# Calcular la resistencia el esfuerzo cortante admisible del material de aporte
def calcular_tao_adm_ma(resistencia_ultima_electrodo):
    tao_adm_ma = 0.30 * resistencia_ultima_electrodo
    return tao_adm_ma


# Comparar el FS de la soldadura con el FDmin
def comparar_fs_soldadura(fs_soldadura, estatica_o_fatiga):
    if fs_soldadura < 1:
        conclusion = f"""No cumple con el factor de diseño mínimo (FDmin-sold = 3.33) recomendado en la cátedra EMI. La soldadura falla por carga {estatica_o_fatiga}."""
    elif 1 <= fs_soldadura < 3.33:
        conclusion = """La soldadura no cumple con el factor de diseño mínimo (FDmin-sold = 3.33) recomendado en la cátedra EMI, pero no es limitante. Queda a criterio del diseñador si se acepta o no."""
    else:
        conclusion = f"""La soldadura, para carga {estatica_o_fatiga}, cumple con los requisitos de funcionamiento y seguridad (FDmin-sold = 3.33)."""

    return conclusion


# Comparar el FS de la pieza 1 con el FDmin
def comparar_fs_pieza1(fs_pieza1, estatica_o_fatiga):
    if fs_pieza1 < 1:
        conclusion = f"""No cumple con el factor de diseño mínimo (FDmin-pieza = 2.5) recomendado en la cátedra EMI. La pieza 1 falla por carga {estatica_o_fatiga}."""
    elif 1 <= fs_pieza1 < 2.5:
        conclusion = """La pieza 1 no cumple con el factor de diseño mínimo (FDmin-pieza = 2.5) recomendado en la cátedra EMI, pero no es limitante. Queda a criterio del diseñador si se acepta o no."""
    else:
        conclusion = f"""La pieza 1, para carga {estatica_o_fatiga}, cumple con los requisitos de funcionamiento y seguridad (FDmin-pieza = 2.5)."""

    return conclusion


# Comparar el FS de la pieza 1 con el FDmin
def comparar_fs_pieza2(fs_pieza2, estatica_o_fatiga):
    if fs_pieza2 < 1:
        conclusion = f"""No cumple con el factor de diseño mínimo (FDmin-pieza = 2.5) recomendado en la cátedra EMI. La pieza 2 falla por carga {estatica_o_fatiga}."""
    elif 1 <= fs_pieza2 < 2.5:
        conclusion = """La pieza 2 no cumple con el factor de diseño mínimo (FDmin-pieza = 2.5) recomendado en la cátedra EMI, pero no es limitante. Queda a criterio del diseñador si se acepta o no."""
    else:
        conclusion = f"""La pieza 2, para carga {estatica_o_fatiga}, cumple con los requisitos de funcionamiento y seguridad (FDmin-pieza = 2.5)."""

    return conclusion


#####################################################################################################################
# CÁLCULOS GENERALES PARA ANÁLISIS DE FATIGA

# Calcular carga alternante y media (Puede ser fuerza, momento flector o momento torsor)
def calcular_carga_alt_y_med(carga_max, carga_min):
    carga_alt = (carga_max - carga_min) / 2
    carga_med = (carga_max + carga_min) / 2
    return carga_alt, carga_med


# Calcular momento máximo y momento mínimo
def calcular_momento_max_y_min(f_max, f_min, b):
    momento_max = f_max * b
    momento_min = f_min * b
    return momento_max, momento_min


# Calcular la resistencia a la fatiga (Se o Sse)
def calcular_resistencia_fatiga(sistema_unidades, resistencia_ultima):

    # Factor de superficie, Ka
    a_valores = {"Internacional": 271, "Inglés": 39.8}
    a = a_valores[sistema_unidades]
    b = -0.995
    if sistema_unidades == "Internacional":
        ka = a * resistencia_ultima ** b
    else:
        ka = a * (resistencia_ultima/1000) ** b

    # Factor de tamaño, Kb
    kb = 1

    # Factor de carga, Kc
    alfa_valores = {"Internacional": 0.258, "Inglés": 0.328}
    alfa = alfa_valores[sistema_unidades]
    beta = 0.125
    if sistema_unidades == "Internacional":
        kc = alfa * resistencia_ultima ** beta
    else:
        kc = alfa * (resistencia_ultima/1000) ** beta

    # Factor de modificacion de la temperatura, Kd
    kd = 1

    # Factor de modificación de efectos diversos, Ke
    ke = 1

    # Límite de resistencia a la fatiga de la viga rotatoria, Se'
    if sistema_unidades == "Internacional":  # Mpa
        if resistencia_ultima <= 1460:
            resistencia_viga_rotatoria = 0.506 * resistencia_ultima
        else:
            resistencia_viga_rotatoria = 740
    else:  # Sistema inglés (psi)
        if resistencia_ultima <= 212000:
            resistencia_viga_rotatoria = 0.506 * resistencia_ultima
        else:
            resistencia_viga_rotatoria = 107000

    # Ecuación para calcular la resistencia a la fatiga, Se o Sse
    resistencia_fatiga = ka * kb * kc * kd * ke * resistencia_viga_rotatoria

    return resistencia_fatiga


# Calcular la resistencia última al cortante (Ssu)
def calcular_resistencia_ultima_al_cortante(resistencia_ultima):
    ssu = 0.67 * resistencia_ultima
    return ssu


# Resolver la ecuación de Gerber para obtener el FS
def resolver_ecuacion_gerber(esfuerzo_alternante, esfuerzo_medio, resistencia_fatiga, resistencia_ultima):
    # Definir la variable a calcular
    fs = symbols("fs")

    # Definir la ecuación
    ecuacion_gerber = ((fs * esfuerzo_medio / resistencia_ultima) ** 2 + (fs * esfuerzo_alternante / resistencia_fatiga)
                       - 1)

    # Resolver la ecuación
    soluciones_fs = solve(ecuacion_gerber, fs)

    # Seleccionar la solución positiva de la ecuación
    for solucion in soluciones_fs:
        if solucion.is_real and solucion > 0:
            return solucion


#####################################################################################################################
# SOLDADURA DE FILETE

class AnalisisSoldaduraFilete:
    def __init__(self, sistema_unidades, tipo_union, carga, material_base_1, material_base_2, electrodo, geometria,
                 geometria_params, espesor_menor_piezas):
        self.sistema_unidades = sistema_unidades
        self.tipo_union = tipo_union
        self.carga = carga
        self.material_base_1 = material_base_1
        self.material_base_2 = material_base_2
        self.electrodo = electrodo
        self.geometria = geometria
        self.geometria_params = geometria_params
        self.espesor_menor_piezas = espesor_menor_piezas

    def __str__(self):
        return "Análisis de Soldadura de Filete"

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

    # GEOMETRIA

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

    # Verificar el tamaño mínimo de la pierna del cordón de soldadura al terminar el análisis de la soldadura
    def verificar_tamano_minimo_pierna_analisis(self):
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
                if 1/8 <= h <= t_menor:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 1/8 pulg.
        Como h = {h} pulg, entonces cumple con la especificación de la norma AWS."""
                elif h < 1/8:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 1/8 pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
                elif h > t_menor:
                    conclusion = f"""El valor de h no debe exceder el espesor de la pieza más delgada, e = {t_menor} pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
            elif 1 / 4 < t_menor <= 1 / 2:
                if 3/16 <= h <= t_menor:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 3/16 pulg.
        Como h = {h} pulg, entonces cumple con la especificación de la norma AWS."""
                elif h < 3/16:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 3/16 pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
                elif h > t_menor:
                    conclusion = f"""El valor de h no debe exceder el espesor de la pieza más delgada, e = {t_menor} pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
            elif 1/2 < t_menor <= 3/4:
                if 1/4 <= h <= t_menor:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 1/4 pulg.
        Como h = {h} pulg, entonces cumple con la especificación de la norma AWS."""
                elif h < 1/4:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 1/4 pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
                elif h > t_menor:
                    conclusion = f"""El valor de h no debe exceder el espesor de la pieza más delgada, e = {t_menor} pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
            elif t_menor > 3 / 4:
                if 5/16 <= h <= t_menor:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 5/16 pulg.
        Como h = {h} pulg, entonces cumple con la especificación de la norma AWS."""
                elif h < 5/16:
                    conclusion = f"""Para un espesor e = {t_menor} pulg, hmin = 5/16 pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""
                elif h > t_menor:
                    conclusion = f"""El valor de h no debe exceder el espesor de la pieza más delgada, e = {t_menor} pulg.
        Como h = {h} pulg, entonces no cumple con la especificación de la norma AWS."""

        return conclusion

    ###################################################################################################################
    # ANALISIS ESTÁTICO

    # Carga Paralela
    def analisis_estatico_cp(self):

        carga_f = self.carga["Fmax"]
        area_sold = self.calcular_area_sold()

        # Calcular el FS en la soldadura
        tao_admisible_sold = calcular_tao_adm_ma(self.electrodo["Sut"])
        tao_sold = 1.414 * carga_f / area_sold
        fs_soldadura = tao_admisible_sold / tao_sold

        # Comparar el FS con el FDmínimo (FDmin = 3.33)
        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "estática")

        # Calcular FS en la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1
        tao_pieza1 = carga_f / area_sold
        fs_pieza1 = ssy_pieza1 / tao_pieza1

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "estática")

        # Calcular FS en la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]
        ssy_pieza2 = 0.577 * sy_pieza2
        tao_pieza2 = carga_f / area_sold
        fs_pieza2 = ssy_pieza2 / tao_pieza2

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "estática")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna_analisis()

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": carga_f,
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
            "tao_sold": round(tao_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "ssy_pieza1": round(ssy_pieza1, 2),
            "ssy_pieza2": round(ssy_pieza2, 2),
            "tao_pieza1": round(tao_pieza1, 2),
            "tao_pieza2": round(tao_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2,
            "verificacion_pierna": verificacion_pierna
        }

        return falla, resultados

    # Carga Transversal
    def analisis_estatico_ctrans(self):

        carga_f = self.carga["Fmax"]
        area_sold = self.calcular_area_sold()

        # Calcular el FS en la soldadura

        tao_admisible_sold = calcular_tao_adm_ma(self.electrodo["Sut"])
        tao_sold = 1.414 * carga_f / area_sold
        fs_soldadura = tao_admisible_sold / tao_sold

        # Comparar el FS con el FDmínimo (FDmin = 3.33)

        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "estática")

        # Calcular FS en la pieza 1 (Pieza P).
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1
        tao_pieza1 = carga_f / area_sold
        fs_pieza1 = ssy_pieza1 / tao_pieza1

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "estática")

        # Calcular FS en la pieza 2 (Pieza T)
        sy_pieza2 = self.material_base_2["Sy"]
        sigma_pieza2 = carga_f / area_sold
        fs_pieza2 = sy_pieza2 / sigma_pieza2

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "estática")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna_analisis()

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": carga_f,
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
            "tao_sold": round(tao_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "ssy_pieza1": round(ssy_pieza1, 2),
            "tao_pieza1": round(tao_pieza1, 2),
            "sigma_pieza2": round(sigma_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2,
            "verificacion_pierna": verificacion_pierna
        }

        return falla, resultados

    # Carga de Flexión debido a una fuerza excéntrica
    def analisis_estatico_cflex(self):

        carga_f = self.carga["Fmax"]
        brazo = self.carga["b"]
        area_sold = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia_sold()
        i_pieza, i_pieza_ecuacion = self.calcular_momento_inercia_pieza()
        c = self.obtener_rx_ry()[1]
        c_ecuacion = self.obtener_rx_ry()[2][1]
        momento_flector = carga_f * brazo

        # Calcular FS en la soldadura

        tao_admisible_sold = calcular_tao_adm_ma(self.electrodo["Sut"])
        tao_primario = 1.414 * carga_f / area_sold
        tao_secundario = momento_flector * c / i_sold
        tao_sold = sqrt(tao_primario ** 2 + tao_secundario ** 2)
        fs_soldadura = tao_admisible_sold / tao_sold

        # Comparar el FS con el FDmínimo (FDmin = 3.33)

        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "estática")

        # Calcular FS en la pieza 1 (Pieza P).
        sy_pieza1 = self.material_base_1["Sy"]
        sigma_p = momento_flector * c / i_pieza
        tao_p = carga_f / area_sold
        sigma_von_misses_1 = sqrt(sigma_p ** 2 + 3 * tao_p ** 2)
        fs_pieza1 = sy_pieza1 / sigma_von_misses_1

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "estática")

        # Calcular FS en la pieza 2 (Pieza T)
        sy_pieza2 = self.material_base_2["Sy"]
        sigma_t = tao_p
        tao_t = sigma_p
        sigma_von_misses_2 = sqrt(sigma_t ** 2 + 3 * tao_t ** 2)
        fs_pieza2 = sy_pieza2 / sigma_von_misses_2

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "estática")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna_analisis()

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": carga_f,
            "b": brazo,
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
            "momento_flector": round(momento_flector, 2),
            "tao_primario": round(tao_primario, 2),
            "tao_secundario": round(tao_secundario, 2),
            "tao_sold": round(tao_sold, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sigma_p": round(sigma_p, 2),
            "tao_p": round(tao_p, 2),
            "sigma_t": round(sigma_t, 2),
            "tao_t": round(tao_t, 2),
            "sigma_von_misses_1": round(sigma_von_misses_1, 2),
            "sigma_von_misses_2": round(sigma_von_misses_2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2,
            "verificacion_pierna": verificacion_pierna
        }

        return falla, resultados

    # Carga de Torsión debido a una fuerza excéntrica
    def analisis_estatico_ctor(self):

        carga_f = self.carga["Fmax"]
        brazo = self.carga["b"]
        area_sold = self.calcular_area_sold()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar_sold()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion
        momento_torsor = carga_f * brazo

        if self.geometria == "ocho":
            ry, rx, ry_rx_ecuacion = self.obtener_rx_ry()
            ry_ecuacion, rx_ecuacion = ry_rx_ecuacion

        # Calcular FS en la soldadura

        tao_admisible_sold = calcular_tao_adm_ma(self.electrodo["Sut"])
        tao_primario = 1.414 * carga_f / area_sold
        tao_secundario_x = momento_torsor * ry / j_sold
        tao_secundario_y = momento_torsor * rx / j_sold
        tao_x = tao_secundario_x
        tao_y = tao_primario + tao_secundario_y
        tao_sold = sqrt(tao_x ** 2 + tao_y ** 2)
        fs_soldadura = tao_admisible_sold / tao_sold

        # Comparar el FS con el FDmínimo (FDmin = 3.33)

        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "estática")

        # Calcular FS en la pieza 1 (Pieza P)
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1
        tao_p = carga_f / area_sold
        fs_pieza1 = ssy_pieza1 / tao_p

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "estática")

        sy_pieza2 = self.material_base_2["Sy"]
        sigma_t = tao_p
        fs_pieza2 = sy_pieza2 / sigma_t

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "estática")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna_analisis()

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": carga_f,
            "b": brazo,
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
            "momento_torsor": round(momento_torsor, 2),
            "tao_primario": round(tao_primario, 2),
            "tao_secundario_x": round(tao_secundario_x, 2),
            "tao_secundario_y": round(tao_secundario_y, 2),
            "tao_x": round(tao_x, 2),
            "tao_y": round(tao_y, 2),
            "tao_sold": round(tao_sold, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "ssy_pieza1": ssy_pieza1,
            "tao_p": round(tao_p, 2),
            "sigma_t": round(sigma_t, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2,
            "verificacion_pierna": verificacion_pierna
        }

        return falla, resultados

    # Carga Combinada debido a uan fuerza excéntrica
    def analisis_estatico_ccomb(self):

        carga_f = self.carga["Fmax"]
        brazo_longitudinal = self.carga["bl"]
        brazo_transversal = self.carga["bt"]
        area_sold = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia_sold()
        i_pieza, i_pieza_ecuacion = self.calcular_momento_inercia_pieza()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar_sold()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        c = ry
        c_ecuacion = rx_ry_ecuacion[1]

        momento_flector = carga_f * brazo_longitudinal
        momento_torsor = carga_f * brazo_transversal

        # Calcular FS en la soldadura

        sy_sold = self.electrodo["Sy"]
        sut_sold = self.electrodo["Sut"]
        tao_admisible_sold = calcular_tao_adm_ma(self.electrodo["Sut"])
        tao_primario = 1.414 * carga_f / area_sold
        tao_secundario = momento_flector * c / i_sold
        tao_terciario_x = momento_torsor * ry / j_sold
        tao_terciario_y = momento_torsor * rx / j_sold
        tao_x = tao_terciario_x
        tao_y = tao_primario + tao_terciario_y
        tao_z = tao_secundario
        tao_sold = sqrt(tao_x ** 2 + tao_y ** 2 + tao_z ** 2)
        fs_soldadura = tao_admisible_sold / tao_sold

        # Comparar el FS con el FDmínimo (FDmin = 3.33)
        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "estática")

        # Calcular FS en la pieza 1 (Pieza P)
        sy_pieza1 = self.material_base_1["Sy"]
        sigma_p = momento_flector * c / i_pieza
        tao_p = carga_f / area_sold
        sigma_von_misses_1 = sqrt(sigma_p ** 2 + 3 * tao_p ** 2)
        fs_pieza1 = sy_pieza1 / sigma_von_misses_1

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "estática")

        # Calcular FS en la pieza 2 (Pieza T)
        sy_pieza2 = self.material_base_2["Sy"]
        sigma_t = tao_p
        tao_t = sigma_p
        sigma_von_misses_2 = sqrt(sigma_t ** 2 + 3 * tao_t ** 2)
        fs_pieza2 = sy_pieza2 / sigma_von_misses_2

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "estática")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna_analisis()

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": carga_f,
            "bl": brazo_longitudinal,
            "bt": brazo_transversal,
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
            "momento_flector": round(momento_flector, 2),
            "momento_torsor": round(momento_torsor, 2),
            "tao_primario": round(tao_primario, 2),
            "tao_secundario": round(tao_secundario, 2),
            "tao_terciario_x": round(tao_terciario_x, 2),
            "tao_terciario_y": round(tao_terciario_y, 2),
            "tao_x": round(tao_x, 2),
            "tao_y": round(tao_y, 2),
            "tao_z": round(tao_z, 2),
            "tao_sold": round(tao_sold, 2),
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "sy_sold": sy_sold,
            "sut_sold": sut_sold,
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sigma_p": round(sigma_p, 2),
            "tao_p": round(tao_p, 2),
            "sigma_t": round(sigma_t, 2),
            "tao_t": round(tao_t, 2),
            "sigma_von_misses_1": round(sigma_von_misses_1, 2),
            "sigma_von_misses_2": round(sigma_von_misses_2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2,
            "verificacion_pierna": verificacion_pierna
        }

        return falla, resultados

    ###################################################################################################################
    # ANALISIS DE FATIGA

    # Carga Paralela
    def analisis_fatiga_cp(self):

        # Obtener cargas max y min
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]

        # Calcular cargas alternantes y medias
        f_alt, f_med = calcular_carga_alt_y_med(f_max, f_min)

        # Factor de concentración de esfuerzo reducido, Kfs (Se considera carga paralela con unión intermedia)
        kfs = 2.7

        # Area de la soldadura
        area_sold = self.calcular_area_sold()

        # Calcular esfuerzo cortante alternante y medio en la soldadura
        tao_alt_sold = kfs * 1.414 * f_alt / area_sold
        tao_med_sold = 1.414 * f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = calcular_resistencia_ultima_al_cortante(sut_sold)

        # Calcular FSsold
        fs_soldadura = resolver_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold)

        # Comparar el FS con el FDmínimo (FDmin = 3.33)
        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "de fatiga")

        # Analizar pieza 1

        # Calcular esfuerzo cortante alternante y medio en la pieza 1
        tao_alt_pieza1 = kfs * f_alt / area_sold
        tao_med_pieza1 = f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia ultima al cortante del material base 1
        ssu_pieza1 = calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Calcular FSpieza1
        fs_pieza1 = resolver_ecuacion_gerber(tao_alt_pieza1, tao_med_pieza1, sse_pieza1, ssu_pieza1)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "de fatiga")

        # Analizar pieza 2

        # Calcular esfuerzo cortante alternante y medio en la pieza 2
        tao_alt_pieza2 = kfs * f_alt / area_sold
        tao_med_pieza2 = f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        sse_pieza2 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular la resistencia ultima al cortante del material base 2
        ssu_pieza2 = calcular_resistencia_ultima_al_cortante(sut_pieza2)

        # Calcular FSpieza2
        fs_pieza2 = resolver_ecuacion_gerber(tao_alt_pieza2, tao_med_pieza2, sse_pieza2, ssu_pieza2)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "de fatiga")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna_analisis()

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
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
            "tao_alt_sold": round(tao_alt_sold, 2),
            "tao_med_sold": round(tao_med_sold, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "tao_alt_pieza1": round(tao_alt_pieza1, 2),
            "tao_med_pieza1": round(tao_med_pieza1, 2),
            "tao_alt_pieza2": round(tao_alt_pieza2, 2),
            "tao_med_pieza2": round(tao_med_pieza2, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "sse_pieza2": round(sse_pieza2, 2),
            "ssu_pieza2": round(ssu_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2,
            "verificacion_pierna": verificacion_pierna
        }

        return falla, resultados

    # Carga Transversal
    def analisis_fatiga_ctrans(self):

        # Obtener cargas max y min
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]

        # Calcular cargas alternantes y medias
        f_alt, f_med = calcular_carga_alt_y_med(f_max, f_min)

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Intermedia": 1.5, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Area de la soldadura
        area_sold = self.calcular_area_sold()

        # Calcular esfuerzo cortante alternante y medio en la soldadura
        tao_alt_sold = kfs * 1.414 * f_alt / area_sold
        tao_med_sold = 1.414 * f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = calcular_resistencia_ultima_al_cortante(sut_sold)

        # Calcular FSsold
        fs_soldadura = resolver_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold)

        # Comparar el FS con el FDmínimo (FDmin = 3.33)
        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "de fatiga")

        # Analizar pieza 1 (Pieza P)

        # Calcular esfuerzo cortante alterante y medio en la pieza 1
        tao_p_alt = kfs * f_alt / area_sold
        tao_p_med = f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia ultima al cortante del material base 1
        ssu_pieza1 = calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Calcular FSpieza1
        fs_pieza1 = resolver_ecuacion_gerber(tao_p_alt, tao_p_med, sse_pieza1, ssu_pieza1)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "de fatiga")

        # Analizar pieza 2 (Pieza T)

        # Calcular esfuerzo cortante alterante y medio en la pieza 2
        sigma_t_alt = kfs * f_alt / area_sold
        sigma_t_med = f_med / area_sold

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular FSpieza2
        fs_pieza2 = resolver_ecuacion_gerber(sigma_t_alt, sigma_t_med, se_pieza2, sut_pieza2)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "de fatiga")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna_analisis()

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
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
            "tao_alt_sold": round(tao_alt_sold, 2),
            "tao_med_sold": round(tao_med_sold, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "tao_p_alt": round(tao_p_alt, 2),
            "tao_p_med": round(tao_p_med, 2),
            "sigma_t_alt": round(sigma_t_alt, 2),
            "sigma_t_med": round(sigma_t_med, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2,
            "verificacion_pierna": verificacion_pierna
        }

        return falla, resultados

    # Carga de Flexión debido a una fuerza excéntrica
    def analisis_fatiga_cflex(self):

        # Obtener cargas max y min, y el brazo
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]
        b = self.carga["b"]
        momento_flector_max, momento_flector_min = calcular_momento_max_y_min(f_max, f_min, b)

        # Calcular cargas alternantes y medias
        f_alt, f_med = calcular_carga_alt_y_med(f_max, f_min)
        momento_flector_alt, momento_flector_med = calcular_carga_alt_y_med(momento_flector_max, momento_flector_min)

        # Factor de concentración de esfuerzo reducido, Kfs (Se considera carga transversal y unión T)
        kfs = 2

        # Cálculo de parámetros geométricos
        area_sold = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia_sold()
        i_pieza, i_pieza_ecuacion = self.calcular_momento_inercia_pieza()
        c = self.obtener_rx_ry()[1]
        c_ecuacion = self.obtener_rx_ry()[2][1]

        # Calcular esfuerzos cortante primario alternante y medio en la soldadura
        tao_primario_alt = kfs * 1.414 * f_alt / area_sold
        tao_primario_med = 1.414 * f_med / area_sold

        # Calcular esfuerzo cortante secundadario alternante y medio en la soldadura
        tao_secundario_alt = kfs * momento_flector_alt * c / i_sold
        tao_secundario_med = momento_flector_med * c / i_sold

        # Calcular el esfuerzo cortante resultante alternante y medio en la soldadura
        tao_alt_sold = sqrt(tao_primario_alt ** 2 + tao_secundario_alt ** 2)
        tao_med_sold = sqrt(tao_primario_med ** 2 + tao_secundario_med ** 2)

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = calcular_resistencia_ultima_al_cortante(sut_sold)

        # Calcular FSsold
        fs_soldadura = resolver_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold)

        # Comparar el FS con el FDmínimo (FDmin = 3.33)
        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "de fatiga")

        # Analizar pieza 1 (Pieza P)

        # Calcular esfuerzo normal alternante y medio en la pieza 1
        sigma_p_alt = kfs * momento_flector_alt * c / i_pieza
        sigma_p_med = momento_flector_med * c / i_pieza

        # Calcular esfuerzo cortante alternante y medio en la pieza 1
        tao_p_alt = kfs * f_alt / area_sold
        tao_p_med = f_med / area_sold

        # Calcular el esfuerzo de Von Misses alternante y medio en la pieza 1
        sigma_p_von_misses_alt = sqrt(sigma_p_alt ** 2 + 3 * tao_p_alt ** 2)
        sigma_p_von_misses_med = sqrt(sigma_p_med ** 2 + 3 * tao_p_med ** 2)

        # Calcular la resistencia a la fatiga de la pieza 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular FSpieza1
        fs_pieza1 = resolver_ecuacion_gerber(sigma_p_von_misses_alt, sigma_p_von_misses_med, se_pieza1, sut_pieza1)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "de fatiga")

        # Analizar pieza 2 (Pieza T)

        # Calcular esfuerzo normal alternante y medio en la pieza 2
        sigma_t_alt = tao_p_alt
        sigma_t_med = tao_p_med

        # Calcular esfuerzo cortante alternante y medio en la pieza 2
        tao_t_alt = sigma_p_alt
        tao_t_med = sigma_p_med

        # Calcular el esfuerzo de Von Misses alternante y medio en la pieza 2
        sigma_t_von_misses_alt = sqrt(sigma_t_alt ** 2 + 3 * tao_t_alt ** 2)
        sigma_t_von_misses_med = sqrt(sigma_t_med ** 2 + 3 * tao_t_med ** 2)

        # Calcular la resistencia a la fatiga de la pieza 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular FSpieza2
        fs_pieza2 = resolver_ecuacion_gerber(sigma_t_von_misses_alt, sigma_t_von_misses_med, se_pieza2, sut_pieza2)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "de fatiga")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna_analisis()

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "b": b,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "momento_flector_alt": round(momento_flector_alt, 2),
            "momento_flector_med": round(momento_flector_med, 2),
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
            "tao_primario_alt": round(tao_primario_alt, 2),
            "tao_primario_med": round(tao_primario_med, 2),
            "tao_secundario_alt": round(tao_secundario_alt, 2),
            "tao_secundario_med": round(tao_secundario_med, 2),
            "tao_alt_sold": round(tao_alt_sold, 2),
            "tao_med_sold": round(tao_med_sold, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sigma_p_alt": round(sigma_p_alt, 2),
            "sigma_p_med": round(sigma_p_med, 2),
            "tao_p_alt": round(tao_p_alt, 2),
            "tao_p_med": round(tao_p_med, 2),
            "sigma_t_alt": round(sigma_t_alt, 2),
            "sigma_t_med": round(sigma_t_med, 2),
            "tao_t_alt": round(tao_t_alt, 2),
            "tao_t_med": round(tao_t_med, 2),
            "sigma_p_von_misses_alt": round(sigma_p_von_misses_alt, 2),
            "sigma_p_von_misses_med": round(sigma_p_von_misses_med, 2),
            "sigma_t_von_misses_alt": round(sigma_t_von_misses_alt, 2),
            "sigma_t_von_misses_med": round(sigma_t_von_misses_med, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2,
            "verificacion_pierna": verificacion_pierna
        }

        return falla, resultados

    # Carga de Torsión debido a una fuerza excéntrica
    def analisis_fatiga_ctor(self):

        # Obtener cargas max y min, y el brazo
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]
        b = self.carga["b"]
        momento_torsor_max, momento_torsor_min = calcular_momento_max_y_min(f_max, f_min, b)

        # Calcular cargas alternantes y medias
        f_alt, f_med = calcular_carga_alt_y_med(f_max, f_min)
        momento_torsor_alt, momento_torsor_med = calcular_carga_alt_y_med(momento_torsor_max, momento_torsor_min)

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

        # Calcular esfuerzos cortante primario alternante y medio en la soldadura
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

        # Calcular el esfuerzo cortante resultante alternante y medio en la soldadura
        tao_alt_sold = sqrt(tao_alt_x ** 2 + tao_alt_y ** 2)
        tao_med_sold = sqrt(tao_med_x ** 2 + tao_med_y ** 2)

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = calcular_resistencia_ultima_al_cortante(sut_sold)

        # Calcular FSsold
        fs_soldadura = resolver_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold)

        # Comparar el FS con el FDmínimo (FDmin = 3.33)
        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "de fatiga")

        # Analizar pieza 1 (Pieza P)

        # Calcular esfuerzo cortante alternante y medio en la pieza 1
        tao_p_alt = kfs * f_alt / area_sold
        tao_p_med = f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante de la pieza 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia ultima al cortante de la pieza 1
        ssu_pieza1 = calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Calcular FSpieza1
        fs_pieza1 = resolver_ecuacion_gerber(tao_p_alt, tao_p_med, sse_pieza1, ssu_pieza1)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "de fatiga")

        # Analizar pieza 2 (Pieza T)

        # Calcular esfuerzo normal alternante y medio en la pieza 2
        sigma_t_alt = tao_p_alt
        sigma_t_med = tao_p_med

        # Calcular la resistencia a la fatiga de la pieza 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular FSpieza2
        fs_pieza2 = resolver_ecuacion_gerber(sigma_t_alt, sigma_t_med, se_pieza2, sut_pieza2)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "de fatiga")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna_analisis()

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "b": b,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "momento_torsor_alt": round(momento_torsor_alt, 2),
            "momento_torsor_med": round(momento_torsor_med, 2),
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
            "tao_primario_alt": round(tao_primario_alt, 2),
            "tao_primario_med": round(tao_primario_med, 2),
            "tao_secundario_alt_x": round(tao_secundario_alt_x, 2),
            "tao_secundario_alt_y": round(tao_secundario_alt_y, 2),
            "tao_secundario_med_x": round(tao_secundario_med_x, 2),
            "tao_secundario_med_y": round(tao_secundario_med_y, 2),
            "tao_alt_x": round(tao_alt_x, 2),
            "tao_alt_y": round(tao_alt_y, 2),
            "tao_med_x": round(tao_med_x, 2),
            "tao_med_y": round(tao_med_y, 2),
            "tao_alt_sold": round(tao_alt_sold, 2),
            "tao_med_sold": round(tao_med_sold, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "tao_p_alt": round(tao_p_alt, 2),
            "tao_p_med": round(tao_p_med, 2),
            "sigma_t_alt": round(sigma_t_alt, 2),
            "sigma_t_med": round(sigma_t_med, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2,
            "verificacion_pierna": verificacion_pierna
        }

        return falla, resultados

    # Carga Combinada debido a uan fuerza excéntrica
    def analisis_fatiga_ccomb(self):

        # Obtener cargas max y min, el brazo longitudinal (bl) y el brazo transversal (bt)
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]
        bl = self.carga["bl"]
        bt = self.carga["bt"]
        momento_flector_max, momento_flector_min = calcular_momento_max_y_min(f_max, f_min, bl)
        momento_torsor_max, momento_torsor_min = calcular_momento_max_y_min(f_max, f_min, bt)

        # Calcular cargas alternantes y medias
        f_alt, f_med = calcular_carga_alt_y_med(f_max, f_min)
        momento_flector_alt, momento_flector_med = calcular_carga_alt_y_med(momento_flector_max, momento_flector_min)
        momento_torsor_alt, momento_torsor_med = calcular_carga_alt_y_med(momento_torsor_max, momento_torsor_min)

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

        # Calcular esfuerzo cortante primario alternante y medio en la soldadura
        tao_primario_alt = kfs * 1.414 * f_alt / area_sold
        tao_primario_med = 1.414 * f_med / area_sold

        # Calcular esfuerzo cortante secundario alternante y medio en la soldadura
        tao_secundario_alt = kfs * momento_flector_alt * c / i_sold
        tao_secundario_med = momento_flector_med * c / i_sold

        # Calcular las componentes x e y del esfuerzo cortante terciario alternante en la soldadura
        tao_terciario_alt_x = kfs * momento_torsor_alt * ry / j_sold
        tao_terciario_alt_y = kfs * momento_torsor_alt * rx / j_sold

        # Calcular las componentes x e y del esfuerzo cortante terciario medio en la soldadura
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

        # Calcular el esfuerzo cortante resultante alternante y medio en la soldadura
        tao_alt_sold = sqrt(tao_alt_x ** 2 + tao_alt_y ** 2 + tao_alt_z ** 2)
        tao_med_sold = sqrt(tao_med_x ** 2 + tao_med_y ** 2 + tao_med_z ** 2)

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = calcular_resistencia_ultima_al_cortante(sut_sold)

        # Calcular FSsold
        fs_soldadura = resolver_ecuacion_gerber(tao_alt_sold, tao_med_sold, sse_sold, ssu_sold)

        # Comparar el FS con el FDmínimo (FDmin = 3.33)
        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "de fatiga")

        # Analizar pieza 1 (Pieza P)

        # Calcular esfuerzo normal alternante y medio en la pieza 1
        sigma_p_alt = kfs * momento_flector_alt * c / i_pieza
        sigma_p_med = momento_flector_med * c / i_pieza

        # Calcular esfuerzo cortante alternante y medio en la pieza 1
        tao_p_alt = kfs * f_alt / area_sold
        tao_p_med = f_med / area_sold

        # Calcular el esfuerzo de Von Misses alternante y medio en la pieza 1
        sigma_p_von_misses_alt = sqrt(sigma_p_alt ** 2 + 3 * tao_p_alt ** 2)
        sigma_p_von_misses_med = sqrt(sigma_p_med ** 2 + 3 * tao_p_med ** 2)

        # Calcular la resistencia a la fatiga de la pieza 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular FSpieza1
        fs_pieza1 = resolver_ecuacion_gerber(sigma_p_von_misses_alt, sigma_p_von_misses_med, se_pieza1, sut_pieza1)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "de fatiga")

        # Analizar pieza 2 (Pieza T)

        # Calcular esfuerzo normal alternante y medio en la pieza 2
        sigma_t_alt = tao_p_alt
        sigma_t_med = tao_p_med

        # Calcular esfuerzo cortante alternante y medio en la pieza 2
        tao_t_alt = sigma_p_alt
        tao_t_med = sigma_p_med

        # Calcular el esfuerzo de Von Misses alternante y medio en la pieza 2
        sigma_t_von_misses_alt = sqrt(sigma_t_alt ** 2 + 3 * tao_t_alt ** 2)
        sigma_t_von_misses_med = sqrt(sigma_t_med ** 2 + 3 * tao_t_med ** 2)

        # Calcular la resistencia a la fatiga de la pieza 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular FSpieza2
        fs_pieza2 = resolver_ecuacion_gerber(sigma_t_von_misses_alt, sigma_t_von_misses_med, se_pieza2, sut_pieza2)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "de fatiga")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Verificacion del tamaño minimo de la pierna
        verificacion_pierna = self.verificar_tamano_minimo_pierna_analisis()

        # Generar diccionario para informe de resultados
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
            "rx_ecuacion": rx_ry_ecuacion[0],
            "ry_ecuacion": rx_ry_ecuacion[1],
            "c": round(c, 3),
            "c_ecuacion": c_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_primario_alt": round(tao_primario_alt, 2),
            "tao_primario_med": round(tao_primario_med, 2),
            "tao_secundario_alt": round(tao_secundario_alt, 2),
            "tao_secundario_med": round(tao_secundario_med, 2),
            "tao_terciario_alt_x": round(tao_terciario_alt_x, 2),
            "tao_terciario_alt_y": round(tao_terciario_alt_y, 2),
            "tao_terciario_med_x": round(tao_terciario_med_x, 2),
            "tao_terciario_med_y": round(tao_terciario_med_y, 2),
            "tao_alt_x": round(tao_alt_x, 2),
            "tao_alt_y": round(tao_alt_y, 2),
            "tao_alt_z": round(tao_alt_z, 2),
            "tao_med_x": round(tao_med_x, 2),
            "tao_med_y": round(tao_med_y, 2),
            "tao_med_z": round(tao_med_z, 2),
            "tao_alt_sold": round(tao_alt_sold, 2),
            "tao_med_sold": round(tao_med_sold, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sigma_p_alt": round(sigma_p_alt, 2),
            "sigma_p_med": round(sigma_p_med, 2),
            "tao_p_alt": round(tao_p_alt, 2),
            "tao_p_med": round(tao_p_med, 2),
            "sigma_t_alt": round(sigma_t_alt, 2),
            "sigma_t_med": round(sigma_t_med, 2),
            "tao_t_alt": round(tao_t_alt, 2),
            "tao_t_med": round(tao_t_med, 2),
            "sigma_p_von_misses_alt": round(sigma_p_von_misses_alt, 2),
            "sigma_p_von_misses_med": round(sigma_p_von_misses_med, 2),
            "sigma_t_von_misses_alt": round(sigma_t_von_misses_alt, 2),
            "sigma_t_von_misses_med": round(sigma_t_von_misses_med, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2,
            "verificacion_pierna": verificacion_pierna
        }

        return falla, resultados


#######################################################################################################################
# SOLDADURA DE RANURA
class AnalisisSoldaduraRanura:
    def __init__(self, sistema_unidades, tipo_union, carga, material_base_1, material_base_2, electrodo, geometria,
                 geometria_params):
        self.sistema_unidades = sistema_unidades
        self.tipo_union = tipo_union
        self.carga = carga
        self.material_base_1 = material_base_1
        self.material_base_2 = material_base_2
        self.electrodo = electrodo
        self.geometria = geometria
        self.geometria_params = geometria_params

    def __str__(self):
        return "Análisis de Soldadura de Ranura"

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
            "tres": pi * (r_ext**2 - r_int**2)
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
            "uno": (0.0834 * t * l**3),
            "dos": (0.0834 * t**3 * l),
            "tres": (0.25 * pi * (r_ext**4 - r_int**4)),
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
            "uno": (t * l**3 / 12),
            "dos": (t * l**3 / 12),
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
            "uno": (0, l/2),
            "dos": (l/2, 0),
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
            "uno": (t/2, l/2),
            "dos": (l/2, t/2),
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
    # ANALISIS ESTÁTICO

    # Carga Paralela
    def analisis_estatico_cp(self):

        carga_f = self.carga["Fmax"]
        area_sold, area_sold_ecuacion = self.calcular_area_sold()

        # Calcular el FS en la soldadura

        tao_admisible_sold = calcular_tao_adm_ma(self.electrodo["Sut"])
        tao_sold = carga_f / area_sold
        fs_soldadura = tao_admisible_sold / tao_sold

        # Comparar el FS con el FDmínimo (FDmin = 3.33)

        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "estática")

        # Calcular FS en la pieza 1
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1
        tao_pieza1 = tao_sold
        fs_pieza1 = ssy_pieza1 / tao_pieza1

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "estática")

        # Calcular FS en la pieza 2
        sy_pieza2 = self.material_base_2["Sy"]
        ssy_pieza2 = 0.577 * sy_pieza2
        tao_pieza2 = tao_sold
        fs_pieza2 = ssy_pieza2 / tao_pieza2

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "estática")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": carga_f,
            "tipo_union": self.tipo_union,
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "area_sold": round(area_sold, 3),
            "area_sold_ecuacion": area_sold_ecuacion,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "tao_sold": round(tao_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "ssy_pieza1": round(ssy_pieza1, 2),
            "ssy_pieza2": round(ssy_pieza2, 2),
            "tao_pieza1": round(tao_pieza1, 2),
            "tao_pieza2": round(tao_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2
        }

        return falla, resultados

    # Carga Transversal
    def analisis_estatico_ctrans(self):

        carga_f = self.carga["Fmax"]
        area_sold, area_sold_ecuacion = self.calcular_area_sold()

        # Calcular el FS en la soldadura

        sy_sold = self.electrodo["Sy"]
        sigma_sold = carga_f / area_sold
        fs_soldadura = sy_sold / sigma_sold

        # Comparar el FS con el FDmínimo (FDmin = 3.33)

        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "estática")

        # Calcular FS en la pieza 1 (Pieza P).

        sy_pieza1 = self.material_base_1["Sy"]
        sigma_pieza1 = sigma_sold
        fs_pieza1 = sy_pieza1 / sigma_pieza1

        # Comparar con el FDmínimo (FDmin = 2.5)

        conclusion_pieza1 = (
            comparar_fs_pieza1(fs_pieza1, "estática"))

        # Calcular FS en la pieza 2 (Pieza T)
        sy_pieza2 = self.material_base_2["Sy"]
        sigma_pieza2 = sigma_sold
        fs_pieza2 = sy_pieza2 / sigma_pieza2

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "estática")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": carga_f,
            "tipo_union": self.tipo_union,
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "r_ext": self.geometria_params["radio exterior"],
            "area_sold": round(area_sold, 3),
            "area_sold_ecuacion": area_sold_ecuacion,
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "sigma_sold": round(sigma_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sigma_pieza1": round(sigma_pieza1, 2),
            "sigma_pieza2": round(sigma_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2
        }

        return falla, resultados

    # Carga de Flexión debido a una fuerza excéntrica
    def analisis_estatico_cflex(self):

        carga_f = self.carga["Fmax"]
        brazo = self.carga["b"]
        area_sold, area_sold_ecuacion = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia()
        c = self.obtener_rx_ry()[1]
        c_ecuacion = self.obtener_rx_ry()[2][1]
        momento_flector = carga_f * brazo

        # Calcular los esfuerzos aplicados
        tao = carga_f / area_sold
        sigma = momento_flector * c / i_sold
        sigma_von_misses = sqrt(sigma**2 + 3 * tao**2)

        # Calcular el FS en la soldadura
        sy_sold = self.electrodo["Sy"]
        fs_soldadura = sy_sold / sigma_von_misses

        # Comparar el FS con el FDmínimo (FDmin = 3.33)
        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "estática")

        # Calcular FS en la pieza 1 (Pieza P)
        sy_pieza1 = self.material_base_1["Sy"]
        fs_pieza1 = sy_pieza1 / sigma_von_misses

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "estática")

        # Calcular FS en la pieza 2 (Pieza T)
        sy_pieza2 = self.material_base_2["Sy"]
        fs_pieza2 = sy_pieza2 / sigma_von_misses

        # Comparar con el FDmínimo (FDmin = 2.5)

        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "estática")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": carga_f,
            "b": brazo,
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
            "momento_flector": round(momento_flector, 2),
            "tao": round(tao, 2),
            "sigma": round(sigma, 2),
            "sigma_von_misses": round(sigma_von_misses, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2
        }

        return falla, resultados

    # Carga de Torsión
    def analisis_estatico_ctor(self):

        momento_torsor = self.carga["Tmax"]
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion
        r = sqrt(rx**2 + ry**2)

        if self.sistema_unidades == "Internacional":
            momento_torsor = momento_torsor * 1000

        # Calcular el esfuerzo aplicado
        tao = momento_torsor * r / j_sold

        # Calcular el FS en la soldadura
        tao_admisible_sold = calcular_tao_adm_ma(self.electrodo["Sut"])
        fs_soldadura = tao_admisible_sold / tao

        # Comparar el FS con el FDmínimo (FDmin = 3.33)

        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "estática")

        # Calcular FS en la pieza 1 (Pieza P)
        sy_pieza1 = self.material_base_1["Sy"]
        ssy_pieza1 = 0.577 * sy_pieza1
        fs_pieza1 = ssy_pieza1 / tao

        # Comparar con el FDmínimo (FDmin = 2.5)

        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "estática")

        # Calcular FS en la pieza 2 (Pieza T)
        sy_pieza2 = self.material_base_2["Sy"]
        ssy_pieza2 = 0.577 * sy_pieza2
        fs_pieza2 = ssy_pieza2 / tao

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "estática")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Generar diccionario para informe de resultados
        resultados = {
            "Tmax": momento_torsor,
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
            "tao": round(tao, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "tao_adm_sold": round(tao_admisible_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "ssy_pieza1": ssy_pieza1,
            "ssy_pieza2": ssy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2
        }

        return falla, resultados

    # Carga Combinada debido a uan fuerza excéntrica
    def analisis_estatico_ccomb(self):

        carga_f = self.carga["Fmax"]
        bl = self.carga["bl"]
        bt = self.carga["bt"]
        area_sold, area_sold_ecuacion = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia()
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion
        c = ry
        c_ecuacion = ry_ecuacion

        # Calcular el momento flector y el momento torsor aplicado
        momento_flector = carga_f * bl
        momento_torsor = carga_f * bt

        # Calcular los esfuerzos aplicados

        # Esfuerzo cortante
        tao_primario = carga_f / area_sold
        tao_secundario_x = momento_torsor * ry / j_sold
        tao_secundario_y = momento_torsor * rx / j_sold
        tao_x = tao_secundario_x
        tao_y = tao_primario + tao_secundario_y
        tao = sqrt(tao_x ** 2 + tao_y ** 2)

        # Esfuerzo normal
        sigma = momento_flector * c / i_sold

        # Von Misses
        sigma_von_misses = sqrt(sigma ** 2 + 3 * tao ** 2)

        # Calcular FS en la soldadura

        sy_sold = self.electrodo["Sy"]
        fs_soldadura = sy_sold / sigma_von_misses

        # Comparar el FS con el FDmínimo (FDmin = 3.33)

        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "estática")

        # Calcular FS en la pieza 1 (Pieza P).
        sy_pieza1 = self.material_base_1["Sy"]
        fs_pieza1 = sy_pieza1 / sigma_von_misses

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "estática")

        # Calcular FS en la pieza 2 (Pieza T)
        sy_pieza2 = self.material_base_2["Sy"]
        fs_pieza2 = sy_pieza2 / sigma_von_misses

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "estática")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": carga_f,
            "bl": bl,
            "bt": bt,
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
            "momento_flector": round(momento_flector, 2),
            "momento_torsor": round(momento_torsor, 2),
            "tao_primario": round(tao_primario, 2),
            "tao_secundario_x": round(tao_secundario_x, 2),
            "tao_secundario_y": round(tao_secundario_y, 2),
            "tao_x": round(tao_x, 2),
            "tao_y": round(tao_y, 2),
            "tao": round(tao, 2),
            "sigma": round(sigma, 2),
            "sigma_von_misses": round(sigma_von_misses, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": self.electrodo["Sut"],
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": sy_pieza1,
            "sy_pieza2": sy_pieza2,
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2
        }

        return falla, resultados
    ###################################################################################################################
    # ANALISIS DE FATIGA

    # Carga Paralela
    def analisis_fatiga_cp(self):

        # Obtener cargas max y min
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]

        # Calcular cargas alternantes y medias
        f_alt, f_med = calcular_carga_alt_y_med(f_max, f_min)

        # Factor de concentración de esfuerzo reducido, Kfs (Se considera carga paralela con unión tope)
        kfs = 1.2

        # Area de la soldadura
        area_sold, area_sold_ecuacion = self.calcular_area_sold()

        # Calcular esfuerzo cortante alternante y medio
        tao_alt = kfs * f_alt / area_sold
        tao_med = f_med / area_sold

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = calcular_resistencia_ultima_al_cortante(sut_sold)

        # Calcular FSsold
        fs_soldadura = resolver_ecuacion_gerber(tao_alt, tao_med, sse_sold, ssu_sold)

        # Comparar el FS con el FDmínimo (FDmin = 3.33)
        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "de fatiga")

        # Analizar pieza 1

        # Calcular la resistencia a la fatiga al cortante del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia ultima al cortante del material base 1
        ssu_pieza1 = calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Calcular FSpieza1
        fs_pieza1 = resolver_ecuacion_gerber(tao_alt, tao_med, sse_pieza1, ssu_pieza1)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "de fatiga")

        # Analizar pieza 2

        # Calcular la resistencia a la fatiga al cortante del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        sse_pieza2 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular la resistencia ultima al cortante del material base 2
        ssu_pieza2 = calcular_resistencia_ultima_al_cortante(sut_pieza2)

        # Calcular FSpieza2
        fs_pieza2 = resolver_ecuacion_gerber(tao_alt, tao_med, sse_pieza2, ssu_pieza2)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "de fatiga")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "area_sold": round(area_sold, 3),
            "area_sold_ecuacion": area_sold_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_alt": round(tao_alt, 2),
            "tao_med": round(tao_med, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "sse_pieza2": round(sse_pieza2, 2),
            "ssu_pieza2": round(ssu_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2
        }

        return falla, resultados

    # Carga Transversal
    def analisis_fatiga_ctrans(self):

        # Obtener cargas max y min
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]

        # Calcular cargas alternantes y medias
        f_alt, f_med = calcular_carga_alt_y_med(f_max, f_min)

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Tope": 1.2, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Area de la soldadura
        area_sold, area_sold_ecuacion = self.calcular_area_sold()

        # Calcular esfuerzo normal alternante y medio
        sigma_alt = kfs * f_alt / area_sold
        sigma_med = f_med / area_sold

        # Calcular la resistencia a la fatiga del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        se_sold = calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular FSsold
        fs_soldadura = resolver_ecuacion_gerber(sigma_alt, sigma_med, se_sold, sut_sold)

        # Comparar el FS con el FDmínimo (FDmin = 3.33)
        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "de fatiga")

        # Analizar pieza 1

        # Calcular la resistencia a la fatiga del material base 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular FSpieza1
        fs_pieza1 = resolver_ecuacion_gerber(sigma_alt, sigma_med, se_pieza1, sut_pieza1)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "de fatiga")

        # Analizar pieza 2

        # Calcular la resistencia a la fatiga del material base 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular FSpieza2
        fs_pieza2 = resolver_ecuacion_gerber(sigma_alt, sigma_med, se_pieza2, sut_pieza2)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "de fatiga")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "garganta": self.geometria_params["espesor"],
            "largo": self.geometria_params["largo"],
            "r_ext": self.geometria_params["radio exterior"],
            "area_sold": round(area_sold, 3),
            "area_sold_ecuacion": area_sold_ecuacion,
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "sigma_alt": round(sigma_alt, 2),
            "sigma_med": round(sigma_med, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "se_sold": round(se_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2
        }

        return falla, resultados

    # Carga de Flexión debido a una fuerza excéntrica
    def analisis_fatiga_cflex(self):

        # Obtener cargas max y min, y el brazo
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]
        b = self.carga["b"]
        momento_flector_max, momento_flector_min = calcular_momento_max_y_min(f_max, f_min, b)

        # Calcular cargas alternantes y medias
        f_alt, f_med = calcular_carga_alt_y_med(f_max, f_min)
        momento_flector_alt, momento_flector_med = calcular_carga_alt_y_med(momento_flector_max, momento_flector_min)

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Tope": 1.2, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Cálculo de parámetros geométricos
        area_sold, area_sold_ecuacion = self.calcular_area_sold()
        i_sold, i_sold_ecuacion = self.calcular_momento_inercia()
        c = self.obtener_rx_ry()[1]
        c_ecuacion = self.obtener_rx_ry()[2][1]

        # Calcular esfuerzo cortante alternante y medio
        tao_alt = kfs * f_alt / area_sold
        tao_med = f_med / area_sold

        # Calcular esfuerzo normal alternante y medio
        sigma_alt = kfs * momento_flector_alt * c / i_sold
        sigma_med = momento_flector_med * c / i_sold

        # Calcular el esfuerzo de Von Misses alternante y medio
        sigma_von_misses_alt = sqrt(sigma_alt**2 + 3 * tao_alt**2)
        sigma_von_misses_med = sqrt(sigma_med**2 + 3 * tao_med**2)

        # Calcular la resistencia a la fatiga del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        se_sold = calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular FSsold
        fs_soldadura = resolver_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_sold, sut_sold)

        # Comparar el FS con el FDmínimo (FDmin = 3.33)
        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "de fatiga")

        # Analizar pieza 1 (Pieza P)

        # Calcular la resistencia a la fatiga de la pieza 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular FSpieza1
        fs_pieza1 = resolver_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_pieza1, sut_pieza1)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "de fatiga")

        # Analizar pieza 2 (Pieza T)

        # Calcular la resistencia a la fatiga de la pieza 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular FSpieza2
        fs_pieza2 = resolver_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_pieza2, sut_pieza2)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "de fatiga")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Generar diccionario para informe de resultados
        resultados = {
            "Fmax": f_max,
            "Fmin": f_min,
            "f_alt": round(f_alt, 2),
            "f_med": round(f_med, 2),
            "b": b,
            "momento_flector_alt": round(momento_flector_alt, 2),
            "momento_flector_med": round(momento_flector_med, 2),
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
            "tao_alt": round(tao_alt, 2),
            "tao_med": round(tao_med, 2),
            "sigma_alt": round(sigma_alt, 2),
            "sigma_med": round(sigma_med, 2),
            "sigma_von_misses_alt": round(sigma_von_misses_alt, 2),
            "sigma_von_misses_med": round(sigma_von_misses_med, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "se_sold": round(se_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2
        }

        return falla, resultados

    # Carga de Torsión Pura
    def analisis_fatiga_ctor(self):

        # Obtener momento torsor max y min
        momento_torsor_max = self.carga.get("Tmax", 0)
        momento_torsor_min = self.carga.get("Tmin", 0)

        if self.sistema_unidades == "Internacional":
            momento_torsor_max = momento_torsor_max * 1000
            momento_torsor_min = momento_torsor_min * 1000

        # Calcular carga alternante y media
        momento_torsor_alt, momento_torsor_med = calcular_carga_alt_y_med(momento_torsor_max, momento_torsor_min)

        # Factor de concentración de esfuerzo reducido, Kfs
        valores_kfs = {"Tope": 1.2, "Unión T": 2}
        kfs = valores_kfs.get(self.tipo_union)

        # Cálculo de parámetros geométricos
        j_sold, j_sold_ecuacion = self.calcular_momento_inercia_polar()
        rx, ry, rx_ry_ecuacion = self.obtener_rx_ry()
        rx_ecuacion, ry_ecuacion = rx_ry_ecuacion
        r = sqrt(rx**2 + ry**2)

        # Calcular el esfuerzo cortante resultante alternante y medio
        tao_alt = kfs * momento_torsor_alt * r / j_sold
        tao_med = momento_torsor_med * r / j_sold

        # Calcular la resistencia a la fatiga al cortante del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        sse_sold = calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular la resistencia ultima al cortante del material de aporte (soldadura)
        ssu_sold = calcular_resistencia_ultima_al_cortante(sut_sold)

        # Calcular FSsold
        fs_soldadura = resolver_ecuacion_gerber(tao_alt, tao_med, sse_sold, ssu_sold)

        # Comparar el FS con el FDmínimo (FDmin = 3.33)
        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "de fatiga")

        # Analizar pieza 1 (Pieza P)

        # Calcular la resistencia a la fatiga al cortante de la pieza 1
        sut_pieza1 = self.material_base_1["Sut"]
        sse_pieza1 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular la resistencia ultima al cortante de la pieza 1
        ssu_pieza1 = calcular_resistencia_ultima_al_cortante(sut_pieza1)

        # Calcular FSpieza1
        fs_pieza1 = resolver_ecuacion_gerber(tao_alt, tao_med, sse_pieza1, ssu_pieza1)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "de fatiga")

        # Analizar pieza 2 (Pieza T)

        # Calcular la resistencia a la fatiga al cortante de la pieza 2
        sut_pieza2 = self.material_base_2["Sut"]
        sse_pieza2 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular la resistencia ultima al cortante de la pieza 2
        ssu_pieza2 = calcular_resistencia_ultima_al_cortante(sut_pieza2)

        # Calcular FSpieza2
        fs_pieza2 = resolver_ecuacion_gerber(tao_alt, tao_med, sse_pieza2, ssu_pieza2)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "de fatiga")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

        # Generar diccionario para informe de resultados
        resultados = {
            "Tmax": momento_torsor_max,
            "Tmin": momento_torsor_min,
            "Talt": round(momento_torsor_alt, 2),
            "Tmed": round(momento_torsor_med, 2),
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
            "tipo_union": self.tipo_union,
            "kfs": kfs,
            "tao_alt": round(tao_alt, 2),
            "tao_med": round(tao_med, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "sse_sold": round(sse_sold, 2),
            "ssu_sold": round(ssu_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "sse_pieza1": round(sse_pieza1, 2),
            "ssu_pieza1": round(ssu_pieza1, 2),
            "sse_pieza2": round(sse_pieza2, 2),
            "ssu_pieza2": round(ssu_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2
        }

        return falla, resultados

    # Carga Combinada debido a uan fuerza excéntrica
    def analisis_fatiga_ccomb(self):

        # Obtener cargas max y min, el brazo longitudinal (bl) y el brazo transversal (bt)
        f_max = self.carga["Fmax"]
        f_min = self.carga["Fmin"]
        bl = self.carga["bl"]
        bt = self.carga["bt"]
        momento_flector_max, momento_flector_min = calcular_momento_max_y_min(f_max, f_min, bl)
        momento_torsor_max, momento_torsor_min = calcular_momento_max_y_min(f_max, f_min, bt)

        # Calcular cargas alternantes y medias
        f_alt, f_med = calcular_carga_alt_y_med(f_max, f_min)
        momento_flector_alt, momento_flector_med = calcular_carga_alt_y_med(momento_flector_max, momento_flector_min)
        momento_torsor_alt, momento_torsor_med = calcular_carga_alt_y_med(momento_torsor_max, momento_torsor_min)

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

        # Calcular el esfuerzo de Von Misses alternante y medio
        sigma_von_misses_alt = sqrt(sigma_alt ** 2 + 3 * tao_alt ** 2)
        sigma_von_misses_med = sqrt(sigma_med ** 2 + 3 * tao_med ** 2)

        # Calcular la resistencia a la fatiga del material de aporte (soldadura)
        sut_sold = self.electrodo["Sut"]
        se_sold = calcular_resistencia_fatiga(self.sistema_unidades, sut_sold)

        # Calcular FSsold
        fs_soldadura = resolver_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_sold, sut_sold)

        # Comparar el FS con el FDmínimo (FDmin = 3.33)
        conclusion_sold = comparar_fs_soldadura(fs_soldadura, "de fatiga")

        # Analizar pieza 1

        # Calcular la resistencia a la fatiga de la pieza 1
        sut_pieza1 = self.material_base_1["Sut"]
        se_pieza1 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza1)

        # Calcular FSpieza1
        fs_pieza1 = resolver_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_pieza1, sut_pieza1)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza1 = comparar_fs_pieza1(fs_pieza1, "de fatiga")

        # Analizar pieza 2

        # Calcular la resistencia a la fatiga de la pieza 2
        sut_pieza2 = self.material_base_2["Sut"]
        se_pieza2 = calcular_resistencia_fatiga(self.sistema_unidades, sut_pieza2)

        # Calcular FSpieza2
        fs_pieza2 = resolver_ecuacion_gerber(sigma_von_misses_alt, sigma_von_misses_med, se_pieza2, sut_pieza2)

        # Comparar con el FDmínimo (FDmin = 2.5)
        conclusion_pieza2 = comparar_fs_pieza2(fs_pieza2, "de fatiga")

        falla = fs_soldadura < 1 or fs_pieza1 < 1 or fs_pieza2 < 1

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
            "tao_primario_alt": round(tao_primario_alt, 2),
            "tao_primario_med": round(tao_primario_med, 2),
            "tao_secundario_alt_x": round(tao_secundario_alt_x, 2),
            "tao_secundario_alt_y": round(tao_secundario_alt_y, 2),
            "tao_secundario_med_x": round(tao_secundario_med_x, 2),
            "tao_secundario_med_y": round(tao_secundario_med_y, 2),
            "tao_alt_x": round(tao_alt_x, 2),
            "tao_alt_y": round(tao_alt_y, 2),
            "tao_med_x": round(tao_med_x, 2),
            "tao_med_y": round(tao_med_y, 2),
            "tao_alt": round(tao_alt, 2),
            "tao_med": round(tao_med, 2),
            "sigma_alt": round(sigma_alt, 2),
            "sigma_med": round(sigma_med, 2),
            "sigma_von_misses_alt": round(sigma_von_misses_alt, 2),
            "sigma_von_misses_med": round(sigma_von_misses_med, 2),
            "sy_sold": self.electrodo["Sy"],
            "sut_sold": sut_sold,
            "se_sold": round(se_sold, 2),
            "fs_sold": round(fs_soldadura, 2),
            "sy_pieza1": self.material_base_1["Sy"],
            "sy_pieza2": self.material_base_2["Sy"],
            "sut_pieza1": self.material_base_1["Sut"],
            "sut_pieza2": self.material_base_2["Sut"],
            "se_pieza1": round(se_pieza1, 2),
            "se_pieza2": round(se_pieza2, 2),
            "fs_pieza1": round(fs_pieza1, 2),
            "fs_pieza2": round(fs_pieza2, 2),
            "conclusion_sold": conclusion_sold,
            "conclusion_pieza1": conclusion_pieza1,
            "conclusion_pieza2": conclusion_pieza2
        }

        return falla, resultados

    ###################################################################################################################
