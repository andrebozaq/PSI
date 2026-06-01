"""
En este módulo se codificará la lógica para la generación de los infórmenes de resultados
"""

from PyQt5.QtCore import QDateTime
from html import escape
from sympy import Float, Integer, Rational

fecha_actual = QDateTime.currentDateTime()
fecha = fecha_actual.toString("dd/MM/yyyy")


# ANALISIS DE FILETE
def informe_analisis_filete_cp(nombre_proyecto, tipo_carga, dic_resultados_estatica, dic_resultados_fatiga, falla,
                               sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):

    """Esta función le dará forma al informe y resumen de resultados de analisis de soldadura de filete
        sometida a carga paralela"""

    informe = f"""
{"*" * 10} Informe de Análisis de Soldadura de Filete Sometida a Carga Paralela {tipo_carga.capitalize()} {"*" * 10}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
El presente informe muestra los resultados del análisis de soldadura de filete sometida a carga paralela {tipo_carga}. El objetivo del análisis es evaluar si la junta soldada cumple con los requisitos mínimos de seguridad y funcionamiento (FDsoldadura = 3.33, FDpieza = 2.5), de acuerdo a la cátedra EMI, así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n"""  # Introducción

    resumen = ""

    resultados_estatica = f"""
Se procede a analizar la soldadura y las piezas soldadas por carga estática.

    F = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}

Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Garganta (t) = 0.707 * h
            t = {dic_resultados_estatica.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_resultados_estatica["lt_ecuacion"]}
            lt = {dic_resultados_estatica.get("longitud_total", 0)} {und_distancia}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_resultados_estatica.get("area_sold", 0)} {und_distancia}²


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_resultados_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la soldadura:

        τ sold = 1.414 * F / Asold
            τ sold = {dic_resultados_estatica.get("tao_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura:

        FS sold = τ adm / τ sold
            FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}

Conclusión: {dic_resultados_estatica["conclusion_sold"]}


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_resultados_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 1:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_resultados_estatica.get("tao_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de seguridad FS de la pieza 1:

        FS pieza1 = Ssy / τ pieza1
            FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza1"]}


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_resultados_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 2:

        τ pieza2 = F / Asold
            τ pieza2 = {dic_resultados_estatica.get("tao_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de seguridad FS de la pieza 2:

        FS pieza2 = Ssy / τ pieza2
            FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza2"]}\n

"""  # Porción con resultados de cálculos de análisis estático.

    resumen_estatica = f"""
<body>

<h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA ESTÁTICA</h2>
<hr>

<p><strong>Factor de seguridad de la soldadura:</strong></p>

<p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_sold'] >= 3.33 else 'red'};">FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}</p>
<p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_sold", 0)}</p>

<p><strong>Factor de seguridad de la pieza 1:</strong></p>

<p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza1'] >= 2.5 else 'red'}">FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}</p>
<p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza1", 0)}</p>

<p><strong>Factor de seguridad de la pieza 2:</strong></p>

<p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza2'] >= 2.5 else 'red'}">FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}</p>
<p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza2", 0)}</p>

</body>
"""  # Resumen de resultados de análisis estático.

    resumen_fatiga = f"""
<body>

<h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA DE FATIGA</h2>
<hr>

<p><strong>Factor de seguridad de la soldadura:</strong></p>

<p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_resultados_fatiga.get('fs_sold', 0)}</p>
<p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_sold", 0)}</p>

<p><strong>Factor de seguridad de la pieza 1:</strong></p>

<p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}</p>
<p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza1", 0)}</p>

<p><strong>Factor de seguridad de la pieza 2:</strong></p>

<p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}</p>
<p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza2", 0)}</p>

</body>

"""  # Resumen de resultados de análisis de fatiga

    verificacion_pierna_resumen = f"""
        <br>
        <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
        <p>{dic_resultados_estatica.get("verificacion_pierna", 0)}</p>


        """  # Porción con verificación de pierna para el resumen

    verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_resultados_estatica.get("verificacion_pierna", 0)}

"""  # Porción con verificación de pierna

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): {dic_resultados_estatica.get("pierna", 0)} {und_distancia}
        Largo (l) : {dic_resultados_estatica.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_resultados_estatica.get("ancho", 0)} {und_distancia}

    Tipo de union:  Intermedia

    Carga Aplicada:

        Tipo: Estática
        Fuerza = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}

    Espesor menor entre las piezas:

        Espesor (e) = {dic_resultados_estatica.get("espesor_menor_piezas", 0)} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        informe += resultados_estatica

        informe += "Análisis estático completado.\n"

        informe += verificacion_pierna

        resumen += "Tipo de carga aplicada en la junta: Carga Paralela Estática\n"

        resumen += resumen_estatica + verificacion_pierna_resumen

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): {dic_resultados_fatiga.get("pierna", 0)} {und_distancia}
        Largo (l) : {dic_resultados_fatiga.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_resultados_fatiga.get("ancho", 0)} {und_distancia}

    Tipo de union:  Intermedia

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima = {dic_resultados_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima = {dic_resultados_fatiga.get("Fmin", 0)} {und_fuerza}

    Espesor menor entre las piezas:

        Espesor (e): {dic_resultados_fatiga.get("espesor_menor_piezas", 0)} {und_distancia}
"""  # Datos de entrada para de fatiga

        informe += resultados_estatica

        informe += "\nAnálisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga Paralela de Fatiga\n"

        resumen += resumen_estatica

        if not falla:

            informe += f"""
Se procede a analizar la soldadura y las piezas soldadas por carga de fatiga.

Cálculos realizados

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_resultados_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_resultados_fatiga.get("f_med", 0)} {und_fuerza}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de filete de unión intermedia sometida a carga paralela, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_resultados_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * 1.414 * Fa / Asold
            τa = {dic_resultados_fatiga.get("tao_alt_sold", 0)} {und_esfuerzo}

        τm = 1.414 * Fm / Asold
            τm = {dic_resultados_fatiga.get("tao_med_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura utilizando ecuación de Gerber:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS sold = {dic_resultados_fatiga.get("fs_sold", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_sold", 0)}


Para la pieza 1:

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_resultados_fatiga.get("tao_alt_pieza1", 0)} {und_esfuerzo}

        τm = Fm / Asold
            τm = {dic_resultados_fatiga.get("tao_med_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 1 utilizando ecuación de Gerber:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza1", 0)}


Para la pieza 2:

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_resultados_fatiga.get("tao_alt_pieza2", 0)} {und_esfuerzo}

        τm = Fm / Asold
            τm = {dic_resultados_fatiga.get("tao_med_pieza2", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_pieza2", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 2 utilizando ecuación de Gerber:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza2", 0)}

                    """  # Resultados de análisis para carga de fatiga.

            informe += "\nAnálisis de fatiga completado.\n"

            informe += verificacion_pierna

            resumen += resumen_fatiga + verificacion_pierna_resumen

        else:

            informe += verificacion_pierna
            resumen += verificacion_pierna_resumen

    return informe, resumen


def informe_analisis_filete_ct(nombre_proyecto, tipo_carga, dic_resultados_estatica, dic_resultados_fatiga, falla,
                               sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de analisis de soldadura de filete
    sometida a carga transversal"""

    informe = f"""
{"*" * 10} Informe de Análisis de Soldadura de Filete Sometida a Carga Transversal {tipo_carga.capitalize()} {"*" * 10}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados del análisis de soldadura de filete sometida a carga transversal {tipo_carga}. El objetivo del análisis es evaluar si la junta soldada cumple con los requisitos mínimos de seguridad y funcionamiento (FDsoldadura = 3.33, FDpieza = 2.5), de acuerdo a la cátedra EMI, así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n"""  # Introducción

    resumen = ""

    resultados_estatica = f"""
Se procede a analizar la soldadura y las piezas soldadas por carga estática.

    F = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}

Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Garganta (t) = 0.707 * h
            t = {dic_resultados_estatica.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_resultados_estatica["lt_ecuacion"]}
            lt = {dic_resultados_estatica.get("longitud_total", 0)} {und_distancia}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_resultados_estatica.get("area_sold", 0)} {und_distancia}²


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_resultados_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la soldadura:

        τ sold = 1.414 * F / Asold
            τ sold = {dic_resultados_estatica.get("tao_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura:

        FS sold = τ adm / τ sold
            FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}

Conclusión: {dic_resultados_estatica["conclusion_sold"]}


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_resultados_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 1:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_resultados_estatica.get("tao_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de seguridad FS de la pieza 1:

        FS pieza1 = Ssy / τ pieza1
            FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza1"]}


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Resistencia a la fluencia:

        Sy = {dic_resultados_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal en la pieza 2:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_resultados_estatica["sigma_pieza2"]} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 2:

        FS pieza2 = Sy / σ pieza2
            FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza2"]}\n
"""  # Resultados de cálculos de análisis por carga estática

    resumen_estatica = f"""
    <body>

    <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA ESTÁTICA</h2>
    <hr>

    <p><strong>Factor de seguridad de la soldadura:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_sold'] >= 3.33 else 'red'};">FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_sold", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 1:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza1'] >= 2.5 else 'red'}">FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza1", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 2:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza2'] >= 2.5 else 'red'}">FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza2", 0)}</p>

    </body>
    """  # Resumen de resultados de análisis estático.

    resumen_fatiga = f"""
    <body>

    <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA DE FATIGA</h2>
    <hr>

    <p><strong>Factor de seguridad de la soldadura:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_resultados_fatiga.get('fs_sold', 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_sold", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 1:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza1", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 2:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza2", 0)}</p>

    </body>

    """  # Resumen de resultados de análisis de fatiga

    verificacion_pierna_resumen = f"""
            <br>
            <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
            <p>{dic_resultados_estatica.get("verificacion_pierna", 0)}</p>


            """  # Porción con verificación de pierna para el resumen

    verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_resultados_estatica.get("verificacion_pierna", 0)}

    """  # Porción con verificación de tamaño de pierna

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1 (pieza paralela a la carga):
            Acero:  {acero1}
            Sy  =   {dic_resultados_estatica["sy_pieza1"]} {und_esfuerzo}
            Sut =   {dic_resultados_estatica["sut_pieza1"]} {und_esfuerzo}

        Pieza 2 (pieza transversal a la carga):
            Acero:  {acero2}
            Sy  =   {dic_resultados_estatica["sy_pieza2"]} {und_esfuerzo}
            Sut =   {dic_resultados_estatica["sut_pieza2"]} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_estatica["sy_sold"]} {und_esfuerzo}
            Sut =  {dic_resultados_estatica["sut_sold"]} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h) =  {dic_resultados_estatica["pierna"]} {und_distancia}
        Largo (l)  =  {dic_resultados_estatica["largo"]} {und_distancia}
        Ancho (a)  =  {dic_resultados_estatica["ancho"]} {und_distancia}
        Radio (r)  =  {dic_resultados_estatica["radio"]} {und_distancia}

    Tipo de union: {dic_resultados_estatica["tipo_union"]}

    Cargas Aplicadas:

        Tipo: Estática
        Fuerza = {dic_resultados_estatica["Fmax"]} {und_fuerza}

    Espesor menor entre las piezas:

        Espesor (e) = {dic_resultados_estatica["espesor_menor_piezas"]} {und_distancia}
"""  # Unión de porción de informe con datos de entrada para análisis estático

        informe += resultados_estatica

        informe += verificacion_pierna

        informe += "Análisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga Transversal Estática\n"

        resumen += resumen_estatica + verificacion_pierna_resumen

    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_fatiga["sy_pieza1"]} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga["sut_pieza1"]} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_fatiga["sy_pieza2"]} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga["sut_pieza2"]} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_fatiga["sy_sold"]} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga["sut_sold"]} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h) = {dic_resultados_fatiga["pierna"]} {und_distancia}
        Largo (l)  = {dic_resultados_fatiga["largo"]} {und_distancia}
        Ancho (a)  = {dic_resultados_fatiga["ancho"]} {und_distancia}
        Radio (r)  =  {dic_resultados_fatiga["radio"]} {und_distancia}

    Tipo de union: {dic_resultados_fatiga["tipo_union"]}

    Cargas Aplicadas:

        Tipo:  Cíclica
        Fuerza máxima = {dic_resultados_fatiga["Fmax"]} {und_fuerza}
        Fuerza mínima = {dic_resultados_fatiga["Fmin"]} {und_fuerza}

"""  # Porción de informe con datos de entrada de fatiga

        informe += resultados_estatica

        informe += "Análisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga Transversal de Fatiga\n"

        resumen += resumen_estatica

        if not falla:
            informe += f"""
Se procede a analizar la soldadura y las piezas soldadas por carga de fatiga.

Cálculos realizados

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_resultados_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_resultados_fatiga.get("f_med", 0)} {und_fuerza}

    Factor de concentración de esfuerzo reducido
        Para soldadura de filete de unión: {dic_resultados_fatiga.get("tipo_union", "")} sometida a carga transversal, el factor de concentración de esfuerzo reducido es:

            Kfs = {dic_resultados_fatiga.get("kfs", 0)}

Para la soldadura:

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * 1.414 * Fa / Asold
            τa = {dic_resultados_fatiga.get("tao_alt_sold", 0)} {und_esfuerzo}

        τm = 1.414 * Fm / Asold
            τm = {dic_resultados_fatiga.get("tao_med_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura utilizando ecuación de Gerber:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS sold = {dic_resultados_fatiga.get("fs_sold", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_sold", 0)}


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_resultados_fatiga.get("tao_p_alt", 0)} {und_esfuerzo}

        τm = Fm / Asold
            τm = {dic_resultados_fatiga.get("tao_p_med", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 1 utilizando ecuación de Gerber:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza1", 0)}


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Cálculo de esfuerzo normale alternante y medio de la pieza 2:

        σa = Kfs * Fa / Asold
            σa = {dic_resultados_fatiga.get("sigma_t_alt", 0)} {und_esfuerzo}

        σm = Fm / Asold
            σm = {dic_resultados_fatiga.get("sigma_t_med", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión de la pieza 2:

        Sut = {dic_resultados_fatiga.get("sut_pieza2")}

    Cálculo del Factor de Seguridad FS utilizando ecuación de Gerber:

        (FS * σa)/Se + ((FS * σm)/Sut)^2 = 1
            FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2")}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza2")}
                    """  # Porción del informe con los resultados de fatiga

            informe += "\nAnálisis de fatiga completado.\n"

            informe += verificacion_pierna  # Porción de informe de verificación de pierna

            resumen += resumen_fatiga + verificacion_pierna_resumen

        else:

            informe += verificacion_pierna
            resumen += verificacion_pierna_resumen

    return informe, resumen


def informe_analisis_filete_cf(nombre_proyecto, tipo_carga, dic_resultados_estatica, dic_resultados_fatiga, falla,
                               sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de analisis de soldadura de filete
    sometida a carga de flexión debido a una fuerza externa"""

    informe = f"""
{"*" * 5} Informe de Análisis de Soldadura de Filete Sometida a Carga de Flexión debido a una Fuerza Externa {tipo_carga.capitalize()} {"*" * 5}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados del análisis de soldadura de filete sometida a carga de flexion debido a una fuerza externa {tipo_carga}. El objetivo del análisis es evaluar si la junta soldada cumple con los requisitos mínimos de seguridad y funcionamiento (FDsoldadura = 3.33, FDpieza = 2.5), de acuerdo a la cátedra EMI, así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n"""  # Introducción

    resumen = ""

    resultados_estatica = f"""
Se procede a analizar la soldadura y las piezas soldadas por carga estática.

    F = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}

Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Garganta (t) = 0.707 * h
            t = {dic_resultados_estatica.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_resultados_estatica["lt_ecuacion"]}
            lt = {dic_resultados_estatica.get("longitud_total", 0)} {und_distancia}

        Distancia del eje nuetro hasta la soldadura (c) = {dic_resultados_estatica["c_ecuacion"]}
            c = {dic_resultados_estatica["c"]} {und_distancia}

    Momento de Inercia (I):

        Para la soldadura:
            I sold = {dic_resultados_estatica["i_sold_ecuacion"]}
                I sold = {dic_resultados_estatica["i_sold"]} {und_distancia}^4

        Para las piezas:
            I piezas = {dic_resultados_estatica["i_pieza_ecuacion"]}
                I piezas = {dic_resultados_estatica["i_pieza"]} {und_distancia}^4

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_resultados_estatica["area_sold"]} {und_distancia}²

Cálculo del momento flector producido por la fuerza externa:

        M = F * b
            M = {dic_resultados_estatica["momento_flector"]} {und_fuerza}{und_distancia}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_resultados_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario en la soldadura:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_resultados_estatica["tao_primario"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante secundario en la soldadura:

        τ'' sold = M * c / I
            τ'' sold = {dic_resultados_estatica["tao_secundario"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τ')^2 + (τ'')^2)
            τ sold = {dic_resultados_estatica["tao_sold"]} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura:

        FS sold = τ adm / τ sold
            FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}

Conclusión: {dic_resultados_estatica["conclusion_sold"]}


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_resultados_estatica["sy_pieza1"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza1 = M * c / I
            σ pieza1 = {dic_resultados_estatica["sigma_p"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_resultados_estatica["tao_p"]} {und_esfuerzo}

    Cálculo del esfuerzo Von Misses σ':

        σ' pieza1 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza1 = {dic_resultados_estatica["sigma_von_misses_1"]} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 1:

        FS pieza1 = Sy / σ'
            FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza1"]}


Para la pieza 2: (Pieza transversal a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_resultados_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_resultados_estatica["sigma_t"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante:

        τ pieza2 = M * c / I
            τ pieza2 = {dic_resultados_estatica["tao_t"]} {und_esfuerzo}

    Cálculo del esfuerzo Von Misses σ':

        σ' pieza2 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza2 = {dic_resultados_estatica["sigma_von_misses_2"]} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 2:

        FS pieza2 = Sy / σ'
            FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza2"]}\n
"""  # Resultados de cálculos de análisis por carga estática

    resumen_estatica = f"""
    <body>

    <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA ESTÁTICA</h2>
    <hr>

    <p><strong>Factor de seguridad de la soldadura:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_sold'] >= 3.33 else 'red'};">FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_sold", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 1:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza1'] >= 2.5 else 'red'}">FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza1", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 2:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza2'] >= 2.5 else 'red'}">FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza2", 0)}</p>

    </body>
    """  # Resumen de resultados de análisis estático.

    resumen_fatiga = f"""
    <body>

    <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA DE FATIGA</h2>
    <hr>

    <p><strong>Factor de seguridad de la soldadura:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_resultados_fatiga.get('fs_sold', 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_sold", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 1:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza1", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 2:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza2", 0)}</p>

    </body>

    """  # Resumen de resultados de análisis de fatiga

    verificacion_pierna_resumen = f"""
            <br>
            <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
            <p>{dic_resultados_estatica.get("verificacion_pierna", 0)}</p>


            """  # Porción con verificación de pierna para el resumen

    verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_resultados_estatica.get("verificacion_pierna", 0)}

    """  # Porción con verificación de tamaño de pierna

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1 (pieza paralela a la carga):
            Acero:  {acero1}
            Sy  =   {dic_resultados_estatica["sy_pieza1"]} {und_esfuerzo}
            Sut =   {dic_resultados_estatica["sut_pieza1"]} {und_esfuerzo}

        Pieza 2 (pieza transversal a la carga):
            Acero:  {acero2}
            Sy  =   {dic_resultados_estatica["sy_pieza2"]} {und_esfuerzo}
            Sut =   {dic_resultados_estatica["sut_pieza2"]} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_estatica["sy_sold"]} {und_esfuerzo}
            Sut =  {dic_resultados_estatica["sut_sold"]} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h) =  {dic_resultados_estatica["pierna"]} {und_distancia}
        Largo (l)  =  {dic_resultados_estatica["largo"]} {und_distancia}
        Ancho (a)  =  {dic_resultados_estatica["ancho"]} {und_distancia}
        Radio (r)  =  {dic_resultados_estatica["radio"]} {und_distancia}

    Tipo de union: T

    Cargas Aplicadas:

        Tipo: Estática
        Fuerza    = {dic_resultados_estatica["Fmax"]} {und_fuerza}
        Brazo (b) = {dic_resultados_estatica["b"]} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e) = {dic_resultados_estatica["espesor_menor_piezas"]} {und_distancia}
"""  # Unión de porción de informe con datos de entrada para análisis estático

        informe += resultados_estatica

        informe += verificacion_pierna

        informe += "Análisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga de Flexión Estática\n"

        resumen += resumen_estatica + verificacion_pierna_resumen

    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_fatiga["sy_pieza1"]} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga["sut_pieza1"]} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_fatiga["sy_pieza2"]} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga["sut_pieza2"]} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_fatiga["sy_sold"]} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga["sut_sold"]} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h) = {dic_resultados_fatiga["pierna"]} {und_distancia}
        Largo (l)  = {dic_resultados_fatiga["largo"]} {und_distancia}
        Ancho (a)  = {dic_resultados_fatiga["ancho"]} {und_distancia}
        Radio (r)  =  {dic_resultados_fatiga["radio"]} {und_distancia}

    Tipo de union: Unión T

    Cargas Aplicadas:

        Tipo:  Cíclica
        Fuerza máxima = {dic_resultados_fatiga["Fmax"]} {und_fuerza}
        Fuerza mínima = {dic_resultados_fatiga["Fmin"]} {und_fuerza}
        Brazo (b)     = {dic_resultados_fatiga["b"]} {und_distancia}

"""  # Porción de informe con datos de entrada de fatiga

        informe += resultados_estatica

        informe += "Análisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga de Flexión de Fatiga\n"

        resumen += resumen_estatica

        if not falla:
            informe += f"""
Se procede a analizar la soldadura y las piezas soldadas por carga de fatiga.

Cálculos realizados

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_resultados_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_resultados_fatiga.get("f_med", 0)} {und_fuerza}

    Cálculo de momento flector alternante y medio:

        Momento flector alternante (Ma) = Fa * b
            Ma = {dic_resultados_fatiga.get("momento_flector_alt", 0)} {und_fuerza}{und_distancia}

        Momento flector medio (Mm) = Fm * b
            Mm = {dic_resultados_fatiga.get("momento_flector_med", 0)} {und_fuerza}{und_distancia}

    Factor de concentración de esfuerzo reducido

        Para soldadura de filete de Unión T sometida a carga de flexión, el factor de concentración de esfuerzo reducido es:

            Kfs = {dic_resultados_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo de esfuerzo cortante primario alternante y medio:

        τa' = Kfs * 1.414 * Fa / Asold
            τa' = {dic_resultados_fatiga.get("tao_primario_alt", 0)} {und_esfuerzo}

        τm' = 1.414 * Fm / Asold
            τm' = {dic_resultados_fatiga.get("tao_primario_med", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante secundario alternante y medio:

        τa'' = Kfs * Ma * c / I
            τa" = {dic_resultados_fatiga.get("tao_secundario_alt", 0)} {und_esfuerzo}

        τm'' = Mm * c / I
            τm" = {dic_resultados_fatiga.get("tao_secundario_med", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante resultante alternante y medio:

        τa = sqrt((τa')^2 + (τa'')^2)
            τa = {dic_resultados_fatiga.get("tao_alt_sold", 0)} {und_esfuerzo}

        τm = sqrt((τm')^2 + (τm'')^2)
            τm = {dic_resultados_fatiga.get("tao_med_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga al cortante del material de aporte:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante del material de aporte:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS sold = {dic_resultados_fatiga["fs_sold"]}

Conclusión: {dic_resultados_fatiga["conclusion_sold"]}


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Resistencia a última a la tensión:

        Sut = {dic_resultados_estatica["sut_pieza1"]} {und_esfuerzo}

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Ma * c / I
            σa = {dic_resultados_fatiga.get("sigma_p_alt", 0)} {und_esfuerzo}

        σm = Mm * c / I
            σm = {dic_resultados_fatiga.get("sigma_p_med", 0)} {und_esfuerzo}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_resultados_fatiga.get("tao_p_alt", 0)} {und_esfuerzo}

        τm = Fm / Asold
            τm = {dic_resultados_fatiga.get("tao_p_med", 0)} {und_esfuerzo}

    Cálculo de esfuerzo Von Misses alternante y medio:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_resultados_fatiga.get("sigma_p_von_misses_alt", 0)} {und_esfuerzo}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ'm = {dic_resultados_fatiga.get("sigma_p_von_misses_med", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS en la pieza 1:

        (FS * σ'a)/Se + ((FS * σ'm)/Sut)^2 = 1
            FS pieza1 = {dic_resultados_fatiga["fs_pieza1"]}

Conclusión: {dic_resultados_fatiga["conclusion_pieza1"]}


Para la pieza 2: (Pieza transversal a la carga aplicada)

    Resistencia a última a la tensión:

        Sut = {dic_resultados_fatiga["sut_pieza2"]} {und_esfuerzo}

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Fa / Asold
            σa = {dic_resultados_fatiga.get("sigma_t_alt", 0)} {und_esfuerzo}

        σm = Fm / Asold
            σm = {dic_resultados_fatiga.get("sigma_t_med", 0)} {und_esfuerzo}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Ma * c / I
            τa = {dic_resultados_fatiga.get("tao_t_alt", 0)} {und_esfuerzo}

        τm = Mm * c / I
            τm = {dic_resultados_fatiga.get("tao_t_med", 0)} {und_esfuerzo}

    Cálculo de esfuerzo de Von Misses alternante y medio:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_resultados_fatiga.get("sigma_t_von_misses_alt", 0)} {und_esfuerzo}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ"m = {dic_resultados_fatiga.get("sigma_t_von_misses_med", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS en la pieza 2:

        (FS * σ'a)/Se + ((FS * σ'm)/Sut)^2 = 1
            FS pieza2 = {dic_resultados_fatiga["fs_pieza2"]} {und_esfuerzo}

Conclusión: {dic_resultados_fatiga["conclusion_pieza2"]}

"""

            informe += "\nAnálisis de fatiga completado.\n"

            resumen += resumen_fatiga + verificacion_pierna_resumen

        else:

            informe += verificacion_pierna
            resumen += verificacion_pierna_resumen

    return informe, resumen


def informe_analisis_filete_ctor(nombre_proyecto, tipo_carga, dic_resultados_estatica, dic_resultados_fatiga, falla,
                                 sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados del analisis de soldadura de filete
    sometida a carga de torsión debido a una fuerza externa"""

    informe = f"""
{"*" * 5} Informe de Análisis de Soldadura de Filete Sometida a Carga de Torsión debido a una Fuerza Externa {tipo_carga.capitalize()} {"*" * 5}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados del análisis de soldadura de filete sometida a carga de torsión debido a una fuerza externa {tipo_carga}. El objetivo del análisis es evaluar si la junta soldada cumple con los requisitos mínimos de seguridad y funcionamiento (FDsoldadura = 3.33, FDpieza = 2.5), de acuerdo a la cátedra EMI, así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n"""  # Introducción

    resumen = ""

    resultados_estatica = f"""
Se procede a analizar por carga estática la soldadura y las piezas.

    F = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}

Cálculos realizados

    Cálculos de parámetros geométricos:

        Garganta (t) = 0.707 * h
            t = {dic_resultados_estatica.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_resultados_estatica["lt_ecuacion"]}
            lt = {dic_resultados_estatica.get("longitud_total", 0)} {und_distancia}

        Distancia en X desde el centroide hasta el punto crítico (rx) = {dic_resultados_estatica["rx_ecuacion"]}
            rx = {dic_resultados_estatica["rx"]} {und_distancia}

        Distancia en Y desde el centroide hasta el punto crítico (ry) = {dic_resultados_estatica["ry_ecuacion"]}
            ry = {dic_resultados_estatica["ry"]} {und_distancia}

    Momento Polar de Inercia (J):

        Para la soldadura:

            J sold = {dic_resultados_estatica["j_sold_ecuacion"]}
                J sold = {dic_resultados_estatica["j_sold"]} {und_distancia}^4

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_resultados_estatica["area_sold"]} {und_distancia}²

    Cálculo del momento torsor producido por la fuerza externa:

        T = F * b
            T = {dic_resultados_estatica["momento_torsor"]} {und_fuerza}{und_distancia}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_resultados_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario en la soldadura:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_resultados_estatica["tao_primario"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante secundario en la soldadura en el eje X y en el eje Y:

        τ'' sold x = T * ry / J
            τ" sold x = {dic_resultados_estatica["tao_secundario_x"]} {und_esfuerzo}

        τ'' sold y = T * rx / J
            τ" sold y = {dic_resultados_estatica["tao_secundario_y"]} {und_esfuerzo}

    Cálculo de la componente en el eje X del esfuerzo cortante resultante en la soldadura:

        τ sold x = τ'' sold x
            τ sold x = {dic_resultados_estatica["tao_x"]} {und_esfuerzo}

    Cálculo de la componente en el eje Y del esfuerzo cortante resultante en la soldadura:

        τ sold y = τ' sold + τ'' sold y
            τ sold y = {dic_resultados_estatica["tao_y"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τx)^2 + (τy)^2)
            τ sold = {dic_resultados_estatica["tao_sold"]} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura:

        FS sold = τ adm / τ sold
            FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}

Conclusión: {dic_resultados_estatica["conclusion_sold"]}


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Resistencia a la fluencia al cortante de la pieza 1:

        Ssy = 0.577 * Sy
            Ssy = {dic_resultados_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_resultados_estatica["tao_p"]} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 1:

        FS pieza1 = Ssy / τ pieza1
            FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza1"]}


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Resistencia a la fluencia:

        Sy = {dic_resultados_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_resultados_estatica["sigma_t"]} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 2:

        FS pieza2 = Sy / σ pieza2
            FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza2"]}\n
"""  # Resultados de cálculos de análisis por carga estática

    resumen_estatica = f"""
    <body>

    <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA ESTÁTICA</h2>
    <hr>

    <p><strong>Factor de seguridad de la soldadura:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_sold'] >= 3.33 else 'red'};">FS sold = {dic_resultados_estatica['fs_sold']}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_sold", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 1:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza1'] >= 2.5 else 'red'}">FS pieza1 = {dic_resultados_estatica.get("fs_pieza1", 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza1", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 2:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza2'] >= 2.5 else 'red'}">FS pieza2 = {dic_resultados_estatica.get("fs_pieza2", 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza2", 0)}</p>

    </body>
    """  # Resumen de resultados de análisis estático.

    resumen_fatiga = f"""
    <body>

    <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA DE FATIGA</h2>
    <hr>

    <p><strong>Factor de seguridad de la soldadura:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_resultados_fatiga.get('fs_sold', 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_sold", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 1:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza1", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 2:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza2", 0)}</p>

    </body>

    """  # Resumen de resultados de análisis de fatiga

    verificacion_pierna_resumen = f"""
            <br>
            <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
            <p>{dic_resultados_estatica.get("verificacion_pierna", 0)}</p>


            """  # Porción con verificación de pierna para el resumen

    verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_resultados_estatica.get("verificacion_pierna", 0)}

    """  # Porción con verificación de tamaño de pierna

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1 (pieza paralela a la carga):
            Acero:  {acero1}
            Sy  =   {dic_resultados_estatica["sy_pieza1"]} {und_esfuerzo}
            Sut =   {dic_resultados_estatica["sut_pieza1"]} {und_esfuerzo}

        Pieza 2 (pieza transversal a la carga):
            Acero:  {acero2}
            Sy  =   {dic_resultados_estatica["sy_pieza2"]} {und_esfuerzo}
            Sut =   {dic_resultados_estatica["sut_pieza2"]} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_estatica["sy_sold"]} {und_esfuerzo}
            Sut =  {dic_resultados_estatica["sut_sold"]} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h) =  {dic_resultados_estatica["pierna"]} {und_distancia}
        Largo (l)  =  {dic_resultados_estatica["largo"]} {und_distancia}
        Ancho (a)  =  {dic_resultados_estatica["ancho"]} {und_distancia}
        Radio (r)  =  {dic_resultados_estatica["radio"]} {und_distancia}

    Tipo de union: {dic_resultados_estatica["tipo_union"]}

    Carga Aplicada:

        Tipo: Estática
        Fuerza    = {dic_resultados_estatica["Fmax"]} {und_fuerza}
        Brazo (b) = {dic_resultados_estatica["b"]} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e) = {dic_resultados_estatica["espesor_menor_piezas"]} {und_distancia}
"""  # Unión de porción de informe con datos de entrada para análisis estático

        informe += resultados_estatica

        informe += verificacion_pierna

        informe += "Análisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga de Torsión Estática\n"

        resumen += resumen_estatica + verificacion_pierna_resumen

    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_fatiga["sy_pieza1"]} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga["sut_pieza1"]} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_fatiga["sy_pieza2"]} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga["sut_pieza2"]} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_fatiga["sy_sold"]} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga["sut_sold"]} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h) = {dic_resultados_fatiga["pierna"]} {und_distancia}
        Largo (l)  = {dic_resultados_fatiga["largo"]} {und_distancia}
        Ancho (a)  = {dic_resultados_fatiga["ancho"]} {und_distancia}
        Radio (r)  =  {dic_resultados_fatiga["radio"]} {und_distancia}

    Tipo de union: {dic_resultados_fatiga["tipo_union"]}

    Cargas Aplicadas:

        Tipo:  Cíclica
        Fuerza máxima = {dic_resultados_fatiga["Fmax"]} {und_fuerza}
        Fuerza mínima = {dic_resultados_fatiga["Fmin"]} {und_fuerza}
        Brazo (b)     = {dic_resultados_fatiga["b"]} {und_distancia}

"""  # Porción de informe con datos de entrada de fatiga

        informe += resultados_estatica

        informe += "Análisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga de Torsión de Fatiga\n"

        resumen += resumen_estatica

        if not falla:
            informe += f"""
Se procede a analizar por carga de fatiga la soldadura y las piezas soldadas.

Cálculos realizados

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_resultados_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_resultados_fatiga.get("f_med", 0)} {und_fuerza}

    Cálculo de momento torsor alternante y medio:

        Momento torsor alternante (Ta) = Fa * b
            Ta = {dic_resultados_fatiga.get("momento_torsor_alt", 0)} {und_fuerza}{und_distancia}

        Momento torsor medio (Tm) = Fm * b
            Tm = {dic_resultados_fatiga.get("momento_torsor_med", 0)} {und_fuerza}{und_distancia}

    Factor de concentración de esfuerzo reducido

        Para soldadura de filete de unión: {dic_resultados_fatiga.get("tipo_union", "")}, sometida a carga de torsión, el factor de concentración de esfuerzo reducido es:

            Kfs = {dic_resultados_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo de esfuerzo cortante primario alternante y medio:

        τa' = Kfs * 1.414 * Fa / Asold
            τa' = {dic_resultados_fatiga.get("tao_primario_alt", 0)} {und_esfuerzo}

        τm = 1.414 * Fm / Asold
            τm' = {dic_resultados_fatiga.get("tao_primario_med", 0)} {und_esfuerzo}

    Cálculo de la componente en el eje X y Y del esfuerzo cortante secundario alternante:

        τa'' x = Kfs * Ta * ry / J
            τa" x = {dic_resultados_fatiga.get("tao_secundario_alt_x", 0)} {und_esfuerzo}

        τa'' y = Kfs * Tm * rx / J
            τa" y = {dic_resultados_fatiga.get("tao_secundario_alt_y", 0)} {und_esfuerzo}

    Cálculo de la componente en el eje X y Y del esfuerzo cortante secundario medio:

        τm'' x = Tm * ry / J
            τm" x = {dic_resultados_fatiga.get("tao_secundario_med_x", 0)} {und_esfuerzo}

        τm'' y = Tm * rx / J
            τm" y = {dic_resultados_fatiga.get("tao_secundario_med_y", 0)} {und_esfuerzo}

    Cálculo de componentes X y Y del esfuerzo cortante alternante:

        τa x = τa'' x
            τa x = {dic_resultados_fatiga.get("tao_alt_x")} {und_esfuerzo}

        τa y = τa' + τa'' y
            τa y = {dic_resultados_fatiga.get("tao_alt_y")} {und_esfuerzo}

    Cálculo de componentes X y Y del esfuerzo cortante medio:

        τm x = τm'' x
            τm x = {dic_resultados_fatiga.get("tao_med_x")} {und_esfuerzo}

        τm y = τm' + τm'' y
            τm y = {dic_resultados_fatiga.get("tao_med_y")} {und_esfuerzo}

    Cálculo del esfuerzo cortante resultante alternante y medio en la soldadura:

        τa = sqrt((τa x)^2 + (τa y)^2)
            τa = {dic_resultados_fatiga.get("tao_alt_sold", 0)} {und_esfuerzo}

        τm = sqrt((τm x)^2 + (τm y)^2)
            τm = {dic_resultados_fatiga.get("tao_med_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga al cortante del material de aporte:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante del material de aporte:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS en la soldadura:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS sold = {dic_resultados_fatiga["fs_sold"]}

Conclusión: {dic_resultados_fatiga["conclusion_sold"]}


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Cálculo de esfuerzo cortante alternante y medio de la pieza 1:

        τa = Kfs * Fa / Asold
            τa = {dic_resultados_fatiga.get("tao_p_alt", 0)} {und_esfuerzo}

        τm = Fm / Asold
            τm = {dic_resultados_fatiga.get("tao_p_med", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS en la pieza 1:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS pieza1 = {dic_resultados_fatiga["fs_pieza1"]}

Conclusión: {dic_resultados_fatiga["conclusion_pieza1"]}


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Resistencia a última a la tensión:

        Sut = {dic_resultados_fatiga["sut_pieza2"]} {und_esfuerzo}

    Cálculo de esfuerzo normal alternante y medio de la pieza 1:

        σa = Kfs * Fa / Asold
            σa = {dic_resultados_fatiga.get("sigma_t_alt", 0)} {und_esfuerzo}

        σm = Fm / Asold
            σm = {dic_resultados_fatiga.get("sigma_t_med", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS en la pieza 2:

        (FS * σa)/Se + ((FS * σm)/Sut)^2 = 1
            FS pieza2 = {dic_resultados_fatiga["fs_pieza2"]}

Conclusión: {dic_resultados_fatiga["conclusion_pieza2"]}

"""

            informe += "\nAnálisis de fatiga completado.\n"

            informe += verificacion_pierna  # Porción de informe de verificación de pierna

            resumen += resumen_fatiga + verificacion_pierna_resumen

        else:

            informe += verificacion_pierna
            resumen += verificacion_pierna_resumen

    return informe, resumen


def informe_analisis_filete_cc(nombre_proyecto, tipo_carga, dic_resultados_estatica, dic_resultados_fatiga, falla,
                               sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados del analisis de soldadura de filete
    sometida a carga combinada debido a una fuerza externa excéntrica al centroide"""

    informe = f"""
{"*" * 5} Informe de Análisis de Soldadura de Filete Sometida a Carga Combinada debido a una Fuerza Externa {tipo_carga.capitalize()} Excéntrica al Centroide de la Soldadura {"*" * 5}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados del análisis de soldadura de filete sometida a carga combinada debido a una fuerza externa {tipo_carga} excéntrica al centroide de la soldadura. El objetivo del análisis es evaluar si la junta soldada cumple con los requisitos mínimos de seguridad y funcionamiento (FDsoldadura = 3.33, FDpieza = 2.5), de acuerdo a la cátedra EMI, así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n"""  # Introducción

    resumen = ""

    resultados_estatica = f"""
Se procede a analizar por carga estática la soldadura y las piezas soldadas.

    F = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}

Cálculos realizados

    Cálculos de parámetros geométricos:

        Garganta (t) = 0.707 * h
            t = {dic_resultados_estatica.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_resultados_estatica["lt_ecuacion"]}
            lt = {dic_resultados_estatica.get("longitud_total", 0)} {und_distancia}

        Distancia en X desde el centroide hasta el punto crítico (rx) = {dic_resultados_estatica["rx_ecuacion"]}
            rx = {dic_resultados_estatica["rx"]} {und_distancia}

        Distancia en Y desde el centroide hasta el punto crítico (ry) = {dic_resultados_estatica["ry_ecuacion"]}
            ry = {dic_resultados_estatica["ry"]} {und_distancia}

        Distancia del eje nuetro hasta la soldadura (c) = {dic_resultados_estatica["c_ecuacion"]}
            c = {dic_resultados_estatica["c"]} {und_distancia}

    Momento de Inercia (I):

        Para la soldadura:
            I sold = {dic_resultados_estatica["i_sold_ecuacion"]}
                I sold = {dic_resultados_estatica["i_sold"]} {und_distancia}^4

        Para las piezas:
            I piezas = {dic_resultados_estatica["i_pieza_ecuacion"]}
                I piezas = {dic_resultados_estatica["i_pieza"]} {und_distancia}^4

    Momento Polar de Inercia (J):

        Para la soldadura:
            J sold = {dic_resultados_estatica["j_sold_ecuacion"]}
                J sold = {dic_resultados_estatica["j_sold"]} {und_distancia}^4

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_resultados_estatica["area_sold"]} {und_distancia}²


Cálculo del momento torsor producido por la fuerza externa:

        T = F * bt
            T = {dic_resultados_estatica["momento_torsor"]} {und_fuerza}{und_distancia}

Cálculo del momento flector producido por la fuerza externa:

        M = F * bl
            M = {dic_resultados_estatica["momento_flector"]} {und_fuerza}{und_distancia}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_resultados_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario en la soldadura:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_resultados_estatica["tao_primario"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante secundario en la soldadura:

        τ'' sold = M * c / I
            τ" sold = {dic_resultados_estatica["tao_secundario"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante terciario en la soldadura:

        En el eje X:
        τ''' sold x = T * ry / J
            τ''' sold x = {dic_resultados_estatica["tao_terciario_x"]} {und_esfuerzo}

        En el eje Y:
        τ''' sold y = T * rx / J
            τ''' sold y = {dic_resultados_estatica["tao_terciario_y"]} {und_esfuerzo}

    Cálculo de la componente en el eje X, Y y Z del esfuerzo cortante resultante en la soldadura:

        τ sold x = τ''' x
            τ sold x = {dic_resultados_estatica["tao_x"]} {und_esfuerzo}

        τ sold y = τ' + τ''' y
            τ sold y = {dic_resultados_estatica["tao_y"]} {und_esfuerzo}

        τ sold z = τ''
            τ sold z = {dic_resultados_estatica["tao_z"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τx)^2 + (τy)^2 + (τz)^2)
            τ sold = {dic_resultados_estatica["tao_sold"]} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura:

        FS sold = τ adm / τ sold
            FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}

Conclusión: {dic_resultados_estatica["conclusion_sold"]}


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Resistencia a la fluencia al cortante de la pieza 1:

        Sy = {dic_resultados_estatica["sy_pieza1"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza1 = M * c / I
            σ pieza1 = {dic_resultados_estatica["sigma_p"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_resultados_estatica["tao_p"]} {und_esfuerzo}

    Cálculo del esfuerzo de Von Misses en la pieza 1:

        σ' pieza1 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza1 = {dic_resultados_estatica["sigma_von_misses_1"]} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 1:

        FS pieza1 = Sy / σ'
            FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza1"]}


Para la pieza 2: (Pieza Transversal a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_resultados_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_resultados_estatica["sigma_t"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante:

        τ pieza2 = M * c / I
            τ pieza2 = {dic_resultados_estatica["tao_t"]} {und_esfuerzo}

    Cálculo del esfuerzo Von Misses σ':

        σ' pieza2 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza2 = {dic_resultados_estatica["sigma_von_misses_2"]} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 2:

        FS pieza2 = Sy / σ'
            FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza2"]}\n
"""  # Resultados de cálculos de análisis por carga estática

    resumen_estatica = f"""
    <body>

    <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA ESTÁTICA</h2>
    <hr>

    <p><strong>Factor de seguridad de la soldadura:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_sold'] >= 3.33 else 'red'};">FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_sold", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 1:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza1'] >= 2.5 else 'red'}">FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza1", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 2:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza2'] >= 2.5 else 'red'}">FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza2", 0)}</p>

    </body>
    """  # Resumen de resultados de análisis estático.

    resumen_fatiga = f"""
    <body>

    <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA DE FATIGA</h2>
    <hr>

    <p><strong>Factor de seguridad de la soldadura:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_resultados_fatiga.get('fs_sold', 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_sold", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 1:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza1", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 2:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza2", 0)}</p>

    </body>

    """  # Resumen de resultados de análisis de fatiga

    verificacion_pierna_resumen = f"""
            <br>
            <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
            <p>{dic_resultados_estatica.get("verificacion_pierna", 0)}</p>


            """  # Porción con verificación de pierna para el resumen

    verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_resultados_estatica.get("verificacion_pierna", 0)}

    """  # Porción con verificación de tamaño de pierna

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1 (pieza paralela a la carga):
            Acero:  {acero1}
            Sy  =   {dic_resultados_estatica["sy_pieza1"]} {und_esfuerzo}
            Sut =   {dic_resultados_estatica["sut_pieza1"]} {und_esfuerzo}

        Pieza 2 (pieza transversal a la carga):
            Acero:  {acero2}
            Sy  =   {dic_resultados_estatica["sy_pieza2"]} {und_esfuerzo}
            Sut =   {dic_resultados_estatica["sut_pieza2"]} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_estatica["sy_sold"]} {und_esfuerzo}
            Sut =  {dic_resultados_estatica["sut_sold"]} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h) =  {dic_resultados_estatica["pierna"]} {und_distancia}
        Largo (l)  =  {dic_resultados_estatica["largo"]} {und_distancia}
        Ancho (a)  =  {dic_resultados_estatica["ancho"]} {und_distancia}
        Radio (r)  =  {dic_resultados_estatica["radio"]} {und_distancia}

    Tipo de union: Unión T

    Cargas Aplicadas:

        Tipo: Estática
        Fuerza    = {dic_resultados_estatica["Fmax"]} {und_fuerza}
        Brazo longitudinal (bl) = {dic_resultados_estatica["bl"]} {und_distancia}
        Brazo transversal (bt) = {dic_resultados_estatica["bt"]} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e) = {dic_resultados_estatica["espesor_menor_piezas"]} {und_distancia}
"""  # Unión de porción de informe con datos de entrada para análisis estático

        informe += resultados_estatica

        informe += verificacion_pierna

        informe += "Análisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga Combinada Estática\n"

        resumen += resumen_estatica + verificacion_pierna_resumen

    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_fatiga["sy_pieza1"]} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga["sut_pieza1"]} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_fatiga["sy_pieza2"]} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga["sut_pieza2"]} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_fatiga["sy_sold"]} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga["sut_sold"]} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h) = {dic_resultados_fatiga["pierna"]} {und_distancia}
        Largo (l)  = {dic_resultados_fatiga["largo"]} {und_distancia}
        Ancho (a)  = {dic_resultados_fatiga["ancho"]} {und_distancia}
        Radio (r)  =  {dic_resultados_fatiga["radio"]} {und_distancia}

    Tipo de union: Unión T

    Cargas Aplicadas:

        Tipo:  Cíclica
        Fuerza máxima = {dic_resultados_fatiga["Fmax"]} {und_fuerza}
        Fuerza mínima = {dic_resultados_fatiga["Fmin"]} {und_fuerza}
        Brazo longitudinal (bl) = {dic_resultados_fatiga["bl"]} {und_distancia}
        Brazo transversal (bt) = {dic_resultados_fatiga["bt"]} {und_distancia}


"""  # Porción de informe con datos de entrada de fatiga

        informe += resultados_estatica

        informe += "Análisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga Combinada de Fatiga\n"

        resumen += resumen_estatica

        if not falla:
            informe += f"""
Se procede a analizar por carga de fatiga la soldadura y las piezas soldadas.

Cálculos realizados

    Cálculo de carga alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_resultados_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_resultados_fatiga.get("f_med", 0)} {und_fuerza}

    Cálculo de momento torsor alternante y medio:

        Momento torsor alternante (Ta) = Fa * b
            Ta = {dic_resultados_fatiga.get("momento_torsor_alt", 0)} {und_fuerza}{und_distancia}

        Momento torsor medio (Tm) = Fm * b
            Tm = {dic_resultados_fatiga.get("momento_torsor_med", 0)} {und_fuerza}{und_distancia}

   Cálculo de momento flector alternante y medio:

        Momento alternante (Ma) = Fa * b
            Ma = {dic_resultados_fatiga.get("momento_flector_alt", 0)} {und_fuerza}{und_distancia}

        Momento medio (Mm) = Fm * b
            Mm = {dic_resultados_fatiga.get("momento_flector_med", 0)} {und_fuerza}{und_distancia}

    Factor de concentración de esfuerzo reducido

        Para soldadura de filete de unión T sometida a carga combinada, el factor de concentración de esfuerzo reducido es:

            Kfs = {dic_resultados_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo de esfuerzo cortante primario alternante y medio:

        τa' = Kfs * 1.414 * Fa / Asold
            τa' = {dic_resultados_fatiga.get("tao_primario_alt", 0)} {und_esfuerzo}

        τm = 1.414 * Fm / Asold
            τm' = {dic_resultados_fatiga.get("tao_primario_med", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante secundario alternante y medio:

        τa'' = Kfs * Ma * c / I
            τa'' = {dic_resultados_fatiga.get("tao_secundario_alt", 0)} {und_esfuerzo}

        τm'' = Mm * c / I
            τm'' = {dic_resultados_fatiga.get("tao_secundario_med", 0)} {und_esfuerzo}

    Cálculo de las componentes X y Y del esfuerzo cortante terciario alternante:

        τa''' x = = Kfs * Ta * ry / J
            τa''' x = {dic_resultados_fatiga.get("tao_terciario_alt_x", 0)} {und_esfuerzo}

        τa''' y = Kfs * Ta * rx / J
            τa''' y ={dic_resultados_fatiga.get("tao_terciario_alt_y", 0)} {und_esfuerzo}

    Cálculo de las componentes X y Y del esfuerzo cortante terciario medio:

        τm''' x = Tm * ry / J
            τm''' x = {dic_resultados_fatiga.get("tao_terciario_med_x", 0)} {und_esfuerzo}

        τm''' y = Tm * rx / J
            τm''' y = {dic_resultados_fatiga.get("tao_terciario_med_y", 0)} {und_esfuerzo}

    Cálculo de las componentes X, Y y Z del esfuerzo cortante alternante:

        τa x = τa''' x
            τa x = {dic_resultados_fatiga.get("tao_alt_x", 0)} {und_esfuerzo}

        τa y = τa' + τa''' y
            τa y = {dic_resultados_fatiga.get("tao_alt_y", 0)} {und_esfuerzo}

        τa z = τa''
            τa z = {dic_resultados_fatiga.get("tao_alt_z", 0)} {und_esfuerzo}

    Cálculo de las componentes X, Y y Z del esfuerzo cortante medio:

        τm x = τm''' x
            τm x = {dic_resultados_fatiga.get("tao_med_x", 0)} {und_esfuerzo}

        τm y = τm' + τm''' y
            τm y = {dic_resultados_fatiga.get("tao_med_y", 0)} {und_esfuerzo}

        τm z = τm''
            τm z = {dic_resultados_fatiga.get("tao_med_z", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante resultante alternante y medio en la soldadura:

        τa = sqrt((τa x)^2 + (τa y)^2 + (τa z)^2)
            τa = {dic_resultados_fatiga.get("tao_alt_sold", 0)} {und_esfuerzo}

        τm = sqrt((τm x)^2 + (τm y)^2 + (τm z)^2)
            τm = {dic_resultados_fatiga.get("tao_med_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga al cortante del material de aporte:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante del material de aporte

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS sold = {dic_resultados_fatiga["fs_sold"]}

Conclusión: {dic_resultados_fatiga["conclusion_sold"]}


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Ma * c / I
            σa = {dic_resultados_fatiga.get("sigma_p_alt", 0)} {und_esfuerzo}

        σm = Mm * c / I
            σm = {dic_resultados_fatiga.get("sigma_p_med", 0)} {und_esfuerzo}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_resultados_fatiga.get("tao_p_alt", 0)} {und_esfuerzo}

        τm = Fm / Asold
            τm = {dic_resultados_fatiga.get("tao_p_med", 0)} {und_esfuerzo}

    Cálculo de esfuerzo Von Misses alternante y medio:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_resultados_fatiga.get("sigma_p_von_misses_alt", 0)} {und_esfuerzo}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ'm = {dic_resultados_fatiga.get("sigma_p_von_misses_med", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia a última a la tensión:

        Sut = {dic_resultados_estatica["sut_pieza1"]} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS en la pieza 1:

        (FS * σ'a)/Se + ((FS * σ'm)/Sut)^2 = 1
            FS pieza1 = {dic_resultados_fatiga["fs_pieza1"]}

Conclusión: {dic_resultados_fatiga["conclusion_pieza1"]}


Para la pieza 2: (Pieza transversal a la carga aplicada)

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Fa / Asold
            σa = {dic_resultados_fatiga.get("sigma_t_alt", 0)} {und_esfuerzo}

        σm = Fm / Asold
            σm = {dic_resultados_fatiga.get("sigma_t_med", 0)} {und_esfuerzo}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Ma * c / I
            τa = {dic_resultados_fatiga.get("tao_t_alt", 0)} {und_esfuerzo}

        τm = Mm * c / I
            τm = {dic_resultados_fatiga.get("tao_t_med", 0)} {und_esfuerzo}

    Cálculo de esfuerzo de Von Misses alternante y medio:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_resultados_fatiga.get("sigma_t_von_misses_alt", 0)} {und_esfuerzo}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ"m = {dic_resultados_fatiga.get("sigma_t_von_misses_med", 0)} {und_esfuerzo}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia a última a la tensión:

        Sut = {dic_resultados_fatiga["sut_pieza2"]} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS en la pieza 2:

        (FS * σ'a)/Se + ((FS * σ'm)/Sut)^2 = 1
            FS pieza2 = {dic_resultados_fatiga["fs_pieza2"]} {und_esfuerzo}

Conclusión: {dic_resultados_fatiga["conclusion_pieza2"]}

"""

            informe += "\nAnálisis de fatiga completado.\n"

            informe += verificacion_pierna  # Porción de informe de verificación de pierna

            resumen += resumen_fatiga + verificacion_pierna_resumen

        else:

            informe += verificacion_pierna
            resumen += verificacion_pierna_resumen

    return informe, resumen


# ANALISIS DE RANURA

def informe_analisis_ranura_cp(nombre_proyecto, tipo_carga, dic_resultados_estatica, dic_resultados_fatiga, falla,
                               sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de analisis de soldadura de ranura
        sometida a carga paralela"""

    informe = f"""
{"*" * 10} Informe de Análisis de Soldadura de Ranura Sometida a Carga Paralela {tipo_carga.capitalize()} {"*" * 10}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados del análisis de soldadura de ranura sometida a carga paralela {tipo_carga}. El objetivo del análisis es evaluar si la junta soldada cumple con los requisitos mínimos de seguridad y funcionamiento (FDsoldadura = 3.33, FDpieza = 2.5), de acuerdo a la cátedra EMI, así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n"""  # Introducción

    resumen = ""

    resultados_estatica = f"""
Se procede a analizar por carga estática la soldadura y las piezas soldadas.

    F = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}

Cálculos realizados

    Área de la soldadura:

        A sold = {dic_resultados_estatica["area_sold_ecuacion"]}
            A sold = {dic_resultados_estatica.get("area_sold", 0)} {und_distancia}²

    Cálculo del esfuerzo cortante aplicado en la junta:

        τ = F / Asold
            τ = {dic_resultados_estatica.get("tao_sold", 0)} {und_esfuerzo}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_resultados_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura:

        FS sold = τ adm / τ
            FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}

Conclusión: {dic_resultados_estatica["conclusion_sold"]}


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_resultados_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de seguridad FS de la pieza 1:

        FS pieza1 = Ssy / τ
            FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza1"]}


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_resultados_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de seguridad FS de la pieza 2:

        FS pieza2 = Ssy / τ
            FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza2"]}\n

"""  # Porción con resultados de cálculos de análisis estático.

    resumen_estatica = f"""
    <body>

    <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA ESTÁTICA</h2>
    <hr>

    <p><strong>Factor de seguridad de la soldadura:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_sold'] >= 3.33 else 'red'};">FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_sold", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 1:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza1'] >= 2.5 else 'red'}">FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza1", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 2:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza2'] >= 2.5 else 'red'}">FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza2", 0)}</p>

    </body>
    """  # Resumen de resultados de análisis estático.

    resumen_fatiga = f"""
    <body>

    <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA DE FATIGA</h2>
    <hr>

    <p><strong>Factor de seguridad de la soldadura:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_resultados_fatiga.get('fs_sold', 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_sold", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 1:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza1", 0)}</p>

    <p><strong>Factor de seguridad de la pieza 2:</strong></p>

    <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}</p>
    <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza2", 0)}</p>

    </body>

    """  # Resumen de resultados de análisis de fatiga.

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_resultados_estatica.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_resultados_estatica.get("largo", 0)} {und_distancia}

    Tipo de union: Tope

    Carga Aplicada:

        Tipo: Estática
        Fuerza = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}
"""  # Datos de entrada para carga estática

        informe += resultados_estatica

        informe += "Análisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga Paralela Estática\n"

        resumen += resumen_estatica

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_resultados_fatiga.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_resultados_fatiga.get("largo", 0)} {und_distancia}

    Tipo de union: Tope

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima = {dic_resultados_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima = {dic_resultados_fatiga.get("Fmin", 0)} {und_fuerza}
"""  # Datos de entrada para de fatiga

        informe += resultados_estatica

        informe += "\nAnálisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga Paralela de Fatiga\n"

        resumen += resumen_estatica

        if not falla:

            informe += f"""
Se procede a analizar por carga de fatiga la soldadura y las piezas soldadas.

Cálculos realizados

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_resultados_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_resultados_fatiga.get("f_med", 0)} {und_fuerza}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión tope sometida a carga paralela, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_resultados_fatiga.get("kfs", 0)}

    Cálculo de esfuerzos cortantes alternantes y medios:

        τa = Kfs * Fa / Asold
            τa = {dic_resultados_fatiga.get("tao_alt", 0)} {und_esfuerzo}

        τm = Fm / Asold
            τm = {dic_resultados_fatiga.get("tao_med", 0)} {und_esfuerzo}


Para la soldadura:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura utilizando ecuación de Gerber:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS sold = {dic_resultados_fatiga.get("fs_sold", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_sold", 0)}


Para la pieza 1:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 1 utilizando ecuación de Gerber:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza1", 0)}


Para la pieza 2:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_pieza2", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 2 utilizando ecuación de Gerber:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza2", 0)}

                    """  # Resultados de análisis para carga de fatiga.

            informe += "\nAnálisis de fatiga completado.\n"

            resumen += resumen_fatiga

    return informe, resumen


def informe_analisis_ranura_ct(nombre_proyecto, tipo_carga, dic_resultados_estatica, dic_resultados_fatiga, falla,
                               sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de analisis de soldadura de ranura
        sometida a carga transversal"""

    informe = f"""
{"*" * 10} Informe de Análisis de Soldadura de Ranura Sometida a Carga Transversal {tipo_carga.capitalize()} {"*" * 10}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados del análisis de soldadura de ranura sometida a carga transversal {tipo_carga}. El objetivo del análisis es evaluar si la junta soldada cumple con los requisitos mínimos de seguridad y funcionamiento (FDsoldadura = 3.33, FDpieza = 2.5), de acuerdo a la cátedra EMI, así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n"""  # Introducción

    resumen = ""

    resultados_estatica = f"""
Se procede a analizar por carga estática la soldadura y las piezas soldadas.

    F = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}

Cálculos realizados

    Área de la soldadura:

        A sold = {dic_resultados_estatica["area_sold_ecuacion"]}
            A sold = {dic_resultados_estatica.get("area_sold", 0)} {und_distancia}²

    Cálculo del esfuerzo normal aplicado en la junta:

        σ = F / Asold
            σ = {dic_resultados_estatica.get("sigma_sold", 0)} {und_esfuerzo}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_resultados_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura:

        FS sold = Sy / σ
            FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}

Conclusión: {dic_resultados_estatica["conclusion_sold"]}


Para la pieza 1:

    Resistencia a la fluencia:

        Sy = {dic_resultados_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de seguridad FS de la pieza 1:

        FS pieza1 = Sy / σ
            FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza1"]}


Para la pieza 2:

    Resistencia a la fluencia:

        Sy = {dic_resultados_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de seguridad FS de la pieza 2:

        FS pieza2 = Sy / σ
            FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza2"]}\n

"""  # Porción con resultados de cálculos de análisis estático.

    resumen_estatica = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_sold'] >= 3.33 else 'red'};">FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza1'] >= 2.5 else 'red'}">FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza2'] >= 2.5 else 'red'}">FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza2", 0)}</p>

        </body>
        """  # Resumen de resultados de análisis estático.

    resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_resultados_fatiga.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza2", 0)}</p>

        </body>

        """  # Resumen de resultados de análisis de fatiga.

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_resultados_estatica.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_resultados_estatica.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_resultados_estatica.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_resultados_estatica["tipo_union"]}

    Carga Aplicada:

        Tipo: Estática
        Fuerza = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}
"""  # Datos de entrada para carga estática

        informe += resultados_estatica

        informe += "Análisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga Transversal Estática\n"

        resumen += resumen_estatica

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_resultados_fatiga.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_resultados_fatiga.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_resultados_fatiga.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_resultados_fatiga["tipo_union"]}

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima = {dic_resultados_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima = {dic_resultados_fatiga.get("Fmin", 0)} {und_fuerza}
"""  # Datos de entrada para de fatiga

        informe += resultados_estatica

        informe += "\nAnálisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga Transversal de Fatiga\n"

        resumen += resumen_estatica

        if not falla:
            informe += f"""
Se procede a analizar por carga de fatiga la soldadura y las piezas soldadas.

Cálculos realizados

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_resultados_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_resultados_fatiga.get("f_med", 0)} {und_fuerza}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión: {dic_resultados_fatiga["tipo_union"]}, sometida a carga transversal, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_resultados_fatiga.get("kfs", 0)}

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Fa / Asold
            σa = {dic_resultados_fatiga.get("sigma_alt", 0)} {und_esfuerzo}

        σm = Fm / Asold
            σm = {dic_resultados_fatiga.get("sigma_med", 0)} {und_esfuerzo}


Para la soldadura:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_sold", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_resultados_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura utilizando ecuación de Gerber:

        (FS * σa)/Se + ((FS * σm)/Sut)^2 = 1
            FS sold = {dic_resultados_fatiga.get("fs_sold", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_sold", 0)}


Para la pieza 1:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_resultados_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 1 utilizando ecuación de Gerber:

        (FS * σa)/Se + ((FS * σm)/Sut)^2 = 1
            FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza1", 0)}


Para la pieza 2:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_resultados_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 2 utilizando ecuación de Gerber:

        (FS * σa)/Se + ((FS * σm)/Sut)^2 = 1
            FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza2", 0)}

                    """  # Resultados de análisis para carga de fatiga.

            informe += "\nAnálisis de fatiga completado.\n"

            resumen += resumen_fatiga

    return informe, resumen


def informe_analisis_ranura_cf(nombre_proyecto, tipo_carga, dic_resultados_estatica, dic_resultados_fatiga, falla,
                               sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de analisis de soldadura de ranura
        sometida a carga de flexión debido a una fuerza excéntrica"""

    informe = f"""
{"*" * 10} Informe de Análisis de Soldadura de Ranura Sometida a Carga de Flexión debido a una Fuerza Externa {tipo_carga.capitalize()} {"*" * 10}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados del análisis de soldadura de ranura sometida a carga de flexión debido a una fuerza externa {tipo_carga}. El objetivo del análisis es evaluar si la junta soldada cumple con los requisitos mínimos de seguridad y funcionamiento (FDsoldadura = 3.33, FDpieza = 2.5), de acuerdo a la cátedra EMI, así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n"""  # Introducción

    resumen = ""

    resultados_estatica = f"""
Se procede a analizar por carga estática la soldadura y las piezas soldadas.

    F = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}

Cálculos realizados

    Distancia del eje nuetro hasta la soldadura (c):

        c = {dic_resultados_estatica["c_ecuacion"]}
            c = {dic_resultados_estatica["c"]} {und_distancia}

    Momento de Inercia (I):

        I = {dic_resultados_estatica["i_sold_ecuacion"]}
            I = {dic_resultados_estatica["i_sold"]} {und_distancia}^4

    Área efectiva de la soldadura:

        A sold = {dic_resultados_estatica["area_sold_ecuacion"]}
            A sold = {dic_resultados_estatica.get("area_sold", 0)} {und_distancia}²

    Cálculo del momento flector producido por la fuerza excéntrica:

        M = F * b
            M = {dic_resultados_estatica["momento_flector"]} {und_fuerza}{und_distancia}

    Esfuerzos aplicados en la junta:

        Cálculo del esfuerzo normal:

            σ = M * c / I
                σ = {dic_resultados_estatica.get("sigma", 0)} {und_esfuerzo}

        Cálculo del esfuerzo cortante:

            τ = F / Asold
                τ = {dic_resultados_estatica.get("tao", 0)} {und_esfuerzo}

        Cálculo del esfuerzo de Von Misses:

            σ' = sqrt(σ^2 + 3 * τ^2)
                σ' = {dic_resultados_estatica["sigma_von_misses"]} {und_esfuerzo}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_resultados_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura:

        FS sold = Sy / σ'
            FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}

Conclusión: {dic_resultados_estatica["conclusion_sold"]}


Para la pieza 1:

    Resistencia a la fluencia:

        Sy = {dic_resultados_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de seguridad FS de la pieza 1:

        FS pieza1 = Sy / σ'
            FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza1"]}


Para la pieza 2:

    Resistencia a la fluencia:

        Sy = {dic_resultados_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de seguridad FS de la pieza 2:

        FS pieza2 = Sy / σ'
            FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza2"]}\n

"""  # Porción con resultados de cálculos de análisis estático.

    resumen_estatica = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_sold'] >= 3.33 else 'red'};">FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza1'] >= 2.5 else 'red'}">FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza2'] >= 2.5 else 'red'}">FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza2", 0)}</p>

        </body>
        """  # Resumen de resultados de análisis estático.

    resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_resultados_fatiga.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza2", 0)}</p>

        </body>

        """  # Resumen de resultados de análisis de fatiga.

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_resultados_estatica.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_resultados_estatica.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_resultados_estatica.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_resultados_estatica["tipo_union"]}

    Carga Aplicada:

        Tipo: Estática
        Fuerza = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}
        Brazo (b) = {dic_resultados_estatica["b"]} {und_distancia}
"""  # Datos de entrada para carga estática

        informe += resultados_estatica

        informe += "Análisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga de Flexion Estática\n"

        resumen += resumen_estatica

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_resultados_fatiga.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_resultados_fatiga.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_resultados_fatiga.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_resultados_fatiga["tipo_union"]}

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima = {dic_resultados_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima = {dic_resultados_fatiga.get("Fmin", 0)} {und_fuerza}
        Brazo (b) = {dic_resultados_fatiga["b"]} {und_distancia}
"""  # Datos de entrada para de fatiga

        informe += resultados_estatica

        informe += "\nAnálisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga de Flexion de Fatiga\n"

        resumen += resumen_estatica

        if not falla:
            informe += f"""
Se procede a analizar por carga de fatiga la soldadura y las piezas soldadas.

Cálculos realizados

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_resultados_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_resultados_fatiga.get("f_med", 0)} {und_fuerza}

    Cálculo de momento flector alternante y medio:

        Momento flector alternante (Ma) = Fa * b
            Ma = {dic_resultados_fatiga.get("momento_flector_alt", 0)} {und_fuerza}{und_distancia}

        Momento flector medio (Mm) = Fm * b
            Mm = {dic_resultados_fatiga.get("momento_flector_med", 0)} {und_fuerza}{und_distancia}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión: {dic_resultados_fatiga["tipo_union"]}, sometida a carga de flexion, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_resultados_fatiga.get("kfs", 0)}

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Ma * c / I
            σa = {dic_resultados_fatiga.get("sigma_alt", 0)} {und_esfuerzo}

        σm = Mm * c / I
            σm = {dic_resultados_fatiga.get("sigma_med", 0)} {und_esfuerzo}

    Cálculo de esfuerzo cortante alternatne y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_resultados_fatiga.get("tao_alt", 0)} {und_esfuerzo}

        τm = Fm / Asold
            τm = {dic_resultados_fatiga.get("tao_med", 0)} {und_esfuerzo}

    Cálculo de esfuerzo de Von Misses alternante y medio:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_resultados_fatiga.get("sigma_von_misses_alt", 0)} {und_esfuerzo}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ'm = {dic_resultados_fatiga.get("sigma_von_misses_med", 0)} {und_esfuerzo}


Para la soldadura:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_sold", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_resultados_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura utilizando ecuación de Gerber:

        (FS * σ'a)/Se + ((FS * σ'm)/Sut)^2 = 1
            FS sold = {dic_resultados_fatiga.get("fs_sold", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_sold", 0)}


Para la pieza 1:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_resultados_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 1 utilizando ecuación de Gerber:

        (FS * σ'a)/Se + ((FS * σ'm)/Sut)^2 = 1
            FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza1", 0)}


Para la pieza 2:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_resultados_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 2 utilizando ecuación de Gerber:

        (FS * σ'a)/Se + ((FS * σ'm)/Sut)^2 = 1
            FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza2", 0)}

                    """  # Resultados de análisis para carga de fatiga.

            informe += "\nAnálisis de fatiga completado.\n"

            resumen += resumen_fatiga

    return informe, resumen


def informe_analisis_ranura_ctor(nombre_proyecto, tipo_carga, dic_resultados_estatica, dic_resultados_fatiga, falla,
                                 sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de analisis de soldadura de ranura
        sometida a carga de torsión pura"""

    informe = f"""
{"*" * 20} Informe de Análisis de Soldadura de Ranura Sometida a Carga de Torsión Pura {tipo_carga.capitalize()} {"*" * 20}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados del análisis de soldadura de ranura sometida a carga de torsión pura {tipo_carga}. El objetivo del análisis es evaluar si la junta soldada cumple con los requisitos mínimos de seguridad y funcionamiento (FDsoldadura = 3.33, FDpieza = 2.5), de acuerdo a la cátedra EMI, así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n"""  # Introducción

    resumen = ""

    resultados_estatica = f"""
Se procede a analizar por carga estática la soldadura y las piezas soldadas.

    T = {dic_resultados_estatica.get("Tmax", 0)} {und_fuerza}{und_distancia}

Cálculos realizados

    Distancia desde el centroide hasta el pto crítico de la soldadura (r):

        r = sqrt(({dic_resultados_estatica["rx_ecuacion"]})^2 + ({dic_resultados_estatica["ry_ecuacion"]})^2)
            r = {dic_resultados_estatica["r"]} {und_distancia}

    Momento de Inercia Polar (J):

        J = {dic_resultados_estatica["j_sold_ecuacion"]}
            J = {dic_resultados_estatica["j_sold"]} {und_distancia}^4

    Área de la soldadura:

        A sold = {dic_resultados_estatica["area_sold_ecuacion"]}
            A sold = {dic_resultados_estatica.get("area_sold", 0)} {und_distancia}²

    Esfuerzos cortante aplicado en la junta:

        τ = T * r / J
            τ = {dic_resultados_estatica.get("tao", 0)} {und_esfuerzo}


Para la soldadura:

    Cálculo de la resistencia cortante admisible:

        τ adm = 0.30 * Sut
            τ adm = {dic_resultados_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura:

        FS sold = τ adm / τ
            FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}

Conclusión: {dic_resultados_estatica["conclusion_sold"]}


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_resultados_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de seguridad FS de la pieza 1:

        FS pieza1 = Ssy / τ
            FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza1"]}


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_resultados_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de seguridad FS de la pieza 2:

        FS pieza2 = Ssy / τ
            FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza2"]}\n

"""  # Porción con resultados de cálculos de análisis estático.

    resumen_estatica = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_sold'] >= 3.33 else 'red'};">FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza1'] >= 2.5 else 'red'}">FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza2'] >= 2.5 else 'red'}">FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza2", 0)}</p>

        </body>
        """  # Resumen de resultados de análisis estático.

    resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_resultados_fatiga.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza2", 0)}</p>

        </body>

        """  # Resumen de resultados de análisis de fatiga.

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_resultados_estatica.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_resultados_estatica.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_resultados_estatica.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_resultados_estatica["tipo_union"]}

    Carga Aplicada:

        Tipo: Estática
        Torque = {dic_resultados_estatica.get("Tmax", 0)} {und_fuerza}{und_distancia}
"""  # Datos de entrada para carga estática

        informe += resultados_estatica

        informe += "Análisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga de Torsión Estática\n"

        resumen += resumen_estatica

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_resultados_fatiga.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_resultados_fatiga.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_resultados_fatiga.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_resultados_fatiga["tipo_union"]}

    Cargas Aplicadas:

        Tipo: Cíclica
        Torque máximo = {dic_resultados_fatiga.get("Tmax", 0)} {und_fuerza}{und_distancia}
        Torque mínimo = {dic_resultados_fatiga.get("Tmin", 0)} {und_fuerza}{und_distancia}
"""  # Datos de entrada para de fatiga

        informe += resultados_estatica

        informe += "\nAnálisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga de Torsión de Fatiga\n"

        resumen += resumen_estatica

        if not falla:
            informe += f"""
Se procede a analizar por carga de fatiga la soldadura y las piezas soldadas.

Cálculos realizados

    Cálculo de momento torsor (Torque) alternante y medio:

        Momento torsor alternante (Ta) = (Tmax - Tmin) / 2
            Ta = {dic_resultados_fatiga.get("Talt", 0)} {und_fuerza}{und_distancia}

        Momento torsor medio (Tm) = (Tmax + Tmin) / 2
            Tm = {dic_resultados_fatiga.get("Tmed", 0)} {und_fuerza}{und_distancia}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión: {dic_resultados_fatiga["tipo_union"]}, sometida a carga de torsión, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_resultados_fatiga.get("kfs", 0)}

    Cálculo de esfuerzos cortantes alternantes y medios:

        τa = Kfs * Ta * r / J
           τa = {dic_resultados_fatiga.get("tao_alt", 0)} {und_esfuerzo}

        τm = Tm * r / J
            τm = {dic_resultados_fatiga.get("tao_med", 0)} {und_esfuerzo}


Para la soldadura:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura utilizando ecuación de Gerber:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS sold = {dic_resultados_fatiga.get("fs_sold", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_sold", 0)}


Para la pieza 1:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 1 utilizando ecuación de Gerber:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza1", 0)}


Para la pieza 2:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_resultados_fatiga.get("sse_pieza2", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_resultados_fatiga.get("ssu_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 2 utilizando ecuación de Gerber:

        (FS * τa)/Sse + ((FS * τm)/Ssu)^2 = 1
            FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza2", 0)}

                    """  # Resultados de análisis para carga de fatiga.

            informe += "\nAnálisis de fatiga completado.\n"

            resumen += resumen_fatiga

    return informe, resumen


def informe_analisis_ranura_ccomb(nombre_proyecto, tipo_carga, dic_resultados_estatica, dic_resultados_fatiga, falla,
                                  sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):

    """Esta función le dará forma al informe y resumen de resultados de analisis de soldadura de ranura
    sometida a carga combinada debido a una fuerza excéntrica"""

    informe = f"""
{"*" * 10} Informe de Análisis de Soldadura de Ranura Sometida a Carga Combinada debido a una Fuerza Externa {tipo_carga.capitalize()} Excéntrica al Centroide {"*" * 10}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados del análisis de soldadura de ranura sometida a carga combinada debido a una fuerza externa {tipo_carga} excéntrica al centroide. El objetivo del análisis es evaluar si la junta soldada cumple con los requisitos mínimos de seguridad y funcionamiento (FDsoldadura = 3.33, FDpieza = 2.5), de acuerdo a la cátedra EMI, así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n"""  # Introducción

    resumen = ""

    resultados_estatica = f"""
Se procede a analizar por carga estática la soldadura y las piezas soldadas.

    F = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}

Cálculos realizados

    Distancia del eje nuetro hasta la soldadura (c):

        c = {dic_resultados_estatica["c_ecuacion"]}
            c = {dic_resultados_estatica["c"]} {und_distancia}

    Distancia en X desde el centroide hasta el punto crítico:

        rx = {dic_resultados_estatica["rx_ecuacion"]}
            rx = {dic_resultados_estatica["rx"]} {und_distancia}

    Distancia en Y desde el centroide hasta el punto crítico:

        ry = {dic_resultados_estatica["ry_ecuacion"]}
            ry = {dic_resultados_estatica["ry"]} {und_distancia}

    Momento de Inercia (I):

        I = {dic_resultados_estatica["i_sold_ecuacion"]}
            I = {dic_resultados_estatica["i_sold"]} {und_distancia}^4

    Momento de Inercia Polar (J):

        J = {dic_resultados_estatica["j_sold_ecuacion"]}
            J = {dic_resultados_estatica["j_sold"]} {und_distancia}^4

    Área de la soldadura:

        A sold = {dic_resultados_estatica["area_sold_ecuacion"]}
            A sold = {dic_resultados_estatica.get("area_sold", 0)} {und_distancia}²

    Cálculo del momento flector producido por la fuerza externa:

        M = F * bl
            M = {dic_resultados_estatica["momento_flector"]} {und_fuerza}{und_distancia}

    Cálculo del momento torsor producido por la fuerza externa:

        T = F * bt
            T = {dic_resultados_estatica["momento_torsor"]} {und_fuerza}{und_distancia}

    Esfuerzos aplicados en la junta:

        Cálculo del esfuerzo cortante primario:

            τ' = F / Asold
                τ' = {dic_resultados_estatica["tao_primario"]} {und_esfuerzo}

        Cálculo del esfuerzo cortante secundario en el eje X y en el eje Y:

            τ''x = T * ry / J
                τ''x = {dic_resultados_estatica["tao_secundario_x"]} {und_esfuerzo}

            τ''y = T * rx / J
                τ''y = {dic_resultados_estatica["tao_secundario_y"]} {und_esfuerzo}

        Cálculo de la componente en el eje X del esfuerzo cortante resultante:

            τx = τ''x
                τx = {dic_resultados_estatica["tao_x"]} {und_esfuerzo}

        Cálculo de la componente en el eje Y del esfuerzo cortante resultante:

            τy = τ' + τ''y
                τy = {dic_resultados_estatica["tao_y"]} {und_esfuerzo}

        Cálculo del esfuerzo cortante resultante en la soldadura:

            τ = sqrt((τx)^2 + (τy)^2)
                τ = {dic_resultados_estatica["tao"]} {und_esfuerzo}

        Cálculo del esfuerzo normal:

            σ = M * c / I
                σ = {dic_resultados_estatica["sigma"]} {und_esfuerzo}

        Cálculo del esfuerzo de Von Misses:

            σ' = sqrt(σ^2 + 3 * τ^2)
                σ' = {dic_resultados_estatica["sigma_von_misses"]} {und_esfuerzo}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_resultados_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura:

        FS sold = Sy / σ'
            FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}

Conclusión: {dic_resultados_estatica["conclusion_sold"]}


Para la pieza 1:

    Resistencia a la fluencia:

        Sy = {dic_resultados_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de seguridad FS de la pieza 1:

        FS pieza1 = Sy / σ'
            FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza1"]}


Para la pieza 2:

    Resistencia a la fluencia:

        Sy = {dic_resultados_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de seguridad FS de la pieza 2:

        FS pieza2 = Sy / σ'
            FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}

Conclusión: {dic_resultados_estatica["conclusion_pieza2"]}\n

"""  # Porción con resultados de cálculos de análisis estático.

    resumen_estatica = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_sold'] >= 3.33 else 'red'};">FS sold = {"{:.2f}".format(dic_resultados_estatica['fs_sold'])}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza1'] >= 2.5 else 'red'}">FS pieza1 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza1"])}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_estatica['fs_pieza2'] >= 2.5 else 'red'}">FS pieza2 = {"{:.2f}".format(dic_resultados_estatica["fs_pieza2"])}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_estatica.get("conclusion_pieza2", 0)}</p>

        </body>
        """  # Resumen de resultados de análisis estático.

    resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL ANÁLISIS POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_resultados_fatiga.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_resultados_fatiga.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_resultados_fatiga.get("conclusion_pieza2", 0)}</p>

        </body>

        """  # Resumen de resultados de análisis de fatiga.

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_resultados_estatica.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_resultados_estatica.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_resultados_estatica.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_resultados_estatica["tipo_union"]}

    Carga Aplicada:

        Tipo: Estática
        Fuerza = {dic_resultados_estatica.get("Fmax", 0)} {und_fuerza}
        Brazo longitudinal (bl) = {dic_resultados_estatica["bl"]} {und_distancia}
        Brazo transversal (bt) = {dic_resultados_estatica["bt"]} {und_distancia}
"""  # Datos de entrada para carga estática

        informe += resultados_estatica

        informe += "Análisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga Combinada Estática\n"

        resumen += resumen_estatica

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_resultados_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_resultados_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_resultados_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_resultados_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_resultados_fatiga.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_resultados_fatiga.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_resultados_fatiga.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_resultados_fatiga["tipo_union"]}

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima = {dic_resultados_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima = {dic_resultados_fatiga.get("Fmin", 0)} {und_fuerza}
        Brazo longitudinal (bl) = {dic_resultados_fatiga["bl"]} {und_distancia}
        Brazo transversal (bt) = {dic_resultados_fatiga["bt"]} {und_distancia}


"""  # Datos de entrada para de fatiga

        informe += resultados_estatica

        informe += "\nAnálisis estático completado.\n"

        resumen += "Tipo de carga aplicada en la junta: Carga Combinada de Fatiga\n"

        resumen += resumen_estatica

        if not falla:
            informe += f"""
Se procede a analizar por carga de fatiga la soldadura y las piezas soldadas.

Cálculos realizados

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_resultados_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_resultados_fatiga.get("f_med", 0)} {und_fuerza}

    Cálculo de momento flector alternante y medio:

        Momento flector alternante (Ma) = Fa * bl
            Ma = {dic_resultados_fatiga.get("momento_flector_alt", 0)} {und_fuerza}{und_distancia}

        Momento flector medio (Mm) = Fm * bl
            Mm = {dic_resultados_fatiga.get("momento_flector_med", 0)} {und_fuerza}{und_distancia}

    Cálculo de momento torsor alternante y medio:

        Momento torsor alternante (Ta) = Fm * bt
            Ta = {dic_resultados_fatiga.get("momento_torsor_alt", 0)} {und_fuerza}{und_distancia}

        Momento torsor medio (Tm) = Fm * bt
            Tm {dic_resultados_fatiga.get("momento_torsor_med", 0)} {und_fuerza}{und_distancia}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión: {dic_resultados_fatiga.get("tipo_union", 0)}, sometida a carga combinada, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_resultados_fatiga.get("kfs", 0)}

    Esfuerzos aplicados en la junta:

        Cálculo del esfuerzo cortante primario alternante y medio:

            τ'a = Kfs * Fa / Asold
                τ'a = {dic_resultados_fatiga.get("tao_primario_alt", 0)} {und_esfuerzo}

            τ'm = Fm / Asold
                τ'm = {dic_resultados_fatiga.get("tao_primario_med", 0)} {und_esfuerzo}

        Cálculo del esfuerzo cortante secundario alternante en el eje X y en el eje Y:

            τ''a x = Kfs * Ta * ry / J
                τ''a x = {dic_resultados_fatiga.get("tao_secundario_alt_x", 0)} {und_esfuerzo}

            τ''a y = Kfs * Ta * rx / J
                τ''a y = {dic_resultados_fatiga.get("tao_secundario_alt_y", 0)} {und_esfuerzo}

        Cálculo del esfuerzo cortante secundario medio en el eje X y en el eje Y:

            τ''m x = Tm * ry / J
                τ''m x = {dic_resultados_fatiga.get("tao_secundario_med_x", 0)} {und_esfuerzo}

            τ''m y = Tm * rx / J
                τ''m y = {dic_resultados_fatiga.get("tao_secundario_med_y", 0)} {und_esfuerzo}

        Cálculo de las componentes X e Y del esfuerzo cortante alternante:

            τa x = τ''a x
                τa x = {dic_resultados_fatiga.get("tao_alt_x", 0)} {und_esfuerzo}

            τa y = τ'a + τ''a y
                τa y ={dic_resultados_fatiga.get("tao_alt_y", 0)} {und_esfuerzo}

        Cálculo de las componentes X e Y del esfuerzo cortante medio:

            τm x = τ''m x
                τm x = {dic_resultados_fatiga.get("tao_med_x", 0)} {und_esfuerzo}

            τm y = τ'm + τ''m y
                τm y = {dic_resultados_fatiga.get("tao_med_y", 0)} {und_esfuerzo}

        Cálculo del esfuerzo cortante alternante y medio resultante:

            τa = sqrt((τa x)^2 + (τa y)^2)
                τa = {dic_resultados_fatiga.get("tao_alt", 0)} {und_esfuerzo}

            τm = sqrt((τm x)^2 + (τm y)^2)
                τm = {dic_resultados_fatiga.get("tao_med", 0)} {und_esfuerzo}

        Cálculo del esfuerzo normal alternante y medio:

            σa = Kfs * Ma * c / I
                σa = {dic_resultados_fatiga.get("sigma_alt", 0)} {und_esfuerzo}

            σm = Mm * c / I
                σm = {dic_resultados_fatiga.get("sigma_med", 0)} {und_esfuerzo}

        Cálculo del esfuerzo de Von Misses alternante y medio:

            σ'a = sqrt((σa)^2 + 3 * (τa)^2)
                σ'a = {dic_resultados_fatiga.get("sigma_von_misses_alt", 0)} {und_esfuerzo}

            σ'm = sqrt((σm)^2 + 3 * (τm)^2)
                σ'm = {dic_resultados_fatiga.get("sigma_von_misses_med", 0)} {und_esfuerzo}


Para la soldadura:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_sold", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_resultados_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la soldadura utilizando ecuación de Gerber:

        (FS * σ'a)/Se + ((FS * σ'm)/Sut)^2 = 1
            FS sold = {dic_resultados_fatiga.get("fs_sold", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_sold", 0)}


Para la pieza 1:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_resultados_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 1 utilizando ecuación de Gerber:

        (FS * σ'a)/Se + ((FS * σ'm)/Sut)^2 = 1
            FS pieza1 = {dic_resultados_fatiga.get("fs_pieza1", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza1", 0)}


Para la pieza 2:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_resultados_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_resultados_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo del Factor de Seguridad FS de la pieza 2 utilizando ecuación de Gerber:

        (FS * σ'a)/Se + ((FS * σ'm)/Sut)^2 = 1
            FS pieza2 = {dic_resultados_fatiga.get("fs_pieza2", 0)}

Conclusión: {dic_resultados_fatiga.get("conclusion_pieza2", 0)}

                    """  # Resultados de análisis para carga de fatiga.

            informe += "\nAnálisis de fatiga completado.\n"

            resumen += resumen_fatiga

    return informe, resumen


# DISEÑO FILETE

# CARGA PERMISIBLE

# Informe para carga permisible: carga paralela
def informe_diseno_carga_filete_cp(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                                   sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):

    """Esta función le dará forma al informe y resumen de resultados de cálculo de diseño para carga permisible de
    soldadura de filete sometida a carga paralela"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Carga Permisible para Soldadura de Filete Sometida a Carga Paralela {tipo_carga.capitalize()} {"*" * 5}
    \nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
            """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados de los cálculos para el diseño de la carga permisible para soldadura de filete sometida a carga paralela {tipo_carga}. El objetivo es determinar la magnitud de la carga máxima permisible en la junta soldada, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI. Así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n""" # Introducción

    resumen = ""

    if dic_diseno_estatica is None:

        verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_diseno_fatiga.get("verificacion_pierna", 0)}

    """

        verificacion_pierna_resumen = f"""
        <br>
        <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
        <p>{dic_diseno_fatiga.get("verificacion_pierna", 0)}</p>

        """  # Porción con verificación de pierna para el resumen

    else:

        verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_diseno_estatica.get("verificacion_pierna", 0)}

"""

        verificacion_pierna_resumen = f"""
        <br>
        <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
        <p>{dic_diseno_estatica.get("verificacion_pierna", 0)}</p>

        """  # Porción con verificación de pierna para el resumen

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): {dic_diseno_estatica.get("pierna", 0)} {und_distancia}
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_estatica.get("ancho", 0)} {und_distancia}

    Tipo de union:  Intermedia

    Cargas Aplicadas:

        Tipo: Estática
        Fuerza: ** A determinar **

    Espesor menor entre las piezas:

        Espesor (e) = {dic_diseno_estatica.get("espesor_menor_piezas", 0)} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Garganta (t) = 0.707 * h
            t = {dic_diseno_estatica.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica.get("area_sold", 0)} {und_distancia}²


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la soldadura:

        τ sold = 1.414 * F / Asold
            τ sold = {dic_diseno_estatica.get("tao_sold", 0)}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = τ adm / τ sold
            Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}  *


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 1:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica.get("tao_pieza1", 0)}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Ssy / τ pieza1
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}  **


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 2:

        τ pieza2 = F / Asold
            τ pieza2 = {dic_diseno_estatica.get("tao_pieza2", 0)}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Ssy / τ pieza2
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        informe += verificacion_pierna

        resumen = f"""
    <body>

    <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
    <hr>

    <p><strong>Carga permisible en la soldadura:</strong></p>

    <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

    <p><strong>Carga permisible en la pieza 1:</strong></p>

    <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

    <p><strong>Carga permisible en la pieza 2:</strong></p>

    <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

    <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

    </body>
    """  # Resumen de resultados del diseño por carga estática.

        resumen += verificacion_pierna_resumen

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): {dic_diseno_fatiga.get("pierna", 0)} {und_distancia}
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_fatiga.get("ancho", 0)} {und_distancia}

    Tipo de union:  Intermedia

    Cargas Aplicadas:

        Tipo: Cíclica
        Relación de carga (Fmax/Fmin) = {dic_diseno_fatiga.get("relacion_cargas", 0)}

    Espesor menor entre las piezas:

        Espesor (e): {dic_diseno_fatiga.get("espesor_menor_piezas", 0)} {und_distancia}
"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la fuerza mínima aplicada, según la relación de fuerzas Fmax/Fmin **

    Cálculos de parámetros geométricos de la soldadura:

        Garganta (t) = 0.707 * h
            t = {dic_diseno_fatiga.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_diseno_fatiga["lt_ecuacion"]}
            lt = {dic_diseno_fatiga.get("longitud_total", 0)} {und_distancia}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_fatiga.get("area_sold", 0)} {und_distancia}²

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de filete de unión intermedia sometida a carga paralela, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo de esfuerzo cortante alternante y medio:

        τa = τa = Kfs * 1.414 * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_alt_sold", 0)}

        τm = 1.414 * Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_med_sold", 0)}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la soldadura utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            F sold = {dic_diseno_fatiga.get("f_sold", 0)} {und_fuerza} *


Para la pieza 1:

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_alt_pieza1", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_med_pieza1", 0)}

    Cálculo de la resistencia a la fatiga al ortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 1 utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            F pieza1 = {dic_diseno_fatiga.get("f_pieza1", 0)} {und_fuerza} **


Para la pieza 2:

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_alt_pieza2", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_med_pieza2", 0)}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza2", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza2", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 2 utilizando la ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            F pieza2 = {dic_diseno_fatiga.get("f_pieza2", 0)} {und_fuerza} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se selecciona la menor de las fuerzas calculadas (*, **, ***) y se multiplica por la relación de carga para determinar la fuerza máxima permisible de la junta.

Fperm = Relación * Fmin  = {dic_diseno_fatiga.get("relacion_cargas")} * {dic_diseno_fatiga.get("f_min")} {und_fuerza}

Por lo que, {dic_diseno_fatiga.get("conclusion_fperm")}.


Diseño por fatiga de la carga permisible completado.


"""  # Resultados de diseño para carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
<body>

<h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
<hr>

<p><strong>Carga permisible en la soldadura:</strong></p>

<p style="margin-left: 20px; color: blue;">Fperm sold = {"{:.2f}".format(dic_diseno_fatiga.get("f_sold") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

<p><strong>Carga permisible en la pieza 1:</strong></p>

<p style="margin-left: 20px; color: blue;">Fperm pieza1 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza1") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

<p><strong>Carga permisible en la pieza 2:</strong></p>

<p style="margin-left: 20px; color: blue;">Fperm pieza2 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza2") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

<p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_fperm")} </strong></p>

</body>
"""  # Resumen de resultados del diseño por fatiga

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
<br><body>

<p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

<p><strong>Factor de seguridad de la soldadura:</strong></p>

<p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
<p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

<p><strong>Factor de seguridad de la pieza 1:</strong></p>

<p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
<p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

<p><strong>Factor de seguridad de la pieza 2:</strong></p>

<p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
<p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

</body>
"""

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            informe += verificacion_pierna

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += verificacion_pierna_resumen

        else:

            informe += verificacion_estatica

            informe += f"Al presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno = f"""

Cálculos realizados

Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

    τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la soldadura:

        τ sold = 1.414 * F / Asold
            τ sold = {dic_diseno_estatica.get("tao_sold", 0)}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = τ adm / τ sold
            Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}  *


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 1:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica.get("tao_pieza1", 0)}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Ssy / τ pieza1
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}  **


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 2:

        τ pieza2 = {dic_diseno_estatica.get("tao_pieza2", 0)}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Ssy / τ pieza2
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la mayor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

            """  # Porción con resultados del rediseño por estática.

            informe += resultados_rediseno

            informe += verificacion_pierna

            resumen_estatica = f"""
    <body>

    <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
    <hr>

    <p><strong>Carga permisible en la soldadura:</strong></p>

    <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

    <p><strong>Carga permisible en la pieza 1:</strong></p>

    <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

    <p><strong>Carga permisible en la pieza 2:</strong></p>

    <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

    <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

    </body>
    """  # Resumen de resultados del rediseño por estática.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

            resumen += verificacion_pierna_resumen

    return informe, resumen


# Informe para carga permisible: carga transversal
def informe_diseno_carga_filete_ct(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                                   sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de cálculo de diseño para carga permisible de
    soldadura de filete sometida a carga transversal"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Carga Permisible para Soldadura de Filete Sometida a Carga Transversal {tipo_carga.capitalize()} {"*" * 5}
    \nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
            """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados de los cálculos para el diseño de la carga permisible para soldadura de filete sometida a carga transversal {tipo_carga}. El objetivo es determinar la magnitud de la carga máxima permisible en la junta soldada, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI. Así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n""" # Introducción

    resumen = ""

    if dic_diseno_estatica is None:

        verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_diseno_fatiga.get("verificacion_pierna", 0)}

        """

        verificacion_pierna_resumen = f"""
            <br>
            <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
            <p>{dic_diseno_fatiga.get("verificacion_pierna", 0)}</p>

            """  # Porción con verificación de pierna para el resumen

    else:

        verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_diseno_estatica.get("verificacion_pierna", 0)}

    """

        verificacion_pierna_resumen = f"""
            <br>
            <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
            <p>{dic_diseno_estatica.get("verificacion_pierna", 0)}</p>

            """  # Porción con verificación de pierna para el resumen

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): {dic_diseno_estatica.get("pierna", 0)} {und_distancia}
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_estatica.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_estatica.get("radio", 0)} {und_distancia}

    Tipo de union:  {dic_diseno_estatica.get("tipo_union", 0)}

    Carga Aplicada:

        Tipo: Estática
        Fuerza: ** A determinar **

    Espesor menor entre las piezas:

        Espesor (e) = {dic_diseno_estatica.get("espesor_menor_piezas", 0)} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar la carga permisible para la junta soldada por carga estática.

Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Garganta (t) = 0.707 * h
            t = {dic_diseno_estatica.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica.get("area_sold", 0)} {und_distancia}²


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica["tao_adm_sold"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la soldadura:

        τ sold = 1.414 * F / Asold
            τ sold = {dic_diseno_estatica["tao_sold"]}

    Cálculo del esfuerzo cortante en la soldadura:

        FS sold = τ adm / τ sold
            F sold = {dic_diseno_estatica.get("f_max_sold", 0)} {und_fuerza} *


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica["ssy_pieza1"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 1:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica["tao_pieza1"]}

    Cálculo de F = Fmin de la soldadura:

        FD pieza = Ssy / τ pieza1
            F pieza1 = {dic_diseno_estatica.get("f_max_pieza1", 0)} {und_fuerza} **


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del esfuerzo normal en la pieza 2:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica.get("sigma_pieza2", 0)}

    Cálculo de F = Fmin de la soldadura:

        FD pieza = Sy / σ pieza2
            F pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

"""  # Resultados de cálculos de diseño por carga estática

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        informe += verificacion_pierna

        resumen = f"""
    <body>

    <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
    <hr>

    <p><strong>Carga permisible en la soldadura:</strong></p>

    <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

    <p><strong>Carga permisible en la pieza 1:</strong></p>

    <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

    <p><strong>Carga permisible en la pieza 2:</strong></p>

    <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

    <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

    </body>
    """  # Resumen de resultados de análisis estático.

        resumen += verificacion_pierna_resumen

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1 (pieza paralela a la carga):
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2 (pieza transversal):
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): {dic_diseno_fatiga.get("pierna", 0)} {und_distancia}
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_fatiga.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_fatiga.get("radio", 0)} {und_distancia}

    Tipo de union:  {dic_diseno_fatiga.get("tipo_union", 0)}

    Cargas Aplicadas:

        Tipo: Cíclica
        Relación de carga (Fmax/Fmin) = {dic_diseno_fatiga.get("relacion_cargas", 0)}

    Espesor menor entre las piezas:

        Espesor (e): {dic_diseno_fatiga.get("espesor_menor_piezas", 0)} {und_distancia}
"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la carga permisible por la junta soldada.

Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Garganta (t) = 0.707 * h
            t = {dic_diseno_fatiga.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_diseno_fatiga["lt_ecuacion"]}
            lt = {dic_diseno_fatiga.get("longitud_total", 0)} {und_distancia}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_fatiga.get("area_sold", 0)} {und_distancia}²

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de filete de unión intermedia sometida a carga paralela, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo del esfuerzo cortante alternante y medio:

        τa = τa = Kfs * 1.414 * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_alt_sold", 0)}

        τm = 1.414 * Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_med_sold", 0)}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la soldadura utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            F sold = {dic_diseno_fatiga.get("f_sold", 0)} {und_fuerza} *


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Cálculo del esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_p_alt", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_p_med", 0)}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la soldadura utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            F pieza1 = {dic_diseno_fatiga.get("f_pieza1", 0)} {und_fuerza} **


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Cálculo del esfuerzo normal alternante y medio:

        σa = Kfs * Fa / Asold
            σa = {dic_diseno_fatiga.get("sigma_t_alt", 0)}

        σm = Fm / Asold
            σm = {dic_diseno_fatiga.get("sigma_t_med", 0)}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la soldadura utilizando ecuación de Gerber:

        (FD * σa)/Se + ((FD * σm)/Sut)^2 = 1
            F pieza2 = {dic_diseno_fatiga.get("f_pieza2", 0)} {und_fuerza} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se selecciona la menor de las fuerzas calculadas (*, **, ***) y se multiplica por la relación de carga para determinar la fuerza máxima permisible de la junta.

Fperm = Relación * Fmin  = {dic_diseno_fatiga.get("relacion_cargas")} * {dic_diseno_fatiga.get("f_min")} {und_fuerza}

Por lo que, {dic_diseno_fatiga.get("conclusion_fperm")}.


Diseño por fatiga de la carga permisible completado.


                    """  # Resultados de diseño para carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {"{:.2f}".format(dic_diseno_fatiga.get("f_sold") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza1") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza2") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados de análisis de fatiga

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            informe += verificacion_pierna

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += verificacion_pierna_resumen

        else:

            informe += verificacion_estatica

            informe += f"\nAl presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno = f"""

Cálculos realizados

Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica["tao_adm_sold"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la soldadura:

        τ sold = 1.414 * F / Asold
            τ sold = {dic_diseno_estatica["tao_sold"]}

    Cálculo del esfuerzo cortante en la soldadura:

        FS sold = τ adm / τ sold
            F sold = {dic_diseno_estatica.get("f_max_sold", 0)} {und_fuerza} *


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica["ssy_pieza1"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 1:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica["tao_pieza1"]}

    Cálculo de F = Fmin de la soldadura:

        FS pieza1 = Ssy / τ pieza1
            F pieza1 = {dic_diseno_estatica.get("f_max_pieza1", 0)} {und_fuerza} **


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del esfuerzo normal en la pieza 2:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica.get("sigma_pieza2", 0)}

    Cálculo de F = Fmin de la soldadura:

        FS pieza2 = Sy / σ pieza2
            F pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la mayor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

            """  # Porción con resultados de cálculos de análisis estático.

            informe += resultados_rediseno

            informe += verificacion_pierna

            resumen_estatica = f"""
            <body>

            <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
            <hr>

            <p><strong>Carga permisible en la soldadura:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

            <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

            </body>
            """  # Resumen de resultados del rediseño por estática.

            resumen += resumen_fatiga

            resumen += resumen_estatica

            resumen += verificacion_estatica_resumen

            resumen += verificacion_pierna_resumen

    return informe, resumen


# Informe carga permisible: carga de flexion
def informe_diseno_carga_filete_cf(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                                   sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de cálculo de diseño para carga permisible de
    soldadura de filete sometida a carga de flexión debido a una fuerza excéntrica"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Carga Permisible para Soldadura de Filete Sometida a Carga de Flexión debido a una Fuerza Externa {tipo_carga.capitalize()} {"*" * 5}
    \nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
            """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados de los cálculos para el diseño de la carga permisible para soldadura de filete sometida a carga de flexión debido a una fuerza externa {tipo_carga}. El objetivo es determinar la magnitud de la carga máxima permisible en la junta soldada, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI. Así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n""" # Introducción

    resumen = ""

    if dic_diseno_estatica is None:

        verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_diseno_fatiga.get("verificacion_pierna", 0)}

        """

        verificacion_pierna_resumen = f"""
            <br>
            <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
            <p>{dic_diseno_fatiga.get("verificacion_pierna", 0)}</p>

            """  # Porción con verificación de pierna para el resumen

    else:

        verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_diseno_estatica.get("verificacion_pierna", 0)}

    """

        verificacion_pierna_resumen = f"""
            <br>
            <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
            <p>{dic_diseno_estatica.get("verificacion_pierna", 0)}</p>

            """  # Porción con verificación de pierna para el resumen

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}
    Dimensiones de la soldadura:

        Pierna (h): {dic_diseno_estatica.get("pierna", 0)} {und_distancia}
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_estatica.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_estatica.get("radio", 0)} {und_distancia}

    Tipo de union:  {dic_diseno_estatica.get("tipo_union", 0)}

    Cargas Aplicadas:

        Tipo: Estática
        Fuerza: ** A determinar **
        Brazo (b) = {dic_diseno_estatica.get("b", 0)} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e) = {dic_diseno_estatica.get("espesor_menor_piezas", 0)} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""

Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Cálculos de parámetros geométricos:

        Garganta (t) = 0.707 * h
            t = {dic_diseno_estatica.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

        Distancia del eje nuetro hasta la soldadura (c) = {dic_diseno_estatica["c_ecuacion"]}
            c = {dic_diseno_estatica["c"]} {und_distancia}

    Momento de Inercia (I):

        Para la soldadura:
            I sold = {dic_diseno_estatica["i_sold_ecuacion"]}
                I sold = {dic_diseno_estatica["i_sold"]} {und_distancia}^4

        Para las piezas:
            I piezas = {dic_diseno_estatica["i_pieza_ecuacion"]}
                I piezas = {dic_diseno_estatica["i_pieza"]} {und_distancia}^4

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica["area_sold"]} {und_distancia}²

    Cálculo del momento flector producido por la fuerza externa:

        M = F * b
            M = {dic_diseno_estatica["momento_flector"]}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_diseno_estatica.get("tao_primario", 0)}

    Cálculo del esfuerzo cortante secundario:

        τ'' sold = M * c / I
            τ'' sold = {dic_diseno_estatica["tao_secundario"]}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τ')^2 + (τ'')^2)
            τ sold = {dic_diseno_estatica["tao_sold"]}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = τ adm / τ sold
            Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}  *


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza1"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza1 = M * c / I
            σ pieza1 = {dic_diseno_estatica["sigma_p"]}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica["tao_p"]}

    Cálculo del esfuerzo Von Misses σ':

        σ' pieza1 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza1 = {dic_diseno_estatica["sigma_von_misses_1"]}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Sy / σ'
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}  **


Para la pieza 2: (Pieza transversal a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica["sigma_t"]}

    Cálculo del esfuerzo cortante:

        τ pieza2 = M * c / I
            τ pieza2 = {dic_diseno_estatica["tao_t"]}

    Cálculo del esfuerzo de Von Misses σ':

        σ' pieza2 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza2 = {dic_diseno_estatica["sigma_von_misses_2"]}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Sy / σ'
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        informe += verificacion_pierna

        resumen = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados de análisis estático.

        resumen += verificacion_pierna_resumen

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): {dic_diseno_fatiga.get("pierna", 0)} {und_distancia}
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_fatiga.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_fatiga.get("radio", 0)} {und_distancia}

    Tipo de union:  Unión T

    Cargas Aplicadas:

        Tipo: Cíclica
        Relación de carga (Fmax/Fmin) = {dic_diseno_fatiga.get("relacion_cargas", 0)}
        Brazo (b) = {dic_diseno_fatiga.get("b", 0)} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e): {dic_diseno_fatiga.get("espesor_menor_piezas", 0)} {und_distancia}
"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
**************
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la fuerza mínima aplicada, según la relación de fuerzas Fmax/Fmin **

    Cálculos de parámetros geométricos de la soldadura:

        Cálculos de parámetros geométricos de la soldadura:

        Garganta (t) = 0.707 * h
            t = {dic_diseno_fatiga.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_diseno_fatiga["lt_ecuacion"]}
            lt = {dic_diseno_fatiga.get("longitud_total", 0)} {und_distancia}

        Distancia del eje neutro hasta la soldadura (c) = {dic_diseno_fatiga["c_ecuacion"]}
            c = {dic_diseno_fatiga.get("c", 0)} {und_distancia}

    Momento de Inercia (I):

        Para la soldadura:
            I sold = {dic_diseno_fatiga["i_sold_ecuacion"]}
                I sold = {dic_diseno_fatiga.get("i_sold", 0)} {und_distancia}^4

        Para las piezas:
            I piezas = {dic_diseno_fatiga["i_pieza_ecuacion"]}
                I piezas = {dic_diseno_fatiga.get("i_pieza", 0)} {und_distancia}^4

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_fatiga.get("area_sold", 0)} {und_distancia}²

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)}

    Cálculo de momento flector alternante y medio:

        Momento flector alternante (Ma) = Fa * b
            Ma = {dic_diseno_fatiga.get("momento_flector_alt", 0)}

        Momento flector medio (Mm) = Fm * b
            Mm = {dic_diseno_fatiga.get("momento_flector_med", 0)}

    Factor de concentración de esfuerzo reducido

        Para soldadura de filete de unión T sometida a carga de flexión, el factor de concentración de esfuerzo reducido es:

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo de esfuerzo cortante primario alternante y medio:

        τa' = Kfs * 1.414 * Fa / Asold
            τa' = {dic_diseno_fatiga.get("tao_primario_alt", 0)}

        τm' = 1.414 * Fm / Asold
            τm' = {dic_diseno_fatiga.get("tao_primario_med", 0)}

    Cálculo de esfuerzo cortante secundario alternante y medio:

        τa'' = Kfs * Ma * c / I
            τa'' = {dic_diseno_fatiga.get("tao_secundario_alt", 0)}

        τm'' = Mm * c / I
            τm'' = {dic_diseno_fatiga.get("tao_secundario_med", 0)}

    Cálculo de esfuerzo cortante resultante alternante y medio:

        τa = sqrt((τa')^2 + (τa'')^2)
            τa = {dic_diseno_fatiga.get("tao_alt_sold", 0)}

        τm = sqrt((τm')^2 + (τm'')^2)
            τm = {dic_diseno_fatiga.get("tao_med_sold", 0)}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la soldadura utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            F sold = {dic_diseno_fatiga.get("f_sold", 0)} {und_fuerza} *


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Ma * c / I
            σa = {dic_diseno_fatiga.get("sigma_p_alt", 0)}

        σm = Mm * c / I
            σm = {dic_diseno_fatiga.get("sigma_p_med", 0)}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_p_alt", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_p_med", 0)}

    Cálculo de esfuerzo de Von Misses alternante y medio:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_diseno_fatiga.get("sigma_p_von_misses_alt", 0)}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ'm = {dic_diseno_fatiga.get("sigma_p_von_misses_med", 0)}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 1 utilizando ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            F pieza1 = {dic_diseno_fatiga.get("f_pieza1", 0)} {und_fuerza} **


Para la pieza 2: (Pieza transversal a la carga aplicada)

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Fa / Asold
            σa = {dic_diseno_fatiga.get("sigma_t_alt", 0)}

        σm = Fm / Asold
            σm = {dic_diseno_fatiga.get("sigma_t_med", 0)}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Ma * c / I
            τa = {dic_diseno_fatiga.get("tao_t_alt", 0)}

        τm = Mm * c / I
            τm = {dic_diseno_fatiga.get("tao_t_med", 0)}

    Cálculo de esfuerzo de Von Misses alternante y medio:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_diseno_fatiga.get("sigma_t_von_misses_alt", 0)}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ'm = {dic_diseno_fatiga.get("sigma_t_von_misses_med", 0)}

    Cálculo de resistencia a la fatiga de la pieza 2:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Cálculo de la resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 2 utilizando la ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            F pieza2 = {dic_diseno_fatiga.get("f_pieza2", 0)} {und_fuerza} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se selecciona la menor de las fuerzas calculadas (*, **, ***) y se multiplica por la relación de carga para determinar la fuerza máxima permisible de la junta.

Fperm = Relación * Fmin  = {dic_diseno_fatiga.get("relacion_cargas")} * {dic_diseno_fatiga.get("f_min")} {und_fuerza}

Por lo que, {dic_diseno_fatiga.get("conclusion_fperm")}.


Diseño por fatiga de la carga permisible completado.


"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {"{:.2f}".format(dic_diseno_fatiga.get("f_sold") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza1") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza2") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados del diseño por fatiga

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            informe += verificacion_pierna

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += verificacion_pierna_resumen

        else:

            informe += verificacion_estatica

            informe += f"\nAl presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno_estatica = f"""
Cálculos realizados

    Cálculo del momento flector producido por la fuerza externa:

        M = F * b
            M = {dic_diseno_estatica["momento_flector"]}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_diseno_estatica.get("tao_primario", 0)}

    Cálculo del esfuerzo cortante secundario:

        τ'' sold = M * c / I
            τ'' sold = {dic_diseno_estatica["tao_secundario"]}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τ')^2 + (τ'')^2)
            τ sold = {dic_diseno_estatica["tao_sold"]}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = τ adm / τ sold
            Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}  *


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza1"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza1 = M * c / I
            σ pieza1 = {dic_diseno_estatica["sigma_p"]}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica["tao_p"]}

    Cálculo del esfuerzo Von Misses σ':

        σ' pieza1 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza1 = {dic_diseno_estatica["sigma_von_misses_1"]}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Sy / σ'
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}  **


Para la pieza 2: (Pieza transversal a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica["sigma_t"]}

    Cálculo del esfuerzo cortante:

        τ pieza2 = M * c / I
            τ pieza2 = {dic_diseno_estatica["tao_t"]}

    Cálculo del esfuerzo de Von Misses σ':

        σ' pieza2 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza2 = {dic_diseno_estatica["sigma_von_misses_2"]}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Sy / σ'
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

            """  # Porción con resultados de cálculos de análisis estático.

            informe += resultados_rediseno_estatica

            informe += verificacion_pierna

            resumen_estatica = f"""
            <body>

            <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
            <hr>

            <p><strong>Carga permisible en la soldadura:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

            <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

            </body>
            """  # Resumen de resultados del rediseño por estática.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

            resumen += verificacion_pierna_resumen

    return informe, resumen


def informe_diseno_carga_filete_ctor(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion,
                                     dic_diseno_estatica, sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1,
                                     acero2, electrodo):

    """Esta función le dará forma al informe y resumen de resultados del diseño de la carga permisible de soldadura de filete
    sometida a carga de torsión debido a una fuerza excéntrica"""

    informe = f"""
{"*" * 5} Informe de Diseño de la Carga Permisible para Soldadura de Filete Sometida a Carga de Torsión debido a una Fuerza Externa {tipo_carga.capitalize()} {"*" * 5}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados del diseño de la carga permisible para soldadura de filete sometida a carga de torsión debido a una fuerza externa {tipo_carga}. El objetivo es determinar la magnitud de la carga máxima permisible en la junta soldada, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI. Así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n""" # Introducción

    resumen = ""

    if dic_diseno_estatica is None:

        verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_diseno_fatiga.get("verificacion_pierna", 0)}

        """

        verificacion_pierna_resumen = f"""
            <br>
            <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
            <p>{dic_diseno_fatiga.get("verificacion_pierna", 0)}</p>

            """  # Porción con verificación de pierna para el resumen

    else:

        verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_diseno_estatica.get("verificacion_pierna", 0)}

    """

        verificacion_pierna_resumen = f"""
            <br>
            <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
            <p>{dic_diseno_estatica.get("verificacion_pierna", 0)}</p>

            """  # Porción con verificación de pierna para el resumen

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): {dic_diseno_estatica.get("pierna", 0)} {und_distancia}
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_estatica.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_estatica.get("radio", 0)} {und_distancia}

    Tipo de union:  {dic_diseno_estatica.get("tipo_union", 0)}

    Cargas Aplicadas:

        Tipo: Estática
        Fuerza: ** A determinar **
        Brazo (b) = {dic_diseno_estatica.get("b", 0)} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e) = {dic_diseno_estatica.get("espesor_menor_piezas", 0)} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""

Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

        Cálculos de parámetros geométricos:

            Garganta (t) = 0.707 * h
                t = {dic_diseno_estatica.get("garganta", 0)} {und_distancia}

            Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
                lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

            Distancia en X desde el centroide hasta el punto crítico (rx) = {dic_diseno_estatica["rx_ecuacion"]}
                rx = {dic_diseno_estatica.get("rx", 0)} {und_distancia}

            Distancia en Y desde el centroide hasta el punto crítico (ry) = {dic_diseno_estatica["ry_ecuacion"]}
                ry = {dic_diseno_estatica.get("ry", 0)} {und_distancia}

        Momento Polar de Inercia (J):

            Para la soldadura:
                J sold = {dic_diseno_estatica["j_sold_ecuacion"]}
                    J sold = {dic_diseno_estatica.get("j_sold", 0)} {und_distancia}^4

        Área de la soldadura:

            A sold = h * lt
                A sold = {dic_diseno_estatica.get("area_sold", 0)} {und_distancia}²

        Cálculo del momento torsor producido por la fuerza externa:

            T = F * b
                T = {dic_diseno_estatica.get("momento_torsor", 0)}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_diseno_estatica.get("tao_primario", 0)}

    Cálculo del esfuerzo cortante secundario en el eje X y en el eje Y:

        τ'' sold x = T * ry / J
            τ'' sold x = {dic_diseno_estatica.get("tao_secundario_x", 0)}

        τ'' sold y = T * rx / J
            τ'' sold y = {dic_diseno_estatica.get("tao_secundario_y", 0)}

    Cálculo de la componente en el eje X del esfuerzo cortante resultante en la soldadura:

        τ sold x = τ'' sold x
            τ sold x = {dic_diseno_estatica.get("tao_x", 0)}

    Cálculo de la componente en el eje Y del esfuerzo cortante resultante en la soldadura:

        τ sold y = τ' sold + τ'' sold y
            τ sold y = {dic_diseno_estatica.get("tao_y", 0)}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τx)^2 + (τy)^2)
            τ sold = {dic_diseno_estatica.get("tao_sold", 0)}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = τ adm / τ sold
            Fperm sold = {dic_diseno_estatica.get("f_max_sold", 0)} {und_fuerza}  *


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica.get("tao_p", 0)}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Ssy / τ pieza1
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1", 0)} {und_fuerza}  **


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica["sigma_t"]}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Sy / σ pieza2
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

    """  # Porción con resultados de cálculos de diseño estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        informe += verificacion_pierna

        resumen = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados de análisis estático.

        resumen += verificacion_pierna_resumen

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): {dic_diseno_fatiga.get("pierna", 0)} {und_distancia}
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_fatiga.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_fatiga.get("radio", 0)} {und_distancia}

    Tipo de union:  {dic_diseno_fatiga.get("tipo_union", 0)}

    Cargas Aplicadas:

        Tipo: Cíclica
        Relación de carga (Fmax/Fmin) = {dic_diseno_fatiga.get("relacion_cargas", 0)}
        Brazo (b) = {dic_diseno_fatiga.get("b", 0)} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e): {dic_diseno_fatiga.get("espesor_menor_piezas", 0)} {und_distancia}
    """  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
**************
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la fuerza mínima aplicada, según la relación de fuerzas Fmax/Fmin **

    Cálculos de parámetros geométricos:

        Garganta (t) = 0.707 * h
                t = {dic_diseno_fatiga.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_diseno_fatiga["lt_ecuacion"]}
            lt = {dic_diseno_fatiga.get("longitud_total", 0)} {und_distancia}

        Distancia en X desde el centroide hasta el punto crítico (rx) = {dic_diseno_fatiga["rx_ecuacion"]}
            rx = {dic_diseno_fatiga.get("rx", 0)} {und_distancia}

        Distancia en Y desde el centroide hasta el punto crítico (ry) = {dic_diseno_fatiga["ry_ecuacion"]}
            ry = {dic_diseno_fatiga.get("ry", 0)} {und_distancia}

        Momento Polar de Inercia (J):

            Para la soldadura

                J sold = {dic_diseno_fatiga["j_sold_ecuacion"]}
                    J sold = {dic_diseno_fatiga.get("j_sold", 0)} {und_distancia}^4

        Área de la soldadura:

            A sold = h * lt
                A sold = {dic_diseno_fatiga.get("area_sold", 0)} {und_distancia}²

    Cálculo de carga alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)}

    Cálculo de momento torsor alternante y medio:

        Momento torsor alternante (Ta) = Fa * b
            Ta = {dic_diseno_fatiga.get("momento_torsor_alt", 0)}

        Momento torsor medio (Tm) = Fm * b
            Tm = {dic_diseno_fatiga.get("momento_torsor_med", 0)}

    Factor de concentración de esfuerzo reducido

        Para soldadura de filete de unión: {dic_diseno_fatiga.get("tipo_union", "")} sometida a carga de torsión, el factor de concentración de esfuerzo reducido es:

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo de esfuerzo cortante primario alternante y medio del material de aporte:

        τa' = Kfs * 1.414 * Fa / Asold
            τa' = {dic_diseno_fatiga.get("tao_primario_alt", 0)}

        τm' = 1.414 * Fm / Asold
            τm' = {dic_diseno_fatiga.get("tao_primario_med", 0)}

    Cálculo de la componente en el eje X y Y del esfuerzo cortante secundario alternante:

        τa'' x = Kfs * Ta * ry / J
            τa'' x = {dic_diseno_fatiga.get("tao_secundario_alt_x", 0)}

        τa'' y = Kfs * Tm * rx / J
            τa'' y = {dic_diseno_fatiga.get("tao_secundario_alt_y", 0)}

    Cálculo de la componente en el eje X y Y del esfuerzo cortante secundario medio:

        τm'' x = Tm * ry / J
            τm'' x = {dic_diseno_fatiga.get("tao_secundario_med_x", 0)}

        τm'' y = Tm * rx / J
            τm'' y = {dic_diseno_fatiga.get("tao_secundario_med_y", 0)}

    Cálculo de componentes X y Y del esfuerzo cortante alternante:

        τa x = τa'' x
            τa x = {dic_diseno_fatiga.get("tao_alt_x", 0)}

        τa y = τa' + τa'' y
            τa y = {dic_diseno_fatiga.get("tao_alt_y", 0)}

    Cálculo de componentes X y Y del esfuerzo cortante medio:

        τm x = τm'' x
            τm x = {dic_diseno_fatiga.get("tao_med_x", 0)}

        τm y = τm' + τm'' y
            τm y = {dic_diseno_fatiga.get("tao_med_y", 0)}

    Cálculo del esfuerzo cortante resultante alternante y medio en la soldadura:

        τa = sqrt((τa x)^2 + (τa y)^2)
            τa = {dic_diseno_fatiga.get("tao_alt_sold", 0)}

        τm = sqrt((τm x)^2 + (τm y)^2)
            τm = {dic_diseno_fatiga.get("tao_med_sold", 0)}

    Cálculo de la resistencia a la fatiga al cortante del material de aporte:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante del material de aporte

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la soldadura utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            F sold = {dic_diseno_fatiga.get("f_sold", 0)} {und_fuerza} *


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Cálculo de esfuerzo cortante alternante y medio de la pieza 1:

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_p_alt", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_p_med", 0)}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante de la pieza 1

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 1 utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            F pieza1 = {dic_diseno_fatiga.get("f_pieza1", 0)} {und_fuerza} **


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Fa / Asold
            σa = {dic_diseno_fatiga.get("sigma_t_alt", 0)}

        σm = Fm / Asold
            σm = {dic_diseno_fatiga.get("sigma_t_med", 0)}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia a última a la tensión:

        Sut = {dic_diseno_fatiga["sut_pieza2"]} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 2 utilizando la ecuación de Gerber:

        (FD * σa)/Se + ((FD * σm)/Sut)^2 = 1
            F pieza2 = {dic_diseno_fatiga.get("f_pieza2", 0)} {und_fuerza} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se selecciona la menor de las fuerzas calculadas (*, **, ***) y se multiplica por la relación de carga para determinar la fuerza máxima permisible de la junta.

Fperm = Relación * Fmin  = {dic_diseno_fatiga.get("relacion_cargas")} * {dic_diseno_fatiga.get("f_min")} {und_fuerza}

Por lo que, {dic_diseno_fatiga.get("conclusion_fperm")}.


Diseño por fatiga de la carga permisible completado.


    """  # Resultados de diseño para carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {"{:.2f}".format(dic_diseno_fatiga.get("f_sold") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza1") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza2") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados del diseño por fatiga

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            informe += verificacion_pierna

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += verificacion_pierna_resumen

        else:

            informe += verificacion_estatica

            informe += f"\nAl presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno_estatica = f"""

Cálculos realizados

    Cálculo del momento torsor producido por la fuerza externa:

        T = F * b
            T = {dic_diseno_estatica.get("momento_torsor", 0)}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_diseno_estatica.get("tao_primario", 0)}

    Cálculo del esfuerzo cortante secundario en el eje X y en el eje Y:

        τ'' sold x = T * ry / J
            τ'' sold x = {dic_diseno_estatica.get("tao_secundario_x", 0)}

        τ'' sold y = T * rx / J
            τ'' sold y = {dic_diseno_estatica.get("tao_secundario_y", 0)}

    Cálculo de la componente en el eje X del esfuerzo cortante resultante en la soldadura:

        τ sold x = τ'' sold x
            τ sold x = {dic_diseno_estatica.get("tao_x", 0)}

    Cálculo de la componente en el eje Y del esfuerzo cortante resultante en la soldadura:

        τ sold y = τ' sold + τ'' sold y
            τ sold y = {dic_diseno_estatica.get("tao_y", 0)}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τx)^2 + (τy)^2)
            τ sold = {dic_diseno_estatica.get("tao_sold", 0)}

    Cálculo de la carga máxima permisible de la soldadura:

        FS sold = τ adm / τ sold
            Fperm sold = {dic_diseno_estatica.get("f_max_sold", 0)} {und_fuerza}  *


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica.get("tao_p", 0)}

    Cálculo de la carga máxima permisible de la pieza 1:

        FS pieza1 = Ssy / τ pieza1
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1", 0)} {und_fuerza}  **


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica["sigma_t"]}

    Cálculo de la carga máxima permisible de la pieza 2:

        FS pieza2 = Sy / σ pieza2
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

"""  # Porción con resultados de cálculos de diseño estático.

            informe += resultados_rediseno_estatica

            informe += verificacion_pierna

            resumen_estatica = f"""
            <body>

            <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
            <hr>

            <p><strong>Carga permisible en la soldadura:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

            <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

            </body>
            """  # Resumen de resultados del rediseño por estática.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

            resumen += verificacion_pierna_resumen

    return informe, resumen


def informe_diseno_carga_filete_cc(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                                   sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados del diseño de la carga permisible de soldadura de filete
    sometida a carga combinada debido a una fuerza excéntrica"""

    informe = f"""
{"*" * 5} Informe de Diseño de la Carga Permisible para Soldadura de Filete Sometida a Carga Combinada debido a una Fuerza Externa {tipo_carga.capitalize()} Excéntrica al Centroide de la Soldadura {"*" * 5}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
"""  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados del diseño de la carga permisible para soldadura de filete sometida a carga combinada debido a una fuerza externa {tipo_carga} excéntrica al centroide de la soldadura. El objetivo es determinar la magnitud de la carga máxima permisible en la junta soldada, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI. Así como también verificar que el tamaño del cordón de soldadura esté dentro de especificación según la norma AWS D1.1.\n\n""" # Introducción

    resumen = ""

    if dic_diseno_estatica is None:

        verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_diseno_fatiga.get("verificacion_pierna", 0)}

        """

        verificacion_pierna_resumen = f"""
            <br>
            <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
            <p>{dic_diseno_fatiga.get("verificacion_pierna", 0)}</p>

            """  # Porción con verificación de pierna para el resumen

    else:

        verificacion_pierna = f"""\n
Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:

{dic_diseno_estatica.get("verificacion_pierna", 0)}

    """

        verificacion_pierna_resumen = f"""
            <br>
            <p style="margin-left: 20px;"><strong>Se verifica si el tamaño de la pierna cumple con las especificaciones de la norma AWS D1.1:</strong></p>
            <p>{dic_diseno_estatica.get("verificacion_pierna", 0)}</p>

            """  # Porción con verificación de pierna para el resumen

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): {dic_diseno_estatica.get("pierna", 0)} {und_distancia}
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_estatica.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_estatica.get("radio", 0)} {und_distancia}

    Tipo de union:  Unión T

    Cargas Aplicadas:

        Tipo: Estática
        Fuerza: ** A determinar **
        Brazo longitudinal (bl) = {dic_diseno_estatica.get("bl", 0)} {und_distancia}
        Brazo transversal (bt) = {dic_diseno_estatica.get("bt", 0)} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e) = {dic_diseno_estatica.get("espesor_menor_piezas", 0)} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""

Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Cálculos de parámetros geométricos:

        Garganta (t) = 0.707 * h
            t = {dic_diseno_estatica.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

        Distancia en X desde el centroide hasta el punto crítico (rx) = {dic_diseno_estatica["rx_ecuacion"]}
            rx = {dic_diseno_estatica.get("rx", 0)} {und_distancia}

        Distancia en Y desde el centroide hasta el punto crítico (ry) = {dic_diseno_estatica["ry_ecuacion"]}
            ry = {dic_diseno_estatica.get("ry", 0)} {und_distancia}

        Distancia del eje nuetro hasta la soldadura (c) = {dic_diseno_estatica["c_ecuacion"]}
            c = {dic_diseno_estatica["c"]} {und_distancia}

    Momento de Inercia (I):

        Para la soldadura:
            I sold = {dic_diseno_estatica["i_sold_ecuacion"]}
                I sold = {dic_diseno_estatica["i_sold"]} {und_distancia}^4

        Para las piezas:
            I piezas = {dic_diseno_estatica["i_pieza_ecuacion"]}
                I piezas = {dic_diseno_estatica["i_pieza"]} {und_distancia}^4

    Momento Polar de Inercia (J):

        Para la soldadura:
            J sold = {dic_diseno_estatica["j_sold_ecuacion"]}
                J sold = {dic_diseno_estatica.get("j_sold", 0)} {und_distancia}^4

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica.get("area_sold", 0)} {und_distancia}²

    Cálculo del momento flector producido por la fuerza externa:

        M = F * bl
            M = {dic_diseno_estatica.get("momento_flector", 0)}

    Cálculo del momento torsor producido por la fuerza externa:

        T = F * bt
            T = {dic_diseno_estatica.get("momento_torsor", 0)}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_diseno_estatica.get("tao_primario", 0)}

    Cálculo del esfuerzo cortante secundario:

        τ'' sold = M * c / I
            τ'' sold = {dic_diseno_estatica.get("tao_secundario", 0)}

    Cálculo de componentes del esfuerzo cortante terciario:

        En el eje X:
        τ''' sold x = T * ry / J
            τ''' sold x = {dic_diseno_estatica.get("tao_terciario_x", 0)}

        En el eje Y:
        τ''' sold y = T * rx / J
            τ''' sold y = {dic_diseno_estatica.get("tao_terciario_y", 0)}

    Cálculo de la componente en el eje X, Y y Z del esfuerzo cortante resultante en la soldadura:

        τ sold x = τ''' x
            τ sold x = {dic_diseno_estatica.get("tao_x", 0)}

        τ sold y = τ' + τ''' y
            τ sold y = {dic_diseno_estatica.get("tao_y", 0)}

        τ sold z = τ''
            τ sold z = {dic_diseno_estatica.get("tao_z", 0)}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τx)^2 + (τy)^2 + (τz)^2)
            τ sold = {dic_diseno_estatica.get("tao_sold", 0)}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = τ adm / τ sold
            Fperm sold = {dic_diseno_estatica.get("f_max_sold", 0)} {und_fuerza}  *


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza1 = M * c / I
            σ pieza1 = {dic_diseno_estatica.get("sigma_p", 0)}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica.get("tao_p", 0)}

    Cálculo del esfuerzo Von Misses en la pieza 1:

        σ' pieza1 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza1 = {dic_diseno_estatica.get("sigma_von_misses_1", 0)}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Sy / σ'
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1", 0)} {und_fuerza}  **


Para la pieza 2: (Pieza Transversal a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica.get("sigma_t", 0)}

    Cálculo del esfuerzo cortante:

        τ pieza2 = M * c / I
            τ pieza2 = {dic_diseno_estatica.get("tao_t", 0)}

    Cálculo del esfuerzo Von Misses en la pieza 1:

        σ' pieza2 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza2 = {dic_diseno_estatica.get("sigma_von_misses_2", 0)}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Sy / σ'
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

    """  # Porción con resultados de cálculos de diseño estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        informe += verificacion_pierna

        resumen = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados de análisis estático.

        resumen += verificacion_pierna_resumen

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): {dic_diseno_fatiga.get("pierna", 0)} {und_distancia}
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_fatiga.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_fatiga.get("radio", 0)} {und_distancia}

    Tipo de union:  Unión T

    Cargas Aplicadas:

        Tipo: Cíclica
        Relación de carga (Fmax/Fmin) = {dic_diseno_fatiga.get("relacion_cargas", 0)}
        Brazo longitudinal (bl) = {dic_diseno_fatiga.get("bl", 0)} {und_distancia}
        Brazo transversal (bt) = {dic_diseno_fatiga.get("bt", 0)} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e): {dic_diseno_fatiga.get("espesor_menor_piezas", 0)} {und_distancia}
    """  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
**************
Se procede a diseñar por carga de fatiga la junta soldada.


Cálculos realizados

** Nota: Los cálculos se realizaron en función de la fuerza mínima aplicada, según la relación de fuerzas Fmax/Fmin **

    Cálculos de parámetros geométricos:

        Garganta (t) = 0.707 * h
            t = {dic_diseno_fatiga.get("garganta", 0)} {und_distancia}

        Longitud total (lt) = {dic_diseno_fatiga["lt_ecuacion"]}
            lt = {dic_diseno_fatiga.get("longitud_total", 0)} {und_distancia}

        Distancia en X desde el centroide hasta el punto crítico (rx) = {dic_diseno_fatiga["rx_ecuacion"]}
            rx = {dic_diseno_fatiga.get("rx", 0)} {und_distancia}

        Distancia en Y desde el centroide hasta el punto crítico (ry) = {dic_diseno_fatiga["ry_ecuacion"]}
            ry = {dic_diseno_fatiga.get("ry", 0)} {und_distancia}

        Distancia del eje nuetro hasta la soldadura (c) = {dic_diseno_fatiga["c_ecuacion"]}
            c = {dic_diseno_fatiga["c"]} {und_distancia}

    Momento de Inercia (I):

        Para la soldadura:
            I sold = {dic_diseno_fatiga["i_sold_ecuacion"]}
                I sold = {dic_diseno_fatiga["i_sold"]} {und_distancia}^4

        Para las piezas:
            I piezas = {dic_diseno_fatiga["i_pieza_ecuacion"]}
                I piezas = {dic_diseno_fatiga["i_pieza"]} {und_distancia}^4

    Momento Polar de Inercia (J):

        Para la soldadura:
            J sold = {dic_diseno_fatiga["j_sold_ecuacion"]}
                J sold = {dic_diseno_fatiga.get("j_sold", 0)} {und_distancia}^4

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_fatiga.get("area_sold", 0)} {und_distancia}²

    Cálculo de carga alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)}

    Cálculo de momento flector alternante y medio:

        Momento flector alternante (Ma) = Fa * bl
            Ma = {dic_diseno_fatiga.get("momento_flector_alt", 0)}

        Momento flector medio (Mm) = Fm * bl
            Mm = {dic_diseno_fatiga.get("momento_flector_med", 0)}

    Cálculo de momento torsor alternante y medio:

        Momento torsor alternante (Ta) = Fm * bt
            Ta = {dic_diseno_fatiga.get("momento_torsor_alt", 0)}

        Momento torsor medio (Tm) = Fm * bt
            Tm = {dic_diseno_fatiga.get("momento_torsor_med", 0)}

    Factor de concentración de esfuerzo reducido

        Para soldadura de filete de unión T sometida a carga combinada, el factor de concentración de esfuerzo reducido es:

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo de esfuerzo cortante primario alternante y medio:

        τa' = Kfs * 1.414 * Fa / Asold
            τa' = {dic_diseno_fatiga.get("tao_primario_alt", 0)}

        τm' = 1.414 * Fm / Asold
            τm' = {dic_diseno_fatiga.get("tao_primario_med", 0)}

    Cálculo del esfuerzo cortante secundario alternante y medio:

        τa'' = Kfs * Ma * c / I
            τa'' = {dic_diseno_fatiga.get("tao_secundario_alt", 0)}

        τm'' = Mm * c / I
            τm'' = {dic_diseno_fatiga.get("tao_secundario_med", 0)}

    Cálculo de las componentes X y Y del esfuerzo cortante terciario alternante:

        τa''' x = = Kfs * Ta * ry / J
            τa''' x = {dic_diseno_fatiga.get("tao_terciario_alt_x", 0)}

        τa''' y = Kfs * Ta * rx / J
            τa''' y = {dic_diseno_fatiga.get("tao_terciario_alt_y", 0)}

    Cálculo de las componentes X y Y del esfuerzo cortante terciario medio:

        τm''' x = Tm * ry / J
            τm''' x = {dic_diseno_fatiga.get("tao_terciario_med_x", 0)}

        τm''' y = Tm * rx / J
            τm''' y = {dic_diseno_fatiga.get("tao_terciario_med_y", 0)}

    Cálculo de las componentes X, Y y Z del esfuerzo cortante terciario alternante:

        τa x = τa''' x
            τa x = {dic_diseno_fatiga.get("tao_alt_x", 0)}

        τa y = τa' + τa''' y
            τa y = {dic_diseno_fatiga.get("tao_alt_y", 0)}

        τa z = τa''
            τa z = {dic_diseno_fatiga.get("tao_alt_z", 0)}

    Cálculo de las componentes X, Y y Z del esfuerzo cortante terciario medio:

        τm x = τm''' x
            τm x = {dic_diseno_fatiga.get("tao_med_x", 0)}

        τm y = τm' + τm''' y
            τm y = {dic_diseno_fatiga.get("tao_med_y", 0)}

        τm z = τm''
            τm z = {dic_diseno_fatiga.get("tao_med_z", 0)}

    Cálculo del esfuerzo cortante resultante alternante y medio del material de aporte:

        τa = sqrt((τa x)^2 + (τa y)^2 + (τa z)^2)
            τa = {dic_diseno_fatiga.get("tao_alt_sold", 0)}

        τm = sqrt((τm x)^2 + (τm y)^2 + (τm z)^2)
            τm = {dic_diseno_fatiga.get("tao_med_sold", 0)}

    Cálculo de la resistencia a la fatiga al cortante del material de aporte:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante del material de aporte

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la soldadura utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            F sold = {dic_diseno_fatiga.get("f_sold", 0)} {und_fuerza} *


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Ma * c / I
            σa = {dic_diseno_fatiga.get("sigma_p_alt", 0)}

        σm = Mm * c / I
            σm = {dic_diseno_fatiga.get("sigma_p_med", 0)}

    Cálculo de esfuerzo cortante alternante y medio::

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_p_alt", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_p_med", 0)}

    Cálculo de esfuerzo de Von Misses alternante y medio en la pieza 1:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_diseno_fatiga.get("sigma_p_von_misses_alt", 0)}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ'm = {dic_diseno_fatiga.get("sigma_p_von_misses_med", 0)}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia última a la tensión de la pieza 1:

        Sut = {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 1 utilizando ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            F pieza1 = {dic_diseno_fatiga.get("f_pieza1", 0)} {und_fuerza} **


Para la pieza 2: (Pieza transversal a la carga aplicada)

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Fa / Asold
            σa = {dic_diseno_fatiga.get("sigma_t_alt", 0)}

        σm = Fm / Asold
            σm = {dic_diseno_fatiga.get("sigma_t_med", 0)}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Ma * c / I
            τa = {dic_diseno_fatiga.get("tao_t_alt", 0)}

        τm = Mm * c / I
            τm = {dic_diseno_fatiga.get("tao_t_med", 0)}

    Cálculo de esfuerzo de Von Misses alternante y medio en la pieza 2:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_diseno_fatiga.get("sigma_t_von_misses_alt", 0)}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ'm = {dic_diseno_fatiga.get("sigma_t_von_misses_med", 0)}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia a última a la tensión:

        Sut = {dic_diseno_fatiga["sut_pieza2"]} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 2 utilizando la ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            F pieza2 = {dic_diseno_fatiga.get("f_pieza2", 0)} {und_fuerza} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se selecciona la menor de las fuerzas calculadas (*, **, ***) y se multiplica por la relación de carga para determinar la fuerza máxima permisible de la junta.

Fperm = Relación * Fmin  = {dic_diseno_fatiga.get("relacion_cargas")} * {dic_diseno_fatiga.get("f_min")} {und_fuerza}

Por lo que, {dic_diseno_fatiga.get("conclusion_fperm")}.


Diseño por fatiga de la carga permisible completado.


    """  # Resultados de diseño para carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {"{:.2f}".format(dic_diseno_fatiga.get("f_sold") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza1") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza2") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados del diseño por fatiga

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            informe += verificacion_pierna

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += verificacion_pierna_resumen

        else:

            informe += verificacion_estatica

            informe += f"\nAl presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno_estatica = f"""

Cálculos realizados

    Cálculo del momento torsor producido por la fuerza externa:

        T = F * bt
            T = {dic_diseno_estatica.get("momento_torsor", 0)}

    Cálculo del momento flector producido por la fuerza externa:

        M = F * bl
            M = {dic_diseno_estatica.get("momento_flector", 0)}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_diseno_estatica.get("tao_primario", 0)}

    Cálculo del esfuerzo cortante secundario:

        τ'' sold = M * c / I
            τ'' sold = {dic_diseno_estatica.get("tao_secundario", 0)}

    Cálculo de componentes del esfuerzo cortante terciario:

        En el eje X:
        τ''' sold x = T * ry / J
            τ''' sold x = {dic_diseno_estatica.get("tao_terciario_x", 0)}

        En el eje Y:
        τ''' sold y = T * rx / J
            τ''' sold y = {dic_diseno_estatica.get("tao_terciario_y", 0)}

    Cálculo de la componente en el eje X, Y y Z del esfuerzo cortante resultante en la soldadura:

        τ sold x = τ''' x
            τ sold x = {dic_diseno_estatica.get("tao_x", 0)}

        τ sold y = τ' + τ''' y
            τ sold y = {dic_diseno_estatica.get("tao_y", 0)}

        τ sold z = τ''
            τ sold z = {dic_diseno_estatica.get("tao_z", 0)}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τx)^2 + (τy)^2 + (τz)^2)
            τ sold = {dic_diseno_estatica.get("tao_sold", 0)}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = τ adm / τ sold
            Fperm sold = {dic_diseno_estatica.get("f_max_sold", 0)} {und_fuerza}  *


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza1 = M * c / I
            σ pieza1 = {dic_diseno_estatica.get("sigma_p", 0)}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica.get("tao_p", 0)}

    Cálculo del esfuerzo Von Misses en la pieza 1:

        σ' pieza1 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza1 = {dic_diseno_estatica.get("sigma_von_misses_1", 0)}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Sy / σ'
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1", 0)} {und_fuerza}  **


Para la pieza 2: (Pieza Transversal a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica.get("sigma_t", 0)}

    Cálculo del esfuerzo cortante:

        τ pieza2 = M * c / I
            τ pieza2 = {dic_diseno_estatica.get("tao_t", 0)}

    Cálculo del esfuerzo Von Misses en la pieza 1:

        σ' pieza2 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza2 = {dic_diseno_estatica.get("sigma_von_misses_2", 0)}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Sy / σ'
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

    """  # Porción con resultados de cálculos de diseño estático.

            informe += resultados_rediseno_estatica

            informe += verificacion_pierna

            resumen_estatica = f"""
            <body>

            <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
            <hr>

            <p><strong>Carga permisible en la soldadura:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

            <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

            </body>
            """  # Resumen de resultados del rediseño por estática.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

            resumen += verificacion_pierna_resumen

    return informe, resumen


# TAMAÑO PIERNA H

# Informe para tamaño pierma: carga paralela
def informe_diseno_h_filete_cp(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                               sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):

    """Esta función le dará forma al informe y resumen de resultados del cálculo para el diseño de la pierna del
    cordón de soldadura sometida a carga paralela"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Pierna del Cordón para Soldadura de Filete Sometida a Carga Paralela {tipo_carga.capitalize()} {"*" * 5}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados de los cálculos para el diseño del tamaño de la pierna del cordón para soldadura de filete sometida a carga paralela {tipo_carga}. El objetivo del diseño es determinar el tamaño mínimo necesario de la pierna del cordón de soldadura, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\n""" # Introducción

    resumen = ""

    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): ** A determinar **
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_estatica.get("ancho", 0)} {und_distancia}

    Tipo de union:  Intermedia

    Carga Aplicada:

        Tipo: Estática
        Fuerza: {dic_diseno_estatica.get("Fmax", 0)} {und_fuerza}

    Espesor menor entre las piezas:

        Espesor (e) = {dic_diseno_estatica.get("espesor_menor_piezas", 0)} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica.get("area_sold", 0)}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la soldadura:

        τ sold = 1.414 * F / Asold
            τ sold = {dic_diseno_estatica.get("tao_sold", 0)}

    Cálculo de la pierna mínima necesaria para la soldadura:

        F sold = τ adm / τ sold
            h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia} *


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 1:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica.get("tao_pieza1", 0)}

    Cálculo de la pierna mínima necesaria para la pieza 1:

        FD pieza = Ssy / τ pieza1
            h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}  **


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 2:

        τ pieza2 = F / Asold
            τ pieza2 = {dic_diseno_estatica.get("tao_pieza2", 0)}

    Cálculo de la pierna mínima necesaria para la pieza 2:

        FD pieza = Ssy / τ pieza2
            h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de pierna calculados (*, **, ***), el mayor de ellos.

{dic_diseno_estatica.get("verificacion_h_max", 0)}

{"~"*5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~"*5}

{dic_diseno_estatica.get("verificacion_h_min", 0)}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen += f"""
<body>

<h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
<hr>

<p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
<p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia}</p>

<p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
<p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}</p>

<p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
<p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}</p>

<div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_estatica.get("verificacion_h_max"))}</strong></div>

<p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
<p>{dic_diseno_estatica.get("verificacion_h_min")}</p>

</body>
    """  # Resumen de resultados del diseño por estática.

    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): ** A determinar **
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_fatiga.get("ancho", 0)} {und_distancia}

    Tipo de union:  Intermedia

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima (Fmax) = {dic_diseno_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima (Fmin) = {dic_diseno_fatiga.get("Fmin", 0)} {und_fuerza}

    Espesor menor entre las piezas:

        Espesor (e): {dic_diseno_fatiga.get("espesor_menor_piezas", 0)} {und_distancia}

"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la pierna del cordón de soldadura **

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_fatiga["lt_ecuacion"]}
            lt = {dic_diseno_fatiga.get("longitud_total", 0)} {und_distancia}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_fatiga.get("area_sold", 0)}

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)} {und_fuerza}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de filete de unión intermedia sometida a carga paralela, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo de esfuerzo cortante alternante y medio:

        τa = τa = Kfs * 1.414 * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_alt_sold", 0)}

        τm = 1.414 * Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_med_sold", 0)}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la soldadura utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            h sold = {dic_diseno_fatiga.get("h_sold", 0)} {und_distancia} *


Para la pieza 1:

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_alt_pieza1", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_med_pieza1", 0)}

    Cálculo de la resistencia a la fatiga al ortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la pieza 1 utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            h pieza1 = {dic_diseno_fatiga.get("h_pieza1", 0)} {und_distancia} **


Para la pieza 2:

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_alt_pieza2", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_med_pieza2", 0)}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza2", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza2", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la pieza 2 utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            h pieza2 = {dic_diseno_fatiga.get("h_pieza2", 0)} {und_distancia} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de pierna calculados (*, **, ***), el mayor de ellos.

{dic_diseno_fatiga.get("verificacion_h_max", 0)}

{"~"*5} Verificación del tamaño mínimo según la especificación de la norma AWS D1.1 {"~"*5}

{dic_diseno_fatiga.get("verificacion_h_min", 0)}

"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen += f"""
<body>

<h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
<hr>

<p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
<p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_fatiga.get("h_sold", 0)} {und_distancia}</p>

<p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
<p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_fatiga.get("h_pieza1", 0)} {und_distancia}</p>

<p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
<p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_fatiga.get("h_pieza2", 0)} {und_distancia}</p>

<div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_fatiga.get("verificacion_h_max"))}</strong></div>

<p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
<p>{dic_diseno_fatiga.get("verificacion_h_min", 0)}</p>

</body>
        """  # Resumen de resultados de diseño de fatiga

        if dic_comprobacion is not None:

            verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

            verificacion_estatica_resumen = f"""
            <br><body>

            <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

            <p><strong>Factor de seguridad de la soldadura:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

            <p><strong>Factor de seguridad de la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

            <p><strong>Factor de seguridad de la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

            </body>
            """

            informe += verificacion_estatica

            resumen += verificacion_estatica_resumen

            if dic_diseno_estatica is not None:

                resultados_estatica = f"""
Se procede a rediseñar por carga estática la junta soldada.

Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica.get("area_sold", 0)}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la soldadura:

        τ sold = 1.414 * F / Asold
            τ sold = {dic_diseno_estatica.get("tao_sold", 0)}

    Cálculo de la pierna mínima necesaria para la soldadura:

        FD sold = τ adm / τ sold
            h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia} *


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 1:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica.get("tao_pieza1", 0)}

    Cálculo de la pierna mínima necesaria para la pieza 1:

        FD pieza = Ssy / τ pieza1
            h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}  **


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 2:

        τ pieza2 = F / Asold
            τ pieza2 = {dic_diseno_estatica.get("tao_pieza2", 0)}

    Cálculo de la pierna mínima necesaria para la pieza 2:

        FD pieza = Ssy / τ pieza2
            h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de piernas calculados (*, **, ***), el mayor de ellos.

{dic_diseno_estatica.get("verificacion_h_max", 0)}

{"~" * 5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~" * 5}

{dic_diseno_estatica.get("verificacion_h_min", 0)}

"""  # Porción con resultados de cálculos del rediseño.

                informe += resultados_estatica

                resumen += f"""
<body>

<h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
<hr>

<p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
<p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia}</p>

<p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
<p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}</p>

<p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
<p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}</p>

<div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_estatica.get("verificacion_h_max"))}</strong></div>

<p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
<p>{dic_diseno_estatica.get("verificacion_h_min")}</p>

</body>
"""

    return informe, resumen


# Informe para tamaño pierna: carga transversal
def informe_diseno_h_filete_ct(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                               sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):

    """Esta función le dará forma al informe y resumen de resultados del cálculo para el diseño de la pierna del
    cordón de soldadura sometida a carga transversal"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Pierna del Cordón para Soldadura de Filete Sometida a Carga Transversal {tipo_carga.capitalize()} {"*" * 5}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados de los cálculos para el diseño del tamaño de la pierna del cordón para soldadura de filete sometida a carga transversal {tipo_carga}. El objetivo del diseño es determinar el tamaño mínimo necesario de la pierna del cordón de soldadura, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\n""" # Introducción

    resumen = ""

    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): ** A determinar **
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_estatica.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_estatica.get("radio", 0)} {und_distancia}

    Tipo de union:  {dic_diseno_estatica.get("tipo_union")}

    Carga Aplicada:

        Tipo: Estática
        Fuerza: {dic_diseno_estatica.get("Fmax", 0)} {und_fuerza}

    Espesor menor entre las piezas:

        Espesor (e) = {dic_diseno_estatica.get("espesor_menor_piezas", 0)} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica.get("area_sold", 0)}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica["tao_adm_sold"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la soldadura:

        τ sold = 1.414 * F / Asold
            τ sold = {dic_diseno_estatica["tao_sold"]}

    Cálculo de la pierna mínima necesaria para la soldadura:

        FD sold = τ adm / τ sold
            h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia} *


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica["ssy_pieza1"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 1:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica["tao_pieza1"]}

    Cálculo de la pierna mínima necesaria para la pieza 1:

        FD pieza = Ssy / τ pieza1
            h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}  **


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del esfuerzo normal en la pieza 2:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica.get("sigma_pieza2", 0)}

    Cálculo de la pierna mínima necesaria para la pieza 2:

        FD pieza = Sy / σ pieza2
            h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de pierna calculados (*, **, ***), el mayor de ellos.

{dic_diseno_estatica.get("verificacion_h_max")}

{"~"*5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~"*5}

{dic_diseno_estatica.get("verificacion_h_min")}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen += f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}</p>

        <div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_estatica.get("verificacion_h_max"))}</strong></div>

        <p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
        <p>{dic_diseno_estatica.get("verificacion_h_min")}</p>

        </body>
            """  # Resumen de resultados del diseño por estática.

    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): ** A determinar **
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_fatiga.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_fatiga.get("radio", 0)} {und_distancia}

    Tipo de union:  {dic_diseno_fatiga.get("tipo_union")}

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima (Fmax) = {dic_diseno_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima (Fmin) = {dic_diseno_fatiga.get("Fmin", 0)} {und_fuerza}

    Espesor menor entre las piezas:

        Espesor (e): {dic_diseno_fatiga.get("espesor_menor_piezas", 0)} {und_distancia}

"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la pierna del cordón de soldadura **

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_fatiga["lt_ecuacion"]}
            lt = {dic_diseno_fatiga.get("longitud_total", 0)} {und_distancia}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_fatiga.get("area_sold", 0)}

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)} {und_fuerza}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de filete de unión: {dic_diseno_fatiga.get("tipo_union")}, sometida a carga transversal, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo de esfuerzo cortante alternante y medio:

        τa = τa = Kfs * 1.414 * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_alt_sold", 0)}

        τm = 1.414 * Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_med_sold", 0)}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la soldadura utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            h sold = {dic_diseno_fatiga.get("h_sold", 0)} {und_distancia} *


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_p_alt", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_p_med", 0)}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la pieza 1 utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            h pieza1 = {dic_diseno_fatiga.get("h_pieza1", 0)} {und_distancia} **


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Cálculo del esfuerzo normal alternante y medio:

        σa = Kfs * Fa / Asold
            σa = {dic_diseno_fatiga.get("sigma_t_alt", 0)}

        σm = Fm / Asold
            σm = {dic_diseno_fatiga.get("sigma_t_med", 0)}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la pieza 2 utilizando ecuación de Gerber:

        (FD * σa)/Se + ((FD * σm)/Sut)^2 = 1
            h pieza2 = {dic_diseno_fatiga.get("h_pieza2", 0)} {und_distancia} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de pierna calculados (*, **, ***), el mayor de ellos.

{dic_diseno_fatiga.get("verificacion_h_max", 0)}

{"~"*5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~"*5}

{dic_diseno_fatiga.get("verificacion_h_min", 0)}

"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen += f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_fatiga.get("h_sold", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_fatiga.get("h_pieza1", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_fatiga.get("h_pieza2", 0)} {und_distancia}</p>

        <div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_fatiga.get("verificacion_h_max"))}</strong></div>

        <p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
        <p>{dic_diseno_fatiga.get("verificacion_h_min", 0)}</p>

        </body>
                """  # Resumen de resultados de diseño de fatiga

        if dic_comprobacion is not None:

            verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

            verificacion_estatica_resumen = f"""
            <br><body>

            <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

            <p><strong>Factor de seguridad de la soldadura:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

            <p><strong>Factor de seguridad de la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

            <p><strong>Factor de seguridad de la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

            </body>
            """

            informe += verificacion_estatica

            resumen += verificacion_estatica_resumen

            if dic_diseno_estatica is not None:

                resultados_estatica = f"""
Se procede a rediseñar por carga estática la junta soldada.

Cálculos realizados

Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica.get("area_sold", 0)}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica["tao_adm_sold"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la soldadura:

        τ sold = 1.414 * F / Asold
            τ sold = {dic_diseno_estatica["tao_sold"]}

    Cálculo de la pierna mínima necesaria para la soldadura:

        FS sold = τ adm / τ sold
            h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia} *


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica["ssy_pieza1"]} {und_esfuerzo}

    Cálculo del esfuerzo cortante en la pieza 1:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica["tao_pieza1"]}

    Cálculo de la pierna mínima necesaria para la pieza 1:

        FS pieza1 = Ssy / τ pieza1
            h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}  **


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del esfuerzo normal en la pieza 2:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica.get("sigma_pieza2", 0)}

    Cálculo de la pierna mínima necesaria para la pieza 2:

        FS pieza2 = Sy / σ pieza2
            h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de piernas calculados (*, **, ***), el mayor de ellos.

{dic_diseno_estatica.get("verificacion_h_max", 0)}

{"~" * 5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~" * 5}

{dic_diseno_estatica.get("verificacion_h_min", 0)}

"""  # Porción con resultados de cálculos del rediseño.

                informe += resultados_estatica

                resumen += f"""
                <body>

                <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
                <hr>

                <p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
                <p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia}</p>

                <p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
                <p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}</p>

                <p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
                <p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}</p>

                <div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_estatica.get("verificacion_h_max"))}</strong></div>

                <p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
                <p>{dic_diseno_estatica.get("verificacion_h_min")}</p>

                </body>
                """

    return informe, resumen


# Informe para tamaño pierna: carga de flexión
def informe_diseno_h_filete_cf(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                               sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):

    """Esta función le dará forma al informe y resumen de resultados del cálculo para el diseño de la pierna del
    cordón de soldadura sometida a carga de flexión debido a una fuerza excéntrica"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Pierna del Cordón para Soldadura de Filete Sometida a Carga de Flexión debido a una Fuerza Externa {tipo_carga.capitalize()} {"*" * 5}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados de los cálculos para el diseño del tamaño de la pierna del cordón para soldadura de filete sometida a carga de flexión debido a una fuerza externa {tipo_carga}. El objetivo del diseño es determinar el tamaño mínimo necesario de la pierna del cordón de soldadura, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\n""" # Introducción

    resumen = ""

    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): ** A determinar **
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_estatica.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_estatica.get("radio", 0)} {und_distancia}

    Tipo de union:  {dic_diseno_estatica.get("tipo_union")}

    Carga Aplicada:

        Tipo: Estática
        Fuerza: {dic_diseno_estatica.get("Fmax", 0)} {und_fuerza}
        Brazo (b) = {dic_diseno_estatica.get("b", 0)} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e) = {dic_diseno_estatica.get("espesor_menor_piezas", 0)} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

        Distancia del eje nuetro hasta la soldadura (c) = {dic_diseno_estatica["c_ecuacion"]}
            c = {dic_diseno_estatica["c"]} {und_distancia}

    Momento de Inercia (I):

        Para la soldadura:
            I sold = {dic_diseno_estatica["i_sold_ecuacion"]}
                I sold = {dic_diseno_estatica["i_sold"]}

        Para las piezas:
            I piezas = {dic_diseno_estatica["i_pieza_ecuacion"]}
                I piezas = {dic_diseno_estatica["i_pieza"]}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica.get("area_sold", 0)}

    Cálculo del momento flector producido por la fuerza externa:

        M = F * b
            M = {dic_diseno_estatica["momento_flector"]} {und_fuerza}{und_distancia}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_diseno_estatica.get("tao_primario", 0)}

    Cálculo del esfuerzo cortante secundario:

        τ'' sold = M * c / I
            τ'' sold = {dic_diseno_estatica["tao_secundario"]}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τ')^2 + (τ'')^2)
            τ sold = {dic_diseno_estatica["tao_sold"]}

    Cálculo de la pierna mínima necesaria para la soldadura:

        FD sold = τ adm / τ sold
            h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia} *


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza1"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza1 = M * c / I
            σ pieza1 = {dic_diseno_estatica["sigma_p"]}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica["tao_p"]}

    Cálculo del esfuerzo Von Misses σ':

        σ' pieza1 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza1 = {dic_diseno_estatica["sigma_von_misses_1"]}

    Cálculo de la pierna mínima necesaria para la pieza 1:

        FD pieza = Sy / σ'
            h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}  **


Para la pieza 2: (Pieza transversal a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica["sigma_t"]}

    Cálculo del esfuerzo cortante:

        τ pieza2 = M * c / I
            τ pieza2 = {dic_diseno_estatica["tao_t"]}

    Cálculo del esfuerzo de Von Misses σ':

        σ' pieza2 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza2 = {dic_diseno_estatica["sigma_von_misses_2"]}

    Cálculo de la pierna mínima necesaria para la pieza 2:

        FD pieza = Sy / σ'
            h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de pierna calculados (*, **, ***), el mayor de ellos.

{dic_diseno_estatica.get("verificacion_h_max")}

{"~"*5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~"*5}

{dic_diseno_estatica.get("verificacion_h_min")}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen += f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}</p>

        <div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_estatica.get("verificacion_h_max"))}</strong></div>

        <p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
        <p>{dic_diseno_estatica.get("verificacion_h_min")}</p>

        </body>
            """  # Resumen de resultados del diseño por estática.

    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): ** A determinar **
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_fatiga.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_fatiga.get("radio", 0)} {und_distancia}

    Tipo de union:  {dic_diseno_fatiga.get("tipo_union")}

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima (Fmax) = {dic_diseno_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima (Fmin) = {dic_diseno_fatiga.get("Fmin", 0)} {und_fuerza}
        Brazo (b) = {dic_diseno_fatiga.get("b", 0)} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e): {dic_diseno_fatiga.get("espesor_menor_piezas", 0)} {und_distancia}

"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la pierna del cordón de soldadura **

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_fatiga["lt_ecuacion"]}
            lt = {dic_diseno_fatiga.get("longitud_total", 0)} {und_distancia}

        Distancia del eje neutro hasta la soldadura (c) = {dic_diseno_fatiga["c_ecuacion"]}
            c = {dic_diseno_fatiga.get("c", 0)} {und_distancia}

    Momento de Inercia (I):

        Para la soldadura:
            I sold = {dic_diseno_fatiga["i_sold_ecuacion"]}
                I sold = {dic_diseno_fatiga.get("i_sold", 0)}

        Para las piezas:
            I piezas = {dic_diseno_fatiga["i_pieza_ecuacion"]}
                I piezas = {dic_diseno_fatiga.get("i_pieza", 0)}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_fatiga.get("area_sold", 0)}

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)} {und_fuerza}

    Cálculo de momento flector alternante y medio:

        Momento flector alternante (Ma) = Fa * b
            Ma = {dic_diseno_fatiga.get("momento_flector_alt", 0)} {und_fuerza}{und_distancia}

        Momento flector medio (Mm) = Fm * b
            Mm = {dic_diseno_fatiga.get("momento_flector_med", 0)} {und_fuerza}{und_distancia}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de filete de unión: {dic_diseno_fatiga.get("tipo_union")}, sometida a carga transversal, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo de esfuerzo cortante primario alternante y medio:

        τa' = Kfs * 1.414 * Fa / Asold
            τa' = {dic_diseno_fatiga.get("tao_primario_alt", 0)}

        τm' = 1.414 * Fm / Asold
            τm' = {dic_diseno_fatiga.get("tao_primario_med", 0)}

    Cálculo de esfuerzo cortante secundario alternante y medio:

        τa'' = Kfs * Ma * c / I
            τa'' = {dic_diseno_fatiga.get("tao_secundario_alt", 0)}

        τm'' = Mm * c / I
            τm'' = {dic_diseno_fatiga.get("tao_secundario_med", 0)}

    Cálculo de esfuerzo cortante resultante alternante y medio:

        τa = sqrt((τa')^2 + (τa'')^2)
            τa = {dic_diseno_fatiga.get("tao_alt_sold", 0)}

        τm = sqrt((τm')^2 + (τm'')^2)
            τm = {dic_diseno_fatiga.get("tao_med_sold", 0)}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la soldadura utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            h sold = {dic_diseno_fatiga.get("h_sold", 0)} {und_distancia} *


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Ma * c / I
            σa = {dic_diseno_fatiga.get("sigma_p_alt", 0)}

        σm = Mm * c / I
            σm = {dic_diseno_fatiga.get("sigma_p_med", 0)}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_p_alt", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_p_med", 0)}

    Cálculo de esfuerzo de Von Misses alternante y medio:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_diseno_fatiga.get("sigma_p_von_misses_alt", 0)}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ'm = {dic_diseno_fatiga.get("sigma_p_von_misses_med", 0)}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la pieza 1 utilizando ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            h pieza1 = {dic_diseno_fatiga.get("h_pieza1", 0)} {und_distancia} **


Para la pieza 2: (Pieza transversal a la carga aplicada)

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Fa / Asold
            σa = {dic_diseno_fatiga.get("sigma_t_alt", 0)}

        σm = Fm / Asold
            σm = {dic_diseno_fatiga.get("sigma_t_med", 0)}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Ma * c / I
            τa = {dic_diseno_fatiga.get("tao_t_alt", 0)}

        τm = Mm * c / I
            τm = {dic_diseno_fatiga.get("tao_t_med", 0)}

    Cálculo de esfuerzo de Von Misses alternante y medio:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_diseno_fatiga.get("sigma_t_von_misses_alt", 0)}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ'm = {dic_diseno_fatiga.get("sigma_t_von_misses_med", 0)}

    Cálculo de resistencia a la fatiga de la pieza 2:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión de la pieza 2:

        Sut = {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la pieza 2 utilizando ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            h pieza2 = {dic_diseno_fatiga.get("h_pieza2", 0)} {und_distancia} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de pierna calculados (*, **, ***), el mayor de ellos.

{dic_diseno_fatiga.get("verificacion_h_max", 0)}

{"~"*5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~"*5}

{dic_diseno_fatiga.get("verificacion_h_min", 0)}

"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen += f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_fatiga.get("h_sold", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_fatiga.get("h_pieza1", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_fatiga.get("h_pieza2", 0)} {und_distancia}</p>

        <div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_fatiga.get("verificacion_h_max"))}</strong></div>

        <p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
        <p>{dic_diseno_fatiga.get("verificacion_h_min", 0)}</p>

        </body>
                """  # Resumen de resultados de diseño de fatiga

        if dic_comprobacion is not None:

            verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

            verificacion_estatica_resumen = f"""
            <br><body>

            <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

            <p><strong>Factor de seguridad de la soldadura:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

            <p><strong>Factor de seguridad de la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

            <p><strong>Factor de seguridad de la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

            </body>
            """

            informe += verificacion_estatica

            resumen += verificacion_estatica_resumen

            if dic_diseno_estatica is not None:

                resultados_estatica = f"""
Se procede a rediseñar por carga estática la junta soldada.

Cálculos realizados


Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

        Distancia del eje nuetro hasta la soldadura (c) = {dic_diseno_estatica["c_ecuacion"]}
            c = {dic_diseno_estatica["c"]} {und_distancia}

    Momento de Inercia (I):

        Para la soldadura:
            I sold = {dic_diseno_estatica["i_sold_ecuacion"]}
                I sold = {dic_diseno_estatica["i_sold"]}

        Para las piezas:
            I piezas = {dic_diseno_estatica["i_pieza_ecuacion"]}
                I piezas = {dic_diseno_estatica["i_pieza"]}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica.get("area_sold", 0)}

    Cálculo del momento flector producido por la fuerza externa:

        M = F * b
            M = {dic_diseno_estatica["momento_flector"]} {und_fuerza}{und_distancia}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_diseno_estatica.get("tao_primario", 0)}

    Cálculo del esfuerzo cortante secundario:

        τ'' sold = M * c / I
            τ'' sold = {dic_diseno_estatica["tao_secundario"]}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τ')^2 + (τ'')^2)
            τ sold = {dic_diseno_estatica["tao_sold"]}

    Cálculo de la pierna mínima necesaria para la soldadura:

        FD sold = τ adm / τ sold
            h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia} *


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza1"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza1 = M * c / I
            σ pieza1 = {dic_diseno_estatica["sigma_p"]}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica["tao_p"]}

    Cálculo del esfuerzo Von Misses σ':

        σ' pieza1 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza1 = {dic_diseno_estatica["sigma_von_misses_1"]}

    Cálculo de la pierna mínima necesaria para la pieza 1:

        FD pieza = Sy / σ'
            h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}  **


Para la pieza 2: (Pieza transversal a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica["sigma_t"]}

    Cálculo del esfuerzo cortante:

        τ pieza2 = M * c / I
            τ pieza2 = {dic_diseno_estatica["tao_t"]}

    Cálculo del esfuerzo de Von Misses σ':

        σ' pieza2 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza2 = {dic_diseno_estatica["sigma_von_misses_2"]}

    Cálculo de la pierna mínima necesaria para la pieza 2:

        FD pieza = Sy / σ'
            h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de pierna calculados (*, **, ***), el mayor de ellos.

{dic_diseno_estatica.get("verificacion_h_max", 0)}

{"~" * 5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~" * 5}

{dic_diseno_estatica.get("verificacion_h_min", 0)}

"""  # Porción con resultados de cálculos de análisis estático.

                informe += resultados_estatica

                resumen += f"""
                <body>

                <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
                <hr>

                <p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
                <p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia}</p>

                <p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
                <p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}</p>

                <p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
                <p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}</p>

                <div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_estatica.get("verificacion_h_max"))}</strong></div>

                <p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
                <p>{dic_diseno_estatica.get("verificacion_h_min")}</p>

                </body>
                """

    return informe, resumen


# Informe para tamaño pierna: carga de torsion
def informe_diseno_h_filete_ctor(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                                 sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados del cálculo para el diseño de la pierna del
    cordón de soldadura sometida a carga de torsión debido a una fuerza excéntrica"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Pierna del Cordón para Soldadura de Filete Sometida a Carga de Torsión debido a una Fuerza Externa {tipo_carga.capitalize()} {"*" * 5}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados de los cálculos para el diseño del tamaño de la pierna del cordón para soldadura de filete sometida a carga de torsión debido a una fuerza externa {tipo_carga}. El objetivo del diseño es determinar el tamaño mínimo necesario de la pierna del cordón de soldadura, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\n""" # Introducción

    resumen = ""

    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): ** A determinar **
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_estatica.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_estatica.get("radio", 0)} {und_distancia}

    Tipo de union:  {dic_diseno_estatica.get("tipo_union")}

    Carga Aplicada:

        Tipo: Estática
        Fuerza: {dic_diseno_estatica.get("Fmax", 0)} {und_fuerza}
        Brazo (b) = {dic_diseno_estatica.get("b", 0)} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e) = {dic_diseno_estatica.get("espesor_menor_piezas", 0)} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

        Distancia en X desde el centroide hasta el punto crítico (rx) = {dic_diseno_estatica["rx_ecuacion"]}
            rx = {dic_diseno_estatica.get("rx", 0)} {und_distancia}

        Distancia en Y desde el centroide hasta el punto crítico (ry) = {dic_diseno_estatica["ry_ecuacion"]}
            ry = {dic_diseno_estatica.get("ry", 0)} {und_distancia}

    Momento Polar de Inercia (J):

            Para la soldadura:
                J sold = {dic_diseno_estatica["j_sold_ecuacion"]}
                    J sold = {dic_diseno_estatica.get("j_sold", 0)}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica.get("area_sold", 0)}

    Cálculo del momento torsor producido por la fuerza externa:

        T = F * b
            T = {dic_diseno_estatica.get("momento_torsor", 0)} {und_fuerza}{und_distancia}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_diseno_estatica.get("tao_primario", 0)}

    Cálculo del esfuerzo cortante secundario en el eje X y en el eje Y:

        τ'' sold x = T * ry / J
            τ'' sold x = {dic_diseno_estatica.get("tao_secundario_x", 0)}

        τ'' sold y = T * rx / J
            τ'' sold y = {dic_diseno_estatica.get("tao_secundario_y", 0)}

    Cálculo de la componente en el eje X del esfuerzo cortante resultante en la soldadura:

        τ sold x = τ'' sold x
            τ sold x = {dic_diseno_estatica.get("tao_x", 0)}

    Cálculo de la componente en el eje Y del esfuerzo cortante resultante en la soldadura:

        τ sold y = τ' sold + τ'' sold y
            τ sold y = {dic_diseno_estatica.get("tao_y", 0)}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τx)^2 + (τy)^2)
            τ sold = {dic_diseno_estatica.get("tao_sold", 0)}

    Cálculo de la pierna mínima necesaria para la soldadura:

        FD sold = τ adm / τ sold
            h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia} *


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica.get("tao_p", 0)}

    Cálculo de la pierna mínima necesaria para la pieza 1:

        FD pieza = Ssy / τ pieza1
            h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}  **


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica["sigma_t"]}

    Cálculo de la pierna mínima necesaria para la pieza 2:

        FD pieza = Sy / σ pieza2
            h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de pierna calculados (*, **, ***), el mayor de ellos.

{dic_diseno_estatica.get("verificacion_h_max")}

{"~" * 5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~" * 5}

{dic_diseno_estatica.get("verificacion_h_min")}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen += f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}</p>

        <div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_estatica.get("verificacion_h_max"))}</strong></div>

        <p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
        <p>{dic_diseno_estatica.get("verificacion_h_min")}</p>

        </body>
            """  # Resumen de resultados del diseño por estática.

    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): ** A determinar **
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_fatiga.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_fatiga.get("radio", 0)} {und_distancia}

    Tipo de union:  {dic_diseno_fatiga.get("tipo_union")}

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima (Fmax) = {dic_diseno_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima (Fmin) = {dic_diseno_fatiga.get("Fmin", 0)} {und_fuerza}
        Brazo (b) = {dic_diseno_fatiga.get("b", 0)} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e): {dic_diseno_fatiga.get("espesor_menor_piezas", 0)} {und_distancia}

"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la pierna del cordón de soldadura **

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_fatiga["lt_ecuacion"]}
            lt = {dic_diseno_fatiga.get("longitud_total", 0)} {und_distancia}

        Distancia en X desde el centroide hasta el punto crítico (rx) = {dic_diseno_fatiga["rx_ecuacion"]}
            rx = {dic_diseno_fatiga.get("rx", 0)} {und_distancia}

        Distancia en Y desde el centroide hasta el punto crítico (ry) = {dic_diseno_fatiga["ry_ecuacion"]}
            ry = {dic_diseno_fatiga.get("ry", 0)} {und_distancia}

    Momento Polar de Inercia (J):

        Para la soldadura:
            J sold = {dic_diseno_fatiga["j_sold_ecuacion"]}
                J sold = {dic_diseno_fatiga.get("j_sold", 0)}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_fatiga.get("area_sold", 0)}

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)} {und_fuerza}

    Cálculo de momento torsor alternante y medio:

        Momento torsor alternante (Ta) = Fa * b
            Ta = {dic_diseno_fatiga.get("momento_torsor_alt", 0)} {und_fuerza}{und_distancia}

        Momento torsor medio (Tm) = Fm * b
            Tm = {dic_diseno_fatiga.get("momento_torsor_med", 0)} {und_fuerza}{und_distancia}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de filete de unión: {dic_diseno_fatiga.get("tipo_union")}, sometida a carga de torsión, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo de esfuerzo cortante primario alternante y medio del material de aporte:

        τa' = Kfs * 1.414 * Fa / Asold
            τa' = {dic_diseno_fatiga.get("tao_primario_alt", 0)}

        τm' = 1.414 * Fm / Asold
            τm' = {dic_diseno_fatiga.get("tao_primario_med", 0)}

    Cálculo de la componente en el eje X y Y del esfuerzo cortante secundario alternante:

        τa'' x = Kfs * Ta * ry / J
            τa'' x = {dic_diseno_fatiga.get("tao_secundario_alt_x", 0)}

        τa'' y = Kfs * Tm * rx / J
            τa'' y = {dic_diseno_fatiga.get("tao_secundario_alt_y", 0)}

    Cálculo de la componente en el eje X y Y del esfuerzo cortante secundario medio:

        τm'' x = Tm * ry / J
            τm'' x = {dic_diseno_fatiga.get("tao_secundario_med_x", 0)}

        τm'' y = Tm * rx / J
            τm'' y = {dic_diseno_fatiga.get("tao_secundario_med_y", 0)}

    Cálculo de componentes X y Y del esfuerzo cortante alternante:

        τa x = τa'' x
            τa x = {dic_diseno_fatiga.get("tao_alt_x", 0)}

        τa y = τa' + τa'' y
            τa y = {dic_diseno_fatiga.get("tao_alt_y", 0)}

    Cálculo de componentes X y Y del esfuerzo cortante medio:

        τm x = τm'' x
            τm x = {dic_diseno_fatiga.get("tao_med_x", 0)}

        τm y = τm' + τm'' y
            τm y = {dic_diseno_fatiga.get("tao_med_y", 0)}

    Cálculo del esfuerzo cortante resultante alternante y medio en la soldadura:

        τa = sqrt((τa x)^2 + (τa y)^2)
            τa = {dic_diseno_fatiga.get("tao_alt_sold", 0)}

        τm = sqrt((τm x)^2 + (τm y)^2)
            τm = {dic_diseno_fatiga.get("tao_med_sold", 0)}

    Cálculo de la resistencia a la fatiga al cortante del material de aporte:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante del material de aporte

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la soldadura utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            h sold = {dic_diseno_fatiga.get("h_sold", 0)} {und_distancia} *


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Cálculo de esfuerzo cortante alternante y medio de la pieza 1:

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_p_alt", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_p_med", 0)}

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante de la pieza 1

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la pieza 1 utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            h pieza1 = {dic_diseno_fatiga.get("h_pieza1", 0)} {und_distancia} **


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Fa / Asold
            σa = {dic_diseno_fatiga.get("sigma_t_alt", 0)}

        σm = Fm / Asold
            σm = {dic_diseno_fatiga.get("sigma_t_med", 0)}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia a última a la tensión:

        Sut = {dic_diseno_fatiga["sut_pieza2"]} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la pieza 2 utilizando ecuación de Gerber:

        (FD * σa)/Se + ((FD * σm)/Sut)^2 = 1
            h pieza2 = {dic_diseno_fatiga.get("h_pieza2", 0)} {und_distancia} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de pierna calculados (*, **, ***), el mayor de ellos.

{dic_diseno_fatiga.get("verificacion_h_max", 0)}

{"~" * 5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~" * 5}

{dic_diseno_fatiga.get("verificacion_h_min", 0)}

"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen += f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_fatiga.get("h_sold", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_fatiga.get("h_pieza1", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_fatiga.get("h_pieza2", 0)} {und_distancia}</p>

        <div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_fatiga.get("verificacion_h_max"))}</strong></div>

        <p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
        <p>{dic_diseno_fatiga.get("verificacion_h_min", 0)}</p>

        </body>
                """  # Resumen de resultados de diseño de fatiga

        if dic_comprobacion is not None:

            verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

            verificacion_estatica_resumen = f"""
            <br><body>

            <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

            <p><strong>Factor de seguridad de la soldadura:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

            <p><strong>Factor de seguridad de la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

            <p><strong>Factor de seguridad de la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

            </body>
            """

            informe += verificacion_estatica

            resumen += verificacion_estatica_resumen

            if dic_diseno_estatica is not None:

                resultados_estatica = f"""
Se procede a rediseñar por carga estática la junta soldada.


Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

        Distancia en X desde el centroide hasta el punto crítico (rx) = {dic_diseno_estatica["rx_ecuacion"]}
            rx = {dic_diseno_estatica.get("rx", 0)} {und_distancia}

        Distancia en Y desde el centroide hasta el punto crítico (ry) = {dic_diseno_estatica["ry_ecuacion"]}
            ry = {dic_diseno_estatica.get("ry", 0)} {und_distancia}

    Momento Polar de Inercia (J):

            Para la soldadura:
                J sold = {dic_diseno_estatica["j_sold_ecuacion"]}
                    J sold = {dic_diseno_estatica.get("j_sold", 0)}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica.get("area_sold", 0)}

    Cálculo del momento torsor producido por la fuerza externa:

        T = F * b
            T = {dic_diseno_estatica.get("momento_torsor", 0)} {und_fuerza}{und_distancia}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_diseno_estatica.get("tao_primario", 0)}

    Cálculo del esfuerzo cortante secundario en el eje X y en el eje Y:

        τ'' sold x = T * ry / J
            τ'' sold x = {dic_diseno_estatica.get("tao_secundario_x", 0)}

        τ'' sold y = T * rx / J
            τ'' sold y = {dic_diseno_estatica.get("tao_secundario_y", 0)}

    Cálculo de la componente en el eje X del esfuerzo cortante resultante en la soldadura:

        τ sold x = τ'' sold x
            τ sold x = {dic_diseno_estatica.get("tao_x", 0)}

    Cálculo de la componente en el eje Y del esfuerzo cortante resultante en la soldadura:

        τ sold y = τ' sold + τ'' sold y
            τ sold y = {dic_diseno_estatica.get("tao_y", 0)}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τx)^2 + (τy)^2)
            τ sold = {dic_diseno_estatica.get("tao_sold", 0)}

    Cálculo de la pierna mínima necesaria para la soldadura:

        FD sold = τ adm / τ sold
            h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia} *


Para la pieza 1: (Pieza paralela a la carga aplicada, sometida a esfuerzo cortante)

    Resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica.get("tao_p", 0)}

    Cálculo de la pierna mínima necesaria para la pieza 1:

        FD pieza = Ssy / τ pieza1
            h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}  **


Para la pieza 2: (Pieza transversal a la carga aplicada, sometida a esfuerzo normal)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica["sigma_t"]}

    Cálculo de la pierna mínima necesaria para la pieza 2:

        FD pieza = Sy / σ pieza2
            h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de pierna calculados (*, **, ***), el mayor de ellos.

{dic_diseno_estatica.get("verificacion_h_max", 0)}

{"~" * 5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~" * 5}

{dic_diseno_estatica.get("verificacion_h_min", 0)}

"""  # Porción con resultados de cálculos del rediseño.

                informe += resultados_estatica

                resumen += f"""
                <body>

                <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
                <hr>

                <p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
                <p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia}</p>

                <p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
                <p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}</p>

                <p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
                <p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}</p>

                <div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_estatica.get("verificacion_h_max"))}</strong></div>

                <p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
                <p>{dic_diseno_estatica.get("verificacion_h_min")}</p>

                </body>
                """

    return informe, resumen


# Informe para tamaño pierna: carga de combinada
def informe_diseno_h_filete_cc(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                               sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados del cálculo para el diseño de la pierna del
    cordón de soldadura sometida a carga combinada debido a una fuerza excéntrica"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Pierna del Cordón para Soldadura de Filete Sometida a Carga Combinada debido a una Fuerza Externa {tipo_carga.capitalize()} Excéntrica al Centroide de la Soldadura {"*" * 5}
\nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
        """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados de los cálculos para el diseño del tamaño de la pierna del cordón para soldadura de filete sometida a carga combinada debido a una fuerza externa {tipo_carga} excéntrica al centroide de la soldadura. El objetivo del diseño es determinar el tamaño mínimo necesario de la pierna del cordón de soldadura, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\n""" # Introducción

    resumen = ""

    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): ** A determinar **
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_estatica.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_estatica.get("radio", 0)} {und_distancia}

    Tipo de union:  {dic_diseno_estatica.get("tipo_union")}

    Carga Aplicada:

        Tipo: Estática
        Fuerza: {dic_diseno_estatica.get("Fmax", 0)} {und_fuerza}
        Brazo longitudinal (bl) = {dic_diseno_estatica.get("bl", 0)} {und_distancia}
        Brazo transversal (bt) = {dic_diseno_estatica.get("bt", 0)} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e) = {dic_diseno_estatica.get("espesor_menor_piezas", 0)} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

        Distancia en X desde el centroide hasta el punto crítico (rx) = {dic_diseno_estatica["rx_ecuacion"]}
            rx = {dic_diseno_estatica.get("rx", 0)} {und_distancia}

        Distancia en Y desde el centroide hasta el punto crítico (ry) = {dic_diseno_estatica["ry_ecuacion"]}
            ry = {dic_diseno_estatica.get("ry", 0)} {und_distancia}

        Distancia del eje nuetro hasta la soldadura (c) = {dic_diseno_estatica["c_ecuacion"]}
            c = {dic_diseno_estatica["c"]} {und_distancia}

    Momento de Inercia (I):

        Para la soldadura:
            I sold = {dic_diseno_estatica["i_sold_ecuacion"]}
                I sold = {dic_diseno_estatica["i_sold"]}

        Para las piezas:
            I piezas = {dic_diseno_estatica["i_pieza_ecuacion"]}
                I piezas = {dic_diseno_estatica["i_pieza"]}

    Momento Polar de Inercia (J):

        Para la soldadura:
            J sold = {dic_diseno_estatica["j_sold_ecuacion"]}
                J sold = {dic_diseno_estatica.get("j_sold", 0)}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica.get("area_sold", 0)}

    Cálculo del momento flector producido por la fuerza externa:

        M = F * bl
            M = {dic_diseno_estatica["momento_flector"]} {und_fuerza}{und_distancia}

    Cálculo del momento torsor producido por la fuerza externa:

        T = F * bt
            T = {dic_diseno_estatica.get("momento_torsor", 0)} {und_fuerza}{und_distancia}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_diseno_estatica.get("tao_primario", 0)}

    Cálculo del esfuerzo cortante secundario:

        τ'' sold = M * c / I
            τ'' sold = {dic_diseno_estatica.get("tao_secundario", 0)}

    Cálculo de componentes del esfuerzo cortante terciario:

        En el eje X:
        τ''' sold x = T * ry / J
            τ''' sold x = {dic_diseno_estatica.get("tao_terciario_x", 0)}

        En el eje Y:
        τ''' sold y = T * rx / J
            τ''' sold y = {dic_diseno_estatica.get("tao_terciario_y", 0)}

    Cálculo de la componente en el eje X, Y y Z del esfuerzo cortante resultante en la soldadura:

        τ sold x = τ''' x
            τ sold x = {dic_diseno_estatica.get("tao_x", 0)}

        τ sold y = τ' + τ''' y
            τ sold y = {dic_diseno_estatica.get("tao_y", 0)}

        τ sold z = τ''
            τ sold z = {dic_diseno_estatica.get("tao_z", 0)}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τx)^2 + (τy)^2 + (τz)^2)
            τ sold = {dic_diseno_estatica.get("tao_sold", 0)}

    Cálculo de la pierna mínima necesaria para la soldadura:

        FD sold = τ adm / τ sold
            h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia} *


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza1"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza1 = M * c / I
            σ pieza1 = {dic_diseno_estatica.get("sigma_p", 0)}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica.get("tao_p", 0)}

    Cálculo del esfuerzo Von Misses en la pieza 1:

        σ' pieza1 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza1 = {dic_diseno_estatica.get("sigma_von_misses_1", 0)}

    Cálculo de la pierna mínima necesaria para la pieza 1:

        FD pieza = Sy / σ'
            h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}  **


Para la pieza 2: (Pieza Transversal a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica.get("sigma_t", 0)}

    Cálculo del esfuerzo cortante:

        τ pieza2 = M * c / I
            τ pieza2 = {dic_diseno_estatica.get("tao_t", 0)}

    Cálculo del esfuerzo Von Misses en la pieza 1:

        σ' pieza2 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza2 = {dic_diseno_estatica.get("sigma_von_misses_2", 0)}

    Cálculo de la pierna mínima necesaria para la pieza 2:

        FD pieza = Sy / σ'
            h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de pierna calculados (*, **, ***), el mayor de ellos.

{dic_diseno_estatica.get("verificacion_h_max")}

{"~" * 5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~" * 5}

{dic_diseno_estatica.get("verificacion_h_min")}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen += f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}</p>

        <div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_estatica.get("verificacion_h_max"))}</strong></div>

        <p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
        <p>{dic_diseno_estatica.get("verificacion_h_min")}</p>

        </body>
            """  # Resumen de resultados del diseño por estática.

    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Pierna (h): ** A determinar **
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Ancho (a) : {dic_diseno_fatiga.get("ancho", 0)} {und_distancia}
        Radio (r) : {dic_diseno_fatiga.get("radio", 0)} {und_distancia}

    Tipo de union:  Unión T

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima (Fmax) = {dic_diseno_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima (Fmin) = {dic_diseno_fatiga.get("Fmin", 0)} {und_fuerza}
        Brazo longitudinal (bl) = {dic_diseno_fatiga.get("bl", 0)} {und_distancia}
        Brazo transversal (bt) = {dic_diseno_fatiga.get("bt", 0)} {und_distancia}

    Espesor menor entre las piezas:

        Espesor (e): {dic_diseno_fatiga.get("espesor_menor_piezas", 0)} {und_distancia}

"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la pierna del cordón de soldadura **

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_fatiga["lt_ecuacion"]}
            lt = {dic_diseno_fatiga.get("longitud_total", 0)} {und_distancia}

        Distancia en X desde el centroide hasta el punto crítico (rx) = {dic_diseno_fatiga["rx_ecuacion"]}
            rx = {dic_diseno_fatiga.get("rx", 0)} {und_distancia}

        Distancia en Y desde el centroide hasta el punto crítico (ry) = {dic_diseno_fatiga["ry_ecuacion"]}
            ry = {dic_diseno_fatiga.get("ry", 0)} {und_distancia}

        Distancia del eje nuetro hasta la soldadura (c) = {dic_diseno_fatiga["c_ecuacion"]}
            c = {dic_diseno_fatiga["c"]} {und_distancia}

    Momento de Inercia (I):

        Para la soldadura:
            I sold = {dic_diseno_fatiga["i_sold_ecuacion"]}
                I sold = {dic_diseno_fatiga.get("i_sold", 0)}

        Para las piezas:
            I piezas = {dic_diseno_fatiga["i_pieza_ecuacion"]}
                I piezas = {dic_diseno_fatiga.get("i_pieza", 0)}

        Momento Polar de Inercia (J):

        Para la soldadura:
            J sold = {dic_diseno_fatiga["j_sold_ecuacion"]}
                J sold = {dic_diseno_fatiga.get("j_sold", 0)}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_fatiga.get("area_sold", 0)}

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)} {und_fuerza}

    Cálculo de momento flector alternante y medio:

        Momento flector alternante (Ma) = Fa * bl
            Ma = {dic_diseno_fatiga.get("momento_flector_alt", 0)} {und_fuerza}{und_distancia}

        Momento flector medio (Mm) = Fm * bl
            Mm = {dic_diseno_fatiga.get("momento_flector_med", 0)} {und_fuerza}{und_distancia}

    Cálculo de momento torsor alternante y medio:

        Momento torsor alternante (Ta) = Fm * bt
            Ta = {dic_diseno_fatiga.get("momento_torsor_alt", 0)} {und_fuerza}{und_distancia}

        Momento torsor medio (Tm) = Fm * bt
            Tm = {dic_diseno_fatiga.get("momento_torsor_med", 0)} {und_fuerza}{und_distancia}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de filete de unión T sometida a carga combinada, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}


Para la soldadura:

    Cálculo de esfuerzo cortante primario alternante y medio:

        τa' = Kfs * 1.414 * Fa / Asold
            τa' = {dic_diseno_fatiga.get("tao_primario_alt", 0)}

        τm' = 1.414 * Fm / Asold
            τm' = {dic_diseno_fatiga.get("tao_primario_med", 0)}

    Cálculo del esfuerzo cortante secundario alternante y medio:

        τa'' = Kfs * Ma * c / I
            τa'' = {dic_diseno_fatiga.get("tao_secundario_alt", 0)}

        τm'' = Mm * c / I
            τm'' = {dic_diseno_fatiga.get("tao_secundario_med", 0)}

    Cálculo de las componentes X y Y del esfuerzo cortante terciario alternante:

        τa''' x = = Kfs * Ta * ry / J
            τa''' x = {dic_diseno_fatiga.get("tao_terciario_alt_x", 0)}

        τa''' y = Kfs * Ta * rx / J
            τa''' y = {dic_diseno_fatiga.get("tao_terciario_alt_y", 0)}

    Cálculo de las componentes X y Y del esfuerzo cortante terciario medio:

        τm''' x = Tm * ry / J
            τm''' x = {dic_diseno_fatiga.get("tao_terciario_med_x", 0)}

        τm''' y = Tm * rx / J
            τm''' y = {dic_diseno_fatiga.get("tao_terciario_med_y", 0)}

    Cálculo de las componentes X, Y y Z del esfuerzo cortante terciario alternante:

        τa x = τa''' x
            τa x = {dic_diseno_fatiga.get("tao_alt_x", 0)}

        τa y = τa' + τa''' y
            τa y = {dic_diseno_fatiga.get("tao_alt_y", 0)}

        τa z = τa''
            τa z = {dic_diseno_fatiga.get("tao_alt_z", 0)}

    Cálculo de las componentes X, Y y Z del esfuerzo cortante terciario medio:

        τm x = τm''' x
            τm x = {dic_diseno_fatiga.get("tao_med_x", 0)}

        τm y = τm' + τm''' y
            τm y = {dic_diseno_fatiga.get("tao_med_y", 0)}

        τm z = τm''
            τm z = {dic_diseno_fatiga.get("tao_med_z", 0)}

    Cálculo del esfuerzo cortante resultante alternante y medio del material de aporte:

        τa = sqrt((τa x)^2 + (τa y)^2 + (τa z)^2)
            τa = {dic_diseno_fatiga.get("tao_alt_sold", 0)}

        τm = sqrt((τm x)^2 + (τm y)^2 + (τm z)^2)
            τm = {dic_diseno_fatiga.get("tao_med_sold", 0)}

    Cálculo de la resistencia a la fatiga al cortante del material de aporte:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante del material de aporte

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la soldadura utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            h sold = {dic_diseno_fatiga.get("h_sold", 0)} {und_distancia} *


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Ma * c / I
            σa = {dic_diseno_fatiga.get("sigma_p_alt", 0)}

        σm = Mm * c / I
            σm = {dic_diseno_fatiga.get("sigma_p_med", 0)}

    Cálculo de esfuerzo cortante alternante y medio::

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_p_alt", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_p_med", 0)}

    Cálculo de esfuerzo de Von Misses alternante y medio en la pieza 1:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_diseno_fatiga.get("sigma_p_von_misses_alt", 0)}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ'm = {dic_diseno_fatiga.get("sigma_p_von_misses_med", 0)}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia última a la tensión de la pieza 1:

        Sut = {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la pieza 1 utilizando ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            h pieza1 = {dic_diseno_fatiga.get("h_pieza1", 0)} {und_distancia} **


Para la pieza 2: (Pieza transversal a la carga aplicada)

    Cálculo de esfuerzo normal alternante y medio:

        σa = Kfs * Fa / Asold
            σa = {dic_diseno_fatiga.get("sigma_t_alt", 0)}

        σm = Fm / Asold
            σm = {dic_diseno_fatiga.get("sigma_t_med", 0)}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Ma * c / I
            τa = {dic_diseno_fatiga.get("tao_t_alt", 0)}

        τm = Mm * c / I
            τm = {dic_diseno_fatiga.get("tao_t_med", 0)}

    Cálculo de esfuerzo de Von Misses alternante y medio en la pieza 2:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_diseno_fatiga.get("sigma_t_von_misses_alt", 0)}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ'm = {dic_diseno_fatiga.get("sigma_t_von_misses_med", 0)}

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión de la pieza 2:

        Sut = {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo de la pierna mínima necesaria para la pieza 2 utilizando ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            h pieza2 = {dic_diseno_fatiga.get("h_pieza2", 0)} {und_distancia} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de pierna calculados (*, **, ***), el mayor de ellos.

{dic_diseno_fatiga.get("verificacion_h_max", 0)}

{"~" * 5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~" * 5}

{dic_diseno_fatiga.get("verificacion_h_min", 0)}

"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen += f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_fatiga.get("h_sold", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_fatiga.get("h_pieza1", 0)} {und_distancia}</p>

        <p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_fatiga.get("h_pieza2", 0)} {und_distancia}</p>

        <div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_fatiga.get("verificacion_h_max"))}</strong></div>

        <p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
        <p>{dic_diseno_fatiga.get("verificacion_h_min", 0)}</p>

        </body>
                """  # Resumen de resultados de diseño de fatiga

        if dic_comprobacion is not None:

            verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

            verificacion_estatica_resumen = f"""
            <br><body>

            <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

            <p><strong>Factor de seguridad de la soldadura:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

            <p><strong>Factor de seguridad de la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

            <p><strong>Factor de seguridad de la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
            <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

            </body>
            """

            informe += verificacion_estatica

            resumen += verificacion_estatica_resumen

            if dic_diseno_estatica is not None:

                resultados_estatica = f"""
Se procede a rediseñar por carga estática la junta soldada.


Cálculos realizados

    Cálculos de parámetros geométricos de la soldadura:

        Longitud total (lt) = {dic_diseno_estatica["lt_ecuacion"]}
            lt = {dic_diseno_estatica.get("longitud_total", 0)} {und_distancia}

        Distancia en X desde el centroide hasta el punto crítico (rx) = {dic_diseno_estatica["rx_ecuacion"]}
            rx = {dic_diseno_estatica.get("rx", 0)} {und_distancia}

        Distancia en Y desde el centroide hasta el punto crítico (ry) = {dic_diseno_estatica["ry_ecuacion"]}
            ry = {dic_diseno_estatica.get("ry", 0)} {und_distancia}

        Distancia del eje nuetro hasta la soldadura (c) = {dic_diseno_estatica["c_ecuacion"]}
            c = {dic_diseno_estatica["c"]} {und_distancia}

    Momento de Inercia (I):

        Para la soldadura:
            I sold = {dic_diseno_estatica["i_sold_ecuacion"]}
                I sold = {dic_diseno_estatica["i_sold"]}

        Para las piezas:
            I piezas = {dic_diseno_estatica["i_pieza_ecuacion"]}
                I piezas = {dic_diseno_estatica["i_pieza"]}

    Momento Polar de Inercia (J):

        Para la soldadura:
            J sold = {dic_diseno_estatica["j_sold_ecuacion"]}
                J sold = {dic_diseno_estatica.get("j_sold", 0)}

    Área de la soldadura:

        A sold = h * lt
            A sold = {dic_diseno_estatica.get("area_sold", 0)}

    Cálculo del momento flector producido por la fuerza externa:

        M = F * bl
            M = {dic_diseno_estatica["momento_flector"]} {und_fuerza}{und_distancia}

    Cálculo del momento torsor producido por la fuerza externa:

        T = F * bt
            T = {dic_diseno_estatica.get("momento_torsor", 0)} {und_fuerza}{und_distancia}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del esfuerzo cortante primario:

        τ' sold = 1.414 * F / Asold
            τ' sold = {dic_diseno_estatica.get("tao_primario", 0)}

    Cálculo del esfuerzo cortante secundario:

        τ'' sold = M * c / I
            τ'' sold = {dic_diseno_estatica.get("tao_secundario", 0)}

    Cálculo de componentes del esfuerzo cortante terciario:

        En el eje X:
        τ''' sold x = T * ry / J
            τ''' sold x = {dic_diseno_estatica.get("tao_terciario_x", 0)}

        En el eje Y:
        τ''' sold y = T * rx / J
            τ''' sold y = {dic_diseno_estatica.get("tao_terciario_y", 0)}

    Cálculo de la componente en el eje X, Y y Z del esfuerzo cortante resultante en la soldadura:

        τ sold x = τ''' x
            τ sold x = {dic_diseno_estatica.get("tao_x", 0)}

        τ sold y = τ' + τ''' y
            τ sold y = {dic_diseno_estatica.get("tao_y", 0)}

        τ sold z = τ''
            τ sold z = {dic_diseno_estatica.get("tao_z", 0)}

    Cálculo del esfuerzo cortante resultante en la soldadura:

        τ sold = sqrt((τx)^2 + (τy)^2 + (τz)^2)
            τ sold = {dic_diseno_estatica.get("tao_sold", 0)}

    Cálculo de la pierna mínima necesaria para la soldadura:

        FD sold = τ adm / τ sold
            h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia} *


Para la pieza 1: (Pieza paralela a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza1"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza1 = M * c / I
            σ pieza1 = {dic_diseno_estatica.get("sigma_p", 0)}

    Cálculo del esfuerzo cortante:

        τ pieza1 = F / Asold
            τ pieza1 = {dic_diseno_estatica.get("tao_p", 0)}

    Cálculo del esfuerzo Von Misses en la pieza 1:

        σ' pieza1 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza1 = {dic_diseno_estatica.get("sigma_von_misses_1", 0)}

    Cálculo de la pierna mínima necesaria para la pieza 1:

        FD pieza = Sy / σ'
            h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}  **


Para la pieza 2: (Pieza Transversal a la carga aplicada)

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica["sy_pieza2"]} {und_esfuerzo}

    Cálculo del esfuerzo normal:

        σ pieza2 = F / Asold
            σ pieza2 = {dic_diseno_estatica.get("sigma_t", 0)}

    Cálculo del esfuerzo cortante:

        τ pieza2 = M * c / I
            τ pieza2 = {dic_diseno_estatica.get("tao_t", 0)}

    Cálculo del esfuerzo Von Misses en la pieza 1:

        σ' pieza2 = sqrt(σ^2 + 3 * τ^2)
            σ' pieza2 = {dic_diseno_estatica.get("sigma_von_misses_2", 0)}

    Cálculo de la pierna mínima necesaria para la pieza 2:

        FD pieza = Sy / σ'
            h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de pierna calculados (*, **, ***), el mayor de ellos.

{dic_diseno_estatica.get("verificacion_h_max", 0)}

{"~" * 5} Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1 {"~" * 5}

{dic_diseno_estatica.get("verificacion_h_min", 0)}

"""  # Porción con resultados de cálculos de análisis estático.

                informe += resultados_estatica

                resumen += f"""
                <body>

                <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
                <hr>

                <p><strong>Cálculo de la pierna mínima necesaria para la soldadura:</strong></p>
                <p style="margin-left: 20px; color: blue;">h sold = {dic_diseno_estatica.get("h_min_sold", 0)} {und_distancia}</p>

                <p><strong>Cálculo de la pierna mínima necesaria para la pieza 1:</strong></p>
                <p style="margin-left: 20px; color: blue;">h pieza1 = {dic_diseno_estatica.get("h_min_pieza1", 0)} {und_distancia}</p>

                <p><strong>Cálculo de la pierna mínima necesaria para la pieza 2:</strong></p>
                <p style="margin-left: 20px; color: blue;">h pieza2 = {dic_diseno_estatica.get("h_min_pieza2", 0)} {und_distancia}</p>

                <div style="color: blue;"><strong>Se concluye que: {escape(dic_diseno_estatica.get("verificacion_h_max"))}</strong></div>

                <p style="margin-left: 20px;"><strong>Verificación del tamaño mínimo de la pierna según la especificación de la norma AWS D1.1:</strong></p>
                <p>{dic_diseno_estatica.get("verificacion_h_min")}</p>

                </body>
                """

    return informe, resumen


# DISEÑO RANURA

# Carga Permisible
def informe_diseno_carga_ranura_cp(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                                   sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):

    """Esta función le dará forma al informe y resumen de resultados de cálculo de diseño para carga permisible de
    soldadura de ranura sometida a carga paralela"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Carga Permisible para Soldadura de Ranura Sometida a Carga Paralela {tipo_carga.capitalize()} {"*" * 5}
    \nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
            """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados para el cálculo de la carga permisible para soldadura de ranura sometida a carga paralela {tipo_carga}. El objetivo es determinar la magnitud de la carga máxima permisible en la junta soldada, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\n"""  # Introducción

    resumen = ""

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_diseno_estatica.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}

    Tipo de union: Tope

    Carga Aplicada:

        Tipo: Estática
        Fuerza: ** A determinar **\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Área de la soldadura:

        A sold = {dic_diseno_estatica["area_sold_ecuacion"]}
            A sold = {dic_diseno_estatica.get("area_sold", 0)} {und_distancia}²

    Cálculo del esfuerzo cortante aplicado en la junta:

        τ = F / Asold
            τ = {dic_diseno_estatica.get("tao", 0)}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = τ adm / τ
            Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}  *


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Ssy / τ
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}  **


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Ssy / τ
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados del diseño por carga estática.

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_diseno_fatiga.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}

    Tipo de union: Tope

    Cargas Aplicadas:

        Tipo: Cíclica
        Relación de carga (Fmax/Fmin) = {dic_diseno_fatiga.get("relacion_cargas", 0)}

"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la fuerza mínima aplicada, según la relación de fuerzas Fmax/Fmin **

    Área de la soldadura:

        A sold = {dic_diseno_fatiga["area_sold_ecuacion"]}
            A sold = {dic_diseno_fatiga.get("area_sold", 0)} {und_distancia}²

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión tope sometida a carga paralela, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_alt", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_med", 0)}


Para la soldadura:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la soldadura utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            F sold = {dic_diseno_fatiga.get("f_sold", 0)} {und_fuerza} *


Para la pieza 1:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 1 utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            F pieza1 = {dic_diseno_fatiga.get("f_pieza1", 0)} {und_fuerza} **


Para la pieza 2:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza2", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza2", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 2 utilizando la ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            F pieza2 = {dic_diseno_fatiga.get("f_pieza2", 0)} {und_fuerza} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se selecciona la menor de las fuerzas calculadas (*, **, ***) y se multiplica por la relación de carga para determinar la fuerza máxima permisible de la junta.

Fperm = Relación * Fmin  = {dic_diseno_fatiga.get("relacion_cargas")} * {dic_diseno_fatiga.get("f_min")} {und_fuerza}

Por lo que, {dic_diseno_fatiga.get("conclusion_fperm")}.


Diseño por fatiga de la carga permisible completado.


"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {"{:.2f}".format(dic_diseno_fatiga.get("f_sold") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza1") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza2") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados del diseño por fatiga

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

        else:

            informe += verificacion_estatica

            informe += f"Al presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno = f"""

Cálculos realizados

    Cálculo del esfuerzo cortante aplicado en la junta:

        τ = F / Asold
            τ = {dic_diseno_estatica.get("tao", 0)}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = τ adm / τ
            Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}  *


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Ssy / τ
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}  **


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Ssy / τ
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

            """  # Porción con resultados de cálculos de análisis estático.

            informe += resultados_rediseno

            resumen_estatica = f"""
            <body>

            <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
            <hr>

            <p><strong>Carga permisible en la soldadura:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

            <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

            </body>
            """  # Resumen de resultados del rediseño por estática.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

    return informe, resumen


def informe_diseno_carga_ranura_ct(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                                   sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de cálculo de diseño para carga permisible de
    soldadura de ranura sometida a carga transversal"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Carga Permisible para Soldadura de Ranura Sometida a Carga Transversal {tipo_carga.capitalize()} {"*" * 5}
    \nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
            """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados para el cálculo de la carga permisible para soldadura de ranura sometida a carga transversal {tipo_carga}. El objetivo es determinar la magnitud de la carga máxima permisible en la junta soldada, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\n"""  # Introducción

    resumen = ""

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_diseno_estatica.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_diseno_estatica.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_diseno_estatica.get("tipo_union", 0)}

    Carga Aplicada:

        Tipo: Estática
        Fuerza: ** A determinar **\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Área de la soldadura:

        A sold = {dic_diseno_estatica["area_sold_ecuacion"]}
            A sold = {dic_diseno_estatica.get("area_sold", 0)} {und_distancia}²

    Cálculo del esfuerzo normal aplicado en la junta:

        σ = F / Asold
            σ = {dic_diseno_estatica.get("sigma", 0)}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = Sy / σ
            Fperm sold = {dic_diseno_estatica.get("f_max_sold", 0)} {und_fuerza}  *


Para la pieza 1:

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Sy / σ
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1", 0)} {und_fuerza}  **


Para la pieza 2:

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Sy / σ
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados del diseño por carga estática.

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_diseno_fatiga.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_diseno_fatiga.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_diseno_fatiga.get("tipo_union", 0)}

    Cargas Aplicadas:

        Tipo: Cíclica
        Relación de carga (Fmax/Fmin) = {dic_diseno_fatiga.get("relacion_cargas", 0)}

"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la fuerza mínima aplicada, según la relación de fuerzas Fmax/Fmin **

    Área de la soldadura:

        A sold = {dic_diseno_fatiga["area_sold_ecuacion"]}
            A sold = {dic_diseno_fatiga.get("area_sold", 0)} {und_distancia}²

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión: {dic_diseno_fatiga.get("tipo_union", 0)}, sometida a carga transversal, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}

    Cálculo de esfuerzo normal alternantes y medio:

        σa = Kfs * Fa / Asold
            σa = {dic_diseno_fatiga.get("sigma_alt", 0)}

        σm = Fm / Asold
            σm = {dic_diseno_fatiga.get("sigma_med", 0)}


Para la soldadura:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_sold", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la soldadura utilizando ecuación de Gerber:

        (FD * σa)/Se + ((FD * σm)/Sut)^2 = 1
            F sold = {dic_diseno_fatiga.get("f_sold", 0)} {und_fuerza} *


Para la pieza 1:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 1 utilizando ecuación de Gerber:

        (FD * σa)/Se + ((FD * σm)/Sut)^2 = 1
            F pieza1 = {dic_diseno_fatiga.get("f_pieza1", 0)} {und_fuerza} **


Para la pieza 2:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 2 utilizando la ecuación de Gerber:

        (FD * σa)/Se + ((FD * σm)/Sut)^2 = 1
            F pieza2 = {dic_diseno_fatiga.get("f_pieza2", 0)} {und_fuerza} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se selecciona la menor de las fuerzas calculadas (*, **, ***) y se multiplica por la relación de carga para determinar la fuerza máxima permisible de la junta.

Fperm = Relación * Fmin  = {dic_diseno_fatiga.get("relacion_cargas", 0)} * {dic_diseno_fatiga.get("f_min", 0)} {und_fuerza}

Por lo que, {dic_diseno_fatiga.get("conclusion_fperm")}


Diseño por fatiga de la carga permisible completado.


"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {"{:.2f}".format(dic_diseno_fatiga.get("f_sold") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza1") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza2") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados del diseño por fatiga

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

        else:

            informe += verificacion_estatica

            informe += f"Al presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno = f"""

Cálculos realizados

    Cálculo del esfuerzo normal aplicado en la junta:

        σ = F / Asold
            σ = {dic_diseno_estatica.get("sigma", 0)}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = Sy / σ
            Fperm sold = {dic_diseno_estatica.get("f_max_sold", 0)} {und_fuerza}  *


Para la pieza 1:

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Sy / σ
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1", 0)} {und_fuerza}  **


Para la pieza 2:

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Sy / σ
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

            """  # Porción con resultados de cálculos de análisis estático.

            informe += resultados_rediseno

            resumen_estatica = f"""
            <body>

            <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
            <hr>

            <p><strong>Carga permisible en la soldadura:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

            <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

            </body>
            """  # Resumen de resultados del rediseño por estática.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

    return informe, resumen


def informe_diseno_carga_ranura_cf(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                                   sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de cálculo de diseño para carga permisible de
    soldadura de ranura sometida a carga de flexión debido a una fuerza excéntrica"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Carga Permisible para Soldadura de Ranura Sometida a Carga de Flexión debido a una Fuerza Externa {tipo_carga.capitalize()}{"*" * 5}
    \nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
            """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados para el cálculo de la carga permisible para soldadura de ranura sometida a carga de flexión debido a una fuerza externa {tipo_carga}. El objetivo es determinar la magnitud de la carga máxima permisible en la junta soldada, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\n"""  # Introducción

    resumen = ""

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_diseno_estatica.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_diseno_estatica.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_diseno_estatica.get("tipo_union", 0)}

    Carga Aplicada:

        Tipo: Estática
        Fuerza: ** A determinar **
        Brazo (b) = {dic_diseno_estatica["b"]} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Distancia del eje nuetro hasta la soldadura (c):

        c = {dic_diseno_estatica["c_ecuacion"]}
            c = {dic_diseno_estatica.get("c", 0)} {und_distancia}

    Momento de Inercia (I):

        I = {dic_diseno_estatica["i_sold_ecuacion"]}
            I = {dic_diseno_estatica.get("i_sold", 0)} {und_distancia}^4

    Área de la soldadura:

        A sold = {dic_diseno_estatica["area_sold_ecuacion"]}
            A sold = {dic_diseno_estatica.get("area_sold", 0)} {und_distancia}²

    Cálculo del momento flector producido por la fuerza externa:

        M = F * b
            M = {dic_diseno_estatica.get("momento_flector", 0)}

    Esfuerzos aplicados en la junta:

        Cálculo del esfuerzo normal:

            σ = M * c / I
                σ = {dic_diseno_estatica.get("sigma", 0)}

        Cálculo del esfuerzo cortante:

            τ = F / Asold
                τ = {dic_diseno_estatica.get("tao", 0)}

        Cálculo del esfuerzo de Von Misses:

            σ' = sqrt(σ^2 + 3 * τ^2)
                σ' = {dic_diseno_estatica.get("sigma_von_misses", 0)}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = Sy / σ'
            Fperm sold = {dic_diseno_estatica.get("f_max_sold", 0)} {und_fuerza}  *


Para la pieza 1:

    Resistencia a la fluencia del metal base 1 (pieza 1):

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Sy / σ'
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1", 0)} {und_fuerza}  **


Para la pieza 2:

    Resistencia a la fluencia del metal base base 2 (pieza 2):

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Sy / σ'
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados del diseño por carga estática.

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_diseno_fatiga.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_diseno_fatiga.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_diseno_fatiga.get("tipo_union", 0)}

    Cargas Aplicadas:

        Tipo: Cíclica
        Relación de carga (Fmax/Fmin) = {dic_diseno_fatiga.get("relacion_cargas", 0)}

"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la fuerza mínima aplicada, según la relación de fuerzas Fmax/Fmin **

    Distancia del eje nuetro hasta la soldadura (c):

        c = {dic_diseno_fatiga["c_ecuacion"]}
            c = {dic_diseno_fatiga.get("c", 0)} {und_distancia}

    Momento de Inercia (I):

        I = {dic_diseno_fatiga["i_sold_ecuacion"]}
            I = {dic_diseno_fatiga.get("i_sold", 0)} {und_distancia}^4

    Área de la soldadura:

        A sold = {dic_diseno_fatiga["area_sold_ecuacion"]}
            A sold = {dic_diseno_fatiga.get("area_sold", 0)} {und_distancia}²

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)}

    Cálculo de momento flector alternante y medio:

        Momento flector alternante (Ma) = Fa * b
            Ma = {dic_diseno_fatiga.get("momento_flector_alt", 0)}

        Momento flector medio (Mm) = Fm * b
            Mm = {dic_diseno_fatiga.get("momento_flector_med", 0)}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión: {dic_diseno_fatiga.get("tipo_union", 0)}, sometida a carga de flexión, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}

    Cálculo de esfuerzo normal alternantes y medio:

        σa = Kfs * Ma * c / I
            σa = {dic_diseno_fatiga.get("sigma_alt", 0)}

        σm = Mm * c / I
            σm = {dic_diseno_fatiga.get("sigma_med", 0)}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_alt", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_med", 0)}

    Cálculo de esfuerzos de Von Misses alternante y medio:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_diseno_fatiga.get("sigma_von_misses_alt", 0)}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ'm = {dic_diseno_fatiga.get("sigma_von_misses_med", 0)}


Para la soldadura:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_sold", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la soldadura utilizando ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            F sold = {dic_diseno_fatiga.get("f_sold", 0)} {und_fuerza} *


Para la pieza 1:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 1 utilizando ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            F pieza1 = {dic_diseno_fatiga.get("f_pieza1", 0)} {und_fuerza} **


Para la pieza 2:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 2 utilizando la ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            F pieza2 = {dic_diseno_fatiga.get("f_pieza2", 0)} {und_fuerza} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se selecciona la menor de las fuerzas calculadas (*, **, ***) y se multiplica por la relación de carga para determinar la fuerza máxima permisible de la junta.

Fperm = Relación * Fmin  = {dic_diseno_fatiga.get("relacion_cargas", 0)} * {dic_diseno_fatiga.get("f_min", 0)} {und_fuerza}

Por lo que, {dic_diseno_fatiga.get("conclusion_fperm")}.


Diseño por fatiga de la carga permisible completado.


"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {"{:.2f}".format(dic_diseno_fatiga.get("f_sold") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza1") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza2") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados del diseño por fatiga

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

        else:

            informe += verificacion_estatica

            informe += f"Al presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno = f"""

Cálculos realizados

    Cálculo del momento flector producido por la fuerza externa:

        M = F * b
            M = {dic_diseno_estatica.get("momento_flector", 0)}

    Esfuerzos aplicados en la junta:

        Cálculo del esfuerzo normal:

            σ = M * c / I
                σ = {dic_diseno_estatica.get("sigma", 0)}

        Cálculo del esfuerzo cortante:

            τ = F / Asold
                τ = {dic_diseno_estatica.get("tao", 0)}

        Cálculo del esfuerzo de Von Misses:

            σ' = sqrt(σ^2 + 3 * τ^2)
                σ' = {dic_diseno_estatica.get("sigma_von_misses", 0)}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = Sy / σ'
            Fperm sold = {dic_diseno_estatica.get("f_max_sold", 0)} {und_fuerza}  *


Para la pieza 1:

    Resistencia a la fluencia del metal base 1 (pieza 1):

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Sy / σ'
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1", 0)} {und_fuerza}  **


Para la pieza 2:

    Resistencia a la fluencia del metal base base 2 (pieza 2):

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Sy / σ'
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm")}

            """  # Porción con resultados de cálculos de análisis estático.

            informe += resultados_rediseno

            resumen_estatica = f"""
            <body>

            <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
            <hr>

            <p><strong>Carga permisible en la soldadura:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

            <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

            </body>
            """  # Resumen de resultados del rediseño por estática.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

    return informe, resumen


def informe_diseno_carga_ranura_ctor(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                                     sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de cálculo de diseño para carga permisible de
    soldadura de ranura sometida a carga de torsión pura"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Carga Permisible para Soldadura de Ranura Sometida a Carga de Torsión Pura {tipo_carga.capitalize()}  {"*" * 5}
    \nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
            """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados de los cálculos para el diseño de la carga permisible para soldadura de ranura sometida a carga de torsión pura {tipo_carga}. El objetivo es determinar la magnitud de la carga máxima permisible en la junta soldada, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\n"""  # Introducción

    resumen = ""

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_diseno_estatica.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_diseno_estatica.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_diseno_estatica.get("tipo_union", 0)}

    Carga Aplicada:

        Tipo: Estática
        Torque: ** A determinar **\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Distancia desde el centroide hasta el pto crítico de la soldadura (r):

        r = sqrt(({dic_diseno_estatica["rx_ecuacion"]})^2 + ({dic_diseno_estatica["ry_ecuacion"]})^2)
            r = {dic_diseno_estatica["r"]} {und_distancia}

    Momento de Inercia Polar (J):

        J = {dic_diseno_estatica["j_sold_ecuacion"]}
            J = {dic_diseno_estatica["j_sold"]} {und_distancia}^4

    Área de la soldadura:

        A sold = {dic_diseno_estatica["area_sold_ecuacion"]}
            A sold = {dic_diseno_estatica.get("area_sold", 0)} {und_distancia}²

    Esfuerzo cortante aplicado en la junta:

        τ = T * r / J
            τ = {dic_diseno_estatica.get("tao", 0)}


Para la soldadura:

    Cálculo de la resistencia cortante admisible:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del momento torsor máximo permisible en la soldadura:

        FD sold = τ adm / τ
            Tperm sold = {dic_diseno_estatica.get("t_max_sold", 0)} {und_fuerza}{und_distancia}  *


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante del metal base 1 (pieza 1):

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del momento torsor máximo permisible en la pieza 1:

        FD pieza = Ssy / τ
            Tperm pieza1 = {dic_diseno_estatica.get("t_max_pieza1", 0)} {und_fuerza}{und_distancia}  **


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante del metal base 2 (pieza 2):

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo del momento torsor máximo permisible en la pieza 2:

        FD pieza = Ssy / τ
            Tperm pieza2 = {dic_diseno_estatica.get("t_max_pieza2", 0)} {und_fuerza}{und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_tperm", 0)}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Tperm sold = {dic_diseno_estatica.get("t_max_sold")} {und_fuerza}{und_distancia}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Tperm pieza1 = {dic_diseno_estatica.get("t_max_pieza1")} {und_fuerza}{und_distancia}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Tperm pieza2 = {dic_diseno_estatica.get("t_max_pieza2")} {und_fuerza}{und_distancia}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_tperm")} </strong></p>

        </body>
        """  # Resumen de resultados del diseño por carga estática.

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_diseno_fatiga.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_diseno_fatiga.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_diseno_fatiga.get("tipo_union", 0)}

    Cargas Aplicadas:

        Tipo: Cíclica
        Relación de carga (Tmax/Tmin) = {dic_diseno_fatiga.get("relacion_cargas", 0)}

"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función del momento torsor mínimo aplicado, según la relación de cargas Tmax/Tmin **

    Distancia desde el centroide hasta el pto crítico de la soldadura (r):

        r = sqrt(({dic_diseno_fatiga["rx_ecuacion"]})^2 + ({dic_diseno_fatiga["ry_ecuacion"]})^2)
            r = {dic_diseno_fatiga["r"]} {und_distancia}

    Momento de Inercia Polar (J):

        J = {dic_diseno_fatiga["j_sold_ecuacion"]}
            J = {dic_diseno_fatiga["j_sold"]} {und_distancia}^4

    Área de la soldadura:

        A sold = {dic_diseno_fatiga["area_sold_ecuacion"]}
            A sold = {dic_diseno_fatiga.get("area_sold", 0)} {und_distancia}²

    Cálculo de momento torsor (Torque) alternante y medio:

        Momento torsor alternante (Ta) = (Tmax - Tmin) / 2
            Ta = {dic_diseno_fatiga.get("momento_torsor_alt", 0)}

        Momento torsor medio (Tm) = (Tmax + Tmin) / 2
            Tm = {dic_diseno_fatiga.get("momento_torsor_med", 0)}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión: {dic_diseno_fatiga["tipo_union"]}, sometida a carga de torsión, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}

    Cálculo de esfuerzos cortantes alternantes y medios:

        τa = Kfs * Ta * r / J
            τa = {dic_diseno_fatiga.get("tao_alt", 0)}

        τm = Tm * r / J
            τm = {dic_diseno_fatiga.get("tao_med", 0)}


Para la soldadura:

    Cálculo de la resistencia a la fatiga:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo de T = Tmin en la soldadura utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            T sold = {dic_diseno_fatiga.get("t_sold", 0)} {und_fuerza}{und_distancia} *


Para la pieza 1:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo de T = Tmin en la pieza 1 utilizando ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            T pieza1 = {dic_diseno_fatiga.get("t_pieza1", 0)} {und_fuerza}{und_distancia} **


Para la pieza 2:

    Cálculo de la resistencia a la fatiga:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza2", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza2", 0)} {und_esfuerzo}

    Cálculo de T = Tmin en la pieza 2 utilizando la ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            T pieza2 = {dic_diseno_fatiga.get("t_pieza2", 0)} {und_fuerza}{und_distancia} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se selecciona la menor de las cargas calculados (*, **, ***) y se multiplica por la relación de carga para determinar la carga máxima permisible de la junta.

Tperm = Relación * Tmin  = {dic_diseno_fatiga.get("relacion_cargas", 0)} * {dic_diseno_fatiga.get("t_min", 0)} {und_fuerza}{und_distancia}

Por lo que, {dic_diseno_fatiga.get("conclusion_tperm")}.


Diseño por fatiga de la carga permisible completado.


"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Tperm sold = {"{:.2f}".format(dic_diseno_fatiga.get("t_sold") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}{und_distancia}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Tperm pieza1 = {"{:.2f}".format(dic_diseno_fatiga.get("t_pieza1") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}{und_distancia}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Tperm pieza2 = {"{:.2f}".format(dic_diseno_fatiga.get("t_pieza2") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}{und_distancia}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_tperm")} </strong></p>

        </body>
        """  # Resumen de resultados de análisis de fatiga

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

        else:
            informe += verificacion_estatica

            informe += f"Al presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno = f"""

Cálculos realizados

    Esfuerzo cortante aplicado en la junta:

        τ = T * r / J
            τ = {dic_diseno_estatica.get("tao", 0)}


Para la soldadura:

    Cálculo de la resistencia cortante admisible:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del momento torsor máximo permisible en la soldadura:

        FD sold = τ adm / τ
            Tperm sold = {dic_diseno_estatica.get("t_max_sold", 0)} {und_fuerza}{und_distancia}  *


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante del metal base 1 (pieza 1):

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del momento torsor máximo permisible en la pieza 1:

        FD pieza = Ssy / τ
            Tperm pieza1 = {dic_diseno_estatica.get("t_max_pieza1", 0)} {und_fuerza}{und_distancia}  **


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante del metal base 2 (pieza 2):

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo del momento torsor máximo permisible en la pieza 2:

        FD pieza = Ssy / τ
            Tperm pieza2 = {dic_diseno_estatica.get("t_max_pieza2", 0)} {und_fuerza}{und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_tperm", 0)}

            """  # Porción con resultados de cálculos de análisis estático.

            informe += resultados_rediseno

            resumen_estatica = f"""
            <body>

            <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
            <hr>

            <p><strong>Carga permisible en la soldadura:</strong></p>

            <p style="margin-left: 20px; color: blue;">Tperm sold = {dic_diseno_estatica.get("t_max_sold")} {und_fuerza}{und_distancia}</p>

            <p><strong>Carga permisible en la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: blue;">Tperm pieza1 = {dic_diseno_estatica.get("t_max_pieza1")} {und_fuerza}{und_distancia}</p>

            <p><strong>Carga permisible en la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: blue;">Tperm pieza2 = {dic_diseno_estatica.get("t_max_pieza2")} {und_fuerza}{und_distancia}</p>

            <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_tperm")} </strong></p>

            </body>
            """  # Resumen de resultados del rediseño por carga estática.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

    return informe, resumen


def informe_diseno_carga_ranura_cc(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica,
                                   sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1, acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de cálculo de diseño para carga permisible de
    soldadura de ranura sometida a carga combinada debido a una fuerza excéntrica"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Carga Permisible para Soldadura de Ranura Sometida a Carga Combinada debido a una Fuerza Externa {tipo_carga.capitalize()} Excéntrica al Centroide {"*" * 5}
    \nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
            """  # Encabezado del informe

    informe += f"""
    El presente informe muestra los resultados de los cálculos para el diseño de la carga permisible de soldadura de ranura sometida a carga combinada debido a una fuerza externa {tipo_carga} excéntrica al centroide. El objetivo es determinar la magnitud de la carga máxima permisible en la junta soldada, garantizando el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\n"""  # Introducción

    resumen = ""

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_diseno_estatica.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_diseno_estatica.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_diseno_estatica.get("tipo_union", 0)}

    Carga Aplicada:

        Tipo: Estática
        Fuerza: ** A determinar **
        Brazo longitudinal (bl) = {dic_diseno_estatica.get("bl", 0)} {und_distancia}
        Brazo transversal (bt) = {dic_diseno_estatica.get("bt", 0)} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Distancia del eje nuetro hasta la soldadura (c):

        c = {dic_diseno_estatica["c_ecuacion"]}
            c = {dic_diseno_estatica["c"]} {und_distancia}

    Distancia en X desde el centroide hasta el punto crítico:

        rx = {dic_diseno_estatica["rx_ecuacion"]}
            rx = {dic_diseno_estatica["rx"]} {und_distancia}

    Distancia en Y desde el centroide hasta el punto crítico:

        ry = {dic_diseno_estatica["ry_ecuacion"]}
            ry = {dic_diseno_estatica["ry"]} {und_distancia}

    Momento de Inercia (I):

        I = {dic_diseno_estatica["i_sold_ecuacion"]}
            I = {dic_diseno_estatica["i_sold"]} {und_distancia}^4

    Momento de Inercia Polar (J):

        J = {dic_diseno_estatica["j_sold_ecuacion"]}
            J = {dic_diseno_estatica["j_sold"]} {und_distancia}^4

    Área de la soldadura:

        A sold = {dic_diseno_estatica["area_sold_ecuacion"]}
            A sold = {dic_diseno_estatica.get("area_sold", 0)} {und_distancia}²

    Cálculo del momento flector producido por la fuerza externa:

        M = F * bl
            M = {dic_diseno_estatica.get("momento_flector", 0)}

    Cálculo del momento torsor producido por la fuerza externa:

        T = F * bt
            T = {dic_diseno_estatica.get("momento_torsor", 0)}

    Esfuerzos aplicados en la junta:

        Cálculo del esfuerzo cortante primario:

            τ' = F / Asold
                τ' = {dic_diseno_estatica.get("tao_primario", 0)}

        Cálculo del esfuerzo cortante secundario en el eje X y en el eje Y:

            τ''x = T * ry / J
                τ''x = {dic_diseno_estatica.get("tao_secundario_x", 0)}

            τ''y = T * rx / J
                τ''y = {dic_diseno_estatica.get("tao_secundario_y", 0)}

        Cálculo de la componente en el eje X del esfuerzo cortante resultante:

            τx = τ''x
                τx = {dic_diseno_estatica.get("tao_x", 0)}

        Cálculo de la componente en el eje Y del esfuerzo cortante resultante:

            τy = τ' + τ''y
                τy = {dic_diseno_estatica.get("tao_y", 0)}

        Cálculo del esfuerzo cortante resultante:

            τ = sqrt((τx)^2 + (τy)^2)
                τ = {dic_diseno_estatica.get("tao", 0)}

        Cálculo del esfuerzo normal:

            σ = M * c / I
                σ = {dic_diseno_estatica.get("sigma", 0)}

        Cálculo del esfuerzo de Von Misses:

            σ' = sqrt(σ^2 + 3 * τ^2)
                σ' = {dic_diseno_estatica.get("sigma_von_misses", 0)}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = Sy / σ'
            Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}  *


Para la pieza 1:

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Sy / σ'
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}  **


Para la pieza 2:

    Resistencia a la fluencia::

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Sy / σ'
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados del diseño por carga estática.

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): {dic_diseno_fatiga.get("garganta", 0)} {und_distancia}
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}
        Radio Exterior (r) : {dic_diseno_fatiga.get("r_ext", 0)} {und_distancia}

    Tipo de union: {dic_diseno_fatiga.get("tipo_union", 0)}

    Cargas Aplicadas:

        Tipo: Cíclica
        Relación de carga (Fmax/Fmin) = {dic_diseno_fatiga.get("relacion_cargas", 0)}

"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la fuerza mínima aplicada, según la relación de fuerzas Fmax/Fmin **

    Distancia del eje nuetro hasta la soldadura (c):

        c = {dic_diseno_fatiga["c_ecuacion"]}
            c = {dic_diseno_fatiga["c"]} {und_distancia}

    Distancia en X desde el centroide hasta el punto crítico:

        rx = {dic_diseno_fatiga["rx_ecuacion"]}
            rx = {dic_diseno_fatiga["rx"]} {und_distancia}

    Distancia en Y desde el centroide hasta el punto crítico:

        ry = {dic_diseno_fatiga["ry_ecuacion"]}
            ry = {dic_diseno_fatiga["ry"]} {und_distancia}

    Momento de Inercia (I):

        I = {dic_diseno_fatiga["i_sold_ecuacion"]}
            I = {dic_diseno_fatiga["i_sold"]} {und_distancia}^4

    Momento de Inercia Polar (J):

        J = {dic_diseno_fatiga["j_sold_ecuacion"]}
            J = {dic_diseno_fatiga["j_sold"]} {und_distancia}^4

    Área de la soldadura:

        A sold = {dic_diseno_fatiga["area_sold_ecuacion"]}
            A sold = {dic_diseno_fatiga.get("area_sold", 0)} {und_distancia}²

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)}

    Cálculo de momento flector alternante y medio:

        Momento flector alternante (Ma) = Fa * bl
            Ma = {dic_diseno_fatiga.get("momento_flector_alt", 0)}

        Momento flector medio (Mm) = Fm * bl
            Mm = {dic_diseno_fatiga.get("momento_flector_med", 0)}

    Cálculo de momento torsor alternante y medio:

        Momento torsor alternante (Ta) = Fm * bt
            Ta = {dic_diseno_fatiga.get("momento_torsor_alt", 0)}

        Momento torsor medio (Tm) = Fm * bt
            Tm = {dic_diseno_fatiga.get("momento_torsor_med", 0)}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión: {dic_diseno_fatiga.get("tipo_union", 0)}, sometida a carga combinada, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}

    Esfuerzos aplicados en la junta:

        Cálculo del esfuerzo cortante primario alternante y medio:

            τ'a = Kfs * Fa / Asold
                τ'a = {dic_diseno_fatiga.get("tao_primario_alt", 0)}

            τ'm = Fm / Asold
                τ'm = {dic_diseno_fatiga.get("tao_primario_med", 0)}

        Cálculo del esfuerzo cortante secundario alternante en el eje X y en el eje Y:

            τ''a x = Kfs * Ta * ry / J
                τ''a x = {dic_diseno_fatiga.get("tao_secundario_alt_x", 0)}

            τ''a y = Kfs * Ta * rx / J
                τ''a y = {dic_diseno_fatiga.get("tao_secundario_alt_y", 0)}

        Cálculo del esfuerzo cortante secundario medio en el eje X y en el eje Y:

            τ''m x = Tm * ry / J
                τ''m x = {dic_diseno_fatiga.get("tao_secundario_med_x", 0)}

            τ''m y = Tm * rx / J
                τ''m y = {dic_diseno_fatiga.get("tao_secundario_med_y", 0)}

        Cálculo de las componentes X e Y del esfuerzo cortante alternante:

            τa x = τ''a x
                τa x = {dic_diseno_fatiga.get("tao_alt_x", 0)}

            τa y = τ'a + τ''a y
                τa y = {dic_diseno_fatiga.get("tao_alt_y", 0)}

        Cálculo de las componentes X e Y del esfuerzo cortante medio:

            τm x = τ''m x
                τm x = {dic_diseno_fatiga.get("tao_med_x", 0)}

            τm y = τ'm + τ''m y
                τm y = {dic_diseno_fatiga.get("tao_med_y", 0)}

        Cálculo del esfuerzo cortante alternante y medio resultante:

            τa = sqrt((τa x)^2 + (τa y)^2)
                τa = {dic_diseno_fatiga.get("tao_alt", 0)}

            τm = sqrt((τm x)^2 + (τm y)^2)
                τm = {dic_diseno_fatiga.get("tao_med", 0)}

        Cálculo del esfuerzo normal alternante y medio:

            σa = Kfs * Ma * c / I
                σa = {dic_diseno_fatiga.get("sigma_alt", 0)}

            σm = Mm * c / I
                σm = {dic_diseno_fatiga.get("sigma_med", 0)}

        Cálculo del esfuerzo de Von Misses alternante y medio:

            σ'a = sqrt((σa)^2 + 3 * (τa)^2)
                σ'a = {dic_diseno_fatiga.get("sigma_von_misses_alt", 0)}

            σ'm = sqrt((σm)^2 + 3 * (τm)^2)
                σ'm = {dic_diseno_fatiga.get("sigma_von_misses_med", 0)}

Para la soldadura:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_sold", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la soldadura utilizando ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            F sold = {dic_diseno_fatiga.get("f_sold", 0)} {und_fuerza} *


Para la pieza 1:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 1 utilizando ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            F pieza1 = {dic_diseno_fatiga.get("f_pieza1", 0)} {und_fuerza} **

Para la pieza 2:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo de F = Fmin de la pieza 2 utilizando la ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            F pieza2 = {dic_diseno_fatiga.get("f_pieza2", 0)} {und_fuerza} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se selecciona la menor de las fuerzas calculadas (*, **, ***) y se multiplica por la relación de carga para determinar la fuerza máxima permisible de la junta.

Fperm = Relación * Fmin  = {dic_diseno_fatiga.get("relacion_cargas")} * {dic_diseno_fatiga.get("f_min")} {und_fuerza}

Por lo que, {dic_diseno_fatiga.get("conclusion_fperm")}.


Diseño por fatiga de la carga permisible completado.


"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Carga permisible en la soldadura:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm sold = {"{:.2f}".format(dic_diseno_fatiga.get("f_sold") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza1") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p><strong>Carga permisible en la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {"{:.2f}".format(dic_diseno_fatiga.get("f_pieza2") * dic_diseno_fatiga.get("relacion_cargas"))} {und_fuerza}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_fperm")} </strong></p>

        </body>
        """  # Resumen de resultados del diseño por fatiga

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

        else:

            informe += verificacion_estatica

            informe += f"Al presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno = f"""

Cálculos realizados

    Cálculo del momento flector producido por la fuerza externa:

        M = F * bl
            M = {dic_diseno_estatica.get("momento_flector", 0)}

    Cálculo del momento torsor producido por la fuerza externa:

        T = F * bt
            T = {dic_diseno_estatica.get("momento_torsor", 0)}

    Esfuerzos aplicados en la junta:

        Cálculo del esfuerzo cortante primario:

            τ' = F / Asold
                τ' = {dic_diseno_estatica.get("tao_primario", 0)}

        Cálculo del esfuerzo cortante secundario en el eje X y en el eje Y:

            τ''x = T * ry / J
                τ''x = {dic_diseno_estatica.get("tao_secundario_x", 0)}

            τ''y = T * rx / J
                τ''y = {dic_diseno_estatica.get("tao_secundario_y", 0)}

        Cálculo de la componente en el eje X del esfuerzo cortante resultante:

            τx = τ''x
                τx = {dic_diseno_estatica.get("tao_x", 0)}

        Cálculo de la componente en el eje Y del esfuerzo cortante resultante:

            τy = τ' + τ''y
                τy = {dic_diseno_estatica.get("tao_y", 0)}

        Cálculo del esfuerzo cortante resultante:

            τ = sqrt((τx)^2 + (τy)^2)
                τ = {dic_diseno_estatica.get("tao", 0)}

        Cálculo del esfuerzo normal:

            σ = M * c / I
                σ = {dic_diseno_estatica.get("sigma", 0)}

        Cálculo del esfuerzo de Von Misses:

            σ' = sqrt(σ^2 + 3 * τ^2)
                σ' = {dic_diseno_estatica.get("sigma_von_misses", 0)}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la soldadura:

        FD sold = Sy / σ'
            Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}  *


Para la pieza 1:

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 1:

        FD pieza = Sy / σ'
            Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}  **


Para la pieza 2:

    Resistencia a la fluencia::

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo de la carga máxima permisible de la pieza 2:

        FD pieza = Sy / σ'
            Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2", 0)} {und_fuerza}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre las tres cargas calculadas (*, **, ***), la menor de ellas.

Por consiguiente: {dic_diseno_estatica.get("conclusion_fperm", 0)}

            """  # Porción con resultados de cálculos de análisis estático.

            informe += resultados_rediseno

            resumen_estatica = f"""
            <body>

            <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
            <hr>

            <p><strong>Carga permisible en la soldadura:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm sold = {dic_diseno_estatica.get("f_max_sold")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 1:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza1 = {dic_diseno_estatica.get("f_max_pieza1")} {und_fuerza}</p>

            <p><strong>Carga permisible en la pieza 2:</strong></p>

            <p style="margin-left: 20px; color: blue;">Fperm pieza2 = {dic_diseno_estatica.get("f_max_pieza2")} {und_fuerza}</p>

            <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_fperm")} </strong></p>

            </body>
            """  # Resumen de resultados del rediseño por estática.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

    return informe, resumen

# Espesor del cordón


def informe_diseno_espesor_ranura_cp(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion,
                                     dic_diseno_estatica, sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1,
                                     acero2, electrodo):

    """Esta función le dará forma al informe y resumen de resultados de cálculo de diseño del espesor mínimo de
    soldadura de ranura sometida a carga paralela"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Tamaño de Garganta o Espesor Mínimo del Cordón para Soldadura de Ranura Sometida a Carga Paralela {tipo_carga.capitalize()} {"*" * 5}
    \nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
            """  # Encabezado del informe

    informe += f"""
El presente informe muestra los resultados de los cálculos para el diseño del espesor mínimo (tamaño de la garganta) del cordón para soldadura de ranura sometida a carga paralela {tipo_carga}. El objetivo del diseño es determinar el espesor mínimo necesario del cordón de soldadura para garantizar el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\nEs importante acotar que se considera la soldadura de ranura de penetración completa, por lo tanto, el espesor del cordón es igual al de las piezas a soldar, o en su defecto, al espesor menor entre las piezas.\n\n""" # Introducción

    resumen = ""

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): ** A determinar **
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}

    Tipo de union: Tope

    Carga Aplicada:

        Tipo: Estática
        Fuerza: {dic_diseno_estatica.get("Fmax", 0)} {und_fuerza}
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Área de la soldadura:

        A sold = {dic_diseno_estatica["area_sold_ecuacion"]}
            A sold = {dic_diseno_estatica.get("area_sold", 0)}

    Cálculo del esfuerzo cortante aplicado en la junta:

        τ = F / Asold
            τ = {dic_diseno_estatica.get("tao", 0)}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo necesario del cordón para soldadura:

        FD sold = τ adm / τ
            t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}  *


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo necesario del cordón para la pieza 1:

        FD pieza = Ssy / τ
            t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}  **


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo necesario del cordón para la pieza 2:

        FD pieza = Ssy / τ
            t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de garganta calculados (*, **, ***), el mayor de ellos.

Por consiguiente: {dic_diseno_estatica.get("conclusion_tmin", 0)}

"""  # Porción con resultados de cálculos del diseño por carga estática.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen = f"""
<body>

<h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
<hr>

<p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
<p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}</p>

<p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
<p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}</p>

<p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
<p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}</p>

<p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_tmin")}</strong></p>

</body>
    """  # Resumen de resultados del diseño por carga estática.

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): ** A determinar **
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}

    Tipo de union: Tope

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima (Fmax) = {dic_diseno_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima (Fmin) = {dic_diseno_fatiga.get("Fmin", 0)} {und_fuerza}\n
"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la garganta o espesor del cordón de soldadura **

    Área de la soldadura:

        A sold = {dic_diseno_fatiga["area_sold_ecuacion"]}
            A sold = {dic_diseno_fatiga.get("area_sold", 0)}

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)} {und_fuerza}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión tope sometida a carga paralela, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_alt", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_med", 0)}


Para la soldadura:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo necesario del cordón para soldadura utilizando la ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            t sold = {dic_diseno_fatiga.get("t_sold", 0)} {und_distancia} *


Para la pieza 1:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo necesario del cordón para la pieza 1 utilizando la ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            t pieza1 = {dic_diseno_fatiga.get("t_pieza1", 0)} {und_distancia} **


Para la pieza 2:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza2", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2 utilizando la ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            t pieza2 = {dic_diseno_fatiga.get("t_pieza2", 0)} {und_distancia} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se debe seleccionar entre los tres tamaños de garganta o espesor del cordón calculados (*, **, ***) el mayor de ellos.

Por lo que, {dic_diseno_fatiga.get("conclusion_tmin")}.


Diseño por fatiga de la garganta o espesor del cordón de la soldadura completado.

"""  # Resultados del diseño por carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_fatiga.get("t_sold")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_fatiga.get("t_pieza1")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_fatiga.get("t_pieza2")} {und_distancia}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_tmin")}</strong></p>

        </body>
            """  # Resumen de resultados del diseño por carga de fatiga.

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

        else:

            informe += verificacion_estatica

            informe += f"Al presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno = f"""

Cálculos realizados

    Cálculo del esfuerzo cortante aplicado en la junta:

        τ = F / Asold
            τ = {dic_diseno_estatica.get("tao", 0)}


Para la soldadura:

    Cálculo del esfuerzo cortante admisible del material de aporte:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la soldadura:

        FD sold = τ adm / τ
            t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}  *


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 1:

        FD pieza = Ssy / τ
            t pieza1 = {dic_diseno_estatica.get("t_max_pieza1")} {und_distancia}  **


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante:

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2:

        FD pieza = Ssy / τ
            t pieza2 = {dic_diseno_estatica.get("t_max_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se debe seleccionar entre los tres tamaños de garganta o espesor del cordón calculados (*, **, ***) el mayor de ellos.

Por consiguiente: {dic_diseno_estatica.get("conclusion_tmin", 0)}

            """  # Porción con resultados de cálculos del rediseño por carga estática.

            informe += resultados_rediseno

            resumen_estatica = f"""
<body>

<h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
<hr>

<p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
<p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}</p>

<p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
<p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}</p>

<p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
<p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}</p>

<p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_tmin")}</strong></p>

</body>
    """  # Resumen de resultados del rediseño por carga estática.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

    return informe, resumen


def informe_diseno_espesor_ranura_ct(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion,
                                     dic_diseno_estatica, sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1,
                                     acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de cálculo de diseño del espesor del cordón de
    soldadura de ranura sometida a carga transversal"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Tamaño de Garganta o Espesor Mínimo del cordón para Soldadura de Ranura Sometida a Carga Transversal {tipo_carga.capitalize()} {"*" * 5}
    \nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
            """  # Encabezado del informe

    informe += f"""
El presente informe muestra los resultados de los cálculos para el diseño del espesor mínimo (tamaño de la garganta) del cordón para soldadura de ranura sometida a carga transversal {tipo_carga}. El objetivo del diseño es determinar el espesor mínimo necesario del cordón de soldadura para garantizar el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\nEs importante acotar que se considera la soldadura de ranura de penetración completa, por lo tanto, el espesor del cordón es igual al de las piezas a soldar, o en su defecto, al espesor menor entre las piezas.\n\n""" # Introducción

    resumen = ""

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): ** A determinar **
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}

    Tipo de union: {dic_diseno_estatica.get("tipo_union", 0)}

    Carga Aplicada:

        Tipo: Estática
        Fuerza: {dic_diseno_estatica.get("Fmax", 0)} {und_fuerza}
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Área de la soldadura:

        A sold = {dic_diseno_estatica["area_sold_ecuacion"]}
            A sold = {dic_diseno_estatica.get("area_sold", 0)}

    Cálculo del esfuerzo normal aplicado en la junta:

        σ = F / Asold
            σ = {dic_diseno_estatica.get("sigma", 0)}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para soldadura:

        FD sold = Sy / σ
            t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}  *


Para la pieza 1:

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 1:

        FD pieza = Sy / σ
            t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}  **


Para la pieza 2:

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2:

        FD pieza = Sy / σ
            t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de garganta calculados (*, **, ***), el mayor de ellos.

Por consiguiente: {dic_diseno_estatica.get("conclusion_tmin", 0)}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_tmin")}</strong></p>

        </body>
            """  # Resumen de resultados de análisis estático.

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): ** A determinar **
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}

    Tipo de union: {dic_diseno_fatiga.get("tipo_union", 0)}

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima (Fmax) = {dic_diseno_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima (Fmin) = {dic_diseno_fatiga.get("Fmin", 0)} {und_fuerza}\n\n
"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la garganta o espesor del cordón de soldadura **

    Área de la soldadura:

        A sold = {dic_diseno_fatiga["area_sold_ecuacion"]}
            A sold = {dic_diseno_fatiga.get("area_sold", 0)}

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)} {und_fuerza}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión: {dic_diseno_fatiga.get("tipo_union", 0)}, sometida a carga transversal, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}

    Cálculo de esfuerzo normal alternantes y medio:

        σa = Kfs * Fa / Asold
            σa = {dic_diseno_fatiga.get("sigma_alt", 0)}

        σm = Fm / Asold
            σm = {dic_diseno_fatiga.get("sigma_med", 0)}


Para la soldadura:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_sold", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para soldadura utilizando la ecuación de Gerber:

        (FD * σa)/Se + ((FD * σm)/Sut)^2 = 1
            t sold = {dic_diseno_fatiga.get("t_sold", 0)} {und_distancia} *


Para la pieza 1:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 1 utilizando la ecuación de Gerber:

        (FD * σa)/Se + ((FD * σm)/Sut)^2 = 1
            t pieza1 = {dic_diseno_fatiga.get("t_pieza1", 0)} {und_distancia} **


Para la pieza 2:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2 utilizando la ecuación de Gerber:

        (FD * σa)/Se + ((FD * σm)/Sut)^2 = 1
            t pieza2 = {dic_diseno_fatiga.get("t_pieza2", 0)} {und_distancia} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se debe seleccionar entre los tres tamaños de garganta o espesor del cordón calculados (*, **, ***) el mayor de ellos.

Por lo que, {dic_diseno_fatiga.get("conclusion_tmin")}.


Diseño por fatiga de la garganta o espesor del cordón de la soldadura completado.

"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_fatiga.get("t_sold")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_fatiga.get("t_pieza1")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_fatiga.get("t_pieza2")} {und_distancia}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_tmin")}</strong></p>

        </body>
            """  # Resumen de resultados de análisis estático.

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

        else:

            informe += verificacion_estatica

            informe += f"Al presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno = f"""

Cálculos realizados

    Cálculo del esfuerzo normal aplicado en la junta:

        σ = F / Asold
            σ = {dic_diseno_estatica.get("sigma", 0)}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la soldadura:

        FD sold = Sy / σ
            t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}  *


Para la pieza 1:

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 1:

        FD pieza = Sy / σ
            t pieza1 = {dic_diseno_estatica.get("t_max_pieza1")} {und_distancia}  **


Para la pieza 2:

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2:

        FD pieza = Sy / σ
            t pieza2 = {dic_diseno_estatica.get("t_max_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se debe seleccionar entre los tres tamaños de garganta o espesor del cordón calculados (*, **, ***) el mayor de ellos.

Por consiguiente: {dic_diseno_estatica.get("conclusion_tmin", 0)}

            """  # Porción con resultados de cálculos de análisis estático.

            informe += resultados_rediseno

            resumen_estatica = f"""
            <body>

            <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
            <hr>

            <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
            <p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}</p>

            <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
            <p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}</p>

            <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
            <p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}</p>

            <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_tmin")}</strong></p>

            </body>
                """  # Resumen de resultados de análisis estático.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

    return informe, resumen


def informe_diseno_espesor_ranura_cf(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion,
                                     dic_diseno_estatica, sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1,
                                     acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de cálculo de diseño del espesor del cordón de
    soldadura de ranura sometida a carga de flexión debido a una fuerza externa a la soldadura"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Tamaño de Garganta o Espesor Mínimo del cordón para Soldadura de Ranura Sometida a Carga de Flexión debido a una Fuerza Externa {tipo_carga.capitalize()}{"*" * 5}
    \nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
            """  # Encabezado del informe

    informe += f"""
El presente informe muestra los resultados de los cálculos para el diseño del espesor mínimo (tamaño de la garganta) del cordón para soldadura de ranura sometida a carga de flexión debido a una fuerza externa {tipo_carga}. El objetivo del diseño es determinar el espesor mínimo necesario del cordón de soldadura para garantizar el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\n Es importante acotar que se considera la soldadura de ranura de penetración completa, por lo tanto, el espesor del cordón es igual al de las piezas a soldar, o en su defecto, al espesor menor entre las piezas.\n\n""" # Introducción

    resumen = ""

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): ** A determinar **
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}

    Tipo de union: {dic_diseno_estatica.get("tipo_union", 0)}

    Carga Aplicada:

        Tipo: Estática
        Fuerza: {dic_diseno_estatica.get("Fmax", 0)} {und_fuerza}
        Brazo (b) = {dic_diseno_estatica["b"]} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Distancia del eje nuetro hasta la soldadura (c):

        c = {dic_diseno_estatica["c_ecuacion"]}
            c = {dic_diseno_estatica.get("c", 0)} {und_distancia if isinstance(dic_diseno_estatica.get("c"), (int, float)) else ""}

    Momento de Inercia (I):

        I = {dic_diseno_estatica["i_sold_ecuacion"]}
            I = {dic_diseno_estatica.get("i_sold", 0)}

    Área de la soldadura:

        A sold = {dic_diseno_estatica["area_sold_ecuacion"]}
            A sold = {dic_diseno_estatica.get("area_sold", 0)}

    Cálculo del momento flector producido por la fuerza externa:

        M = F * b
            M = {dic_diseno_estatica.get("momento_flector", 0)} {und_fuerza}{und_distancia}

    Esfuerzos aplicados en la junta:

        Cálculo del esfuerzo normal:

            σ = M * c / I
                σ = {dic_diseno_estatica.get("sigma", 0)}

        Cálculo del esfuerzo cortante:

            τ = F / Asold
                τ = {dic_diseno_estatica.get("tao", 0)}

        Cálculo del esfuerzo de Von Misses:

            σ' = sqrt(σ^2 + 3 * τ^2)
                σ' = {dic_diseno_estatica.get("sigma_von_misses", 0)}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para soldadura:

        FD sold = Sy / σ'
            t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}  *


Para la pieza 1:

    Resistencia a la fluencia del metal base 1 (pieza 1):

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 1:

        FD pieza = Sy / σ'
            t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}  **


Para la pieza 2:

    Resistencia a la fluencia del metal base base 2 (pieza 2):

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2:

        FD pieza = Sy / σ'
            t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de garganta calculados (*, **, ***), el mayor de ellos.

Por consiguiente: {dic_diseno_estatica.get("conclusion_tmin", 0)}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_tmin")}</strong></p>

        </body>
            """  # Resumen de resultados de análisis estático.

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): ** A determinar **
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}

    Tipo de union: {dic_diseno_fatiga.get("tipo_union", 0)}

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima (Fmax) = {dic_diseno_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima (Fmin) = {dic_diseno_fatiga.get("Fmin", 0)} {und_fuerza}
        Brazo (b) = {dic_diseno_fatiga["b"]} {und_distancia}\n\n
"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la garganta o espesor del cordón de soldadura **

    Distancia del eje nuetro hasta la soldadura (c):

        c = {dic_diseno_fatiga["c_ecuacion"]}
            c = {dic_diseno_fatiga.get("c", 0)} {und_distancia if isinstance(dic_diseno_fatiga.get("c"), (int, float)) else ""}

    Momento de Inercia (I):

        I = {dic_diseno_fatiga["i_sold_ecuacion"]}
            I = {dic_diseno_fatiga.get("i_sold", 0)}

    Área de la soldadura:

        A sold = {dic_diseno_fatiga["area_sold_ecuacion"]}
            A sold = {dic_diseno_fatiga.get("area_sold", 0)}

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)} {und_fuerza}

    Cálculo de momento flector alternante y medio:

        Momento flector alternante (Ma) = Fa * b
            Ma = {dic_diseno_fatiga.get("momento_flector_alt", 0)} {und_fuerza}{und_distancia}

        Momento flector medio (Mm) = Fm * b
            Mm = {dic_diseno_fatiga.get("momento_flector_med", 0)} {und_fuerza}{und_distancia}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión: {dic_diseno_fatiga.get("tipo_union", 0)}, sometida a carga de flexión, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}

    Cálculo de esfuerzo normal alternantes y medio:

        σa = Kfs * Ma * c / I
            σa = {dic_diseno_fatiga.get("sigma_alt", 0)}

        σm = Mm * c / I
            σm = {dic_diseno_fatiga.get("sigma_med", 0)}

    Cálculo de esfuerzo cortante alternante y medio:

        τa = Kfs * Fa / Asold
            τa = {dic_diseno_fatiga.get("tao_alt", 0)}

        τm = Fm / Asold
            τm = {dic_diseno_fatiga.get("tao_med", 0)}

    Cálculo de esfuerzos de Von Misses alternante y medio:

        σ'a = sqrt((σa)^2 + 3 * (τa)^2)
            σ'a = {dic_diseno_fatiga.get("sigma_von_misses_alt", 0)}

        σ'm = sqrt((σm)^2 + 3 * (τm)^2)
            σ'm = {dic_diseno_fatiga.get("sigma_von_misses_med", 0)}


Para la soldadura:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_sold", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para soldadura utilizando la ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            t sold = {dic_diseno_fatiga.get("t_sold", 0)} {und_distancia} *


Para la pieza 1:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 1 utilizando la ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            t pieza1 = {dic_diseno_fatiga.get("t_pieza1", 0)} {und_distancia} **


Para la pieza 2:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2 utilizando la ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            t pieza2 = {dic_diseno_fatiga.get("t_pieza2", 0)} {und_distancia} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se debe seleccionar entre los tres tamaños de garganta o espesor del cordón calculados (*, **, ***) el mayor de ellos.

Por lo que, {dic_diseno_fatiga.get("conclusion_tmin")}.


Diseño por fatiga de la garganta o espesor del cordón de la soldadura completado.


"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_fatiga.get("t_sold")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_fatiga.get("t_pieza1")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_fatiga.get("t_pieza2")} {und_distancia}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_tmin")}</strong></p>

        </body>
            """  # Resumen de resultados de análisis estático.

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

        else:

            informe += verificacion_estatica

            informe += f"Al presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno = f"""

Cálculos realizados

    Cálculo del momento flector producido por la fuerza externa:

        M = F * b
            M = {dic_diseno_estatica.get("momento_flector", 0)} {und_fuerza}{und_distancia}

    Esfuerzos aplicados en la junta:

        Cálculo del esfuerzo normal:

            σ = M * c / I
                σ = {dic_diseno_estatica.get("sigma", 0)}

        Cálculo del esfuerzo cortante:

            τ = F / Asold
                τ = {dic_diseno_estatica.get("tao", 0)}

        Cálculo del esfuerzo de Von Misses:

            σ' = sqrt(σ^2 + 3 * τ^2)
                σ' = {dic_diseno_estatica.get("sigma_von_misses", 0)}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la soldadura:

        FD sold = Sy / σ'
            t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}  *


Para la pieza 1:

    Resistencia a la fluencia del metal base 1 (pieza 1):

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 1:

        FD pieza = Sy / σ'
            t pieza1 = {dic_diseno_estatica.get("t_max_pieza1")} {und_distancia}  **


Para la pieza 2:

    Resistencia a la fluencia del metal base base 2 (pieza 2):

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2:

        FD pieza = Sy / σ'
            t pieza2 = {dic_diseno_estatica.get("t_max_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se debe seleccionar entre los tres tamaños de garganta o espesor del cordón calculados (*, **, ***) el mayor de ellos.

Por consiguiente: {dic_diseno_estatica.get("conclusion_tmin", 0)}

            """  # Porción con resultados del rediseño.

            informe += resultados_rediseno

            resumen_estatica = f"""
            <body>

            <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
            <hr>

            <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
            <p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}</p>

            <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
            <p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}</p>

            <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
            <p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}</p>

            <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_tmin")}</strong></p>

            </body>
                """  # Resumen de resultados del rediseño.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

    return informe, resumen


def informe_diseno_espesor_ranura_ctor(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion,
                                       dic_diseno_estatica, sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1,
                                       acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de cálculo de diseño del espesor del cordón de
    soldadura de ranura sometida a carga de torsión pura"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Tamaño de Garganta o Espesor Mínimo del cordón para Soldadura de Ranura Sometida a Carga de Torsión Pura {tipo_carga.capitalize()}  {"*" * 5}
    \nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
            """  # Encabezado del informe

    informe += f"""
El presente informe muestra los resultados de los cálculos para el diseño del espesor mínimo (tamaño de la garganta) del cordón para soldadura de ranura sometida a carga de torsión pura {tipo_carga}. El objetivo del diseño es determinar el espesor mínimo necesario del cordón de soldadura para garantizar el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\nEs importante acotar que se considera la soldadura de ranura de penetración completa, por lo tanto, el espesor del cordón es igual al de las piezas a soldar, o en su defecto, al espesor menor entre las piezas.\n\n""" # Introducción

    resumen = ""

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): ** A determinar **
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}

    Tipo de union: {dic_diseno_estatica.get("tipo_union", 0)}

    Carga Aplicada:

        Tipo: Estática
        Torque: {dic_diseno_estatica.get("Tmax", 0)} {und_fuerza}{und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Distancia desde el centroide hasta el pto crítico de la soldadura (r):

        r = sqrt(({dic_diseno_estatica["rx_ecuacion"]})^2 + ({dic_diseno_estatica["ry_ecuacion"]})^2)
            r = {dic_diseno_estatica["r"]} {und_distancia if isinstance(dic_diseno_estatica.get("r"), (int, float)) else ""}

    Momento de Inercia Polar (J):

        J = {dic_diseno_estatica["j_sold_ecuacion"]}
            J = {dic_diseno_estatica["j_sold"]}

    Área de la soldadura:

        A sold = {dic_diseno_estatica["area_sold_ecuacion"]}
            A sold = {dic_diseno_estatica.get("area_sold", 0)}

    Esfuerzo cortante aplicado en la junta:

        τ = T * r / J
            τ = {dic_diseno_estatica.get("tao", 0)}


Para la soldadura:

    Cálculo de la resistencia cortante admisible:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para soldadura:

        FD sold = τ adm / τ
            t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}  *


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante del metal base 1 (pieza 1):

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 1:

        FD pieza = Ssy / τ
            t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}  **


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante del metal base 2 (pieza 2):

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2:

        FD pieza = Ssy / τ
            t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de garganta calculados (*, **, ***), el mayor de ellos.

Por consiguiente: {dic_diseno_estatica.get("conclusion_tmin", 0)}

"""  # Porción con resultados de cálculos del diseño por carga estática.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_tmin")}</strong></p>

        </body>
            """  # Resumen de resultados del diseño por carga estática.

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): ** A determinar **
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}

    Tipo de union: {dic_diseno_fatiga.get("tipo_union", 0)}

    Cargas Aplicadas:

        Tipo: Cíclica
        Torque máximo = {dic_diseno_fatiga.get("Tmax", 0)} {und_fuerza}{und_distancia}
        Torque mínimo = {dic_diseno_fatiga.get("Tmin", 0)} {und_fuerza}{und_distancia}


"""  # Datos de entrada para carga de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la garganta o espesor del cordón de soldadura **

    Distancia desde el centroide hasta el pto crítico de la soldadura (r):

        r = sqrt(({dic_diseno_fatiga["rx_ecuacion"]})^2 + ({dic_diseno_fatiga["ry_ecuacion"]})^2)
            r = {dic_diseno_fatiga["r"]} {und_distancia if isinstance(dic_diseno_fatiga.get("r"), (int, float)) else ""}

    Momento de Inercia Polar (J):

        J = {dic_diseno_fatiga["j_sold_ecuacion"]}
            J = {dic_diseno_fatiga["j_sold"]}

    Área de la soldadura:

        A sold = {dic_diseno_fatiga["area_sold_ecuacion"]}
            A sold = {dic_diseno_fatiga.get("area_sold", 0)}

    Cálculo de momento torsor (Torque) alternante y medio:

        Momento torsor alternante (Ta) = (Tmax - Tmin) / 2
            Ta = {dic_diseno_fatiga.get("Talt", 0)} {und_fuerza}{und_distancia}

        Momento torsor medio (Tm) = (Tmax + Tmin) / 2
            Tm = {dic_diseno_fatiga.get("Tmed", 0)} {und_fuerza}{und_distancia}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión: {dic_diseno_fatiga["tipo_union"]}, sometida a carga de torsión, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}

    Cálculo de esfuerzos cortantes alternantes y medios:

        τa = Kfs * Ta * r / J
            τa = {dic_diseno_fatiga.get("tao_alt", 0)}

        τm = Tm * r / J
            τm = {dic_diseno_fatiga.get("tao_med", 0)}


Para la soldadura:

    Cálculo de la resistencia a la fatiga:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_sold", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para soldadura utilizando la ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            t sold = {dic_diseno_fatiga.get("t_sold", 0)} {und_distancia} *


Para la pieza 1:

    Cálculo de la resistencia a la fatiga al cortante:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza1", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 1 utilizando la ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            t pieza1 = {dic_diseno_fatiga.get("t_pieza1", 0)} {und_distancia} **


Para la pieza 2:

    Cálculo de la resistencia a la fatiga:

        Sse = ka * kb * kc * kd * ke * Se'
            Sse = {dic_diseno_fatiga.get("sse_pieza2", 0)} {und_esfuerzo}

    Cálculo de la resistencia última al cortante:

        Ssu = 0.67 * Sut
            Ssu = {dic_diseno_fatiga.get("ssu_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2 utilizando la ecuación de Gerber:

        (FD * τa)/Sse + ((FD * τm)/Ssu)^2 = 1
            t pieza2 = {dic_diseno_fatiga.get("t_pieza2", 0)} {und_distancia} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se debe seleccionar entre los tres tamaños de garganta o espesor del cordón calculados (*, **, ***) el mayor de ellos.

Por lo que, {dic_diseno_fatiga.get("conclusion_tmin")}.


Diseño por fatiga de la garganta o espesor del cordón de la soldadura completado.


"""  # Resultados de análisis para carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_fatiga.get("t_sold")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_fatiga.get("t_pieza1")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_fatiga.get("t_pieza2")} {und_distancia}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_tmin")}</strong></p>

        </body>
            """  # Resumen de resultados del diseño por carga de fatiga.

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

        else:
            informe += verificacion_estatica

            informe += f"Al presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno = f"""

Cálculos realizados

    Esfuerzo cortante aplicado en la junta:

        τ = T * r / J
            τ = {dic_diseno_estatica.get("tao", 0)}


Para la soldadura:

    Cálculo de la resistencia cortante admisible:

        τ adm = 0.30 * Sut
            τ adm = {dic_diseno_estatica.get("tao_adm_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la soldadura:

        FD sold = τ adm / τ
            t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}  *


Para la pieza 1:

    Cálculo de la resistencia a la fluencia al cortante del metal base 1 (pieza 1):

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 1:

        FD pieza = Ssy / τ
            t pieza1 = {dic_diseno_estatica.get("t_max_pieza1")} {und_distancia}  **


Para la pieza 2:

    Cálculo de la resistencia a la fluencia al cortante del metal base 2 (pieza 2):

        Ssy = 0.577 * Sy
            Ssy = {dic_diseno_estatica.get("ssy_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2:

        FD pieza = Ssy / τ
            t pieza2 = {dic_diseno_estatica.get("t_max_pieza2", 0)} {und_fuerza}{und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se debe seleccionar entre los tres tamaños de garganta o espesor del cordón calculados (*, **, ***) el mayor de ellos.

Por consiguiente: {dic_diseno_estatica.get("conclusion_tmin", 0)}

            """  # Porción con resultados de cálculos de análisis estático.

            informe += resultados_rediseno

            resumen_estatica = f"""
            <body>

            <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
            <hr>

            <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
            <p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}</p>

            <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
            <p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}</p>

            <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
            <p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}</p>

            <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_tmin")}</strong></p>

            </body>
                """  # Resumen de resultados del rediseño por carga estática.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

    return informe, resumen


def informe_diseno_espesor_ranura_cc(nombre_proyecto, tipo_carga, dic_diseno_fatiga, dic_comprobacion,
                                     dic_diseno_estatica, sist_und, und_fuerza, und_distancia, und_esfuerzo, acero1,
                                     acero2, electrodo):
    """Esta función le dará forma al informe y resumen de resultados de cálculo de diseño del espesor del cordón de
    soldadura de ranura sometida a carga combinada debido a una fuerza excéntrica"""

    informe = f"""
{"*" * 5} Informe de Resultados de Diseño de Tamaño de Garganta o Espesor Mínimo del cordón para Soldadura de Ranura Sometida a Carga Combinada debido a una Fuerza Externa {tipo_carga.capitalize()} Excéntrica al Centroide {"*" * 5}
    \nFecha: {fecha}\nNombre del proyecto: {nombre_proyecto}\n
            """  # Encabezado del informe

    informe += f"""
El presente informe muestra los resultados de los cálculos para el diseño del espesor mínimo (tamaño de la garganta) del cordón para soldadura de ranura sometida a carga combinada debido a una fuerza externa {tipo_carga} excéntrica al centroide. El objetivo del diseño es determinar el espesor mínimo necesario del cordón de soldadura para garantizar el cumplimiento de los requisitos mínimos de seguridad y funcionamiento (FD sold = 3.33, FD pieza = 2.5), de acuerdo a la cátedra EMI.\n\nEs importante acotar que se considera la soldadura de ranura de penetración completa, por lo tanto, el espesor del cordón es igual al de las piezas a soldar, o en su defecto, al espesor menor entre las piezas.\n\n"""  # Introducción

    resumen = ""

    # Generación de informe para carga estática
    if tipo_carga == "estática":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_estatica.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): ** A determinar **
        Largo (l) : {dic_diseno_estatica.get("largo", 0)} {und_distancia}

    Tipo de union: {dic_diseno_estatica.get("tipo_union", 0)}

    Carga Aplicada:

        Tipo: Estática
        Fuerza: {dic_diseno_estatica.get("Fmax", 0)} {und_fuerza}
        Brazo longitudinal (bl) = {dic_diseno_estatica.get("bl", 0)} {und_distancia}
        Brazo transversal (bt) = {dic_diseno_estatica.get("bt", 0)} {und_distancia}\n\n
"""  # Datos de entrada para carga estática

        resultados_estatica = f"""
Se procede a diseñar por carga estática la junta soldada.

Cálculos realizados

    Distancia del eje nuetro hasta la soldadura (c):

        c = {dic_diseno_estatica["c_ecuacion"]}
            c = {dic_diseno_estatica["c"]} {und_distancia if isinstance(dic_diseno_estatica.get("c"), (int, float)) else ""}

    Distancia en X desde el centroide hasta el punto crítico:

        rx = {dic_diseno_estatica["rx_ecuacion"]}
            rx = {dic_diseno_estatica["rx"]} {und_distancia if isinstance(dic_diseno_estatica.get("rx"), (int, float)) else ""}

    Distancia en Y desde el centroide hasta el punto crítico:

        ry = {dic_diseno_estatica["ry_ecuacion"]}
            ry = {dic_diseno_estatica["ry"]} {und_distancia if isinstance(dic_diseno_estatica.get("ry"), (int, float)) else ""}

    Momento de Inercia (I):

        I = {dic_diseno_estatica["i_sold_ecuacion"]}
            I = {dic_diseno_estatica["i_sold"]}

    Momento de Inercia Polar (J):

        J = {dic_diseno_estatica["j_sold_ecuacion"]}
            J = {dic_diseno_estatica["j_sold"]}

    Área de la soldadura:

        A sold = {dic_diseno_estatica["area_sold_ecuacion"]}
            A sold = {dic_diseno_estatica.get("area_sold", 0)}

    Cálculo del momento flector producido por la fuerza externa:

        M = F * bl
            M = {dic_diseno_estatica.get("momento_flector", 0)} {und_fuerza}{und_distancia}

    Cálculo del momento torsor producido por la fuerza externa:

        T = F * bt
            T = {dic_diseno_estatica.get("momento_torsor", 0)} {und_fuerza}{und_distancia}

    Esfuerzos aplicados en la junta:

        Cálculo del esfuerzo cortante primario:

            τ' = F / Asold
                τ' = {dic_diseno_estatica.get("tao_primario", 0)}

        Cálculo del esfuerzo cortante secundario en el eje X y en el eje Y:

            τ''x = T * ry / J
                τ''x = {round(float(dic_diseno_estatica.get("tao_secundario_x")), 2) if isinstance(dic_diseno_estatica.get("tao_secundario_x"), (Float, Integer, Rational)) else dic_diseno_estatica.get("tao_secundario_x")} {und_esfuerzo if isinstance(dic_diseno_estatica.get("tao_secundario_x"), (Float, Integer, Rational)) else ""}

            τ''y = T * rx / J
                τ''y = {round(dic_diseno_estatica.get("tao_secundario_y"), 2) if isinstance(dic_diseno_estatica.get("tao_secundario_y"), (Float, Integer, Rational)) else dic_diseno_estatica.get("tao_secundario_y")} {und_esfuerzo if isinstance(dic_diseno_estatica.get("tao_secundario_y"), (Float, Integer, Rational)) else ""}

        Cálculo de la componente en el eje X del esfuerzo cortante resultante:

            τx = τ''x
                τx = {round(float(dic_diseno_estatica.get("tao_x")), 2) if isinstance(dic_diseno_estatica.get("tao_x"), (Float, Integer, Rational)) else dic_diseno_estatica.get("tao_x")} {und_esfuerzo if isinstance(dic_diseno_estatica.get("tao_x"), (Float, Integer, Rational)) else ""}

        Cálculo de la componente en el eje Y del esfuerzo cortante resultante:

            τy = τ' + τ''y
                τy = {dic_diseno_estatica.get("tao_y", 0)}

        Cálculo del esfuerzo cortante resultante:

            τ = sqrt((τx)^2 + (τy)^2)
                τ = {dic_diseno_estatica.get("tao", 0)}

        Cálculo del esfuerzo normal:

            σ = M * c / I
                σ = {dic_diseno_estatica.get("sigma", 0)}

        Cálculo del esfuerzo de Von Misses:

            σ' = sqrt(σ^2 + 3 * τ^2)
                σ' = {dic_diseno_estatica.get("sigma_von_misses", 0)}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para soldadura:

        FD sold = Sy / σ'
            t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}  *


Para la pieza 1:

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 1:

        FD pieza = Sy / σ'
            t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}  **


Para la pieza 2:

    Resistencia a la fluencia::

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2:

        FD pieza = Sy / σ'
            t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad en la junta soldada (soldadura y piezas), se debe seleccionar entre los tres tamaños de garganta calculados (*, **, ***), el mayor de ellos.

Por consiguiente: {dic_diseno_estatica.get("conclusion_tmin", 0)}

"""  # Porción con resultados de cálculos de análisis estático.

        informe += resultados_estatica

        informe += "Diseño por carga estática completado.\n"

        resumen = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA ESTÁTICA</h2>
        <hr>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_tmin")}</strong></p>

        </body>
            """  # Resumen de resultados del diseño por carga estática.

    # Generación de informe para carga de fatiga
    elif tipo_carga == "de fatiga":

        informe += f"""
Datos de Entrada:

    Sistema de unidades: {sist_und}

    Materiales base:

        Pieza 1:
            Acero: {acero1}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza1", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

        Pieza 2:
            Acero: {acero2}
            Sy  =  {dic_diseno_fatiga.get("sy_pieza2", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Material de aporte:

        Electrodo: {electrodo}
            Sy  =  {dic_diseno_fatiga.get("sy_sold", 0)} {und_esfuerzo}
            Sut =  {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Dimensiones de la soldadura:

        Garganta / Espesor (t): ** A determinar **
        Largo (l) : {dic_diseno_fatiga.get("largo", 0)} {und_distancia}

    Tipo de union: {dic_diseno_fatiga.get("tipo_union", 0)}

    Cargas Aplicadas:

        Tipo: Cíclica
        Fuerza máxima (Fmax) = {dic_diseno_fatiga.get("Fmax", 0)} {und_fuerza}
        Fuerza mínima (Fmin) = {dic_diseno_fatiga.get("Fmin", 0)} {und_fuerza}
        Brazo longitudinal (bl) = {dic_diseno_fatiga.get("bl", 0)} {und_distancia}
        Brazo transversal (bt) = {dic_diseno_fatiga.get("bt", 0)} {und_distancia}\n\n
"""  # Datos de entrada para de fatiga

        resultados_fatiga = f"""
Se procede a diseñar por carga de fatiga la junta soldada.

Cálculos realizados

** Nota: Los cálculos se realizaron en función de la garganta o espesor del cordón de soldadura **

    Distancia del eje nuetro hasta la soldadura (c):

        c = {dic_diseno_fatiga["c_ecuacion"]}
            c = {dic_diseno_fatiga["c"]} {und_distancia if isinstance(dic_diseno_fatiga.get("c"), (int, float)) else ""}

    Distancia en X desde el centroide hasta el punto crítico:

        rx = {dic_diseno_fatiga["rx_ecuacion"]}
            rx = {dic_diseno_fatiga["rx"]} {und_distancia if isinstance(dic_diseno_fatiga.get("rx"), (int, float)) else ""}

    Distancia en Y desde el centroide hasta el punto crítico:

        ry = {dic_diseno_fatiga["ry_ecuacion"]}
            ry = {dic_diseno_fatiga["ry"]} {und_distancia if isinstance(dic_diseno_fatiga.get("ry"), (int, float)) else ""}

    Momento de Inercia (I):

        I = {dic_diseno_fatiga["i_sold_ecuacion"]}
            I = {dic_diseno_fatiga["i_sold"]}

    Momento de Inercia Polar (J):

        J = {dic_diseno_fatiga["j_sold_ecuacion"]}
            J = {dic_diseno_fatiga["j_sold"]}

    Área de la soldadura:

        A sold = {dic_diseno_fatiga["area_sold_ecuacion"]}
            A sold = {dic_diseno_fatiga.get("area_sold", 0)}

    Cálculo de fuerza alternante y media:

        Fuerza alternante (Fa) = (Fmax - Fmin) / 2
            Fa = {dic_diseno_fatiga.get("f_alt", 0)} {und_fuerza}

        Fuerza media (Fm) = (Fmax + Fmin) / 2
            Fm = {dic_diseno_fatiga.get("f_med", 0)} {und_fuerza}

    Cálculo de momento flector alternante y medio:

        Momento flector alternante (Ma) = Fa * bl
            Ma = {dic_diseno_fatiga.get("momento_flector_alt", 0)} {und_fuerza}{und_distancia}

        Momento flector medio (Mm) = Fm * bl
            Mm = {dic_diseno_fatiga.get("momento_flector_med", 0)} {und_fuerza}{und_distancia}

    Cálculo de momento torsor alternante y medio:

        Momento torsor alternante (Ta) = Fm * bt
            Ta = {dic_diseno_fatiga.get("momento_torsor_alt", 0)} {und_fuerza}{und_distancia}

        Momento torsor medio (Tm) = Fm * bt
            Tm = {dic_diseno_fatiga.get("momento_torsor_med", 0)} {und_fuerza}{und_distancia}

    Factor de concentración de esfuerzo reducido:

        Para soldadura de ranura de unión: {dic_diseno_fatiga.get("tipo_union", 0)}, sometida a carga combinada, el factor de concentración de esfuerzo reducido es

            Kfs = {dic_diseno_fatiga.get("kfs", 0)}

    Esfuerzos aplicados en la junta:

        Cálculo del esfuerzo cortante primario alternante y medio:

            τ'a = Kfs * Fa / Asold
                τ'a = {dic_diseno_fatiga.get("tao_primario_alt", 0)}

            τ'm = Fm / Asold
                τ'm = {dic_diseno_fatiga.get("tao_primario_med", 0)}

        Cálculo del esfuerzo cortante secundario alternante en el eje X y en el eje Y:

            τ''a x = Kfs * Ta * ry / J
                τ''a x = {round(float(dic_diseno_fatiga.get("tao_secundario_alt_x")), 2) if isinstance(dic_diseno_fatiga.get("tao_secundario_alt_x"), (Float, Integer, Rational)) else dic_diseno_fatiga.get("tao_secundario_alt_x")} {und_esfuerzo if isinstance(dic_diseno_fatiga.get("tao_secundario_alt_x"), (Float, Integer, Rational)) else ""}

            τ''a y = Kfs * Ta * rx / J
                τ''a y = {round(float(dic_diseno_fatiga.get("tao_secundario_alt_y")), 2) if isinstance(dic_diseno_fatiga.get("tao_secundario_alt_y"), (Float, Integer, Rational)) else dic_diseno_fatiga.get("tao_secundario_alt_y")} {und_esfuerzo if isinstance(dic_diseno_fatiga.get("tao_secundario_alt_y"), (Float, Integer, Rational)) else ""}

        Cálculo del esfuerzo cortante secundario medio en el eje X y en el eje Y:

            τ''m x = Tm * ry / J
                τ''m x = {round(float(dic_diseno_fatiga.get("tao_secundario_med_x")), 2) if isinstance(dic_diseno_fatiga.get("tao_secundario_med_x"), (Float, Integer, Rational)) else dic_diseno_fatiga.get("tao_secundario_med_x")} {und_esfuerzo if isinstance(dic_diseno_fatiga.get("tao_secundario_med_x"), (Float, Integer, Rational)) else ""}

            τ''m y = Tm * rx / J
                τ''m y = {dic_diseno_fatiga.get("tao_secundario_med_y", 0)}
                τ''m y = {round(float(dic_diseno_fatiga.get("tao_secundario_med_y")), 2) if isinstance(dic_diseno_fatiga.get("tao_secundario_med_y"), (Float, Integer, Rational)) else dic_diseno_fatiga.get("tao_secundario_med_y")} {und_esfuerzo if isinstance(dic_diseno_fatiga.get("tao_secundario_med_y"), (Float, Integer, Rational)) else ""}

        Cálculo de las componentes X e Y del esfuerzo cortante alternante:

            τa x = τ''a x
                τa x = {round(float(dic_diseno_fatiga.get("tao_alt_x")), 2) if isinstance(dic_diseno_fatiga.get("tao_alt_x"), (Float, Integer, Rational)) else dic_diseno_fatiga.get("tao_alt_x")} {und_esfuerzo if isinstance(dic_diseno_fatiga.get("tao_alt_x"), (Float, Integer, Rational)) else ""}

            τa y = τ'a + τ''a y
                τa y = {dic_diseno_fatiga.get("tao_alt_y", 0)}

        Cálculo de las componentes X e Y del esfuerzo cortante medio:

            τm x = τ''m x
                τm x = {round(float(dic_diseno_fatiga.get("tao_med_x")), 2) if isinstance(dic_diseno_fatiga.get("tao_med_x"), (Float, Integer, Rational)) else dic_diseno_fatiga.get("tao_med_x")} {und_esfuerzo if isinstance(dic_diseno_fatiga.get("tao_med_x"), (Float, Integer, Rational)) else ""}

            τm y = τ'm + τ''m y
                τm y = {dic_diseno_fatiga.get("tao_med_y", 0)}

        Cálculo del esfuerzo cortante alternante y medio resultante:

            τa = sqrt((τa x)^2 + (τa y)^2)
                τa = {dic_diseno_fatiga.get("tao_alt", 0)}

            τm = sqrt((τm x)^2 + (τm y)^2)
                τm = {dic_diseno_fatiga.get("tao_med", 0)}

        Cálculo del esfuerzo normal alternante y medio:

            σa = Kfs * Ma * c / I
                σa = {dic_diseno_fatiga.get("sigma_alt", 0)}

            σm = Mm * c / I
                σm = {dic_diseno_fatiga.get("sigma_med", 0)}

        Cálculo del esfuerzo de Von Misses alternante y medio:

            σ'a = sqrt((σa)^2 + 3 * (τa)^2)
                σ'a = {dic_diseno_fatiga.get("sigma_von_misses_alt", 0)}

            σ'm = sqrt((σm)^2 + 3 * (τm)^2)
                σ'm = {dic_diseno_fatiga.get("sigma_von_misses_med", 0)}

Para la soldadura:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_sold", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para soldadura utilizando la ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            t sold = {dic_diseno_fatiga.get("t_sold", 0)} {und_distancia} *


Para la pieza 1:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza1", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 1 utilizando la ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            t pieza1 = {dic_diseno_fatiga.get("t_pieza1", 0)} {und_distancia} **

Para la pieza 2:

    Cálculo de la resistencia a la fatiga:

        Se = ka * kb * kc * kd * ke * Se'
            Se = {dic_diseno_fatiga.get("se_pieza2", 0)} {und_esfuerzo}

    Resistencia última a la tensión:

        Sut = {dic_diseno_fatiga.get("sut_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2 utilizando la ecuación de Gerber:

        (FD * σ'a)/Se + ((FD * σ'm)/Sut)^2 = 1
            t pieza2 = {dic_diseno_fatiga.get("t_pieza2", 0)} {und_distancia} ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se debe seleccionar entre los tres tamaños de garganta o espesor del cordón calculados (*, **, ***) el mayor de ellos.

Por lo que, {dic_diseno_fatiga.get("conclusion_tmin")}.


Diseño por fatiga de la garganta o espesor del cordón de la soldadura completado.


"""  # Resultados del diseño por carga de fatiga.

        informe += resultados_fatiga

        resumen_fatiga = f"""
        <body>

        <h2 style="text-align:center;">RESUMEN DEL DISEÑO POR CARGA DE FATIGA</h2>
        <hr>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
        <p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_fatiga.get("t_sold")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_fatiga.get("t_pieza1")} {und_distancia}</p>

        <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
        <p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_fatiga.get("t_pieza2")} {und_distancia}</p>

        <p style="color: blue;"><strong>Se concluye que: {dic_diseno_fatiga.get("conclusion_tmin")}</strong></p>

        </body>
            """  # Resumen de resultados del diseño por carga de fatiga.

        verificacion_estatica = f"""
 {"~" * 5} Verificación por análisis estático {"~" * 5}

Factor de seguridad de la soldadura:

    FS sold = {dic_comprobacion.get("fs_sold", 0)}

Conclusión: {dic_comprobacion.get("conclusion_sold", 0)}

Factor de seguridad de la pieza 1:

    FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza1", 0)}

Factor de seguridad de la pieza 2:

    FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}

Conclusión: {dic_comprobacion.get("conclusion_pieza2", 0)}\n\n"""

        verificacion_estatica_resumen = f"""
        <br><body>

        <p style="margin-left: 20px;"><strong>VERIFICACIÓN POR ANÁLISIS ESTÁTICO</strong></p>

        <p><strong>Factor de seguridad de la soldadura:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_sold', 0) >= 3.33 else 'red'};">FS sold = {dic_comprobacion.get('fs_sold', 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_sold", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 1:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza1', 0) >= 2.5 else 'red'};">FS pieza1 = {dic_comprobacion.get("fs_pieza1", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza1", 0)}</p>

        <p><strong>Factor de seguridad de la pieza 2:</strong></p>

        <p style="margin-left: 20px; color: {'blue' if dic_comprobacion.get('fs_pieza2', 0) >= 2.5 else 'red'};">FS pieza2 = {dic_comprobacion.get("fs_pieza2", 0)}</p>
        <p><strong>Conclusión:</strong> {dic_comprobacion.get("conclusion_pieza2", 0)}</p>

        </body>
        """

        if dic_diseno_estatica is None:

            informe += verificacion_estatica

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

        else:

            informe += verificacion_estatica

            informe += f"Al presentarse la falla al realizar la verificación, se procede a rediseñar por carga estática."

            resultados_rediseno = f"""

Cálculos realizados

    Cálculo del momento flector producido por la fuerza externa:

        M = F * bl
            M = {dic_diseno_estatica.get("momento_flector", 0)} {und_fuerza}{und_distancia}

    Cálculo del momento torsor producido por la fuerza externa:

        T = F * bt
            T = {dic_diseno_estatica.get("momento_torsor", 0)} {und_fuerza}{und_distancia}

    Esfuerzos aplicados en la junta:

        Cálculo del esfuerzo cortante primario:

            τ' = F / Asold
                τ' = {dic_diseno_estatica.get("tao_primario", 0)}

        Cálculo del esfuerzo cortante secundario en el eje X y en el eje Y:

            τ''x = T * ry / J
                τ''x = {round(float(dic_diseno_estatica.get("tao_secundario_x")), 2) if isinstance(dic_diseno_estatica.get("tao_secundario_x"), (Float, Integer, Rational)) else dic_diseno_estatica.get("tao_secundario_x")} {und_esfuerzo if isinstance(dic_diseno_estatica.get("tao_secundario_x"), (Float, Integer, Rational)) else ""}

            τ''y = T * rx / J
                τ''y = {round(dic_diseno_estatica.get("tao_secundario_y"), 2) if isinstance(dic_diseno_estatica.get("tao_secundario_y"), (Float, Integer, Rational)) else dic_diseno_estatica.get("tao_secundario_y")} {und_esfuerzo if isinstance(dic_diseno_estatica.get("tao_secundario_y"), (Float, Integer, Rational)) else ""}

        Cálculo de la componente en el eje X del esfuerzo cortante resultante:

            τx = τ''x
                τx = {round(float(dic_diseno_estatica.get("tao_x")), 2) if isinstance(dic_diseno_estatica.get("tao_x"), (Float, Integer, Rational)) else dic_diseno_estatica.get("tao_x")} {und_esfuerzo if isinstance(dic_diseno_estatica.get("tao_x"), (Float, Integer, Rational)) else ""}

        Cálculo de la componente en el eje Y del esfuerzo cortante resultante:

            τy = τ' + τ''y
                τy = {dic_diseno_estatica.get("tao_y", 0)}

        Cálculo del esfuerzo cortante resultante:

            τ = sqrt((τx)^2 + (τy)^2)
                τ = {dic_diseno_estatica.get("tao", 0)}

        Cálculo del esfuerzo normal:

            σ = M * c / I
                σ = {dic_diseno_estatica.get("sigma", 0)}

        Cálculo del esfuerzo de Von Misses:

            σ' = sqrt(σ^2 + 3 * τ^2)
                σ' = {dic_diseno_estatica.get("sigma_von_misses", 0)}


Para la soldadura:

    Resistencia a la fluencia del material de aporte:

        Sy = {dic_diseno_estatica.get("sy_sold", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la soldadura:

        FD sold = Sy / σ'
            t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}  *


Para la pieza 1:

    Resistencia a la fluencia:

        Sy = {dic_diseno_estatica.get("sy_pieza1", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 1:

        FD pieza = Sy / σ'
            t pieza1 = {dic_diseno_estatica.get("t_max_pieza1")} {und_distancia}  **


Para la pieza 2:

    Resistencia a la fluencia::

        Sy = {dic_diseno_estatica.get("sy_pieza2", 0)} {und_esfuerzo}

    Cálculo del espesor mínimo del cordón necesario para la pieza 2:

        FD pieza = Sy / σ'
            t pieza2 = {dic_diseno_estatica.get("t_max_pieza2", 0)} {und_distancia}  ***


Conclusión: Para garantizar las condiciones de funcionamiento y seguridad de la junta, se debe seleccionar entre los tres tamaños de garganta o espesor del cordón calculados (*, **, ***) el mayor de ellos.

Por consiguiente: {dic_diseno_estatica.get("conclusion_tmin", 0)}

            """  # Porción con resultados del rediseño por carga estática.

            informe += resultados_rediseno

            resumen_estatica = f"""
            <body>

            <h2 style="text-align:center;">RESUMEN DEL REDISEÑO POR CARGA ESTÁTICA</h2>
            <hr>

            <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para soldadura:</strong></p>
            <p style="margin-left: 20px; color: blue;">t sold = {dic_diseno_estatica.get("t_min_sold")} {und_distancia}</p>

            <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 1:</strong></p>
            <p style="margin-left: 20px; color: blue;">t pieza1 = {dic_diseno_estatica.get("t_min_pieza1")} {und_distancia}</p>

            <p><strong>Tamaño de garganta o espesor mínimo necesario del cordón para la pieza 2:</strong></p>
            <p style="margin-left: 20px; color: blue;">t pieza2 = {dic_diseno_estatica.get("t_min_pieza2")} {und_distancia}</p>

            <p style="color: blue;"><strong>Se concluye que: {dic_diseno_estatica.get("conclusion_tmin")}</strong></p>

            </body>
                """  # Resumen de resultados del rediseño por carga estática.

            resumen += resumen_fatiga

            resumen += verificacion_estatica_resumen

            resumen += resumen_estatica

    return informe, resumen
