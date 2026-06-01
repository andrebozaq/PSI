"""Código fuente de la lógica de la interfaz gráfica de EIM Weld One"""

import sys
import os
import PyQt5.uic
import PyQt5.QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QDialog, QMessageBox, QTextBrowser, QComboBox,
                             QRadioButton, QFileDialog, QDesktopWidget)
from PyQt5.QtGui import *
from src.calculos import analisis, diseno, generador_informes
from docx import Document
from math import sqrt

# Cargar ventanas de la app


# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


ui_ventana, qt_baseclass = PyQt5.uic.loadUiType(resource_path(r'src\gui\ventana_principal.ui'), 'EIM WELD ONE')
ui_ventana_analisis_filete, base_class_filete = PyQt5.uic.loadUiType(resource_path(r'src\gui\ventana_analisis_filete.ui'),
                                                                     'Análsis de Soldadura de Filete')
ui_ventana_analisis_ranura, base_class_ranura = PyQt5.uic.loadUiType(resource_path(r'src\gui\ventana_analisis_ranura.ui'),
                                                                     'Analisis de Soldadura de Ranura')
ui_ventana_seleccion_diseno, base_class_disenofilete = PyQt5.uic.loadUiType(resource_path(r'src\gui\ventana_seleccion_diseno.ui'),
                                                                            'Selección de diseño')
ui_ventana_disenocarga_filete, base_class_cpfilete = PyQt5.uic.loadUiType(resource_path(r"src\gui\ventana_diseno_filete_carga.ui"),
                                                                          'Diseño de carga en filete')
ui_ventana_disenoh_filete, base_class_hfilete = PyQt5.uic.loadUiType(resource_path(r'src\gui\ventana_diseno_filete_h.ui'),
                                                                     'Diseño de pierna en filete')
ui_ventana_diseno_ranura, base_class_disenoranura = PyQt5.uic.loadUiType(resource_path(r'src\gui\ventana_diseno_ranura.ui'),
                                                                         'Diseno de carga en ranura')
ui_ventana_seleccion_diseno_ranura, base_class_disenoranuras = PyQt5.uic.loadUiType(resource_path(r'src\gui\ventana_seleccion_diseno_ranura.ui'),
                                                                            'Selección de diseño ranura')
ui_ventana_disenoespesor_ranura, base_class_tranura = PyQt5.uic.loadUiType(resource_path(r"src\gui\ventana_diseno_ranura_espesor.ui"),
                                                                          'Diseño de espesor en ranura')
ui_ventana_acercade, base_class_acercade = PyQt5.uic.loadUiType(resource_path(r"src\gui\acercade.ui"),
                                                                          'Acerca del programa')


# VENTANA DE INICIO
class VentanaPrincipal(QMainWindow, ui_ventana):
    """
    Clase que representa la ventana principal de la aplicación de interfaz gráfica.
    Hereda de QMainWindow y ui_ventana (contiene el código fuente del diseño de la ventana).
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor de la clase VentanaPrincipal.

        Args:
            *args: Argumentos posicionales adicionales.
            **kwargs: Argumentos de palabras clave adicionales.
        """

        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # Conexión de señales y slots
        self.label_filete.setVisible(False)
        self.label_ranura.setVisible(False)
        self.boton_filete_analisis.setVisible(False)
        self.boton_ranura_analisis.setVisible(False)
        self.boton_ranura_diseno.setVisible(False)
        self.boton_filete_diseno.setVisible(False)
        self.boton_analisis.clicked.connect(self.presionar_boton_analisis)
        self.boton_diseno.clicked.connect(self.presionar_boton_diseno)
        self.boton_volver.setVisible(False)
        self.boton_volver.clicked.connect(self.volver_inicio)
        self.boton_filete_analisis.clicked.connect(self.abrir_analisis_filete)
        self.boton_ranura_analisis.clicked.connect(self.abrir_analisis_ranura)
        self.boton_filete_diseno.clicked.connect(self.abrir_selecciondiseno_filete)
        self.boton_ranura_diseno.clicked.connect(self.abrir_selecciondiseno_ranura)
        self.boton_info.clicked.connect(self.acercade)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def presionar_boton_analisis(self):

        """Slot para el evento de clic del botón de análisis.
        Realiza acciones específicas al presionar el botón de análisis.
        """
        # Código para el evento de clic del botón de análisis

        # Mostrar etiqueta de módulo e imagenes de soldadura, ocultar y deshabilitar botón de análisis
        self.label_modulo.setText('Módulo: Análisis')
        self.boton_analisis.setVisible(False)
        self.boton_analisis.setDisabled(True)
        self.label_filete.setVisible(True)
        self.label_ranura.setVisible(True)

        # Ocultar y deshabilitar botón diseño
        self.boton_diseno.setVisible(False)
        self.boton_diseno.setDisabled(True)

        # Mostrar y habilitar botón para volver a pantalla principal
        self.boton_volver.setVisible(True)
        self.boton_volver.setDisabled(False)

        # Mostrar y habilitar botón de análisis de filete
        self.boton_filete_analisis.setVisible(True)
        self.boton_filete_analisis.setDisabled(False)
        self.boton_filete_analisis.raise_()  # Traer al frente

        # Mostrar y habilitar botón de análisis de ranura
        self.boton_ranura_analisis.setVisible(True)
        self.boton_ranura_analisis.setDisabled(False)
        self.boton_ranura_analisis.raise_()  # Traer al frente

    def presionar_boton_diseno(self):
        """
        Slot para el evento de clic del botón de diseño.
        Realiza acciones específicas al presionar el botón de diseño.
        """

        # Código para el evento de clic del botón de diseño

        # Mostrar etiqueta de módulo, ocultar y deshabilitar botón de analisis
        self.label_filete.setVisible(True)
        self.label_ranura.setVisible(True)
        self.label_modulo.setText('Módulo: Diseño')
        self.boton_analisis.setVisible(False)
        self.boton_analisis.setDisabled(True)

        # Ocultar y deshabilitar boton de diseño
        self.boton_diseno.setVisible(False)
        self.boton_diseno.setDisabled(True)

        # Mostrar y habilitar botón volver
        self.boton_volver.setVisible(True)
        self.boton_volver.setDisabled(False)

        # Mostrar y habilitar boton de diseño de filete
        self.boton_filete_diseno.setVisible(True)
        self.boton_filete_diseno.setDisabled(False)
        self.boton_filete_diseno.raise_()  # Traer al frente

        # Mostrar y habilitar boton de diseño de ranura
        self.boton_ranura_diseno.setVisible(True)
        self.boton_ranura_diseno.setDisabled(False)
        self.boton_ranura_diseno.raise_()

    def volver_inicio(self):
        """
        Slot para el evento de clic del botón de volver.
        Realiza acciones específicas al presionar el botón de volver.
        """

        # Código para el evento de clic del botón de volver

        # Vaciar el contenido de la etiqueta de módulo
        self.label_modulo.setText('')

        # Ocultar los botones de diseño de filete y ranura
        self.label_filete.setVisible(False)
        self.label_ranura.setVisible(False)
        self.boton_filete_diseno.setVisible(False)
        self.boton_ranura_diseno.setVisible(False)

        # OCultar los botones de analisis de filete y ranura
        self.boton_filete_analisis.setVisible(False)
        self.boton_ranura_analisis.setVisible(False)

        # Ocultar boton de volver
        self.boton_volver.setVisible(False)

        # Mostrar y habilitar botones de análisis y diseño
        self.boton_analisis.setVisible(True)
        self.boton_analisis.setDisabled(False)
        self.boton_diseno.setVisible(True)
        self.boton_diseno.setDisabled(False)

    def abrir_analisis_filete(self):
        """
        Slot para el evento de clic del botón de análisis de filete.
        Realiza acciones específicas al presionar el botón de análisis de filete.
        """

        # Código para el evento de clic del botón de análisis de filete

        # Declarar la ventana como una clase
        self.ventana_analisis_filete = VentanaAnalisisFilete()

        # Abrir ventana de análisis de filete
        self.ventana_analisis_filete.show()

        # Cerrar ventana principal
        self.close()

    def abrir_analisis_ranura(self):
        """
        Slot para el evento de clic del botón de análisis de ranura.
        Realiza acciones específicas al presionar el botón de análisis de ranura.
        """

        # Código para el evento de clic del botón de análisis de ranura

        # Declarar la ventana como una clase
        self.ventana_analisis_ranura = VentanaAnalisisRanura()

        # Abrir ventana de análisis de ranura
        self.ventana_analisis_ranura.show()

        # Cerrar ventana principal
        self.close()

    def abrir_selecciondiseno_filete(self):
        """
        Slot para el evento de clic del botón de diseño de filete.
        Realiza acciones específicas al presionar el botón de diseño de filete.
        """

        # Código para el evento de clic del botón de diseño de filete

        # Declarar la ventana como una clase
        self.ventana_selecciondiseno_filete = VentanaSeleccionDiseno()

        # Abrir ventana de análisis de ranura
        self.ventana_selecciondiseno_filete.show()

        self.close()

    def abrir_selecciondiseno_ranura(self):
        # Código para el evento de clic del botón de diseño de ranura

        # Declarar la ventana como una clase
        self.ventana_selecciondiseno_ranura = VentanaSeleccionDisenoRanura()

        # Abrir ventana de análisis de ranura
        self.ventana_selecciondiseno_ranura.show()

        self.close()

    def acercade(self):
        # Código para el evento de clic del botón de acerca

        # Declarar la ventana como una clase
        self.ventana_acercade = VentanaAcercade()

        # Abrir ventana de análisis de ranura
        self.ventana_acercade.show()


class VentanaAcercade(QDialog, ui_ventana_acercade):
    # Clase de la ventana de acerca del programa

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.cerrar_ventana)  # Conexión al botón OK

        self.center()

    # Función para centrar ventana
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Evento de cerrar ventana
    def cerrar_ventana(self):
        self.close()


# Clase para la ventana de análisis de filete
class VentanaAnalisisFilete(QMainWindow, ui_ventana_analisis_filete):
    """
    Clase que representa la ventana para análisis de filete de la aplicación de interfaz gráfica.
    Hereda de QMainWindow y ui_ventana.
    """

    def __init__(self):
        """
        Constructor de la clase VentanaAnalisisFilete.
        """
        super().__init__()
        self.setupUi(self)

        # Conexión de señales y slots

        ############################################################################################################

        # Señal para cambiar las etiquetas de sistema de unidades
        comboboxes_sist_und = [self.sist_und_afcp, self.sist_und_afct, self.sist_und_afcf,
                               self.sist_und_afctor, self.sist_und_afcc]

        for combobox in comboboxes_sist_und:
            combobox.currentIndexChanged.connect(self.evento_actualizar_etiquetas)

        ############################################################################################################

        # Señal para copiar nombre del acero y resistencias para piezas de igual material
        checkboxes_material_base = [self.mb_iguales_afcp, self.mb_iguales_afct, self.mb_iguales_afcf,
                                    self.mb_iguales_afctor, self.mb_iguales_afcc]

        for checkbox in checkboxes_material_base:
            checkbox.toggled.connect(self.evento_copiar_resistenias_mb)

        ############################################################################################################

        # Señal para extraer de la base de datos las resistencias del material base
        comboboxes_material_base = [self.mb1_afcp, self.mb1_afct, self.mb1_afcf, self.mb1_afctor, self.mb1_afcc,
                                    self.mb2_afcp, self.mb2_afct, self.mb2_afcf, self.mb2_afctor, self.mb2_afcc]

        for combobox in comboboxes_material_base:
            combobox.currentIndexChanged.connect(self.evento_resistencias_materiales_base)

        ############################################################################################################

        # Señal para extraer de la base de datos las resistencias del material de aporte
        comboboxes_material_aporte = [self.electrodo_afcp, self.electrodo_afct, self.electrodo_afcf,
                                      self.electrodo_afctor, self.electrodo_afcc]

        for combobox in comboboxes_material_aporte:
            combobox.currentIndexChanged.connect(self.resistencias_material_aporte)

        ############################################################################################################

        # Diccionario de qlineedits de ingreso de datos
        qlineedit_datos_entrada = {
            "Carga paralela": [self.sy_mb1_afcp, self.sut_mb1_afcp,
                               self.sy_mb2_afcp, self.sut_mb2_afcp,
                               self.sy_e_afcp, self.sut_e_afcp,
                               self.h_afcp, self.e_afcp, self.l_afcp, self.a_afcp,
                               self.fmax_afcp, self.fmin_afcp],
            "Carga transversal": [self.sy_mb1_afct, self.sy_mb2_afct,
                                  self.sut_mb1_afct, self.sut_mb2_afct,
                                  self.sy_e_afct, self.sut_e_afct,
                                  self.h_afct, self.e_afct, self.l_afct,
                                  self.a_afct, self.radio_afct,
                                  self.fmax_afct, self.fmin_afct],
            "Carga de flexión": [self.sy_mb1_afcf, self.sy_mb2_afcf,
                                 self.sut_mb1_afcf, self.sut_mb2_afcf,
                                 self.sy_e_afcf, self.sut_e_afcf,
                                 self.h_afcf, self.e_afcf, self.l_afcf,
                                 self.a_afcf, self.radio_afcf,
                                 self.fmax_afcf, self.fmin_afcf, self.b_afcf],
            "Carga de torsión": [self.sy_mb1_afctor, self.sy_mb2_afctor,
                                 self.sut_mb1_afctor, self.sut_mb2_afctor,
                                 self.sy_e_afctor, self.sut_e_afctor,
                                 self.h_afctor, self.e_afctor, self.l_afctor,
                                 self.a_afctor, self.radio_afctor,
                                 self.fmax_afctor, self.fmin_afctor, self.b_afctor],
            "Carga combinada": [self.sy_mb1_afcc, self.sy_mb2_afcc,
                                self.sut_mb1_afcc, self.sut_mb2_afcc,
                                self.sy_e_afcc, self.sut_e_afcc,
                                self.h_afcc, self.e_afcc, self.l_afcc,
                                self.a_afcc, self.radio_afcc,
                                self.fmax_afcc, self.fmin_afcc,
                                self.bl_afcc, self.bt_afcc]
        }

        # Asignar validador en qlineedits para permitir sólo ingreso de floats
        for tipo_carga, qlineedits in qlineedit_datos_entrada.items():
            for qlineedit in qlineedits:
                qlineedit.setValidator(QDoubleValidator())

        ############################################################################################################

        # Señal de boton en barra menu de volver a inicio
        self.actionVolver_al_inicio.triggered.connect(self.cerrar_y_volver_a_inicio)

        # Señal de boton en barra menu de cerrar
        self.actionCerrar.triggered.connect(self.cerrar_ventana)

        # Señal de boton en barra menú para cálculo nuevo
        self.actionNuevo_calculo.triggered.connect(self.evento_limpiar_tab_actionnuevocalculo)

        # SEÑALES DE BOTONES PARA CALCULAR FS

        # Señal de botón para calcular FS para carga paralela
        self.boton_calcularfs_afcp.clicked.connect(self.calcular_fs_afcp)

        # Señal de botón para calcular FS para carga transversal
        self.boton_calcularfs_afct.clicked.connect(self.calcular_fs_afct)

        # Señal de botón para calcular FS para carga flexion
        self.boton_calcularfs_afcf.clicked.connect(self.calcular_fs_afcf)

        # Señal de botón para calcular FS para carga torsion
        self.boton_calcularfs_afctor.clicked.connect(self.calcular_fs_afctor)

        # Señal de botón para calcular FS para carga combinada
        self.boton_calcularfs_afcc.clicked.connect(self.calcular_fs_afcc)

        # SEÑALES DE BOTONES PARA GUARDAR INFORMES

        # Carga paralela
        self.boton_guardar_afcp.clicked.connect(self.evento_guardar)

        # Carga transversal
        self.boton_guardar_afct.clicked.connect(self.evento_guardar)

        # Carga flexión debido a una fuerza excéntrica
        self.boton_guardar_afcf.clicked.connect(self.evento_guardar)

        # Carga torsión debido a una fuerza excéntrica
        self.boton_guardar_afctor.clicked.connect(self.evento_guardar)

        # Carga combinada debido a una fuerza excéntrica
        self.boton_guardar_afcc.clicked.connect(self.evento_guardar)

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @classmethod
    def validar_datos(cls, palabra_clave, *datos):

        if palabra_clave == 'ceros':
            for dato in datos:
                validacion = 1/dato

        elif palabra_clave == 'negativos':
            for dato in datos:
                if dato < 0:
                    validacion = sqrt(dato)

    @classmethod
    def cambiar_etiquetas(cls, dic_labels, objeto, contenido_objeto):

        # Diccionario de unidades
        unidades = {'Internacional': {'Esfuerzo': '[MPa]', 'Distancia': '[mm]', 'Fuerza': '[N]', 'Torque': '[N.m]'},
                    'Inglés': {'Esfuerzo': '[psi]', 'Distancia': '[pulg]', 'Fuerza': '[lb]', 'Torque': '[lb.pulg]'}}

        # Cambio de unidades en objetos etiqueta con unidades en ventana de carga transversal
        for sist_und_combobox, magnitud_fisica in dic_labels.items():
            if sist_und_combobox == objeto and contenido_objeto == 'Internacional':
                label_esfuerzo = magnitud_fisica["esfuerzo"]
                label_distancia = magnitud_fisica["distancia"]
                label_fuerza = magnitud_fisica["fuerza"]
                label_torque = magnitud_fisica["torque"]
                for label in label_esfuerzo:
                    label.setText(unidades["Internacional"]["Esfuerzo"])
                for label in label_distancia:
                    label.setText(unidades["Internacional"]["Distancia"])
                for label in label_fuerza:
                    label.setText(unidades["Internacional"]["Fuerza"])
                for label in label_torque:
                    label.setText(unidades["Internacional"]["Torque"])
            elif sist_und_combobox == objeto and contenido_objeto == 'Inglés':
                label_esfuerzo = magnitud_fisica["esfuerzo"]
                label_distancia = magnitud_fisica["distancia"]
                label_fuerza = magnitud_fisica["fuerza"]
                label_torque = magnitud_fisica["torque"]
                for label in label_esfuerzo:
                    label.setText(unidades["Inglés"]["Esfuerzo"])
                for label in label_distancia:
                    label.setText(unidades["Inglés"]["Distancia"])
                for label in label_fuerza:
                    label.setText(unidades["Inglés"]["Fuerza"])
                for label in label_torque:
                    label.setText(unidades["Inglés"]["Torque"])

    @classmethod
    def copiar_resistencias_mb(cls, dic_checkbox_widgets):

        for checkbox_metales_iguales in dic_checkbox_widgets:
            if checkbox_metales_iguales["mb_iguales"].isChecked():
                acero = checkbox_metales_iguales["mb1"].currentText()
                checkbox_metales_iguales["mb2"].setCurrentText(acero)
                valor_sy = checkbox_metales_iguales["sy_mb1"].text()
                valor_sut = checkbox_metales_iguales["sut_mb1"].text()
                checkbox_metales_iguales["sy_mb2"].setText(valor_sy)
                checkbox_metales_iguales["sut_mb2"].setText(valor_sut)
            else:
                checkbox_metales_iguales["sy_mb2"].setText("0")
                checkbox_metales_iguales["sut_mb2"].setText("0")
                checkbox_metales_iguales["mb2"].setCurrentText("")

    @classmethod
    def obtencion_resistencias_mb(cls, dic_checkbox_mb, dic_widgets, objeto, contenido_objeto):
        # Verificar que el acero exista en la base de datos y obtener los valores correspondientes (tipo diccionario)
        """material_base contiene valores de sy y sut del metal seleccionado en ambos sistemas de unidades"""

        # Base de datps de metales base disponibles
        data_metales_base = {
            '': {
                'Sy [MPa]': 0,
                'Sy [psi]': 0,
                'Sut [MPa]': 0,
                'Sut [psi]': 0
            },
            'Otro': {
                'Sy [MPa]': '',
                'Sy [psi]': '',
                'Sut [MPa]': '',
                'Sut [psi]': ''
            },
            'ASTM A36': {
                'Sy [MPa]': 250,
                'Sy [psi]': 36000,
                'Sut [MPa]': 400,
                'Sut [psi]': 58000
            },
            'ASTM A572 Grado 42': {
                'Sy [MPa]': 290,
                'Sy [psi]': 42000,
                'Sut [MPa]': 415,
                'Sut [psi]': 60000
            },
            'ASTM A572 Grado 50': {
                'Sy [MPa]': 345,
                'Sy [psi]': 50000,
                'Sut [MPa]': 450,
                'Sut [psi]': 65000
            },
            'ASTM A514': {
                'Sy [MPa]': 690,
                'Sy [psi]': 100000,
                'Sut [MPa]': 828,
                'Sut [psi]': 120000
            },
            'ASTM A53': {
                'Sy [MPa]': 240,
                'Sy [psi]': 35000,
                'Sut [MPa]': 415,
                'Sut [psi]': 60000
            },
            'ASTM A106': {
                'Sy [MPa]': 240,
                'Sy [psi]': 35000,
                'Sut [MPa]': 415,
                'Sut [psi]': 60000
            },
            'ASTM A131': {
                'Sy [MPa]': 235,
                'Sy [psi]': 34000,
                'Sut [MPa]': 400,
                'Sut [psi]': 58000
            },
            'ASTM A139': {
                'Sy [MPa]': 240,
                'Sy [psi]': 35000,
                'Sut [MPa]': 415,
                'Sut [psi]': 60000
            },
            'ASTM A501 Grado A': {
                'Sy [MPa]': 250,
                'Sy [psi]': 36000,
                'Sut [MPa]': 400,
                'Sut [psi]': 58000
            },
            'ASTM A516 Grado 55': {
                'Sy [MPa]': 205,
                'Sy [psi]': 30000,
                'Sut [MPa]': 380,
                'Sut [psi]': 55000
            },
            'ASTM A516 Grado 60': {
                'Sy [MPa]': 220,
                'Sy [psi]': 32000,
                'Sut [MPa]': 415,
                'Sut [psi]': 60000
            },
            'ASTM A524 Grado I': {
                'Sy [MPa]': 240,
                'Sy [psi]': 35000,
                'Sut [MPa]': 415,
                'Sut [psi]': 60000
            },
            'ASTM A524 Grado II': {
                'Sy [MPa]': 205,
                'Sy [psi]': 30000,
                'Sut [MPa]': 300,
                'Sut [psi]': 55000
            },
            'ASTM A573 Grado 65': {
                'Sy [MPa]': 240,
                'Sy [psi]': 35000,
                'Sut [MPa]': 450,
                'Sut [psi]': 65000
            },
            'ASTM A573 Grado 58': {
                'Sy [MPa]': 220,
                'Sy [psi]': 32000,
                'Sut [MPa]': 400,
                'Sut [psi]': 58000
            },
            'ASTM A1008 SS Grado 30': {
                'Sy [MPa]': 205,
                'Sy [psi]': 30000,
                'Sut [MPa]': 310,
                'Sut [psi]': 45000
            },
            'ASTM A1008 SS Grado 40 Tipo 1': {
                'Sy [MPa]': 230,
                'Sy [psi]': 33000,
                'Sut [MPa]': 330,
                'Sut [psi]': 48000
            },
            'ASTM A1008 SS Grado 33 Tipo 2': {
                'Sy [MPa]': 275,
                'Sy [psi]': 40000,
                'Sut [MPa]': 360,
                'Sut [psi]': 52000
            },
            'ASTM A1018 SS Grado 30': {
                'Sy [MPa]': 205,
                'Sy [psi]': 30000,
                'Sut [MPa]': 340,
                'Sut [psi]': 49000
            },
            'ASTM A1018 SS Grado 33': {
                'Sy [MPa]': 230,
                'Sy [psi]': 33000,
                'Sut [MPa]': 360,
                'Sut [psi]': 52000
            },
            'ASTM A1018 SS Grado 36': {
                'Sy [MPa]': 250,
                'Sy [psi]': 36000,
                'Sut [MPa]': 365,
                'Sut [psi]': 53000
            },
            'ASTM A1018 SS Grado 40': {
                'Sy [MPa]': 275,
                'Sy [psi]': 40000,
                'Sut [MPa]': 380,
                'Sut [psi]': 55000
            },
            'ASTM A992': {
                'Sy [MPa]': 345,
                'Sy [psi]': 50000,
                'Sut [MPa]': 450,
                'Sut [psi]': 65000
            },
            'ASTM A572 Grado 55': {
                'Sy [MPa]': 380,
                'Sy [psi]': 55000,
                'Sut [MPa]': 485,
                'Sut [psi]': 70000
            },
            'ASTM A709': {
                'Sy [MPa]': 250,
                'Sy [psi]': 36000,
                'Sut [MPa]': 400,
                'Sut [psi]': 58000
            },
            'ASTM A913 Grado 50': {
                'Sy [MPa]': 345,
                'Sy [psi]': 50000,
                'Sut [MPa]': 450,
                'Sut [psi]': 65000
            },
            'ASTM API 5L': {
                'Sy [MPa]': 241,
                'Sy [psi]': 35000,
                'Sut [MPa]': 414,
                'Sut [psi]': 60000
            },
            'SAE 1010': {
                'Sy [MPa]': 179,
                'Sy [psi]': 26000,
                'Sut [MPa]': 324,
                'Sut [psi]': 47000
            },
            'SAE 1020': {
                'Sy [MPa]': 207,
                'Sy [psi]': 30000,
                'Sut [MPa]': 379,
                'Sut [psi]': 55000
            },
            'SAE 1030': {
                'Sy [MPa]': 259,
                'Sy [psi]': 38000,
                'Sut [MPa]': 469,
                'Sut [psi]': 68000
            },
            'SAE 1035': {
                'Sy [MPa]': 276,
                'Sy [psi]': 40000,
                'Sut [MPa]': 496,
                'Sut [psi]': 72000
            },
            'SAE 1040': {
                'Sy [MPa]': 290,
                'Sy [psi]': 42000,
                'Sut [MPa]': 524,
                'Sut [psi]': 76000
            }
        }

        if contenido_objeto in data_metales_base:
            material_base = data_metales_base[contenido_objeto]

            # Ubicar objetos dependientes del objeto lista de aceros y verificar el sistema de unidades actual
            for sist_und_combobox, material_base_cb in dic_widgets.items():
                if sist_und_combobox.currentText() == 'Internacional':
                    for mb, valor_resistencia in material_base_cb.items():
                        if mb == objeto:
                            # Mostrar valores correspondientes al metal y sistema de unidades en objetos qlineedit
                            valor_sy = material_base['Sy [MPa]']
                            valor_sut = material_base['Sut [MPa]']
                            valor1 = valor_resistencia[0]
                            valor2 = valor_resistencia[1]
                            valor1.setText(str(valor_sy))
                            valor2.setText(str(valor_sut))

                            # Deshabilitar campos para edicion si existen valores de resistencia
                            if mb.currentText() != 'Otro':
                                valor1.setEnabled(False)
                                valor2.setEnabled(False)
                            else:
                                valor1.setEnabled(True)
                                valor2.setEnabled(True)

                else:
                    for mb, valor_resistencia in material_base_cb.items():
                        if mb == objeto:
                            valor_sy = material_base['Sy [psi]']
                            valor_sut = material_base['Sut [psi]']
                            valor1 = valor_resistencia[0]
                            valor2 = valor_resistencia[1]
                            valor1.setText(str(valor_sy))
                            valor2.setText(str(valor_sut))

                            # Deshabilitar campos para edicion si existen valores de resistencia
                            if mb.currentText() != 'Otro':
                                valor1.setEnabled(False)
                                valor2.setEnabled(False)
                            else:
                                valor1.setEnabled(True)
                                valor2.setEnabled(True)

        for checkbox_metales_iguales in dic_checkbox_mb:
            if checkbox_metales_iguales["mb_iguales"].isChecked():
                acero = checkbox_metales_iguales["mb1"].currentText()
                checkbox_metales_iguales["mb2"].setCurrentText(acero)
                valor_sy = checkbox_metales_iguales["sy_mb1"].text()
                valor_sut = checkbox_metales_iguales["sut_mb1"].text()
                checkbox_metales_iguales["sy_mb2"].setText(valor_sy)
                checkbox_metales_iguales["sut_mb2"].setText(valor_sut)

    @classmethod
    def obtencion_resistencias_ma(cls, dic_comboboxes, objeto, contenido_objeto):

        # Base de datos de electrodos y sus resistencias
        data_material_aporte = {
            'E60xx': {
                'Sy [MPa]': 345,
                'Sy [psi]': 50000,
                'Sut [MPa]': 415,
                'Sut [psi]': 60000
            },
            'E70xx': {
                'Sy [MPa]': 393,
                'Sy [psi]': 57000,
                'Sut [MPa]': 482,
                'Sut [psi]': 70000
            },
            'E80xx': {
                'Sy [MPa]': 462,
                'Sy [psi]': 67000,
                'Sut [MPa]': 551,
                'Sut [psi]': 80000
            },
            'E90xx': {
                'Sy [MPa]': 531,
                'Sy [psi]': 77000,
                'Sut [MPa]': 620,
                'Sut [psi]': 90000
            },
            'E100xx': {
                'Sy [MPa]': 600,
                'Sy [psi]': 87000,
                'Sut [MPa]': 689,
                'Sut [psi]': 100000
            },
            'E120xx': {
                'Sy [MPa]': 737,
                'Sy [psi]': 107000,
                'Sut [MPa]': 828,
                'Sut [psi]': 120000
            },
            '': {
                'Sy [MPa]': 0,
                'Sy [psi]': 0,
                'Sut [MPa]': 0,
                'Sut [psi]': 0
            }
        }

        # Verificar que el acero exista en la base de datos y obtener los valores correspondientes (tipo diccionario)
        """material_aporte contiene valores de sy y sut del electrodo seleccionado en ambos sistemas de unidades"""
        if contenido_objeto in data_material_aporte:
            material_aporte = data_material_aporte[contenido_objeto]

            # Ubicar objetos dependientes del objeto lista de aceros y verificar el sistema de unidades actual
            for sist_und_combobox, material_aporte_cb in dic_comboboxes.items():

                if sist_und_combobox.currentText() == 'Internacional':
                    for ma, valor_resistencia in material_aporte_cb.items():
                        if ma == objeto:
                            # Mostrar valores correspondientes al metal y sistema de unidades en objetos qlineedit
                            valor_sy = material_aporte['Sy [MPa]']
                            valor_sut = material_aporte['Sut [MPa]']
                            valor1 = valor_resistencia[0]
                            valor2 = valor_resistencia[1]
                            valor1.setText(str(valor_sy))
                            valor2.setText(str(valor_sut))
                            valor1.setEnabled(False)
                            valor2.setEnabled(False)

                else:
                    for ma, valor_resistencia in material_aporte_cb.items():
                        if ma == objeto:
                            valor_sy = material_aporte['Sy [psi]']
                            valor_sut = material_aporte['Sut [psi]']
                            valor1 = valor_resistencia[0]
                            valor2 = valor_resistencia[1]
                            valor1.setText(str(valor_sy))
                            valor2.setText(str(valor_sut))
                            valor1.setEnabled(False)
                            valor2.setEnabled(False)

    @staticmethod
    def mostrar_msg_error():

        # Mostrar error si no se ejecuta try
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("¡Ups!")
        msg.setInformativeText('Ha ocurrido un error inesperado.\nPor favor, verifica los datos ingresados.')
        msg.setWindowTitle("Error")
        msg.exec_()

    @staticmethod
    def mostrar_msg_aviso_electrodo():

        # Mensaje de aviso si sut del electrodo es menor a alguno de los sut de las piezas
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText(
            "Se sugiere seleccionar un electrodo con resistencia última igual o mayor a la menor de las resistencias de los metales base.")
        message_box.setWindowTitle("Aviso")
        message_box.exec_()

    def guardar_informe(self, objeto, dic_botones):
        """
        Método de clase para guardar el contenido de un informe asociado a un botón en un archivo.

        Args:
            objeto: El botón que emite la señal. El diccionario mapea botones a text browsers que contienen el contenido del informe.
        """
        contenido_informe = ""
        for boton, textbrowser in dic_botones.items():
            if boton == objeto:
                contenido_informe = textbrowser.toPlainText()

        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar informe", "", "Documentos de Word (*.docx)")

        if file_name:
            doc = Document()
            doc.add_paragraph(contenido_informe)
            doc.save(file_name)

    def evento_guardar(self):
        """
        Método de evento para manejar la señal de clic en un botón de guardar.

        Obtiene el botón que emite la señal y llama al método 'guardar_informe' para guardar el informe asociado al botón.
        """
        dic_botones = {
            self.boton_guardar_afcp: self.informe_resultados_afcp,
            self.boton_guardar_afct: self.informe_resultados_afct,
            self.boton_guardar_afcf: self.informe_resultados_afcf,
            self.boton_guardar_afctor: self.informe_resultados_afctor,
            self.boton_guardar_afcc: self.informe_resultados_afcc
        }

        objeto = self.sender()

        self.guardar_informe(objeto, dic_botones)

    def evento_limpiar_tab_actionnuevocalculo(self):

        # Obtener pestaña activa
        tab_widget = self.tab_widget
        tab_activa_index = tab_widget.currentIndex()
        tab_activa = tab_widget.widget(tab_activa_index)

        # Colocar todos los QlineEdits en 0 (datos de entrada)
        for widget in tab_activa.findChildren(QLineEdit):
            if isinstance(widget, QLineEdit):
                widget.setText("0")

        # Vaciar el contenido de todos los QTextBrowsers (resumen e informe de resultados)
        for widget in tab_activa.findChildren(QTextBrowser):
            if isinstance(widget, QTextBrowser):
                widget.setText("")

        # Deseleccionar el nombre de algún material
        for widget in tab_activa.findChildren(QComboBox):
            if isinstance(widget, QComboBox):
                widget.setCurrentText("")

        # Deseleccionar los QRadioButtons
        for widget in tab_activa.findChildren(QRadioButton):
            if isinstance(widget, QRadioButton):
                widget.setChecked(False)

    def cerrar_y_volver_a_inicio(self):
        """
        Slot para el evento de clic del botón de Volver a inicio en la barra menú.
        Realiza acciones específicas al presionar el botón.
        """

        # Declarar la ventana como una clase
        self.ventana_volver_inicio = VentanaPrincipal()

        # Abrir ventana de análisis de ranura
        self.ventana_volver_inicio.show()

        # Cerrar ventana de análisis de filete
        self.close()

    def cerrar_ventana(self):
        self.close()

    def evento_actualizar_etiquetas(self):
        """Slot para el evento de cambio de indice de la lista desplegable de sistema de unidades.
       Realiza acciones específicas al seleccionar un indice de la lista desplegable.
       """
        # Diccionario de objetos etiquetas con unidades de esfuerzo, distancia y fuerza
        etiquetas_unidades = {
            self.sist_und_afct: {
                'esfuerzo': [self.und_esfuerzo_afct_1,
                             self.und_esfuerzo_afct_2,
                             self.und_esfuerzo_afct_3,
                             self.und_esfuerzo_afct_4,
                             self.und_esfuerzo_afct_5,
                             self.und_esfuerzo_afct_6],
                'distancia': [self.und_distancia_afct_1,
                              self.und_distancia_afct_2,
                              self.und_distancia_afct_3,
                              self.und_distancia_afct_4,
                              self.und_distancia_afct_5],
                'fuerza': [self.und_fuerza_afct_1,
                           self.und_fuerza_afct_2],
                'torque': []
            },
            self.sist_und_afcp: {
                "esfuerzo": [self.und_esfuerzo_afcp_1,
                             self.und_esfuerzo_afcp_2,
                             self.und_esfuerzo_afcp_3,
                             self.und_esfuerzo_afcp_4,
                             self.und_esfuerzo_afcp_5,
                             self.und_esfuerzo_afcp_6],
                'distancia': [self.und_distancia_afcp_1,
                              self.und_distancia_afcp_2,
                              self.und_distancia_afcp_3,
                              self.und_distancia_afcp_4],
                'fuerza': [self.und_fuerza_afcp_1,
                           self.und_fuerza_afcp_2],
                'torque': []
            },
            self.sist_und_afcf: {
                "esfuerzo": [self.und_esfuerzo_afcf_1,
                             self.und_esfuerzo_afcf_2,
                             self.und_esfuerzo_afcf_3,
                             self.und_esfuerzo_afcf_4,
                             self.und_esfuerzo_afcf_5,
                             self.und_esfuerzo_afcf_6],
                'distancia': [self.und_distancia_afcf_1,
                              self.und_distancia_afcf_2,
                              self.und_distancia_afcf_3,
                              self.und_distancia_afcf_4,
                              self.und_distancia_afcf_5,
                              self.und_distancia_afcf_6,
                              self.und_distancia_afcf_7,
                              self.und_distancia_afcf_8,
                              self.und_distancia_afcf_9],
                'fuerza': [self.und_fuerza_afcf_1,
                           self.und_fuerza_afcf_2],
                'torque': []

            },
            self.sist_und_afctor: {
                'esfuerzo': [self.und_esfuerzo_afctor_1,
                             self.und_esfuerzo_afctor_2,
                             self.und_esfuerzo_afctor_3,
                             self.und_esfuerzo_afctor_4,
                             self.und_esfuerzo_afctor_5,
                             self.und_esfuerzo_afctor_6],
                'distancia': [self.und_distancia_afctor_1,
                              self.und_distancia_afctor_2,
                              self.und_distancia_afctor_3,
                              self.und_distancia_afctor_4,
                              self.und_distancia_afctor_5,
                              self.und_distancia_afctor_6,
                              self.und_distancia_afctor_7,
                              self.und_distancia_afctor_8,
                              self.und_distancia_afctor_9],
                'fuerza': [self.und_fuerza_afctor_1,
                           self.und_fuerza_afctor_2],
                "torque": []

            },
            self.sist_und_afcc: {
                'esfuerzo': [self.und_esfuerzo_afcc_1,
                             self.und_esfuerzo_afcc_2,
                             self.und_esfuerzo_afcc_3,
                             self.und_esfuerzo_afcc_4,
                             self.und_esfuerzo_afcc_5,
                             self.und_esfuerzo_afcc_6],
                'distancia': [self.und_distancia_afcc_1,
                              self.und_distancia_afcc_2,
                              self.und_distancia_afcc_3,
                              self.und_distancia_afcc_4,
                              self.und_distancia_afcc_5,
                              self.und_distancia_afcc_6,
                              self.und_distancia_afcc_7,
                              self.und_distancia_afcc_8,
                              self.und_distancia_afcc_9,
                              self.und_distancia_afcc_10,
                              self.und_distancia_afcc_11],
                'fuerza': [self.und_fuerza_afcc_1,
                           self.und_fuerza_afcc_2],
                'torque': []
            }
        }

        # Código para el evento

        # Obtener objeto que emite la señal
        objeto = self.sender()

        # Obtener contenido del objeto que emite la señal (nombre de material seleccionado de lista desplegable)
        contenido_objeto = self.sender().currentText()

        VentanaAnalisisFilete.cambiar_etiquetas(etiquetas_unidades, objeto, contenido_objeto)

    def evento_copiar_resistenias_mb(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
         Realiza acciones específicas al hacer click en el radiobutton.
         """
        # Código para el evento

        widgets_material_base = [
            {
                "mb_iguales": self.mb_iguales_afcp,
                "mb1": self.mb1_afcp,
                "mb2": self.mb2_afcp,
                "sy_mb1": self.sy_mb1_afcp,
                "sut_mb1": self.sut_mb1_afcp,
                "sy_mb2": self.sy_mb2_afcp,
                "sut_mb2": self.sut_mb2_afcp
            },
            {
                "mb_iguales": self.mb_iguales_afct,
                "mb1": self.mb1_afct,
                "mb2": self.mb2_afct,
                "sy_mb1": self.sy_mb1_afct,
                "sut_mb1": self.sut_mb1_afct,
                "sy_mb2": self.sy_mb2_afct,
                "sut_mb2": self.sut_mb2_afct
            },
            {
                "mb_iguales": self.mb_iguales_afcf,
                "mb1": self.mb1_afcf,
                "mb2": self.mb2_afcf,
                "sy_mb1": self.sy_mb1_afcf,
                "sut_mb1": self.sut_mb1_afcf,
                "sy_mb2": self.sy_mb2_afcf,
                "sut_mb2": self.sut_mb2_afcf
            },
            {
                "mb_iguales": self.mb_iguales_afctor,
                "mb1": self.mb1_afctor,
                "mb2": self.mb2_afctor,
                "sy_mb1": self.sy_mb1_afctor,
                "sut_mb1": self.sut_mb1_afctor,
                "sy_mb2": self.sy_mb2_afctor,
                "sut_mb2": self.sut_mb2_afctor
            },
            {
                "mb_iguales": self.mb_iguales_afcc,
                "mb1": self.mb1_afcc,
                "mb2": self.mb2_afcc,
                "sy_mb1": self.sy_mb1_afcc,
                "sut_mb1": self.sut_mb1_afcc,
                "sy_mb2": self.sy_mb2_afcc,
                "sut_mb2": self.sut_mb2_afcc
            }

        ]

        VentanaAnalisisFilete.copiar_resistencias_mb(widgets_material_base)

    def evento_resistencias_materiales_base(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
        Realiza acciones específicas al cambiar el contenido del combobox.
        """
        # Código para el evento

        # Diccionario de dependecia de objetos (lista desplegable de sistund, lista de materiales, lineas de texto
        mb_comboboxes = {
            self.sist_und_afcp: {
                self.mb1_afcp: (self.sy_mb1_afcp, self.sut_mb1_afcp),
                self.mb2_afcp: (self.sy_mb2_afcp, self.sut_mb2_afcp)
            },
            self.sist_und_afct: {
                self.mb1_afct: (self.sy_mb1_afct, self.sut_mb1_afct),
                self.mb2_afct: (self.sy_mb2_afct, self.sut_mb2_afct)
            },
            self.sist_und_afcf: {
                self.mb1_afcf: (self.sy_mb1_afcf, self.sut_mb1_afcf),
                self.mb2_afcf: (self.sy_mb2_afcf, self.sut_mb2_afcf)
            },
            self.sist_und_afctor: {
                self.mb1_afctor: (self.sy_mb1_afctor, self.sut_mb1_afctor),
                self.mb2_afctor: (self.sy_mb2_afctor, self.sut_mb2_afctor)
            },
            self.sist_und_afcc: {
                self.mb1_afcc: (self.sy_mb1_afcc, self.sut_mb1_afcc),
                self.mb2_afcc: (self.sy_mb2_afcc, self.sut_mb2_afcc)}}

        # Obtener objeto que emite la señal
        objeto = self.sender()

        # Obtener contenido del objeto que emite la señal (nombre de material seleccionado de lista desplegable)
        contenido_objeto = self.sender().currentText()

        widgets_material_base = [
            {
                "mb_iguales": self.mb_iguales_afcp,
                "mb1": self.mb1_afcp,
                "mb2": self.mb2_afcp,
                "sy_mb1": self.sy_mb1_afcp,
                "sut_mb1": self.sut_mb1_afcp,
                "sy_mb2": self.sy_mb2_afcp,
                "sut_mb2": self.sut_mb2_afcp
            },
            {
                "mb_iguales": self.mb_iguales_afct,
                "mb1": self.mb1_afct,
                "mb2": self.mb2_afct,
                "sy_mb1": self.sy_mb1_afct,
                "sut_mb1": self.sut_mb1_afct,
                "sy_mb2": self.sy_mb2_afct,
                "sut_mb2": self.sut_mb2_afct
            },
            {
                "mb_iguales": self.mb_iguales_afcf,
                "mb1": self.mb1_afcf,
                "mb2": self.mb2_afcf,
                "sy_mb1": self.sy_mb1_afcf,
                "sut_mb1": self.sut_mb1_afcf,
                "sy_mb2": self.sy_mb2_afcf,
                "sut_mb2": self.sut_mb2_afcf
            },
            {
                "mb_iguales": self.mb_iguales_afctor,
                "mb1": self.mb1_afctor,
                "mb2": self.mb2_afctor,
                "sy_mb1": self.sy_mb1_afctor,
                "sut_mb1": self.sut_mb1_afctor,
                "sy_mb2": self.sy_mb2_afctor,
                "sut_mb2": self.sut_mb2_afctor
            },
            {
                "mb_iguales": self.mb_iguales_afcc,
                "mb1": self.mb1_afcc,
                "mb2": self.mb2_afcc,
                "sy_mb1": self.sy_mb1_afcc,
                "sut_mb1": self.sut_mb1_afcc,
                "sy_mb2": self.sy_mb2_afcc,
                "sut_mb2": self.sut_mb2_afcc
            }

        ]

        VentanaAnalisisFilete.obtencion_resistencias_mb(widgets_material_base, mb_comboboxes, objeto, contenido_objeto)

    def resistencias_material_aporte(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
           Realiza acciones específicas al seleccionar un tipo de electrodo de la lista desplegable.
           """

        # Código para el evento

        # Diccionario de dependencia de objetos (lista de electrodos, campos de resistencia para cada ventana)
        """Material de aporte comboboxes"""
        ma_comboboxes = {
            self.sist_und_afcp: {
                self.electrodo_afcp: (self.sy_e_afcp,
                                      self.sut_e_afcp)
            },
            self.sist_und_afct: {
                self.electrodo_afct: (self.sy_e_afct,
                                      self.sut_e_afct)
            },
            self.sist_und_afcf: {
                self.electrodo_afcf: (self.sy_e_afcf,
                                      self.sut_e_afcf)
            },
            self.sist_und_afctor: {
                self.electrodo_afctor: (self.sy_e_afctor,
                                        self.sut_e_afctor)
            },
            self.sist_und_afcc: {
                self.electrodo_afcc: (self.sy_e_afcc,
                                      self.sut_e_afcc)
            }
        }

        # Obtener objeto y contenido del objeto que emite la señal
        objeto = self.sender()
        contenido_objeto = self.sender().currentText()

        VentanaAnalisisFilete.obtencion_resistencias_ma(ma_comboboxes, objeto, contenido_objeto)

    # Evento para calcular FS para análisis de filete para carga paralela
    def calcular_fs_afcp(self):

        self.informe_resultados_afcp.clear()
        self.resumen_resultados_afcp.clear()

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "dos": self.g_2_afcp,
            "seis": self.g_6_afcp
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "dos":
            self.a_afcp.setText("0")

        if self.iden_proyecto_afcp is not None:
            nombre_proyecto = self.iden_proyecto_afcp.text()
        else:
            nombre_proyecto = "S/I"

        # Calculo de FS para carga estática

        # Verificar si se seleccionó carga estática
        try:

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_afcp.text()),
                "sut_mb1": float(self.sut_mb1_afcp.text()),
                "sy_mb2": float(self.sy_mb2_afcp.text()),
                "sut_mb2": float(self.sut_mb2_afcp.text()),
                "sy_e": float(self.sy_e_afcp.text()),
                "sut_e": float(self.sut_e_afcp.text()),
                "h": float(self.h_afcp.text()),
                "e": float(self.e_afcp.text()),
                "l": float(self.l_afcp.text()),
                "a": float(self.a_afcp.text()),
                "fmax": float(self.fmax_afcp.text()),
                "fmin": float(self.fmin_afcp.text())
            }

            if self.cestatica_afcp.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_afcp.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Intermedia"
                fmax = diccionario_datos["fmax"]
                carga = {"Fmax": fmax}
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, fmax)

                # Validador de resistencia del electrodo mayor a resistencias de los metales base
                if sut_e < min(sut_mb1, sut_mb2):
                    self.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = analisis.AnalisisSoldaduraFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos, espesor)

                # Extraer diccionario con resultados y bool de si falla (aunque no se usa en este contexto)
                falla, dic_resultados_estatica = resultados.analisis_estatico_cp()

                info_resum = generador_informes.informe_analisis_filete_cp(nombre_proyecto, "estática",
                                                                           dic_resultados_estatica, {},
                                                                           falla, self.sist_und_afcp.currentText(),
                                                                           self.und_fuerza_afcp_2.text(),
                                                                           self.und_distancia_afcp_2.text(),
                                                                           self.und_esfuerzo_afcp_2.text(),
                                                                           self.mb1_afcp.currentText(),
                                                                           self.mb2_afcp.currentText(),
                                                                           self.electrodo_afcp.currentText()
                                                                           )

                self.informe_resultados_afcp.setText(info_resum[0])
                self.resumen_resultados_afcp.setHtml(info_resum[1])

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_afcp.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_afcp.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Intermedia"
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                carga = {"Fmax": fmax, "Fmin": fmin}
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    self.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = analisis.AnalisisSoldaduraFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos, espesor)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_cp()

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga = resultados.analisis_fatiga_cp()[1]

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_filete_cp(nombre_proyecto, "de fatiga",
                                                                           dic_resultados_estatica, dic_resultados_fatiga,
                                                                           falla, self.sist_und_afcp.currentText(),
                                                                           self.und_fuerza_afcp_2.text(),
                                                                           self.und_distancia_afcp_2.text(),
                                                                           self.und_esfuerzo_afcp_2.text(),
                                                                           self.mb1_afcp.currentText(),
                                                                           self.mb2_afcp.currentText(),
                                                                           self.electrodo_afcp.currentText()
                                                                           )
                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_afcp.setText(info_resum[0])
                self.resumen_resultados_afcp.setHtml(resumen)

            else:

                self.mostrar_msg_error()

        except:

            self.mostrar_msg_error()

        else:
            # Habilitar boton de guardar
            self.boton_guardar_afcp.setEnabled(True)

    # Evento para calcular FS para análisis de filete para carga transversal
    def calcular_fs_afct(self):

        self.informe_resultados_afct.clear()
        self.resumen_resultados_afct.clear()

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_afct,
            "tres": self.g_3_afct,
            "cinco": self.g_5_afct,
            "siete": self.g_7_afct,
            "ocho": self.g_8_afct,
            "diez": self.g_10_afct,
            "once": self.g_11_afct,
            "doce": self.g_12_afct
        }

        geometria_seleccionada = None

        # Obtencion de geometria seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "uno":
            self.a_afct.setText("0")
            self.radio_afct.setText("0")
        elif geometria_seleccionada == "ocho":
            self.l_afct.setText("0")
            self.a_afct.setText("0")
        else:
            self.radio_afct.setText("0")

        if self.iden_proyecto_afct is not None:
            nombre_proyecto = self.iden_proyecto_afct.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Intermedia": self.union_interm_afct,
            "Unión T": self.union_t_afct
        }

        union_seleccionada = None

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Calculo de FS para carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Casting de datos ingresados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_afct.text()),
                "sut_mb1": float(self.sut_mb1_afct.text()),
                "sy_mb2": float(self.sy_mb2_afct.text()),
                "sut_mb2": float(self.sut_mb2_afct.text()),
                "sy_e": float(self.sy_e_afct.text()),
                "sut_e": float(self.sut_e_afct.text()),
                "h": float(self.h_afct.text()),
                "e": float(self.e_afct.text()),
                "l": float(self.l_afct.text()),
                "a": float(self.a_afct.text()),
                "radio": float(self.radio_afct.text()),
                "fmax": float(self.fmax_afct.text()),
                "fmin": float(self.fmin_afct.text())
            }

            # Verificar si se seleccionó carga estática
            if self.cestatica_afct.isChecked():

                # Asignación de datos necesarios a variables

                sist_und = self.sist_und_afct.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                fmax = diccionario_datos["fmax"]
                carga = {"Fmax": fmax}
                tipo_union = union_seleccionada
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    self.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga transversal
                resultados = analisis.AnalisisSoldaduraFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos, espesor)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_ctrans()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_filete_ct(nombre_proyecto, "estática",
                                                                           dic_resultados_estatica,
                                                                           {},
                                                                           falla, self.sist_und_afct.currentText(),
                                                                           self.und_fuerza_afct_2.text(),
                                                                           self.und_distancia_afct_2.text(),
                                                                           self.und_esfuerzo_afct_2.text(),
                                                                           self.mb1_afct.currentText(),
                                                                           self.mb2_afct.currentText(),
                                                                           self.electrodo_afct.currentText()
                                                                           )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_afct.setText(info_resum[0])
                self.resumen_resultados_afct.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_afct.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_afct.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                carga = {"Fmax": fmax, "Fmin": fmin}
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    self.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis de fatiga de carga transversal
                resultados = analisis.AnalisisSoldaduraFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos, espesor)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_ctrans()

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga = resultados.analisis_fatiga_ctrans()[1]

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_filete_ct(nombre_proyecto, "de fatiga",
                                                                           dic_resultados_estatica,
                                                                           dic_resultados_fatiga,
                                                                           falla, self.sist_und_afct.currentText(),
                                                                           self.und_fuerza_afct_2.text(),
                                                                           self.und_distancia_afct_2.text(),
                                                                           self.und_esfuerzo_afct_2.text(),
                                                                           self.mb1_afct.currentText(),
                                                                           self.mb2_afct.currentText(),
                                                                           self.electrodo_afct.currentText()
                                                                           )
                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_afct.setText(info_resum[0])
                self.resumen_resultados_afct.setHtml(resumen)

            else:

                self.mostrar_msg_error()

        except:

            self.mostrar_msg_error()

        else:

            self.boton_guardar_afct.setEnabled(True)

    # Evento para calcular FS para análisis de filete para carga de flexion
    def calcular_fs_afcf(self):

        self.informe_resultados_afcf.clear()
        self.resumen_resultados_afcf.clear()

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_afcf,
            "tres": self.g_3_afcf,
            "cinco": self.g_5_afcf,
            "seis": self.g_6_afcf,
            "siete": self.g_7_afcf,
            "ocho": self.g_8_afcf,
            "nueve": self.g_9_afcf,
            "diez": self.g_10_afcf,
            "once": self.g_11_afcf,
            "doce": self.g_12_afcf
        }

        geometria_seleccionada = None

        # Obtencion de geometria seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "uno":
            self.a_afcf.setText("0")
            self.radio_afcf.setText("0")
        elif geometria_seleccionada == "ocho":
            self.l_afcf.setText("0")
            self.a_afcf.setText("0")
        else:
            self.radio_afcf.setText("0")

        if self.iden_proyecto_afcf is not None:
            nombre_proyecto = self.iden_proyecto_afct.text()
        else:
            nombre_proyecto = "S/I"

        # Calculo de FS para carga estática
        try:
            # Casting de datos ingresados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_afcf.text()),
                "sut_mb1": float(self.sut_mb1_afcf.text()),
                "sy_mb2": float(self.sy_mb2_afcf.text()),
                "sut_mb2": float(self.sut_mb2_afcf.text()),
                "sy_e": float(self.sy_e_afcf.text()),
                "sut_e": float(self.sut_e_afcf.text()),
                "h": float(self.h_afcf.text()),
                "e": float(self.e_afcf.text()),
                "l": float(self.l_afcf.text()),
                "a": float(self.a_afcf.text()),
                "radio": float(self.radio_afcf.text()),
                "fmax": float(self.fmax_afcf.text()),
                "fmin": float(self.fmin_afcf.text()),
                "brazo": float(self.b_afcf.text())
            }

            # Verificar si se seleccionó carga estática
            if self.cestatica_afcf.isChecked():

                # Asignación de datos necesarios a variables

                sist_und = self.sist_und_afcf.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                fmax = diccionario_datos["fmax"]
                brazo = diccionario_datos["brazo"]
                carga = {"Fmax": fmax, "b": brazo}
                tipo_union = "Unión T"
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, brazo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, brazo, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    self.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga transversal
                resultados = analisis.AnalisisSoldaduraFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria,
                                                              parametros_geometricos, espesor)

                # Resultados a mostrar en cuadros: x, y, c
                x, y = resultados.obtener_coordenadas_centroide()
                c = str(round(resultados.obtener_rx_ry()[1], 3))
                self.x_afcf.setText(str(round(x, 3)))
                self.y_afcf.setText(str(round(y, 3)))
                self.c_afcf.setText(c)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_cflex()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_filete_cf(nombre_proyecto, "estática",
                                                                           dic_resultados_estatica,
                                                                           {},
                                                                           falla, self.sist_und_afcf.currentText(),
                                                                           self.und_fuerza_afcf_2.text(),
                                                                           self.und_distancia_afcf_2.text(),
                                                                           self.und_esfuerzo_afcf_2.text(),
                                                                           self.mb1_afcf.currentText(),
                                                                           self.mb2_afcf.currentText(),
                                                                           self.electrodo_afcf.currentText()
                                                                           )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_afcf.setText(info_resum[0])
                self.resumen_resultados_afcf.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_afcf.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_afcf.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Unión T"
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                brazo = diccionario_datos["brazo"]
                carga = {"Fmax": fmax, "Fmin": fmin, "b": brazo}
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, brazo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, brazo, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    self.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis de fatiga de carga transversal
                resultados = analisis.AnalisisSoldaduraFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos, espesor)

                # Resultados a mostrar en cuadros: x, y, c
                x, y = resultados.obtener_coordenadas_centroide()
                c = str(round(resultados.obtener_rx_ry()[1], 3))
                self.x_afcf.setText(str(round(x, 3)))
                self.y_afcf.setText(str(round(y, 3)))
                self.c_afcf.setText(c)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_cflex()

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga = resultados.analisis_fatiga_cflex()[1]

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_filete_cf(nombre_proyecto, "de fatiga",
                                                                           dic_resultados_estatica,
                                                                           dic_resultados_fatiga,
                                                                           falla, self.sist_und_afcf.currentText(),
                                                                           self.und_fuerza_afcf_2.text(),
                                                                           self.und_distancia_afcf_2.text(),
                                                                           self.und_esfuerzo_afcf_2.text(),
                                                                           self.mb1_afcf.currentText(),
                                                                           self.mb2_afcf.currentText(),
                                                                           self.electrodo_afcf.currentText()
                                                                           )
                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_afcf.setText(info_resum[0])
                self.resumen_resultados_afcf.setHtml(resumen)

            else:

                self.mostrar_msg_error()

        except:

            self.mostrar_msg_error()

        else:

            self.boton_guardar_afcf.setEnabled(True)

    # Evento para calcular FS para análisis de filete para carga de torsion
    def calcular_fs_afctor(self):

        self.informe_resultados_afctor.clear()
        self.resumen_resultados_afctor.clear()

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_afctor,
            "tres": self.g_3_afctor,
            "cinco": self.g_5_afctor,
            "seis": self.g_6_afctor,
            "siete": self.g_7_afctor,
            "ocho": self.g_8_afctor,
            "nueve": self.g_9_afctor,
            "diez": self.g_10_afctor,
            "once": self.g_11_afctor,
            "doce": self.g_12_afctor
        }

        geometria_seleccionada = None

        # Obtencion de geometria seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "uno":
            self.a_afctor.setText("0")
            self.radio_afctor.setText("0")
        elif geometria_seleccionada == "ocho":
            self.l_afctor.setText("0")
            self.a_afctor.setText("0")
        else:
            self.radio_afctor.setText("0")

        if self.iden_proyecto_afctor is not None:
            nombre_proyecto = self.iden_proyecto_afctor.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Intermedia": self.union_interm_afctor,
            "Unión T": self.union_t_afctor
        }

        union_seleccionada = None

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Calculo de FS para carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Casting de datos ingresados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_afctor.text()),
                "sut_mb1": float(self.sut_mb1_afctor.text()),
                "sy_mb2": float(self.sy_mb2_afctor.text()),
                "sut_mb2": float(self.sut_mb2_afctor.text()),
                "sy_e": float(self.sy_e_afctor.text()),
                "sut_e": float(self.sut_e_afctor.text()),
                "h": float(self.h_afctor.text()),
                "e": float(self.e_afctor.text()),
                "l": float(self.l_afctor.text()),
                "a": float(self.a_afctor.text()),
                "radio": float(self.radio_afctor.text()),
                "fmax": float(self.fmax_afctor.text()),
                "fmin": float(self.fmin_afctor.text()),
                "brazo": float(self.b_afctor.text())
            }

            # Verificar si se seleccionó carga estática
            if self.cestatica_afctor.isChecked():

                print("Carga Estática")

                # Asignación de datos necesarios a variables

                sist_und = self.sist_und_afctor.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                fmax = diccionario_datos["fmax"]
                brazo = diccionario_datos["brazo"]
                carga = {"Fmax": fmax, "b": brazo}
                tipo_union = union_seleccionada
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, brazo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, brazo, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    self.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga transversal
                resultados = analisis.AnalisisSoldaduraFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria,
                                                              parametros_geometricos, espesor)

                # Resultados a mostrar en cuadros: x, y, r
                x, y = resultados.obtener_coordenadas_centroide()
                rx, ry = resultados.obtener_rx_ry()[0:2]
                r = str(round((rx ** 2 + ry ** 2) ** 0.5, 3))
                self.x_afctor.setText(str(round(x, 3)))
                self.y_afctor.setText(str(round(y, 3)))
                self.r_afctor.setText(r)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_ctor()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_filete_ctor(nombre_proyecto, "estática",
                                                                             dic_resultados_estatica,
                                                                             {},
                                                                             falla, self.sist_und_afctor.currentText(),
                                                                             self.und_fuerza_afctor_2.text(),
                                                                             self.und_distancia_afctor_2.text(),
                                                                             self.und_esfuerzo_afctor_2.text(),
                                                                             self.mb1_afctor.currentText(),
                                                                             self.mb2_afctor.currentText(),
                                                                             self.electrodo_afctor.currentText()
                                                                             )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_afctor.setText(info_resum[0])
                self.resumen_resultados_afctor.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_afctor.isChecked():

                # Asignación de datos necesarios a variables

                sist_und = self.sist_und_afctor.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                brazo = diccionario_datos["brazo"]
                carga = {"Fmax": fmax, "Fmin": fmin, "b": brazo}
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, brazo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, brazo, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    self.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis de fatiga de carga transversal
                resultados = analisis.AnalisisSoldaduraFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos, espesor)

                # Resultados a mostrar en cuadros: x, y, r
                x, y = resultados.obtener_coordenadas_centroide()
                rx, ry = resultados.obtener_rx_ry()[0:2]
                r = str(round((rx ** 2 + ry ** 2) ** 0.5, 3))
                self.x_afctor.setText(str(round(x, 3)))
                self.y_afctor.setText(str(round(y, 3)))
                self.r_afctor.setText(r)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_ctor()

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga = resultados.analisis_fatiga_ctor()[1]

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_filete_ctor(nombre_proyecto, "de fatiga",
                                                                             dic_resultados_estatica,
                                                                             dic_resultados_fatiga,
                                                                             falla, self.sist_und_afctor.currentText(),
                                                                             self.und_fuerza_afctor_2.text(),
                                                                             self.und_distancia_afctor_2.text(),
                                                                             self.und_esfuerzo_afctor_2.text(),
                                                                             self.mb1_afctor.currentText(),
                                                                             self.mb2_afctor.currentText(),
                                                                             self.electrodo_afctor.currentText()
                                                                             )
                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_afctor.setText(info_resum[0])
                self.resumen_resultados_afctor.setHtml(resumen)

            else:
                self.mostrar_msg_error()

        except:

            self.mostrar_msg_error()

        else:

            self.boton_guardar_afctor.setEnabled(True)

    # Evento para calcular FS para análisis de filete para carga combinada
    def calcular_fs_afcc(self):

        self.informe_resultados_afcc.clear()
        self.resumen_resultados_afcc.clear()

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_afcc,
            "cinco": self.g_5_afcc,
            "seis": self.g_6_afcc,
            "ocho": self.g_8_afcc,
            "nueve": self.g_9_afcc,
            "once": self.g_11_afcc,
            "doce": self.g_12_afcc
        }

        geometria_seleccionada = None

        # Obtencion de geometria seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "uno":
            self.a_afcc.setText("0")
            self.radio_afcc.setText("0")
        elif geometria_seleccionada == "ocho":
            self.l_afcc.setText("0")
            self.a_afcc.setText("0")
        else:
            self.radio_afcc.setText("0")

        if self.iden_proyecto_afcc is not None:
            nombre_proyecto = self.iden_proyecto_afcc.text()
        else:
            nombre_proyecto = "S/I"

        # Calculo de FS para carga estática
        try:
            # Casting de datos ingresados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_afcc.text()),
                "sut_mb1": float(self.sut_mb1_afcc.text()),
                "sy_mb2": float(self.sy_mb2_afcc.text()),
                "sut_mb2": float(self.sut_mb2_afcc.text()),
                "sy_e": float(self.sy_e_afcc.text()),
                "sut_e": float(self.sut_e_afcc.text()),
                "h": float(self.h_afcc.text()),
                "e": float(self.e_afcc.text()),
                "l": float(self.l_afcc.text()),
                "a": float(self.a_afcc.text()),
                "radio": float(self.radio_afcc.text()),
                "fmax": float(self.fmax_afcc.text()),
                "fmin": float(self.fmin_afcc.text()),
                "brazo_l": float(self.bl_afcc.text()),
                "brazo_t": float(self.bt_afcc.text())
            }

            # Verificar si se seleccionó carga estática
            if self.cestatica_afcc.isChecked():

                # Asignación de datos necesarios a variables

                sist_und = self.sist_und_afcc.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                fmax = diccionario_datos["fmax"]
                brazo_l = diccionario_datos["brazo_l"]
                brazo_t = diccionario_datos["brazo_t"]
                carga = {"Fmax": fmax, "bl": brazo_l, "bt": brazo_t}
                tipo_union = "Unión T"
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, brazo_l, brazo_t)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, brazo_l, brazo_t, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    self.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga de torsion
                resultados = analisis.AnalisisSoldaduraFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria,
                                                              parametros_geometricos, espesor)

                # Resultados a mostrar en cuadros: x, y, r, c
                x, y = resultados.obtener_coordenadas_centroide()
                rx, ry = resultados.obtener_rx_ry()[0:2]
                c = str(round(ry, 3))
                r = str(round((rx ** 2 + ry ** 2) ** 0.5, 3))
                self.x_afcc.setText(str(round(x, 3)))
                self.y_afcc.setText(str(round(y, 3)))
                self.r_afcc.setText(r)
                self.c_afcc.setText(c)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_ccomb()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_filete_cc(nombre_proyecto, "estática",
                                                                           dic_resultados_estatica,
                                                                           {},
                                                                           falla, self.sist_und_afcc.currentText(),
                                                                           self.und_fuerza_afcc_2.text(),
                                                                           self.und_distancia_afcc_2.text(),
                                                                           self.und_esfuerzo_afcc_2.text(),
                                                                           self.mb1_afcc.currentText(),
                                                                           self.mb2_afcc.currentText(),
                                                                           self.electrodo_afcc.currentText()
                                                                           )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_afcc.setText(info_resum[0])
                self.resumen_resultados_afcc.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_afcc.isChecked():

                # Asignación de datos necesarios a variables

                sist_und = self.sist_und_afcc.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Unión T"
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                brazo_l = diccionario_datos["brazo_l"]
                brazo_t = diccionario_datos["brazo_t"]
                carga = {"Fmax": fmax, "Fmin": fmin, "bl": brazo_l, "bt": brazo_t}
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, brazo_l, brazo_t)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, brazo_l, brazo_t, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    self.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis de fatiga de carga de torsion
                resultados = analisis.AnalisisSoldaduraFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos, espesor)

                # Resultados a mostrar en cuadros: x, y, r, c
                x, y = resultados.obtener_coordenadas_centroide()
                rx, ry = resultados.obtener_rx_ry()[0:2]
                c = str(round(ry, 3))
                r = str(round((rx ** 2 + ry ** 2) ** 0.5, 3))
                self.x_afcc.setText(str(round(x, 3)))
                self.y_afcc.setText(str(round(y, 3)))
                self.r_afcc.setText(r)
                self.c_afcc.setText(c)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_ccomb()

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga = resultados.analisis_fatiga_ccomb()[1]

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_filete_cc(nombre_proyecto, "de fatiga",
                                                                           dic_resultados_estatica,
                                                                           dic_resultados_fatiga,
                                                                           falla, self.sist_und_afcc.currentText(),
                                                                           self.und_fuerza_afcc_2.text(),
                                                                           self.und_distancia_afcc_2.text(),
                                                                           self.und_esfuerzo_afcc_2.text(),
                                                                           self.mb1_afcc.currentText(),
                                                                           self.mb2_afcc.currentText(),
                                                                           self.electrodo_afcc.currentText()
                                                                           )
                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_afcc.setText(info_resum[0])
                self.resumen_resultados_afcc.setHtml(resumen)

            else:

                self.mostrar_msg_error()

        except:

            self.mostrar_msg_error()

        else:

            self.boton_guardar_afcc.setEnabled(True)


# Clase para ventana de ranura. Hereda de la clase de ventana de filete
class VentanaAnalisisRanura(QMainWindow, ui_ventana_analisis_ranura):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Herencia de la clase de Analisis filete
        self.ventana_analisis_filete = VentanaAnalisisFilete()

        # Conexión de señales y slots

        ############################################################################################################

        # Señal para cambiar las etiquetas de sistema de unidades
        comboboxes_sist_und = [self.sist_und_arcp, self.sist_und_arct, self.sist_und_arcf,
                               self.sist_und_arctor, self.sist_und_arcc]

        for combobox in comboboxes_sist_und:
            combobox.currentIndexChanged.connect(self.evento_actualizar_etiquetas)

        ############################################################################################################

        # Señal para copiar nombre del acero y resistencias para piezas de igual material
        checkboxes_material_base = [self.mb_iguales_arcp, self.mb_iguales_arct, self.mb_iguales_arcf,
                                    self.mb_iguales_arctor, self.mb_iguales_arcc]

        for checkbox in checkboxes_material_base:
            checkbox.toggled.connect(self.evento_copiar_resistenias_mb)

        ############################################################################################################

        # Señal para extraer de la base de datos las resistencias del material base
        comboboxes_material_base = [self.mb1_arcp, self.mb1_arct, self.mb1_arcf, self.mb1_arctor, self.mb1_arcc,
                                    self.mb2_arcp, self.mb2_arct, self.mb2_arcf, self.mb2_arctor, self.mb2_arcc]

        for combobox in comboboxes_material_base:
            combobox.currentIndexChanged.connect(self.evento_resistencias_materiales_base)

        ############################################################################################################

        # Señal para extraer de la base de datos las resistencias del material de aporte
        comboboxes_material_aporte = [self.electrodo_arcp, self.electrodo_arct, self.electrodo_arcf,
                                      self.electrodo_arctor, self.electrodo_arcc]

        for combobox in comboboxes_material_aporte:
            combobox.currentIndexChanged.connect(self.resistencias_material_aporte)

        ############################################################################################################

        # Diccionario de qlineedits de ingreso de datos
        qlineedit_datos_entrada = {
            "Carga paralela": [self.sy_mb1_arcp, self.sut_mb1_arcp,
                               self.sy_mb2_arcp, self.sut_mb2_arcp,
                               self.sy_e_arcp, self.sut_e_arcp,
                               self.t_arcp, self.l_arcp,
                               self.fmax_arcp, self.fmin_arcp],
            "Carga transversal": [self.sy_mb1_arct, self.sy_mb2_arct,
                                  self.sut_mb1_arct, self.sut_mb2_arct,
                                  self.sy_e_arct, self.sut_e_arct,
                                  self.t_arct, self.l_arct, self.radio_arct,
                                  self.fmax_arct, self.fmin_arct],
            "Carga de flexión": [self.sy_mb1_arcf, self.sy_mb2_arcf,
                                 self.sut_mb1_arcf, self.sut_mb2_arcf,
                                 self.sy_e_arcf, self.sut_e_arcf,
                                 self.t_arcf, self.l_arcf, self.radio_arcf,
                                 self.fmax_arcf, self.fmin_arcf, self.b_arcf],
            "Carga de torsión": [self.sy_mb1_arctor, self.sy_mb2_arctor,
                                 self.sut_mb1_arctor, self.sut_mb2_arctor,
                                 self.sy_e_arctor, self.sut_e_arctor,
                                 self.t_arctor, self.l_arctor, self.radio_arctor,
                                 self.tmax_arctor, self.tmin_arctor],
            "Carga combinada": [self.sy_mb1_arcc, self.sy_mb2_arcc,
                                self.sut_mb1_arcc, self.sut_mb2_arcc,
                                self.sy_e_arcc, self.sut_e_arcc,
                                self.t_arcc, self.l_arcc, self.radio_arcc,
                                self.fmax_arcc, self.fmin_arcc,
                                self.bl_arcc, self.bt_arcc]
        }

        # Asignar validador en qlineedits para permitir sólo ingreso de floats
        for tipo_carga, qlineedits in qlineedit_datos_entrada.items():
            for qlineedit in qlineedits:
                qlineedit.setValidator(QDoubleValidator())

        ############################################################################################################

        # Señal de boton en barra menu de volver a inicio
        self.actionVolver_al_inicio.triggered.connect(self.cerrar_y_volver_a_inicio)

        # Señal de boton en barra menu de cerrar
        self.actionCerrar.triggered.connect(self.cerrar_ventana)

        # Señal de boton en barra menú para cálculo nuevo
        self.actionNuevo_calculo.triggered.connect(self.evento_limpiar_tab_actionnuevocalculo)

        # SEÑALES PARA BOTONES DE CALCULAR FS

        # Carga paralela
        self.boton_calcularfs_arcp.clicked.connect(self.calcular_fs_arcp)

        # Carga transversal
        self.boton_calcularfs_arct.clicked.connect(self.calcular_fs_arct)

        # Carga de flexion
        self.boton_calcularfs_arcf.clicked.connect(self.calcular_fs_arcf)

        # Carga de torsion
        self.boton_calcularfs_arctor.clicked.connect(self.calcular_fs_arctor)

        # Carga de torsion
        self.boton_calcularfs_arcc.clicked.connect(self.calcular_fs_arcc)

        # SEÑALES PARA GUARDAR INFORMES

        # Carga paralela
        self.boton_guardar_arcp.clicked.connect(self.evento_guardar)

        # Carga transversal
        self.boton_guardar_arct.clicked.connect(self.evento_guardar)

        # Carga de flexion
        self.boton_guardar_arcf.clicked.connect(self.evento_guardar)

        # Carga de torsion
        self.boton_guardar_arctor.clicked.connect(self.evento_guardar)

        # Carga combinada
        self.boton_guardar_arcc.clicked.connect(self.evento_guardar)

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def evento_actualizar_etiquetas(self):
        """Slot para el evento de cambio de indice de la lista desplegable de sistema de unidades.
       Realiza acciones específicas al seleccionar un indice de la lista desplegable.
       """

        # Diccionario de objetos etiquetas con unidades de esfuerzo, distancia y fuerza
        etiquetas_unidades = {
            self.sist_und_arct: {
                'esfuerzo': [self.und_esfuerzo_arct_1,
                             self.und_esfuerzo_arct_2,
                             self.und_esfuerzo_arct_3,
                             self.und_esfuerzo_arct_4,
                             self.und_esfuerzo_arct_5,
                             self.und_esfuerzo_arct_6],
                'distancia': [self.und_distancia_arct_1,
                              self.und_distancia_arct_2,
                              self.und_distancia_arct_3],
                'fuerza': [self.und_fuerza_arct_1,
                           self.und_fuerza_arct_2],
                'torque': []
            },
            self.sist_und_arcp: {
                "esfuerzo": [self.und_esfuerzo_arcp_1,
                             self.und_esfuerzo_arcp_2,
                             self.und_esfuerzo_arcp_3,
                             self.und_esfuerzo_arcp_4,
                             self.und_esfuerzo_arcp_5,
                             self.und_esfuerzo_arcp_6],
                'distancia': [self.und_distancia_arcp_1,
                              self.und_distancia_arcp_2],
                'fuerza': [self.und_fuerza_arcp_1,
                           self.und_fuerza_arcp_2],
                'torque': []
            },
            self.sist_und_arcf: {
                "esfuerzo": [self.und_esfuerzo_arcf_1,
                             self.und_esfuerzo_arcf_2,
                             self.und_esfuerzo_arcf_3,
                             self.und_esfuerzo_arcf_4,
                             self.und_esfuerzo_arcf_5,
                             self.und_esfuerzo_arcf_6],
                'distancia': [self.und_distancia_arcf_1,
                              self.und_distancia_arcf_2,
                              self.und_distancia_arcf_3,
                              self.und_distancia_arcf_4],
                'fuerza': [self.und_fuerza_arcf_1,
                           self.und_fuerza_arcf_2],
                'torque': []
            },
            self.sist_und_arctor: {
                'esfuerzo': [self.und_esfuerzo_arctor_1,
                             self.und_esfuerzo_arctor_2,
                             self.und_esfuerzo_arctor_3,
                             self.und_esfuerzo_arctor_4,
                             self.und_esfuerzo_arctor_5,
                             self.und_esfuerzo_arctor_6],
                'distancia': [self.und_distancia_arctor_1,
                              self.und_distancia_arctor_2,
                              self.und_distancia_arctor_3],
                'fuerza': [],
                'torque': [self.und_torque_arctor_1,
                           self.und_torque_arctor_2]
            },
            self.sist_und_arcc: {
                'esfuerzo': [self.und_esfuerzo_arcc_1,
                             self.und_esfuerzo_arcc_2,
                             self.und_esfuerzo_arcc_3,
                             self.und_esfuerzo_arcc_4,
                             self.und_esfuerzo_arcc_5,
                             self.und_esfuerzo_arcc_6],
                'distancia': [self.und_distancia_arcc_1,
                              self.und_distancia_arcc_2,
                              self.und_distancia_arcc_3,
                              self.und_distancia_arcc_4,
                              self.und_distancia_arcc_5],
                'fuerza': [self.und_fuerza_arcc_1,
                           self.und_fuerza_arcc_2],
                'torque': []
            }
        }

        # Código para el evento

        # Obtener objeto que emite la señal y su contenido
        objeto = self.sender()
        contenido_objeto = self.sender().currentText()

        # Uso del método de clase para cambiar contenido sist und de etiquetas
        VentanaAnalisisFilete.cambiar_etiquetas(etiquetas_unidades, objeto, contenido_objeto)

    def evento_copiar_resistenias_mb(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
         Realiza acciones específicas al hacer click en el radiobutton.
         """
        # Código para el evento

        widgets_material_base = [
            {
                "mb_iguales": self.mb_iguales_arcp,
                "mb1": self.mb1_arcp,
                "mb2": self.mb2_arcp,
                "sy_mb1": self.sy_mb1_arcp,
                "sut_mb1": self.sut_mb1_arcp,
                "sy_mb2": self.sy_mb2_arcp,
                "sut_mb2": self.sut_mb2_arcp
            },
            {
                "mb_iguales": self.mb_iguales_arct,
                "mb1": self.mb1_arct,
                "mb2": self.mb2_arct,
                "sy_mb1": self.sy_mb1_arct,
                "sut_mb1": self.sut_mb1_arct,
                "sy_mb2": self.sy_mb2_arct,
                "sut_mb2": self.sut_mb2_arct
            },
            {
                "mb_iguales": self.mb_iguales_arcf,
                "mb1": self.mb1_arcf,
                "mb2": self.mb2_arcf,
                "sy_mb1": self.sy_mb1_arcf,
                "sut_mb1": self.sut_mb1_arcf,
                "sy_mb2": self.sy_mb2_arcf,
                "sut_mb2": self.sut_mb2_arcf
            },
            {
                "mb_iguales": self.mb_iguales_arctor,
                "mb1": self.mb1_arctor,
                "mb2": self.mb2_arctor,
                "sy_mb1": self.sy_mb1_arctor,
                "sut_mb1": self.sut_mb1_arctor,
                "sy_mb2": self.sy_mb2_arctor,
                "sut_mb2": self.sut_mb2_arctor
            },
            {
                "mb_iguales": self.mb_iguales_arcc,
                "mb1": self.mb1_arcc,
                "mb2": self.mb2_arcc,
                "sy_mb1": self.sy_mb1_arcc,
                "sut_mb1": self.sut_mb1_arcc,
                "sy_mb2": self.sy_mb2_arcc,
                "sut_mb2": self.sut_mb2_arcc
            }

        ]

        VentanaAnalisisFilete.copiar_resistencias_mb(widgets_material_base)

    def evento_resistencias_materiales_base(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
        Realiza acciones específicas al cambiar el contenido del combobox.
        """
        # Código para el evento

        # Diccionario de dependecia de objetos (lista desplegable de sistund, lista de materiales, lineas de texto
        mb_comboboxes = {
            self.sist_und_arcp: {
                self.mb1_arcp: (self.sy_mb1_arcp, self.sut_mb1_arcp),
                self.mb2_arcp: (self.sy_mb2_arcp, self.sut_mb2_arcp)
            },
            self.sist_und_arct: {
                self.mb1_arct: (self.sy_mb1_arct, self.sut_mb1_arct),
                self.mb2_arct: (self.sy_mb2_arct, self.sut_mb2_arct)
            },
            self.sist_und_arcf: {
                self.mb1_arcf: (self.sy_mb1_arcf, self.sut_mb1_arcf),
                self.mb2_arcf: (self.sy_mb2_arcf, self.sut_mb2_arcf)
            },
            self.sist_und_arctor: {
                self.mb1_arctor: (self.sy_mb1_arctor, self.sut_mb1_arctor),
                self.mb2_arctor: (self.sy_mb2_arctor, self.sut_mb2_arctor)
            },
            self.sist_und_arcc: {
                self.mb1_arcc: (self.sy_mb1_arcc, self.sut_mb1_arcc),
                self.mb2_arcc: (self.sy_mb2_arcc, self.sut_mb2_arcc)
            }
        }

        # Obtener objeto que emite la señal
        objeto = self.sender()

        # Obtener contenido del objeto que emite la señal (nombre de material seleccionado de lista desplegable)
        contenido_objeto = self.sender().currentText()

        widgets_material_base = [
            {
                "mb_iguales": self.mb_iguales_arcp,
                "mb1": self.mb1_arcp,
                "mb2": self.mb2_arcp,
                "sy_mb1": self.sy_mb1_arcp,
                "sut_mb1": self.sut_mb1_arcp,
                "sy_mb2": self.sy_mb2_arcp,
                "sut_mb2": self.sut_mb2_arcp
            },
            {
                "mb_iguales": self.mb_iguales_arct,
                "mb1": self.mb1_arct,
                "mb2": self.mb2_arct,
                "sy_mb1": self.sy_mb1_arct,
                "sut_mb1": self.sut_mb1_arct,
                "sy_mb2": self.sy_mb2_arct,
                "sut_mb2": self.sut_mb2_arct
            },
            {
                "mb_iguales": self.mb_iguales_arcf,
                "mb1": self.mb1_arcf,
                "mb2": self.mb2_arcf,
                "sy_mb1": self.sy_mb1_arcf,
                "sut_mb1": self.sut_mb1_arcf,
                "sy_mb2": self.sy_mb2_arcf,
                "sut_mb2": self.sut_mb2_arcf
            },
            {
                "mb_iguales": self.mb_iguales_arctor,
                "mb1": self.mb1_arctor,
                "mb2": self.mb2_arctor,
                "sy_mb1": self.sy_mb1_arctor,
                "sut_mb1": self.sut_mb1_arctor,
                "sy_mb2": self.sy_mb2_arctor,
                "sut_mb2": self.sut_mb2_arctor
            },
            {
                "mb_iguales": self.mb_iguales_arcc,
                "mb1": self.mb1_arcc,
                "mb2": self.mb2_arcc,
                "sy_mb1": self.sy_mb1_arcc,
                "sut_mb1": self.sut_mb1_arcc,
                "sy_mb2": self.sy_mb2_arcc,
                "sut_mb2": self.sut_mb2_arcc
            }
        ]

        VentanaAnalisisFilete.obtencion_resistencias_mb(widgets_material_base, mb_comboboxes, objeto, contenido_objeto)

    def resistencias_material_aporte(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
           Realiza acciones específicas al seleccionar un tipo de electrodo de la lista desplegable.
           """

        # Código para el evento

        # Diccionario de dependencia de objetos (lista de electrodos, campos de resistencia para cada ventana)
        """Material de aporte comboboxes"""
        ma_comboboxes = {
            self.sist_und_arcp: {
                self.electrodo_arcp: (self.sy_e_arcp,
                                      self.sut_e_arcp)
            },
            self.sist_und_arct: {
                self.electrodo_arct: (self.sy_e_arct,
                                      self.sut_e_arct)
            },
            self.sist_und_arcf: {
                self.electrodo_arcf: (self.sy_e_arcf,
                                      self.sut_e_arcf)
            },
            self.sist_und_arctor: {
                self.electrodo_arctor: (self.sy_e_arctor,
                                        self.sut_e_arctor)
            },
            self.sist_und_arcc: {
                self.electrodo_arcc: (self.sy_e_arcc,
                                      self.sut_e_arcc)
            }
        }

        # Obtener objeto y contenido del objeto que emite la señal
        objeto = self.sender()
        contenido_objeto = self.sender().currentText()

        VentanaAnalisisFilete.obtencion_resistencias_ma(ma_comboboxes, objeto, contenido_objeto)

    # Evento para limpiar los campos necesarios para realizar un nuevo cálculo
    def evento_limpiar_tab_actionnuevocalculo(self):

        # Obtener pestaña activa
        tab_widget = self.tab_widget
        tab_activa_index = tab_widget.currentIndex()
        tab_activa = tab_widget.widget(tab_activa_index)

        # Colocar todos los QlineEdits en 0 (datos de entrada)
        for widget in tab_activa.findChildren(QLineEdit):
            if isinstance(widget, QLineEdit):
                widget.setText("0")

        # Vaciar el contenido de todos los QTextBrowsers (resumen e informe de resultados)
        for widget in tab_activa.findChildren(QTextBrowser):
            if isinstance(widget, QTextBrowser):
                widget.setText("")

        # Deseleccionar el nombre de algún material
        for widget in tab_activa.findChildren(QComboBox):
            if isinstance(widget, QComboBox):
                widget.setCurrentText("")

        # Deseleccionar los QRadioButtons
        for widget in tab_activa.findChildren(QRadioButton):
            if isinstance(widget, QRadioButton):
                widget.setChecked(False)

    def cerrar_y_volver_a_inicio(self):
        """
        Slot para el evento de clic del botón de Volver a inicio en la barra menú.
        Realiza acciones específicas al presionar el botón.
        """

        # Declarar la ventana como una clase
        self.ventana_volver_inicio = VentanaPrincipal()

        # Abrir ventana de análisis de ranura
        self.ventana_volver_inicio.show()

        # Cerrar ventana de análisis de filete
        self.close()

    def cerrar_ventana(self):
        self.close()

    # Evento para calcular el FS para analisis de ranura para carga paralela
    def calcular_fs_arcp(self):

        self.informe_resultados_arcp.clear()
        self.resumen_resultados_arcp.clear()

        if self.iden_proyecto_arcp is not None:
            nombre_proyecto = self.iden_proyecto_arcp.text()
        else:
            nombre_proyecto = "S/I"

        # Calculo de FS para carga estática

        # Verificar si se seleccionó carga estática
        try:

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_arcp.text()),
                "sut_mb1": float(self.sut_mb1_arcp.text()),
                "sy_mb2": float(self.sy_mb2_arcp.text()),
                "sut_mb2": float(self.sut_mb2_arcp.text()),
                "sy_e": float(self.sy_e_arcp.text()),
                "sut_e": float(self.sut_e_arcp.text()),
                "t": float(self.t_arcp.text()),
                "l": float(self.l_arcp.text()),
                "fmax": float(self.fmax_arcp.text()),
                "fmin": float(self.fmin_arcp.text())
            }

            if self.cestatica_arcp.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_arcp.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Tope"
                fmax = diccionario_datos["fmax"]
                carga = {"Fmax": fmax}
                geometria = "uno"
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                parametros_geometricos = {"espesor": garganta, "largo": largo}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = analisis.AnalisisSoldaduraRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_cp()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_ranura_cp(nombre_proyecto, "estática",
                                                                           dic_resultados_estatica,
                                                                           {},
                                                                           falla, self.sist_und_arcp.currentText(),
                                                                           self.und_fuerza_arcp_2.text(),
                                                                           self.und_distancia_arcp_2.text(),
                                                                           self.und_esfuerzo_arcp_2.text(),
                                                                           self.mb1_arcp.currentText(),
                                                                           self.mb2_arcp.currentText(),
                                                                           self.electrodo_arcp.currentText()
                                                                           )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_arcp.setText(info_resum[0])
                self.resumen_resultados_arcp.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_arcp.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_arcp.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Tope"
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                carga = {"Fmax": fmax, "Fmin": fmin}
                geometria = "uno"
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                parametros_geometricos = {"espesor": garganta, "largo": largo}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = analisis.AnalisisSoldaduraRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_cp()

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga = resultados.analisis_fatiga_cp()[1]

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_ranura_cp(nombre_proyecto, "de fatiga",
                                                                           dic_resultados_estatica,
                                                                           dic_resultados_fatiga,
                                                                           falla, self.sist_und_arcp.currentText(),
                                                                           self.und_fuerza_arcp_2.text(),
                                                                           self.und_distancia_arcp_2.text(),
                                                                           self.und_esfuerzo_arcp_2.text(),
                                                                           self.mb1_arcp.currentText(),
                                                                           self.mb2_arcp.currentText(),
                                                                           self.electrodo_arcp.currentText()
                                                                           )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_arcp.setText(info_resum[0])
                self.resumen_resultados_arcp.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_arcp.setEnabled(True)

    # Evento para calcular el FS para analisis de ranura para carga transversal
    def calcular_fs_arct(self):

        self.informe_resultados_arct.clear()
        self.resumen_resultados_arct.clear()

        if self.iden_proyecto_arct is not None:
            nombre_proyecto = self.iden_proyecto_arct.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_arct,
            "tres": self.g_3_arct,
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "tres":
            self.l_arct.setText("0")
        else:
            self.radio_arct.setText("0")

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Tope": self.union_tope_arct,
            "Unión T": self.union_t_arct
        }

        union_seleccionada = None

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Calculo de FS para carga estática

        # Verificar si se seleccionó carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_arct.text()),
                "sut_mb1": float(self.sut_mb1_arct.text()),
                "sy_mb2": float(self.sy_mb2_arct.text()),
                "sut_mb2": float(self.sut_mb2_arct.text()),
                "sy_e": float(self.sy_e_arct.text()),
                "sut_e": float(self.sut_e_arct.text()),
                "t": float(self.t_arct.text()),
                "l": float(self.l_arct.text()),
                "radio": float(self.radio_arct.text()),
                "fmax": float(self.fmax_arct.text()),
                "fmin": float(self.fmin_arct.text())
            }

            if self.cestatica_arct.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_arct.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                carga = {"Fmax": fmax}
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, fmax, radio)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                if geometria == "tres" and garganta >= radio:
                    VentanaAnalisisRanura.mostrar_msg_aviso_espesor()

                # Instancia para el análisis estático de carga paralela
                resultados = analisis.AnalisisSoldaduraRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_ctrans()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_ranura_ct(nombre_proyecto, "estática",
                                                                           dic_resultados_estatica,
                                                                           {},
                                                                           falla, self.sist_und_arct.currentText(),
                                                                           self.und_fuerza_arct_2.text(),
                                                                           self.und_distancia_arct_2.text(),
                                                                           self.und_esfuerzo_arct_2.text(),
                                                                           self.mb1_arct.currentText(),
                                                                           self.mb2_arct.currentText(),
                                                                           self.electrodo_arct.currentText()
                                                                           )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_arct.setText(info_resum[0])
                self.resumen_resultados_arct.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_arct.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_arct.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                carga = {"Fmax": fmax, "Fmin": fmin}
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, fmax, radio)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                if geometria == "tres" and garganta >= radio:
                    VentanaAnalisisRanura.mostrar_msg_aviso_espesor()

                # Instancia para el análisis estático de carga paralela
                resultados = analisis.AnalisisSoldaduraRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_ctrans()

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga = resultados.analisis_fatiga_ctrans()[1]

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_ranura_ct(nombre_proyecto, "de fatiga",
                                                                           dic_resultados_estatica,
                                                                           dic_resultados_fatiga,
                                                                           falla, self.sist_und_arct.currentText(),
                                                                           self.und_fuerza_arct_2.text(),
                                                                           self.und_distancia_arct_2.text(),
                                                                           self.und_esfuerzo_arct_2.text(),
                                                                           self.mb1_arct.currentText(),
                                                                           self.mb2_arct.currentText(),
                                                                           self.electrodo_arct.currentText()
                                                                           )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_arct.setText(info_resum[0])
                self.resumen_resultados_arct.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_arct.setEnabled(True)

    # Evento para calcular el FS para analisis de ranura para carga de flexion
    def calcular_fs_arcf(self):

        self.informe_resultados_arcf.clear()
        self.resumen_resultados_arcf.clear()

        if self.iden_proyecto_arct is not None:
            nombre_proyecto = self.iden_proyecto_arct.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_arcf,
            "dos": self.g_2_arcf,
            "tres": self.g_3_arcf
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "tres":
            self.l_arcf.setText("0")
        else:
            self.radio_arcf.setText("0")

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Tope": self.union_tope_arcf,
            "Unión T": self.union_t_arcf
        }

        union_seleccionada = None

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Calculo de FS para carga estática

        # Verificar si se seleccionó carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_arcf.text()),
                "sut_mb1": float(self.sut_mb1_arcf.text()),
                "sy_mb2": float(self.sy_mb2_arcf.text()),
                "sut_mb2": float(self.sut_mb2_arcf.text()),
                "sy_e": float(self.sy_e_arcf.text()),
                "sut_e": float(self.sut_e_arcf.text()),
                "t": float(self.t_arcf.text()),
                "l": float(self.l_arcf.text()),
                "radio": float(self.radio_arcf.text()),
                "fmax": float(self.fmax_arcf.text()),
                "fmin": float(self.fmin_arcf.text()),
                "brazo": float(self.b_arcf.text())
            }

            if self.cestatica_arcf.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_arcf.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                brazo = diccionario_datos["brazo"]
                carga = {"Fmax": fmax, "b": brazo}
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, fmax, radio)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = analisis.AnalisisSoldaduraRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_cflex()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_ranura_cf(nombre_proyecto, "estática",
                                                                           dic_resultados_estatica,
                                                                           {},
                                                                           falla, self.sist_und_arcf.currentText(),
                                                                           self.und_fuerza_arcf_2.text(),
                                                                           self.und_distancia_arcf_2.text(),
                                                                           self.und_esfuerzo_arcf_2.text(),
                                                                           self.mb1_arcf.currentText(),
                                                                           self.mb2_arcf.currentText(),
                                                                           self.electrodo_arcf.currentText()
                                                                           )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_arcf.setText(info_resum[0])
                self.resumen_resultados_arcf.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_arcf.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_arcf.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                brazo = diccionario_datos["brazo"]
                carga = {"Fmax": fmax, "Fmin": fmin, "b": brazo}
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, fmax, radio)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = analisis.AnalisisSoldaduraRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_cflex()
                print(dic_resultados_estatica)

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga = resultados.analisis_fatiga_cflex()[1]

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_ranura_cf(nombre_proyecto, "de fatiga",
                                                                           dic_resultados_estatica,
                                                                           dic_resultados_fatiga,
                                                                           falla, self.sist_und_arcf.currentText(),
                                                                           self.und_fuerza_arcf_2.text(),
                                                                           self.und_distancia_arcf_2.text(),
                                                                           self.und_esfuerzo_arcf_2.text(),
                                                                           self.mb1_arcf.currentText(),
                                                                           self.mb2_arcf.currentText(),
                                                                           self.electrodo_arcf.currentText()
                                                                           )
                print(dic_resultados_fatiga)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_arcf.setText(info_resum[0])
                self.resumen_resultados_arcf.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_arcf.setEnabled(True)

    # Evento para calcular el FS para analisis de ranura para carga de torsion
    def calcular_fs_arctor(self):

        self.informe_resultados_arctor.clear()
        self.resumen_resultados_arctor.clear()

        if self.iden_proyecto_arctor is not None:
            nombre_proyecto = self.iden_proyecto_arctor.text()
        else:
            nombre_proyecto = "S/I"

        print(1)

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_arctor,
            "tres": self.g_3_arctor,
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        print(2)

        if geometria_seleccionada == "tres":
            self.l_arctor.setText("0")
        else:
            self.radio_arctor.setText("0")

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Tope": self.union_tope_arctor,
            "Unión T": self.union_t_arctor
        }

        union_seleccionada = None

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Calculo de FS para carga estática

        # Verificar si se seleccionó carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_arctor.text()),
                "sut_mb1": float(self.sut_mb1_arctor.text()),
                "sy_mb2": float(self.sy_mb2_arctor.text()),
                "sut_mb2": float(self.sut_mb2_arctor.text()),
                "sy_e": float(self.sy_e_arctor.text()),
                "sut_e": float(self.sut_e_arctor.text()),
                "t": float(self.t_arctor.text()),
                "l": float(self.l_arctor.text()),
                "radio": float(self.radio_arctor.text()),
                "tmax": float(self.tmax_arctor.text()),
                "tmin": float(self.tmin_arctor.text())
            }

            if self.cestatica_arctor.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_arctor.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                tmax = diccionario_datos["tmax"]
                carga = {"Tmax": tmax}
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, tmax, radio)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el análisis estático de carga paralela
                resultados = analisis.AnalisisSoldaduraRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_ctor()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_ranura_ctor(nombre_proyecto, "estática",
                                                                             dic_resultados_estatica,
                                                                             {},
                                                                             falla, self.sist_und_arctor.currentText(),
                                                                             und_fuerza,
                                                                             self.und_distancia_arctor_1.text(),
                                                                             self.und_esfuerzo_arctor_1.text(),
                                                                             self.mb1_arctor.currentText(),
                                                                             self.mb2_arctor.currentText(),
                                                                             self.electrodo_arctor.currentText()
                                                                             )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_arctor.setText(info_resum[0])
                self.resumen_resultados_arctor.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_arctor.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_arctor.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                tmax = diccionario_datos["tmax"]
                tmin = diccionario_datos["tmin"]
                carga = {"Tmax": tmax, "Tmin": tmin}
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, tmax, radio)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el análisis estático de carga paralela
                resultados = analisis.AnalisisSoldaduraRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_ctor()

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga = resultados.analisis_fatiga_ctor()[1]

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_ranura_ctor(nombre_proyecto, "de fatiga",
                                                                             dic_resultados_estatica,
                                                                             dic_resultados_fatiga,
                                                                             falla, self.sist_und_arctor.currentText(),
                                                                             und_fuerza,
                                                                             self.und_distancia_arctor_1.text(),
                                                                             self.und_esfuerzo_arctor_1.text(),
                                                                             self.mb1_arctor.currentText(),
                                                                             self.mb2_arctor.currentText(),
                                                                             self.electrodo_arctor.currentText()
                                                                             )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_arctor.setText(info_resum[0])
                self.resumen_resultados_arctor.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_arctor.setEnabled(True)

    # Evento para calcular el FS para analisis de ranura para carga combinada
    def calcular_fs_arcc(self):

        self.informe_resultados_arcc.clear()
        self.resumen_resultados_arcc.clear()

        if self.iden_proyecto_arcc is not None:
            nombre_proyecto = self.iden_proyecto_arcc.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_arcc,
            "dos": self.g_2_arcc,
            "tres": self.g_3_arcc,
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "tres":
            self.l_arcc.setText("0")
        else:
            self.radio_arcc.setText("0")

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Tope": self.union_tope_arcc,
            "Unión T": self.union_t_arcc
        }

        union_seleccionada = None

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Calculo de FS para carga estática

        # Verificar si se seleccionó carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_arcc.text()),
                "sut_mb1": float(self.sut_mb1_arcc.text()),
                "sy_mb2": float(self.sy_mb2_arcc.text()),
                "sut_mb2": float(self.sut_mb2_arcc.text()),
                "sy_e": float(self.sy_e_arcc.text()),
                "sut_e": float(self.sut_e_arcc.text()),
                "t": float(self.t_arcc.text()),
                "l": float(self.l_arcc.text()),
                "radio": float(self.radio_arcc.text()),
                "fmax": float(self.fmax_arcc.text()),
                "fmin": float(self.fmin_arcc.text()),
                "bl": float(self.bl_arcc.text()),
                "bt": float(self.bt_arcc.text())
            }

            if self.cestatica_arcc.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_arcc.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                bl = diccionario_datos["bl"]
                bt = diccionario_datos["bt"]
                carga = {"Fmax": fmax, "bl": bl, "bt": bt}
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta, bl, bt)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, fmax, radio, bl, bt)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = analisis.AnalisisSoldaduraRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_ccomb()

                print(3)

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_ranura_ccomb(nombre_proyecto, "estática",
                                                                              dic_resultados_estatica,
                                                                              {}, falla,
                                                                              self.sist_und_arcc.currentText(),
                                                                              self.und_fuerza_arcc_1.text(),
                                                                              self.und_distancia_arcc_1.text(),
                                                                              self.und_esfuerzo_arcc_2.text(),
                                                                              self.mb1_arcc.currentText(),
                                                                              self.mb2_arcc.currentText(),
                                                                              self.electrodo_arcc.currentText()
                                                                              )

                print(4)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_arcc.setText(info_resum[0])
                self.resumen_resultados_arcc.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_arcc.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_arcc.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                bl = diccionario_datos["bl"]
                bt = diccionario_datos["bt"]

                carga = {"Fmax": fmax, "Fmin": fmin, "bl": bl, "bt": bt}
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta, bl, bt)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, fmax, radio, bl, bt)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = analisis.AnalisisSoldaduraRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                              geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                falla, dic_resultados_estatica = resultados.analisis_estatico_ccomb()

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga = resultados.analisis_fatiga_ccomb()[1]

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_analisis_ranura_ccomb(nombre_proyecto, "de fatiga",
                                                                              dic_resultados_estatica,
                                                                              dic_resultados_fatiga, falla,
                                                                              self.sist_und_arcc.currentText(),
                                                                              self.und_fuerza_arcc_1.text(),
                                                                              self.und_distancia_arcc_1.text(),
                                                                              self.und_esfuerzo_arcc_2.text(),
                                                                              self.mb1_arcc.currentText(),
                                                                              self.mb2_arcc.currentText(),
                                                                              self.electrodo_arcc.currentText()
                                                                              )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_arcc.setText(info_resum[0])
                self.resumen_resultados_arcc.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_arcc.setEnabled(True)

    def evento_guardar(self):
        """
        Método de evento para manejar la señal de clic en un botón de guardar.

        Obtiene el botón que emite la señal y llama al método 'guardar_informe' para guardar el informe asociado al botón.
        """

        dic_botones = {
            self.boton_guardar_arcp: self.informe_resultados_arcp,
            self.boton_guardar_arct: self.informe_resultados_arct,
            self.boton_guardar_arcf: self.informe_resultados_arcf,
            self.boton_guardar_arctor: self.informe_resultados_arctor,
            self.boton_guardar_arcc: self.informe_resultados_arcc
        }

        objeto = self.sender()

        VentanaAnalisisFilete.guardar_informe(self, objeto, dic_botones)


# Clase para ventana de seleccion de tipo de diseño
class VentanaSeleccionDiseno(QDialog, ui_ventana_seleccion_diseno):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.abrir_ventana_seleccionada)  # Conexión al botón OK
        self.buttonBox.rejected.connect(self.abrir_ventana_principal)  # Conexión al botón CANCEL

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def abrir_ventana_seleccionada(self):
        seleccion = self.seleccion.currentText()

        if seleccion == "Carga permisible":
            # Abre la ventana correspondiente a la Opción 1
            self.ventana_disenocarga_filete = VentanaDisenoCargaFilete()
            self.ventana_disenocarga_filete.show()

        elif seleccion == "Pierna del cordón de soldadura":
            # Abre la ventana correspondiente a la Opción 2
            self.ventana_disenoh = VentanaDisenoPiernaFilete()
            self.ventana_disenoh.show()

        # Cerrar ventana de dialogo
        self.close()

    def abrir_ventana_principal(self):
        # Declarar la ventana como una clase
        self.ventana_inicio = VentanaPrincipal()

        # Abrir ventana de análisis de ranura
        self.ventana_inicio.show()

        self.close()


class VentanaSeleccionDisenoRanura(QDialog, ui_ventana_seleccion_diseno_ranura):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.abrir_ventana_seleccionada)  # Conexión al botón OK
        self.buttonBox.rejected.connect(self.abrir_ventana_principal)  # Conexión al botón CANCEL

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def abrir_ventana_seleccionada(self):
        seleccion = self.seleccion.currentText()

        if seleccion == "Carga permisible":
            # Abre la ventana correspondiente a la Opción 1
            self.ventana_disenocarga_ranura = VentanaDisenoRanura()
            self.ventana_disenocarga_ranura.show()

        elif seleccion == "Espesor mínimo del cordón":
            # Abre la ventana correspondiente a la Opción 2
            self.ventana_disenoespesor_ranura = VentanaDisenoEspesorRanura()
            self.ventana_disenoespesor_ranura.show()

        # Cerrar ventana de diálogo
        self.close()

    def abrir_ventana_principal(self):
        # Declarar la ventana como una clase
        self.ventana_inicio = VentanaPrincipal()

        # Abrir ventana de análisis de ranura
        self.ventana_inicio.show()

        self.close()


class VentanaDisenoCargaFilete(QMainWindow, ui_ventana_disenocarga_filete):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ventana_analisis_filete = VentanaAnalisisFilete()

        # Conexión de señales y slots

        ############################################################################################################

        # Señal para cambiar las etiquetas de sistema de unidades
        comboboxes_sist_und = [self.sist_und_dfcp, self.sist_und_dfct, self.sist_und_dfcf,
                               self.sist_und_dfctor, self.sist_und_dfcc]

        for combobox in comboboxes_sist_und:
            combobox.currentIndexChanged.connect(self.evento_actualizar_etiquetas)

        ############################################################################################################

        # Señal para copiar nombre del acero y resistencias para piezas de igual material
        checkboxes_material_base = [self.mb_iguales_dfcp, self.mb_iguales_dfct, self.mb_iguales_dfcf,
                                    self.mb_iguales_dfctor, self.mb_iguales_dfcc]

        for checkbox in checkboxes_material_base:
            checkbox.toggled.connect(self.evento_copiar_resistencias_mb)

        ############################################################################################################

        # Señal para extraer de la base de datos las resistencias del material base
        comboboxes_material_base = [self.mb1_dfcp, self.mb1_dfct, self.mb1_dfcf, self.mb1_dfctor, self.mb1_dfcc,
                                    self.mb2_dfcp, self.mb2_dfct, self.mb2_dfcf, self.mb2_dfctor, self.mb2_dfcc]

        for combobox in comboboxes_material_base:
            combobox.currentIndexChanged.connect(self.evento_resistencias_materiales_base)

        ############################################################################################################

        # Señal para extraer de la base de datos las resistencias del material de aporte
        comboboxes_material_aporte = [self.electrodo_dfcp, self.electrodo_dfct, self.electrodo_dfcf,
                                      self.electrodo_dfctor, self.electrodo_dfcc]

        for combobox in comboboxes_material_aporte:
            combobox.currentIndexChanged.connect(self.resistencias_material_aporte)

        ############################################################################################################

        # Diccionario de qlineedits de ingreso de datos
        qlineedit_datos_entrada = {
            "Carga paralela": [self.sy_mb1_dfcp, self.sut_mb1_dfcp,
                               self.sy_mb2_dfcp, self.sut_mb2_dfcp,
                               self.sy_e_dfcp, self.sut_e_dfcp,
                               self.h_dfcp, self.e_dfcp, self.l_dfcp, self.a_dfcp,
                               self.relacionf_dfcp],
            "Carga transversal": [self.sy_mb1_dfct, self.sy_mb2_dfct,
                                  self.sut_mb1_dfct, self.sut_mb2_dfct,
                                  self.sy_e_dfct, self.sut_e_dfct,
                                  self.h_dfct, self.e_dfct, self.l_dfct,
                                  self.a_dfct, self.radio_dfct,
                                  self.relacionf_dfct],
            "Carga de flexión": [self.sy_mb1_dfcf, self.sy_mb2_dfcf,
                                 self.sut_mb1_dfcf, self.sut_mb2_dfcf,
                                 self.sy_e_dfcf, self.sut_e_dfcf,
                                 self.h_dfcf, self.e_dfcf, self.l_dfcf,
                                 self.a_dfcf, self.radio_dfcf,
                                 self.relacionf_dfcf, self.b_dfcf],
            "Carga de torsión": [self.sy_mb1_dfctor, self.sy_mb2_dfctor,
                                 self.sut_mb1_dfctor, self.sut_mb2_dfctor,
                                 self.sy_e_dfctor, self.sut_e_dfctor,
                                 self.h_dfctor, self.e_dfctor, self.l_dfctor,
                                 self.a_dfctor, self.radio_dfctor,
                                 self.relacionf_dfctor, self.b_dfctor],
            "Carga combinada": [self.sy_mb1_dfcc, self.sy_mb2_dfcc,
                                self.sut_mb1_dfcc, self.sut_mb2_dfcc,
                                self.sy_e_dfcc, self.sut_e_dfcc,
                                self.h_dfcc, self.e_dfcc, self.l_dfcc,
                                self.a_dfcc, self.radio_dfcc,
                                self.relacionf_dfcc,
                                self.bl_dfcc, self.bt_dfcc]
        }

        # Asignar validador en qlineedits para permitir sólo ingreso de floats
        for tipo_carga, qlineedits in qlineedit_datos_entrada.items():
            for qlineedit in qlineedits:
                qlineedit.setValidator(QDoubleValidator())

        ############################################################################################################

        # Señal de boton en barra menu de volver a inicio
        self.actionVolver_al_inicio.triggered.connect(self.cerrar_y_volver_a_inicio)

        # Señal de boton en barra menu de cerrar
        self.actionCerrar.triggered.connect(self.cerrar_ventana)

        # Señal de boton en barra menú para cálculo nuevo
        self.actionNuevo_calculo.triggered.connect(self.evento_limpiar_tab_actionnuevocalculo)

        # SEÑALES DE BOTONES PARA CALCULAR FS

        # Señal del boton de calcular la carga permisible para carga paralela
        self.boton_calcular_carga_dfcp.clicked.connect(self.calcular_carga_dfcp)

        # Señal del boton de calcular la carga permisible para carga transversal
        self.boton_calcular_carga_dfct.clicked.connect(self.calcular_carga_dfct)

        # Señal del boton de calcular la carga permisible para carga de flexion
        self.boton_calcular_carga_dfcf.clicked.connect(self.calcular_carga_dfcf)

        # Señal del boton de calcular la carga permisible para carga de torsion
        self.boton_calcular_carga_dfctor.clicked.connect(self.calcular_carga_dfctor)

        # Señal del boton de calcular la carga permisible para carga combinada
        self.boton_calcular_carga_dfcc.clicked.connect(self.calcular_carga_dfcc)

        # SEÑALES PARA GUARDAR INFORMES

        # Carga paralela
        self.boton_guardar_dfcp.clicked.connect(self.evento_guardar)

        # Carga transversal
        self.boton_guardar_dfct.clicked.connect(self.evento_guardar)

        # Carga de flexión debido a una fuerza excéntrica
        self.boton_guardar_dfcf.clicked.connect(self.evento_guardar)

        # Carga de torsión debido a una fuerza excéntrica
        self.boton_guardar_dfctor.clicked.connect(self.evento_guardar)

        # Carga combinada debido a una fuerza excéntrica
        self.boton_guardar_dfcc.clicked.connect(self.evento_guardar)

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def evento_guardar(self):
        """
        Método de evento para manejar la señal de clic en un botón de guardar.

        Obtiene el botón que emite la señal y llama al método 'guardar_informe' para guardar el informe asociado al botón.
        """

        dic_botones = {
            self.boton_guardar_dfcp: self.informe_resultados_dfcp,
            self.boton_guardar_dfct: self.informe_resultados_dfct,
            self.boton_guardar_dfcf: self.informe_resultados_dfcf,
            self.boton_guardar_dfctor: self.informe_resultados_dfctor,
            self.boton_guardar_dfcc: self.informe_resultados_dfcc
        }

        objeto = self.sender()

        VentanaAnalisisFilete.guardar_informe(self, objeto, dic_botones)

    def evento_actualizar_etiquetas(self):
        """Slot para el evento de cambio de indice de la lista desplegable de sistema de unidades.
       Realiza acciones específicas al seleccionar un indice de la lista desplegable.
       """

        # Diccionario de objetos etiquetas con unidades de esfuerzo, distancia y fuerza
        etiquetas_unidades = {
            self.sist_und_dfct: {
                'esfuerzo': [self.und_esfuerzo_dfct_1,
                             self.und_esfuerzo_dfct_2,
                             self.und_esfuerzo_dfct_3,
                             self.und_esfuerzo_dfct_4,
                             self.und_esfuerzo_dfct_5,
                             self.und_esfuerzo_dfct_6],
                'distancia': [self.und_distancia_dfct_1,
                              self.und_distancia_dfct_2,
                              self.und_distancia_dfct_3,
                              self.und_distancia_dfct_4,
                              self.und_distancia_dfct_5],
                'fuerza': [],
                'torque': []
            },
            self.sist_und_dfcp: {
                "esfuerzo": [self.und_esfuerzo_dfcp_1,
                             self.und_esfuerzo_dfcp_2,
                             self.und_esfuerzo_dfcp_3,
                             self.und_esfuerzo_dfcp_4,
                             self.und_esfuerzo_dfcp_5,
                             self.und_esfuerzo_dfcp_6],
                'distancia': [self.und_distancia_dfcp_1,
                              self.und_distancia_dfcp_2,
                              self.und_distancia_dfcp_3,
                              self.und_distancia_dfcp_4],
                'fuerza': [],
                'torque': []
            },
            self.sist_und_dfcf: {
                "esfuerzo": [self.und_esfuerzo_dfcf_1,
                             self.und_esfuerzo_dfcf_2,
                             self.und_esfuerzo_dfcf_3,
                             self.und_esfuerzo_dfcf_4,
                             self.und_esfuerzo_dfcf_5,
                             self.und_esfuerzo_dfcf_6],
                'distancia': [self.und_distancia_dfcf_1,
                              self.und_distancia_dfcf_2,
                              self.und_distancia_dfcf_3,
                              self.und_distancia_dfcf_4,
                              self.und_distancia_dfcf_5,
                              self.und_distancia_dfcf_6,
                              self.und_distancia_dfcf_7,
                              self.und_distancia_dfcf_8,
                              self.und_distancia_dfcf_9],
                'fuerza': [],
                'torque': []

            },
            self.sist_und_dfctor: {
                'esfuerzo': [self.und_esfuerzo_dfctor_1,
                             self.und_esfuerzo_dfctor_2,
                             self.und_esfuerzo_dfctor_3,
                             self.und_esfuerzo_dfctor_4,
                             self.und_esfuerzo_dfctor_5,
                             self.und_esfuerzo_dfctor_6],
                'distancia': [self.und_distancia_dfctor_1,
                              self.und_distancia_dfctor_2,
                              self.und_distancia_dfctor_3,
                              self.und_distancia_dfctor_4,
                              self.und_distancia_dfctor_5,
                              self.und_distancia_dfctor_6,
                              self.und_distancia_dfctor_7,
                              self.und_distancia_dfctor_8,
                              self.und_distancia_dfctor_9],
                'fuerza': [],
                'torque': []

            },
            self.sist_und_dfcc: {
                'esfuerzo': [self.und_esfuerzo_dfcc_1,
                             self.und_esfuerzo_dfcc_2,
                             self.und_esfuerzo_dfcc_3,
                             self.und_esfuerzo_dfcc_4,
                             self.und_esfuerzo_dfcc_5,
                             self.und_esfuerzo_dfcc_6],
                'distancia': [self.und_distancia_dfcc_1,
                              self.und_distancia_dfcc_2,
                              self.und_distancia_dfcc_3,
                              self.und_distancia_dfcc_4,
                              self.und_distancia_dfcc_5,
                              self.und_distancia_dfcc_6,
                              self.und_distancia_dfcc_7,
                              self.und_distancia_dfcc_8,
                              self.und_distancia_dfcc_9,
                              self.und_distancia_dfcc_10,
                              self.und_distancia_dfcc_11],
                'fuerza': [],
                'torque': []
            }
        }

        # Código para el evento

        # Obtener objeto que emite la señal
        objeto = self.sender()

        # Obtener contenido del objeto que emite la señal (nombre de material seleccionado de lista desplegable)
        contenido_objeto = self.sender().currentText()

        VentanaAnalisisFilete.cambiar_etiquetas(etiquetas_unidades, objeto, contenido_objeto)

    def evento_copiar_resistencias_mb(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
         Realiza acciones específicas al hacer click en el radiobutton.
         """
        # Código para el evento

        widgets_material_base = [
            {
                "mb_iguales": self.mb_iguales_dfcp,
                "mb1": self.mb1_dfcp,
                "mb2": self.mb2_dfcp,
                "sy_mb1": self.sy_mb1_dfcp,
                "sut_mb1": self.sut_mb1_dfcp,
                "sy_mb2": self.sy_mb2_dfcp,
                "sut_mb2": self.sut_mb2_dfcp
            },
            {
                "mb_iguales": self.mb_iguales_dfct,
                "mb1": self.mb1_dfct,
                "mb2": self.mb2_dfct,
                "sy_mb1": self.sy_mb1_dfct,
                "sut_mb1": self.sut_mb1_dfct,
                "sy_mb2": self.sy_mb2_dfct,
                "sut_mb2": self.sut_mb2_dfct
            },
            {
                "mb_iguales": self.mb_iguales_dfcf,
                "mb1": self.mb1_dfcf,
                "mb2": self.mb2_dfcf,
                "sy_mb1": self.sy_mb1_dfcf,
                "sut_mb1": self.sut_mb1_dfcf,
                "sy_mb2": self.sy_mb2_dfcf,
                "sut_mb2": self.sut_mb2_dfcf
            },
            {
                "mb_iguales": self.mb_iguales_dfctor,
                "mb1": self.mb1_dfctor,
                "mb2": self.mb2_dfctor,
                "sy_mb1": self.sy_mb1_dfctor,
                "sut_mb1": self.sut_mb1_dfctor,
                "sy_mb2": self.sy_mb2_dfctor,
                "sut_mb2": self.sut_mb2_dfctor
            },
            {
                "mb_iguales": self.mb_iguales_dfcc,
                "mb1": self.mb1_dfcc,
                "mb2": self.mb2_dfcc,
                "sy_mb1": self.sy_mb1_dfcc,
                "sut_mb1": self.sut_mb1_dfcc,
                "sy_mb2": self.sy_mb2_dfcc,
                "sut_mb2": self.sut_mb2_dfcc
            }

        ]

        VentanaAnalisisFilete.copiar_resistencias_mb(widgets_material_base)

    def evento_resistencias_materiales_base(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
        Realiza acciones específicas al cambiar el contenido del combobox.
        """
        # Código para el evento

        # Diccionario de dependecia de objetos (lista desplegable de sistund, lista de materiales, lineas de texto
        mb_comboboxes = {
            self.sist_und_dfcp: {
                self.mb1_dfcp: (self.sy_mb1_dfcp, self.sut_mb1_dfcp),
                self.mb2_dfcp: (self.sy_mb2_dfcp, self.sut_mb2_dfcp)
            },
            self.sist_und_dfct: {
                self.mb1_dfct: (self.sy_mb1_dfct, self.sut_mb1_dfct),
                self.mb2_dfct: (self.sy_mb2_dfct, self.sut_mb2_dfct)
            },
            self.sist_und_dfcf: {
                self.mb1_dfcf: (self.sy_mb1_dfcf, self.sut_mb1_dfcf),
                self.mb2_dfcf: (self.sy_mb2_dfcf, self.sut_mb2_dfcf)
            },
            self.sist_und_dfctor: {
                self.mb1_dfctor: (self.sy_mb1_dfctor, self.sut_mb1_dfctor),
                self.mb2_dfctor: (self.sy_mb2_dfctor, self.sut_mb2_dfctor)
            },
            self.sist_und_dfcc: {
                self.mb1_dfcc: (self.sy_mb1_dfcc, self.sut_mb1_dfcc),
                self.mb2_dfcc: (self.sy_mb2_dfcc, self.sut_mb2_dfcc)}}

        # Obtener objeto que emite la señal
        objeto = self.sender()

        # Obtener contenido del objeto que emite la señal (nombre de material seleccionado de lista desplegable)
        contenido_objeto = self.sender().currentText()

        widgets_material_base = [
            {
                "mb_iguales": self.mb_iguales_dfcp,
                "mb1": self.mb1_dfcp,
                "mb2": self.mb2_dfcp,
                "sy_mb1": self.sy_mb1_dfcp,
                "sut_mb1": self.sut_mb1_dfcp,
                "sy_mb2": self.sy_mb2_dfcp,
                "sut_mb2": self.sut_mb2_dfcp
            },
            {
                "mb_iguales": self.mb_iguales_dfct,
                "mb1": self.mb1_dfct,
                "mb2": self.mb2_dfct,
                "sy_mb1": self.sy_mb1_dfct,
                "sut_mb1": self.sut_mb1_dfct,
                "sy_mb2": self.sy_mb2_dfct,
                "sut_mb2": self.sut_mb2_dfct
            },
            {
                "mb_iguales": self.mb_iguales_dfcf,
                "mb1": self.mb1_dfcf,
                "mb2": self.mb2_dfcf,
                "sy_mb1": self.sy_mb1_dfcf,
                "sut_mb1": self.sut_mb1_dfcf,
                "sy_mb2": self.sy_mb2_dfcf,
                "sut_mb2": self.sut_mb2_dfcf
            },
            {
                "mb_iguales": self.mb_iguales_dfctor,
                "mb1": self.mb1_dfctor,
                "mb2": self.mb2_dfctor,
                "sy_mb1": self.sy_mb1_dfctor,
                "sut_mb1": self.sut_mb1_dfctor,
                "sy_mb2": self.sy_mb2_dfctor,
                "sut_mb2": self.sut_mb2_dfctor
            },
            {
                "mb_iguales": self.mb_iguales_dfcc,
                "mb1": self.mb1_dfcc,
                "mb2": self.mb2_dfcc,
                "sy_mb1": self.sy_mb1_dfcc,
                "sut_mb1": self.sut_mb1_dfcc,
                "sy_mb2": self.sy_mb2_dfcc,
                "sut_mb2": self.sut_mb2_dfcc
            }

        ]

        VentanaAnalisisFilete.obtencion_resistencias_mb(widgets_material_base, mb_comboboxes, objeto, contenido_objeto)

    def resistencias_material_aporte(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
           Realiza acciones específicas al seleccionar un tipo de electrodo de la lista desplegable.
           """

        # Código para el evento

        # Diccionario de dependencia de objetos (lista de electrodos, campos de resistencia para cada ventana)
        """Material de aporte comboboxes"""
        ma_comboboxes = {
            self.sist_und_dfcp: {
                self.electrodo_dfcp: (self.sy_e_dfcp,
                                      self.sut_e_dfcp)
            },
            self.sist_und_dfct: {
                self.electrodo_dfct: (self.sy_e_dfct,
                                      self.sut_e_dfct)
            },
            self.sist_und_dfcf: {
                self.electrodo_dfcf: (self.sy_e_dfcf,
                                      self.sut_e_dfcf)
            },
            self.sist_und_dfctor: {
                self.electrodo_dfctor: (self.sy_e_dfctor,
                                        self.sut_e_dfctor)
            },
            self.sist_und_dfcc: {
                self.electrodo_dfcc: (self.sy_e_dfcc,
                                      self.sut_e_dfcc)
            }
        }

        # Obtener objeto y contenido del objeto que emite la señal
        objeto = self.sender()
        contenido_objeto = self.sender().currentText()

        VentanaAnalisisFilete.obtencion_resistencias_ma(ma_comboboxes, objeto, contenido_objeto)

    def evento_limpiar_tab_actionnuevocalculo(self):

        # Obtener pestaña activa
        tab_widget = self.tab_widget
        tab_activa_index = tab_widget.currentIndex()
        tab_activa = tab_widget.widget(tab_activa_index)

        # Colocar todos los QlineEdits en 0 (datos de entrada)
        for widget in tab_activa.findChildren(QLineEdit):
            if isinstance(widget, QLineEdit):
                widget.setText("0")

        # Vaciar el contenido de todos los QTextBrowsers (resumen e informe de resultados)
        for widget in tab_activa.findChildren(QTextBrowser):
            if isinstance(widget, QTextBrowser):
                widget.setText("")

        # Deseleccionar el nombre de algún material
        for widget in tab_activa.findChildren(QComboBox):
            if isinstance(widget, QComboBox):
                widget.setCurrentText("")

        # Deseleccionar los QRadioButtons
        for widget in tab_activa.findChildren(QRadioButton):
            if isinstance(widget, QRadioButton):
                widget.setChecked(False)

    def cerrar_y_volver_a_inicio(self):
        """
        Slot para el evento de clic del botón de Volver a inicio en la barra menú.
        Realiza acciones específicas al presionar el botón.
        """

        # Declarar la ventana como una clase
        self.ventana_volver_inicio = VentanaPrincipal()

        # Abrir ventana de análisis de ranura
        self.ventana_volver_inicio.show()

        # Cerrar ventana de análisis de filete
        self.close()

    def cerrar_ventana(self):
        self.close()

    def calcular_carga_dfcp(self):

        self.informe_resultados_dfcp.clear()
        self.resumen_resultados_dfcp.clear()

        if self.iden_proyecto_dfcp is not None:
            nombre_proyecto = self.iden_proyecto_dfcp.text()
        else:
            nombre_proyecto = "S/I"


        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "dos": self.g_2_dfcp,
            "seis": self.g_6_dfcp
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "dos":
            self.a_dfcp.setText("0")

        # Cálculo de carga permisible

        # Verificar si se seleccionó carga estática
        try:

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_dfcp.text()),
                "sut_mb1": float(self.sut_mb1_dfcp.text()),
                "sy_mb2": float(self.sy_mb2_dfcp.text()),
                "sut_mb2": float(self.sut_mb2_dfcp.text()),
                "sy_e": float(self.sy_e_dfcp.text()),
                "sut_e": float(self.sut_e_dfcp.text()),
                "e": float(self.e_dfcp.text()),
                "h": float(self.h_dfcp.text()),
                "l": float(self.l_dfcp.text()),
                "a": float(self.a_dfcp.text()),
                "relacion": float(self.relacionf_dfcp.text())
            }

            if self.cestatica_dfcp.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfcp.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Intermedia"
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoCargaPermisibleFilete(sist_und, tipo_union, 0, 0, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos, espesor)

                # Extraer diccionario con resultados de diseño por estática
                dic_resultados_estatica = resultados.carga_permisible_estatica_cp()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_filete_cp(nombre_proyecto, "estática",
                                                                               {}, {},
                                                                               dic_resultados_estatica,
                                                                               self.sist_und_dfcp.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_dfcp_1.text(),
                                                                               self.und_esfuerzo_dfcp_1.text(),
                                                                               self.mb1_dfcp.currentText(),
                                                                               self.mb2_dfcp.currentText(),
                                                                               self.electrodo_dfcp.currentText()
                                                                               )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfcp.setText(info_resum[0])
                self.resumen_resultados_dfcp.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_dfcp.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfcp.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Intermedia"
                relacion = diccionario_datos["relacion"]
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoCargaPermisibleFilete(sist_und, tipo_union, relacion, 0, mb1, mb2, electrodo,
                                                                geometria, parametros_geometricos, espesor)

                # Extraer diccionario con resultados de diseño por estática
                dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica = resultados.carga_permisible_cp()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_filete_cp(nombre_proyecto, "de fatiga",
                                                                               dic_diseno_fatiga, dic_comprobacion,
                                                                               dic_diseno_estatica,
                                                                               self.sist_und_dfcp.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_dfcp_1.text(),
                                                                               self.und_esfuerzo_dfcp_1.text(),
                                                                               self.mb1_dfcp.currentText(),
                                                                               self.mb2_dfcp.currentText(),
                                                                               self.electrodo_dfcp.currentText()
                                                                               )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfcp.setText(info_resum[0])
                self.resumen_resultados_dfcp.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_dfcp.setEnabled(True)

    def calcular_carga_dfct(self):

        self.informe_resultados_dfct.clear()
        self.resumen_resultados_dfct.clear()

        if self.iden_proyecto_dfct is not None:
            nombre_proyecto = self.iden_proyecto_dfct.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_dfct,
            "tres": self.g_3_dfct,
            "cinco": self.g_5_dfct,
            "siete": self.g_7_dfct,
            "ocho": self.g_8_dfct,
            "diez": self.g_10_dfct,
            "once": self.g_11_dfct,
            "doce": self.g_12_dfct,
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "uno":
            self.a_dfct.setText("0")
            self.radio_dfct.setText("0")
        elif geometria_seleccionada == "ocho":
            self.l_dfct.setText("0")
            self.a_dfct.setText("0")
        else:
            self.radio_dfct.setText("0")

        print(self.radio_dfct.text())

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Intermedia": self.union_interm_dfct,
            "Unión T": self.union_t_dfct}

        union_seleccionada = None

        print(union_seleccionada)

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Cálculo de carga permisible

        # Verificar si se seleccionó carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_dfct.text()),
                "sut_mb1": float(self.sut_mb1_dfct.text()),
                "sy_mb2": float(self.sy_mb2_dfct.text()),
                "sut_mb2": float(self.sut_mb2_dfct.text()),
                "sy_e": float(self.sy_e_dfct.text()),
                "sut_e": float(self.sut_e_dfct.text()),
                "e": float(self.e_dfct.text()),
                "h": float(self.h_dfct.text()),
                "l": float(self.l_dfct.text()),
                "a": float(self.a_dfct.text()),
                "relacion": float(self.relacionf_dfct.text()),
                "radio": float(self.radio_dfct.text())
            }

            print(diccionario_datos)

            if self.cestatica_dfct.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfct.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoCargaPermisibleFilete(sist_und, tipo_union, 0, 0, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos, espesor)

                print(resultados)

                # Extraer diccionario con resultados de diseño por estática
                dic_resultados_estatica = resultados.carga_permisible_estatica_ctrans()

                print(1)

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_filete_ct(nombre_proyecto, "estática",
                                                                               {}, {},
                                                                               dic_resultados_estatica,
                                                                               self.sist_und_dfct.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_dfct_1.text(),
                                                                               self.und_esfuerzo_dfct_1.text(),
                                                                               self.mb1_dfct.currentText(),
                                                                               self.mb2_dfct.currentText(),
                                                                               self.electrodo_dfct.currentText()
                                                                               )

                print(2)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfct.setText(info_resum[0])
                self.resumen_resultados_dfct.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_dfct.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfct.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                relacion = diccionario_datos["relacion"]
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoCargaPermisibleFilete(sist_und, tipo_union, relacion, 0, mb1, mb2, electrodo,
                                                                geometria, parametros_geometricos, espesor)

                print(0)

                # Extraer diccionario con resultados de diseño por estática
                dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica = resultados.carga_permisible_ctrans()

                print(1)

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_filete_ct(nombre_proyecto, "de fatiga",
                                                                               dic_diseno_fatiga,
                                                                               dic_comprobacion, dic_diseno_estatica,
                                                                               self.sist_und_dfct.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_dfct_1.text(),
                                                                               self.und_esfuerzo_dfct_1.text(),
                                                                               self.mb1_dfct.currentText(),
                                                                               self.mb2_dfct.currentText(),
                                                                               self.electrodo_dfct.currentText()
                                                                               )

                print(2)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfct.setText(info_resum[0])
                self.resumen_resultados_dfct.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_dfct.setEnabled(True)

    # Evento para calcular carga permisible carga flexión
    def calcular_carga_dfcf(self):

        self.informe_resultados_dfcf.clear()
        self.resumen_resultados_dfcf.clear()

        if self.iden_proyecto_dfcf is not None:
            nombre_proyecto = self.iden_proyecto_dfcf.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_dfcf,
            "tres": self.g_3_dfcf,
            "cinco": self.g_5_dfcf,
            "seis": self.g_6_dfcf,
            "siete": self.g_7_dfcf,
            "ocho": self.g_8_dfcf,
            "nueve": self.g_9_dfcf,
            "diez": self.g_10_dfcf,
            "once": self.g_11_dfcf,
            "doce": self.g_12_dfcf,
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "uno":
            self.a_dfcf.setText("0")
            self.radio_dfcf.setText("0")
        elif geometria_seleccionada == "ocho":
            self.l_dfcf.setText("0")
            self.a_dfcf.setText("0")
        else:
            self.radio_dfcf.setText("0")

        # Cálculo de carga permisible

        # Verificar si se seleccionó carga estática
        try:

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_dfcf.text()),
                "sut_mb1": float(self.sut_mb1_dfcf.text()),
                "sy_mb2": float(self.sy_mb2_dfcf.text()),
                "sut_mb2": float(self.sut_mb2_dfcf.text()),
                "sy_e": float(self.sy_e_dfcf.text()),
                "sut_e": float(self.sut_e_dfcf.text()),
                "e": float(self.e_dfcf.text()),
                "h": float(self.h_dfcf.text()),
                "l": float(self.l_dfcf.text()),
                "a": float(self.a_dfcf.text()),
                "r": float(self.radio_dfcf.text()),
                "relacion": float(self.relacionf_dfcf.text()),
                "brazo": float(self.b_dfcf.text())
            }

            print(diccionario_datos)

            if self.cestatica_dfcf.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfcf.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Unión T"
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]
                brazo = diccionario_datos["brazo"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, brazo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, brazo)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                print(sist_und, tipo_union, brazo, mb1, mb2, electrodo, geometria, parametros_geometricos, espesor)

                resultados = diseno.DisenoCargaPermisibleFilete(sist_und, tipo_union, 0, brazo, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos, espesor)

                # Resultados a mostrar en cuadros: x, y, c
                x, y = resultados.obtener_coordenadas_centroide()
                c = str(round(resultados.obtener_rx_ry()[1], 3))
                self.x_dfcf.setText(str(round(x, 3)))
                self.y_dfcf.setText(str(round(y, 3)))
                self.c_dfcf.setText(c)

                print(0)

                # Extraer diccionario con resultados de diseño por estática
                dic_resultados_estatica = resultados.carga_permisible_estatica_cflex()

                print(1)
                print(dic_resultados_estatica)

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_filete_cf(nombre_proyecto, "estática",
                                                                               {}, {},
                                                                               dic_resultados_estatica,
                                                                               self.sist_und_dfcf.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_dfcf_1.text(),
                                                                               self.und_esfuerzo_dfcf_1.text(),
                                                                               self.mb1_dfcf.currentText(),
                                                                               self.mb2_dfct.currentText(),
                                                                               self.electrodo_dfcf.currentText()
                                                                               )

                print(2)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfcf.setText(info_resum[0])
                self.resumen_resultados_dfcf.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_dfcf.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfcf.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Unión T"
                relacion = diccionario_datos["relacion"]
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]
                brazo = diccionario_datos["brazo"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, brazo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, brazo)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoCargaPermisibleFilete(sist_und, tipo_union, relacion, brazo, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos, espesor)

                # Resultados a mostrar en cuadros: x, y, c
                x, y = resultados.obtener_coordenadas_centroide()
                c = str(round(resultados.obtener_rx_ry()[1], 3))
                self.x_dfcf.setText(str(round(x, 3)))
                self.y_dfcf.setText(str(round(y, 3)))
                self.c_dfcf.setText(c)

                print(0)

                # Extraer diccionario con resultados de diseño por estática
                dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica = resultados.carga_permisible_cflex()

                print(1)

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_filete_cf(nombre_proyecto, "de fatiga",
                                                                               dic_diseno_fatiga,
                                                                               dic_comprobacion, dic_diseno_estatica,
                                                                               self.sist_und_dfcf.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_dfcf_1.text(),
                                                                               self.und_esfuerzo_dfcf_1.text(),
                                                                               self.mb1_dfcf.currentText(),
                                                                               self.mb2_dfcf.currentText(),
                                                                               self.electrodo_dfcf.currentText()
                                                                               )

                print(2)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfcf.setText(info_resum[0])
                self.resumen_resultados_dfcf.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_dfcf.setEnabled(True)

    def calcular_carga_dfctor(self):

        self.informe_resultados_dfctor.clear()
        self.resumen_resultados_dfctor.clear()

        if self.iden_proyecto_dfctor is not None:
            nombre_proyecto = self.iden_proyecto_dfctor.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_dfctor,
            "tres": self.g_3_dfctor,
            "cinco": self.g_5_dfctor,
            "seis": self.g_6_dfctor,
            "siete": self.g_7_dfctor,
            "ocho": self.g_8_dfctor,
            "nueve": self.g_9_dfctor,
            "diez": self.g_10_dfctor,
            "once": self.g_11_dfctor,
            "doce": self.g_12_dfctor,
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "uno":
            self.a_dfctor.setText("0")
            self.radio_dfctor.setText("0")
        elif geometria_seleccionada == "ocho":
            self.l_dfctor.setText("0")
            self.a_dfctor.setText("0")
        else:
            self.radio_dfctor.setText("0")

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Intermedia": self.union_interm_dfctor,
            "Unión T": self.union_t_dfctor
        }

        union_seleccionada = None

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Cálculo de carga permisible

        # Verificar si se seleccionó carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_dfctor.text()),
                "sut_mb1": float(self.sut_mb1_dfctor.text()),
                "sy_mb2": float(self.sy_mb2_dfctor.text()),
                "sut_mb2": float(self.sut_mb2_dfctor.text()),
                "sy_e": float(self.sy_e_dfctor.text()),
                "sut_e": float(self.sut_e_dfctor.text()),
                "e": float(self.e_dfctor.text()),
                "h": float(self.h_dfctor.text()),
                "l": float(self.l_dfctor.text()),
                "a": float(self.a_dfctor.text()),
                "r": float(self.radio_dfctor.text()),
                "relacion": float(self.relacionf_dfctor.text()),
                "brazo": float(self.b_dfctor.text())
            }

            if self.cestatica_dfctor.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfctor.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]
                brazo = diccionario_datos["brazo"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, brazo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, brazo)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el diseño por fatiga de carga permisible de filete
                resultados = diseno.DisenoCargaPermisibleFilete(sist_und, tipo_union, 0, brazo, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos, espesor)

                # Resultados a mostrar en cuadros: x, y, r
                x, y = resultados.obtener_coordenadas_centroide()
                rx, ry = resultados.obtener_rx_ry()[0:2]
                r = str(round((rx ** 2 + ry ** 2) ** 0.5, 3))
                self.x_dfctor.setText(str(round(x, 3)))
                self.y_dfctor.setText(str(round(y, 3)))
                self.r_dfctor.setText(r)

                # Extraer diccionario con resultados de diseño por estática
                dic_resultados_estatica = resultados.carga_permisible_estatica_ctor()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_filete_ctor(nombre_proyecto, "estática",
                                                                                 {}, {},
                                                                                 dic_resultados_estatica,
                                                                                 self.sist_und_dfctor.currentText(),
                                                                                 und_fuerza,
                                                                                 self.und_distancia_dfctor_1.text(),
                                                                                 self.und_esfuerzo_dfctor_1.text(),
                                                                                 self.mb1_dfctor.currentText(),
                                                                                 self.mb2_dfctor.currentText(),
                                                                                 self.electrodo_dfctor.currentText()
                                                                                 )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfctor.setText(info_resum[0])
                self.resumen_resultados_dfctor.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_dfctor.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfctor.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                relacion = diccionario_datos["relacion"]
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]
                brazo = diccionario_datos["brazo"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, brazo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, brazo)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoCargaPermisibleFilete(sist_und, tipo_union, relacion, brazo, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos, espesor)

                # Resultados a mostrar en cuadros: x, y, r
                x, y = resultados.obtener_coordenadas_centroide()
                rx, ry = resultados.obtener_rx_ry()[0:2]
                r = str(round((rx ** 2 + ry ** 2) ** 0.5, 3))
                self.x_dfctor.setText(str(round(x, 3)))
                self.y_dfctor.setText(str(round(y, 3)))
                self.r_dfctor.setText(r)

                # Extraer diccionario con resultados de diseño por estática
                dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica = resultados.carga_permisible_ctor()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_filete_ctor(nombre_proyecto, "de fatiga",
                                                                                 dic_diseno_fatiga, dic_comprobacion,
                                                                                 dic_diseno_estatica,
                                                                                 self.sist_und_dfctor.currentText(),
                                                                                 und_fuerza,
                                                                                 self.und_distancia_dfctor_1.text(),
                                                                                 self.und_esfuerzo_dfctor_1.text(),
                                                                                 self.mb1_dfctor.currentText(),
                                                                                 self.mb2_dfctor.currentText(),
                                                                                 self.electrodo_dfctor.currentText()
                                                                                 )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfctor.setText(info_resum[0])
                self.resumen_resultados_dfctor.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_dfctor.setEnabled(True)

    def calcular_carga_dfcc(self):

        self.informe_resultados_dfcc.clear()
        self.resumen_resultados_dfcc.clear()

        if self.iden_proyecto_dfcc is not None:
            nombre_proyecto = self.iden_proyecto_dfcc.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_dfcc,
            "cinco": self.g_5_dfcc,
            "seis": self.g_6_dfcc,
            "ocho": self.g_8_dfcc,
            "nueve": self.g_9_dfcc,
            "once": self.g_11_dfcc,
            "doce": self.g_12_dfcc,
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "uno":
            self.a_dfcc.setText("0")
            self.radio_dfcc.setText("0")
        elif geometria_seleccionada == "ocho":
            self.l_dfcc.setText("0")
            self.a_dfcc.setText("0")
        else:
            self.radio_dfcc.setText("0")

        # Cálculo de carga permisible

        # Verificar si se seleccionó carga estática
        try:

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_dfcc.text()),
                "sut_mb1": float(self.sut_mb1_dfcc.text()),
                "sy_mb2": float(self.sy_mb2_dfcc.text()),
                "sut_mb2": float(self.sut_mb2_dfcc.text()),
                "sy_e": float(self.sy_e_dfcc.text()),
                "sut_e": float(self.sut_e_dfcc.text()),
                "e": float(self.e_dfcc.text()),
                "h": float(self.h_dfcc.text()),
                "l": float(self.l_dfcc.text()),
                "a": float(self.a_dfcc.text()),
                "r": float(self.radio_dfcc.text()),
                "relacion": float(self.relacionf_dfcc.text()),
                "bl": float(self.bl_dfcc.text()),
                "bt": float(self.bt_dfcc.text())
            }

            print(diccionario_datos)

            if self.cestatica_dfcc.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfcc.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Unión T"
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]
                bl = diccionario_datos["bl"]
                bt = diccionario_datos["bt"]
                brazo = {"bl": bl, "bt": bt}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, bl, bt)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, bl, bt)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                print(sist_und, tipo_union, brazo, mb1, mb2, electrodo, geometria, parametros_geometricos, espesor)

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoCargaPermisibleFilete(sist_und, tipo_union, 0, brazo, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos,
                                                                espesor)

                # Resultados a mostrar en cuadros: x, y, r, c
                x, y = resultados.obtener_coordenadas_centroide()
                rx, ry = resultados.obtener_rx_ry()[0:2]
                c = str(round(resultados.obtener_rx_ry()[1], 3))
                r = str(round((rx ** 2 + ry ** 2) ** 0.5, 3))
                self.x_dfcc.setText(str(round(x, 3)))
                self.y_dfcc.setText(str(round(y, 3)))
                self.r_dfcc.setText(r)
                self.c_dfcc.setText(c)

                print(0)

                # Extraer diccionario con resultados de diseño por estática
                dic_resultados_estatica = resultados.carga_permisible_estatica_ccomb()

                print(1)

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_filete_cc(nombre_proyecto, "estática",
                                                                               {}, {},
                                                                               dic_resultados_estatica,
                                                                               self.sist_und_dfcc.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_dfcc_1.text(),
                                                                               self.und_esfuerzo_dfcc_1.text(),
                                                                               self.mb1_dfcc.currentText(),
                                                                               self.mb2_dfcc.currentText(),
                                                                               self.electrodo_dfcc.currentText()
                                                                               )

                print(2)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfcc.setText(info_resum[0])
                self.resumen_resultados_dfcc.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_dfcc.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfcc.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Unión T"
                relacion = diccionario_datos["relacion"]
                geometria = geometria_seleccionada
                pierna = diccionario_datos["h"]
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"pierna": pierna, "largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]
                bl = diccionario_datos["bl"]
                bt = diccionario_datos["bt"]
                brazo = {"bl": bl, "bt": bt}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, bl, bt)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, pierna, largo, ancho, radio, bl, bt)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoCargaPermisibleFilete(sist_und, tipo_union, relacion, brazo, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos, espesor)

                # Resultados a mostrar en cuadros: x, y, r, c
                x, y = resultados.obtener_coordenadas_centroide()
                rx, ry = resultados.obtener_rx_ry()[0:2]
                c = str(round(resultados.obtener_rx_ry()[1], 3))
                r = str(round((rx ** 2 + ry ** 2) ** 0.5, 3))
                self.x_dfcc.setText(str(round(x, 3)))
                self.y_dfcc.setText(str(round(y, 3)))
                self.r_dfcc.setText(r)
                self.c_dfcc.setText(c)

                # Extraer diccionario con resultados de diseño por estática
                dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica = resultados.carga_permisible_ccomb()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_filete_cc(nombre_proyecto, "de fatiga",
                                                                               dic_diseno_fatiga,
                                                                               dic_comprobacion, dic_diseno_estatica,
                                                                               self.sist_und_dfcc.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_dfcc_1.text(),
                                                                               self.und_esfuerzo_dfcc_1.text(),
                                                                               self.mb1_dfcc.currentText(),
                                                                               self.mb2_dfcc.currentText(),
                                                                               self.electrodo_dfcc.currentText()
                                                                               )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfcc.setText(info_resum[0])
                self.resumen_resultados_dfcc.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_dfcc.setEnabled(True)


class VentanaDisenoPiernaFilete(QMainWindow, ui_ventana_disenoh_filete):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Heredar metodos de clase de la clase VentanaAnalisisFilete
        self.ventana_analisis_filete = VentanaAnalisisFilete()

        # Conexión de señales y slots

        ############################################################################################################

        # Señal para cambiar las etiquetas de sistema de unidades
        comboboxes_sist_und = [self.sist_und_dfcp, self.sist_und_dfct, self.sist_und_dfcf,
                               self.sist_und_dfctor, self.sist_und_dfcc]

        for combobox in comboboxes_sist_und:
            combobox.currentIndexChanged.connect(self.evento_actualizar_etiquetas)

        ############################################################################################################

        # Señal para copiar nombre del acero y resistencias para piezas de igual material
        checkboxes_material_base = [self.mb_iguales_dfcp, self.mb_iguales_dfct, self.mb_iguales_dfcf,
                                    self.mb_iguales_dfctor, self.mb_iguales_dfcc]

        for checkbox in checkboxes_material_base:
            checkbox.toggled.connect(self.evento_copiar_resistenias_mb)

        ############################################################################################################

        # Señal para extraer de la base de datos las resistencias del material base
        comboboxes_material_base = [self.mb1_dfcp, self.mb1_dfct, self.mb1_dfcf, self.mb1_dfctor, self.mb1_dfcc,
                                    self.mb2_dfcp, self.mb2_dfct, self.mb2_dfcf, self.mb2_dfctor, self.mb2_dfcc]

        for combobox in comboboxes_material_base:
            combobox.currentIndexChanged.connect(self.evento_resistencias_materiales_base)

        ############################################################################################################

        # Señal para extraer de la base de datos las resistencias del material de aporte
        comboboxes_material_aporte = [self.electrodo_dfcp, self.electrodo_dfct, self.electrodo_dfcf,
                                      self.electrodo_dfctor, self.electrodo_dfcc]

        for combobox in comboboxes_material_aporte:
            combobox.currentIndexChanged.connect(self.resistencias_material_aporte)

        ############################################################################################################

        # Diccionario de qlineedits de ingreso de datos
        qlineedit_datos_entrada = {
            "Carga paralela": [self.sy_mb1_dfcp, self.sut_mb1_dfcp,
                               self.sy_mb2_dfcp, self.sut_mb2_dfcp,
                               self.sy_e_dfcp, self.sut_e_dfcp,
                               self.e_dfcp, self.l_dfcp, self.a_dfcp,
                               self.fmax_dfcp, self.fmin_dfcp],
            "Carga transversal": [self.sy_mb1_dfct, self.sy_mb2_dfct,
                                  self.sut_mb1_dfct, self.sut_mb2_dfct,
                                  self.sy_e_dfct, self.sut_e_dfct,
                                  self.e_dfct, self.l_dfct,
                                  self.a_dfct, self.radio_dfct,
                                  self.fmax_dfct, self.fmin_dfct],
            "Carga de flexión": [self.sy_mb1_dfcf, self.sy_mb2_dfcf,
                                 self.sut_mb1_dfcf, self.sut_mb2_dfcf,
                                 self.sy_e_dfcf, self.sut_e_dfcf,
                                 self.e_dfcf, self.l_dfcf,
                                 self.a_dfcf, self.radio_dfcf,
                                 self.fmax_dfcf, self.fmin_dfcf, self.b_dfcf],
            "Carga de torsión": [self.sy_mb1_dfctor, self.sy_mb2_dfctor,
                                 self.sut_mb1_dfctor, self.sut_mb2_dfctor,
                                 self.sy_e_dfctor, self.sut_e_dfctor,
                                 self.e_dfctor, self.l_dfctor,
                                 self.a_dfctor, self.radio_dfctor,
                                 self.fmax_dfctor, self.fmin_dfctor, self.b_dfctor],
            "Carga combinada": [self.sy_mb1_dfcc, self.sy_mb2_dfcc,
                                self.sut_mb1_dfcc, self.sut_mb2_dfcc,
                                self.sy_e_dfcc, self.sut_e_dfcc,
                                self.e_dfcc, self.l_dfcc,
                                self.a_dfcc, self.radio_dfcc,
                                self.fmax_dfcc, self.fmin_dfcc,
                                self.bl_dfcc, self.bt_dfcc]
        }

        # Asignar validador en qlineedits para permitir sólo ingreso de floats
        for tipo_carga, qlineedits in qlineedit_datos_entrada.items():
            for qlineedit in qlineedits:
                qlineedit.setValidator(QDoubleValidator())

        ############################################################################################################

        # Señal de boton en barra menu de volver a inicio
        self.actionVolver_al_inicio.triggered.connect(self.cerrar_y_volver_a_inicio)

        # Señal de boton en barra menu de cerrar
        self.actionCerrar.triggered.connect(self.cerrar_ventana)

        # Señal de boton en barra menú para cálculo nuevo
        self.actionNuevo_calculo.triggered.connect(self.evento_limpiar_tab_actionnuevocalculo)

        # SEÑALES DE BOTONES PARA CALCULAR FS

        # Señal de boton para calcular pierna del cordón de soldadura sometida a carga paralela
        self.boton_calcular_h_dfcp.clicked.connect(self.calcular_h_dfcp)

        # Señal de boton para calcular pierna del cordón de soldadura sometida a carga transversal
        self.boton_calcular_h_dfct.clicked.connect(self.calcular_h_dfct)

        # Señal de boton para calcular pierna del cordón de soldadura sometida a carga de flexión
        self.boton_calcular_h_dfcf.clicked.connect(self.calcular_h_dfcf)

        # Señal de boton para calcular pierna del cordón de soldadura sometida a carga de torsión
        self.boton_calcular_h_dfctor.clicked.connect(self.calcular_h_dfctor)

        # Señal de boton para calcular pierna del cordón de soldadura sometida a carga combinada
        self.boton_calcular_h_dfcc.clicked.connect(self.calcular_h_dfcc)

        # SEÑALES PARA GUARDAR INFORMES

        # Carga paralela
        self.boton_guardar_dfcp.clicked.connect(self.evento_guardar)

        # Carga transversal
        self.boton_guardar_dfct.clicked.connect(self.evento_guardar)

        # Carga de flexión debido a una fuerza excéntrica
        self.boton_guardar_dfcf.clicked.connect(self.evento_guardar)

        # Carga de torsión debido a una fuerza excéntrica
        self.boton_guardar_dfctor.clicked.connect(self.evento_guardar)

        # Carga combinada debido a una fuerza excéntrica
        self.boton_guardar_dfcc.clicked.connect(self.evento_guardar)

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def evento_guardar(self):
        """
        Método de evento para manejar la señal de clic en un botón de guardar.

        Obtiene el botón que emite la señal y llama al método 'guardar_informe' para guardar el informe asociado al botón.
        """

        dic_botones = {
            self.boton_guardar_dfcp: self.informe_resultados_dfcp,
            self.boton_guardar_dfct: self.informe_resultados_dfct,
            self.boton_guardar_dfcf: self.informe_resultados_dfcf,
            self.boton_guardar_dfctor: self.informe_resultados_dfctor,
            self.boton_guardar_dfcc: self.informe_resultados_dfcc
        }

        objeto = self.sender()

        VentanaAnalisisFilete.guardar_informe(self, objeto, dic_botones)

    def evento_actualizar_etiquetas(self):
        """Slot para el evento de cambio de indice de la lista desplegable de sistema de unidades.
       Realiza acciones específicas al seleccionar un indice de la lista desplegable.
       """
        # Diccionario de objetos etiquetas con unidades de esfuerzo, distancia y fuerza
        etiquetas_unidades = {
            self.sist_und_dfct: {
                'esfuerzo': [self.und_esfuerzo_dfct_1,
                             self.und_esfuerzo_dfct_2,
                             self.und_esfuerzo_dfct_3,
                             self.und_esfuerzo_dfct_4,
                             self.und_esfuerzo_dfct_5,
                             self.und_esfuerzo_dfct_6],
                'distancia': [self.und_distancia_dfct_1,
                              self.und_distancia_dfct_2,
                              self.und_distancia_dfct_3,
                              self.und_distancia_dfct_4],
                'fuerza': [self.und_fuerza_dfct_1,
                           self.und_fuerza_dfct_2],
                'torque': []
            },
            self.sist_und_dfcp: {
                "esfuerzo": [self.und_esfuerzo_dfcp_1,
                             self.und_esfuerzo_dfcp_2,
                             self.und_esfuerzo_dfcp_3,
                             self.und_esfuerzo_dfcp_4,
                             self.und_esfuerzo_dfcp_5,
                             self.und_esfuerzo_dfcp_6],
                'distancia': [self.und_distancia_dfcp_1,
                              self.und_distancia_dfcp_2,
                              self.und_distancia_dfcp_3],
                'fuerza': [self.und_fuerza_dfcp_1,
                           self.und_fuerza_dfcp_2],
                'torque': []
            },
            self.sist_und_dfcf: {
                "esfuerzo": [self.und_esfuerzo_dfcf_1,
                             self.und_esfuerzo_dfcf_2,
                             self.und_esfuerzo_dfcf_3,
                             self.und_esfuerzo_dfcf_4,
                             self.und_esfuerzo_dfcf_5,
                             self.und_esfuerzo_dfcf_6],
                'distancia': [self.und_distancia_dfcf_1,
                              self.und_distancia_dfcf_2,
                              self.und_distancia_dfcf_3,
                              self.und_distancia_dfcf_4,
                              self.und_distancia_dfcf_5,
                              self.und_distancia_dfcf_6,
                              self.und_distancia_dfcf_7,
                              self.und_distancia_dfcf_8],
                'fuerza': [self.und_fuerza_dfcf_1,
                           self.und_fuerza_dfcf_2],
                'torque': []

            },
            self.sist_und_dfctor: {
                'esfuerzo': [self.und_esfuerzo_dfctor_1,
                             self.und_esfuerzo_dfctor_2,
                             self.und_esfuerzo_dfctor_3,
                             self.und_esfuerzo_dfctor_4,
                             self.und_esfuerzo_dfctor_5,
                             self.und_esfuerzo_dfctor_6],
                'distancia': [self.und_distancia_dfctor_1,
                              self.und_distancia_dfctor_2,
                              self.und_distancia_dfctor_3,
                              self.und_distancia_dfctor_4,
                              self.und_distancia_dfctor_5,
                              self.und_distancia_dfctor_6,
                              self.und_distancia_dfctor_7,
                              self.und_distancia_dfctor_8],
                'fuerza': [self.und_fuerza_dfctor_1,
                           self.und_fuerza_dfctor_2],
                'torque': []

            },
            self.sist_und_dfcc: {
                'esfuerzo': [self.und_esfuerzo_dfcc_1,
                             self.und_esfuerzo_dfcc_2,
                             self.und_esfuerzo_dfcc_3,
                             self.und_esfuerzo_dfcc_4,
                             self.und_esfuerzo_dfcc_5,
                             self.und_esfuerzo_dfcc_6],
                'distancia': [self.und_distancia_dfcc_1,
                              self.und_distancia_dfcc_2,
                              self.und_distancia_dfcc_3,
                              self.und_distancia_dfcc_4,
                              self.und_distancia_dfcc_5,
                              self.und_distancia_dfcc_6,
                              self.und_distancia_dfcc_7,
                              self.und_distancia_dfcc_8,
                              self.und_distancia_dfcc_9,
                              self.und_distancia_dfcc_10],
                'fuerza': [self.und_fuerza_dfcc_1,
                           self.und_fuerza_dfcc_2],
                'torque': []
            }
        }

        # Código para el evento

        # Obtener objeto que emite la señal
        objeto = self.sender()

        # Obtener contenido del objeto que emite la señal (nombre de material seleccionado de lista desplegable)
        contenido_objeto = self.sender().currentText()

        VentanaAnalisisFilete.cambiar_etiquetas(etiquetas_unidades, objeto, contenido_objeto)

    def evento_copiar_resistenias_mb(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
         Realiza acciones específicas al hacer click en el radiobutton.
         """
        # Código para el evento

        widgets_material_base = [
            {
                "mb_iguales": self.mb_iguales_dfcp,
                "mb1": self.mb1_dfcp,
                "mb2": self.mb2_dfcp,
                "sy_mb1": self.sy_mb1_dfcp,
                "sut_mb1": self.sut_mb1_dfcp,
                "sy_mb2": self.sy_mb2_dfcp,
                "sut_mb2": self.sut_mb2_dfcp
            },
            {
                "mb_iguales": self.mb_iguales_dfct,
                "mb1": self.mb1_dfct,
                "mb2": self.mb2_dfct,
                "sy_mb1": self.sy_mb1_dfct,
                "sut_mb1": self.sut_mb1_dfct,
                "sy_mb2": self.sy_mb2_dfct,
                "sut_mb2": self.sut_mb2_dfct
            },
            {
                "mb_iguales": self.mb_iguales_dfcf,
                "mb1": self.mb1_dfcf,
                "mb2": self.mb2_dfcf,
                "sy_mb1": self.sy_mb1_dfcf,
                "sut_mb1": self.sut_mb1_dfcf,
                "sy_mb2": self.sy_mb2_dfcf,
                "sut_mb2": self.sut_mb2_dfcf
            },
            {
                "mb_iguales": self.mb_iguales_dfctor,
                "mb1": self.mb1_dfctor,
                "mb2": self.mb2_dfctor,
                "sy_mb1": self.sy_mb1_dfctor,
                "sut_mb1": self.sut_mb1_dfctor,
                "sy_mb2": self.sy_mb2_dfctor,
                "sut_mb2": self.sut_mb2_dfctor
            },
            {
                "mb_iguales": self.mb_iguales_dfcc,
                "mb1": self.mb1_dfcc,
                "mb2": self.mb2_dfcc,
                "sy_mb1": self.sy_mb1_dfcc,
                "sut_mb1": self.sut_mb1_dfcc,
                "sy_mb2": self.sy_mb2_dfcc,
                "sut_mb2": self.sut_mb2_dfcc
            }

        ]

        VentanaAnalisisFilete.copiar_resistencias_mb(widgets_material_base)

    def evento_resistencias_materiales_base(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
        Realiza acciones específicas al cambiar el contenido del combobox.
        """
        # Código para el evento

        # Diccionario de dependecia de objetos (lista desplegable de sistund, lista de materiales, lineas de texto
        mb_comboboxes = {
            self.sist_und_dfcp: {
                self.mb1_dfcp: (self.sy_mb1_dfcp, self.sut_mb1_dfcp),
                self.mb2_dfcp: (self.sy_mb2_dfcp, self.sut_mb2_dfcp)
            },
            self.sist_und_dfct: {
                self.mb1_dfct: (self.sy_mb1_dfct, self.sut_mb1_dfct),
                self.mb2_dfct: (self.sy_mb2_dfct, self.sut_mb2_dfct)
            },
            self.sist_und_dfcf: {
                self.mb1_dfcf: (self.sy_mb1_dfcf, self.sut_mb1_dfcf),
                self.mb2_dfcf: (self.sy_mb2_dfcf, self.sut_mb2_dfcf)
            },
            self.sist_und_dfctor: {
                self.mb1_dfctor: (self.sy_mb1_dfctor, self.sut_mb1_dfctor),
                self.mb2_dfctor: (self.sy_mb2_dfctor, self.sut_mb2_dfctor)
            },
            self.sist_und_dfcc: {
                self.mb1_dfcc: (self.sy_mb1_dfcc, self.sut_mb1_dfcc),
                self.mb2_dfcc: (self.sy_mb2_dfcc, self.sut_mb2_dfcc)}}

        # Obtener objeto que emite la señal
        objeto = self.sender()

        # Obtener contenido del objeto que emite la señal (nombre de material seleccionado de lista desplegable)
        contenido_objeto = self.sender().currentText()

        widgets_material_base = [
            {
                "mb_iguales": self.mb_iguales_dfcp,
                "mb1": self.mb1_dfcp,
                "mb2": self.mb2_dfcp,
                "sy_mb1": self.sy_mb1_dfcp,
                "sut_mb1": self.sut_mb1_dfcp,
                "sy_mb2": self.sy_mb2_dfcp,
                "sut_mb2": self.sut_mb2_dfcp
            },
            {
                "mb_iguales": self.mb_iguales_dfct,
                "mb1": self.mb1_dfct,
                "mb2": self.mb2_dfct,
                "sy_mb1": self.sy_mb1_dfct,
                "sut_mb1": self.sut_mb1_dfct,
                "sy_mb2": self.sy_mb2_dfct,
                "sut_mb2": self.sut_mb2_dfct
            },
            {
                "mb_iguales": self.mb_iguales_dfcf,
                "mb1": self.mb1_dfcf,
                "mb2": self.mb2_dfcf,
                "sy_mb1": self.sy_mb1_dfcf,
                "sut_mb1": self.sut_mb1_dfcf,
                "sy_mb2": self.sy_mb2_dfcf,
                "sut_mb2": self.sut_mb2_dfcf
            },
            {
                "mb_iguales": self.mb_iguales_dfctor,
                "mb1": self.mb1_dfctor,
                "mb2": self.mb2_dfctor,
                "sy_mb1": self.sy_mb1_dfctor,
                "sut_mb1": self.sut_mb1_dfctor,
                "sy_mb2": self.sy_mb2_dfctor,
                "sut_mb2": self.sut_mb2_dfctor
            },
            {
                "mb_iguales": self.mb_iguales_dfcc,
                "mb1": self.mb1_dfcc,
                "mb2": self.mb2_dfcc,
                "sy_mb1": self.sy_mb1_dfcc,
                "sut_mb1": self.sut_mb1_dfcc,
                "sy_mb2": self.sy_mb2_dfcc,
                "sut_mb2": self.sut_mb2_dfcc
            }

        ]

        VentanaAnalisisFilete.obtencion_resistencias_mb(widgets_material_base, mb_comboboxes, objeto, contenido_objeto)

    def resistencias_material_aporte(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
           Realiza acciones específicas al seleccionar un tipo de electrodo de la lista desplegable.
           """

        # Código para el evento

        # Diccionario de dependencia de objetos (lista de electrodos, campos de resistencia para cada ventana)
        """Material de aporte comboboxes"""
        ma_comboboxes = {
            self.sist_und_dfcp: {
                self.electrodo_dfcp: (self.sy_e_dfcp,
                                      self.sut_e_dfcp)
            },
            self.sist_und_dfct: {
                self.electrodo_dfct: (self.sy_e_dfct,
                                      self.sut_e_dfct)
            },
            self.sist_und_dfcf: {
                self.electrodo_dfcf: (self.sy_e_dfcf,
                                      self.sut_e_dfcf)
            },
            self.sist_und_dfctor: {
                self.electrodo_dfctor: (self.sy_e_dfctor,
                                        self.sut_e_dfctor)
            },
            self.sist_und_dfcc: {
                self.electrodo_dfcc: (self.sy_e_dfcc,
                                      self.sut_e_dfcc)
            }
        }

        # Obtener objeto y contenido del objeto que emite la señal
        objeto = self.sender()
        contenido_objeto = self.sender().currentText()

        VentanaAnalisisFilete.obtencion_resistencias_ma(ma_comboboxes, objeto, contenido_objeto)

    def evento_limpiar_tab_actionnuevocalculo(self):

        # Obtener pestaña activa
        tab_widget = self.tab_widget
        tab_activa_index = tab_widget.currentIndex()
        tab_activa = tab_widget.widget(tab_activa_index)

        # Colocar todos los QlineEdits en 0 (datos de entrada)
        for widget in tab_activa.findChildren(QLineEdit):
            if isinstance(widget, QLineEdit):
                widget.setText("0")

        # Vaciar el contenido de todos los QTextBrowsers (resumen e informe de resultados)
        for widget in tab_activa.findChildren(QTextBrowser):
            if isinstance(widget, QTextBrowser):
                widget.setText("")

        # Deseleccionar el nombre de algún material
        for widget in tab_activa.findChildren(QComboBox):
            if isinstance(widget, QComboBox):
                widget.setCurrentText("")

        # Deseleccionar los QRadioButtons
        for widget in tab_activa.findChildren(QRadioButton):
            if isinstance(widget, QRadioButton):
                widget.setChecked(False)

    def cerrar_y_volver_a_inicio(self):
        """
        Slot para el evento de clic del botón de Volver a inicio en la barra menú.
        Realiza acciones específicas al presionar el botón.
        """

        # Declarar la ventana como una clase
        self.ventana_volver_inicio = VentanaPrincipal()

        # Abrir ventana de análisis de ranura
        self.ventana_volver_inicio.show()

        # Cerrar ventana de análisis de filete
        self.close()

    def cerrar_ventana(self):
        self.close()

    def calcular_h_dfcp(self):

        self.informe_resultados_dfcp.clear()
        self.resumen_resultados_dfcp.clear()

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "dos": self.g_2_dfcp,
            "seis": self.g_6_dfcp
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "dos":
            self.a_dfcp.setText("0")

        if self.iden_proyecto_dfcp is not None:
            nombre_proyecto = self.iden_proyecto_dfcp.text()
        else:
            nombre_proyecto = "S/I"

        # Cálculo de la pierna del cordón de soldadura

        # Verificar si se seleccionó carga estática
        try:

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_dfcp.text()),
                "sut_mb1": float(self.sut_mb1_dfcp.text()),
                "sy_mb2": float(self.sy_mb2_dfcp.text()),
                "sut_mb2": float(self.sut_mb2_dfcp.text()),
                "sy_e": float(self.sy_e_dfcp.text()),
                "sut_e": float(self.sut_e_dfcp.text()),
                "e": float(self.e_dfcp.text()),
                "l": float(self.l_dfcp.text()),
                "a": float(self.a_dfcp.text()),
                "fmax": float(self.fmax_dfcp.text()),
                "fmin": float(self.fmin_dfcp.text())
                }

            if self.cestatica_dfcp.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfcp.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Intermedia"
                fmax = diccionario_datos["fmax"]
                carga = {"Fmax": fmax}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                parametros_geometricos = {"largo": largo, "ancho": ancho}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, largo, ancho, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el diseño por estática de la pierna del cordón de soldadura
                resultados = diseno.DisenoPiernaFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo, geometria,
                                                       parametros_geometricos, espesor)

                print(1)

                # Extraer diccionario con resultados de diseño por estática
                dic_resultados_estatica = resultados.pierna_cp_estatica()

                print(2)

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_h_filete_cp(nombre_proyecto, "estática",
                                                                           {}, {},
                                                                           dic_resultados_estatica,
                                                                           self.sist_und_dfcp.currentText(),
                                                                           self.und_fuerza_dfcp_1.text(),
                                                                           self.und_distancia_dfcp_1.text(),
                                                                           self.und_esfuerzo_dfcp_1.text(),
                                                                           self.mb1_dfcp.currentText(),
                                                                           self.mb2_dfcp.currentText(),
                                                                           self.electrodo_dfcp.currentText()
                                                                           )

                print(3)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfcp.setText(info_resum[0])
                self.resumen_resultados_dfcp.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_dfcp.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfcp.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Intermedia"
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                carga = {"Fmax": fmax, "Fmin": fmin}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                parametros_geometricos = {"largo": largo, "ancho": ancho}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, largo, ancho, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el diseño por fatiga de la pierna del cordón de soldadura
                resultados = diseno.DisenoPiernaFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo, geometria,
                                                       parametros_geometricos, espesor)

                # Extraer diccionario con resultados de diseño por estática
                dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica = resultados.pierna_cp()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_h_filete_cp(nombre_proyecto, "de fatiga",
                                                                           dic_diseno_fatiga,
                                                                           dic_comprobacion, dic_diseno_estatica,
                                                                           self.sist_und_dfcp.currentText(),
                                                                           self.und_fuerza_dfcp_1.text(),
                                                                           self.und_distancia_dfcp_1.text(),
                                                                           self.und_esfuerzo_dfcp_1.text(),
                                                                           self.mb1_dfcp.currentText(),
                                                                           self.mb2_dfcp.currentText(),
                                                                           self.electrodo_dfcp.currentText()
                                                                           )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfcp.setText(info_resum[0])
                self.resumen_resultados_dfcp.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_dfcp.setEnabled(True)

    def calcular_h_dfct(self):

        self.informe_resultados_dfct.clear()
        self.resumen_resultados_dfct.clear()

        if self.iden_proyecto_dfct is not None:
            nombre_proyecto = self.iden_proyecto_dfct.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_dfct,
            "tres": self.g_3_dfct,
            "cinco": self.g_5_dfct,
            "siete": self.g_7_dfct,
            "ocho": self.g_8_dfct,
            "diez": self.g_10_dfct,
            "once": self.g_11_dfct,
            "doce": self.g_12_dfct,
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "uno":
            self.a_dfct.setText("0")
            self.radio_dfct.setText("0")
        elif geometria_seleccionada == "ocho":
            self.l_dfct.setText("0")
            self.a_dfct.setText("0")
        else:
            self.radio_dfct.setText("0")

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Intermedia": self.union_interm_dfct,
            "Unión T": self.union_t_dfct
        }

        union_seleccionada = None

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Cálculo de la pierna del cordón de soldadura

        # Verificar si se seleccionó carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_dfct.text()),
                "sut_mb1": float(self.sut_mb1_dfct.text()),
                "sy_mb2": float(self.sy_mb2_dfct.text()),
                "sut_mb2": float(self.sut_mb2_dfct.text()),
                "sy_e": float(self.sy_e_dfct.text()),
                "sut_e": float(self.sut_e_dfct.text()),
                "e": float(self.e_dfct.text()),
                "l": float(self.l_dfct.text()),
                "a": float(self.a_dfct.text()),
                "r": float(self.radio_dfct.text()),
                "fmax": float(self.fmax_dfct.text()),
                "fmin": float(self.fmin_dfct.text())
                }

            if self.cestatica_dfct.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfct.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                carga = {"Fmax": fmax}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, largo, ancho, radio, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el diseño por estática de la pierna del cordón de soldadura
                resultados = diseno.DisenoPiernaFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo, geometria,
                                                       parametros_geometricos, espesor)

                # Extraer diccionario con resultados de diseño por estática
                dic_resultados_estatica = resultados.pierna_ctrans_estatica()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_h_filete_ct(nombre_proyecto, "estática", {},
                                                                           {}, dic_resultados_estatica,
                                                                           self.sist_und_dfct.currentText(),
                                                                           self.und_fuerza_dfct_1.text(),
                                                                           self.und_distancia_dfct_1.text(),
                                                                           self.und_esfuerzo_dfct_1.text(),
                                                                           self.mb1_dfct.currentText(),
                                                                           self.mb2_dfct.currentText(),
                                                                           self.electrodo_dfct.currentText()
                                                                           )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfct.setText(info_resum[0])
                self.resumen_resultados_dfct.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_dfct.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfct.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                carga = {"Fmax": fmax, "Fmin": fmin}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, largo, ancho, radio, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el diseño por fatiga de la pierna del cordón de soldadura
                resultados = diseno.DisenoPiernaFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo, geometria,
                                                       parametros_geometricos, espesor)

                # Extraer diccionario con resultados de diseño por estática
                dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica = resultados.pierna_ctrans()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_h_filete_ct(nombre_proyecto, "de fatiga", dic_diseno_fatiga,
                                                                           dic_comprobacion, dic_diseno_estatica,
                                                                           self.sist_und_dfct.currentText(),
                                                                           self.und_fuerza_dfct_1.text(),
                                                                           self.und_distancia_dfct_1.text(),
                                                                           self.und_esfuerzo_dfct_1.text(),
                                                                           self.mb1_dfct.currentText(),
                                                                           self.mb2_dfct.currentText(),
                                                                           self.electrodo_dfct.currentText()
                                                                           )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfct.setText(info_resum[0])
                self.resumen_resultados_dfct.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_dfct.setEnabled(True)

    def calcular_h_dfcf(self):

        self.informe_resultados_dfcf.clear()
        self.resumen_resultados_dfcf.clear()

        if self.iden_proyecto_dfcf is not None:
            nombre_proyecto = self.iden_proyecto_dfcf.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_dfcf,
            "tres": self.g_3_dfcf,
            "cinco": self.g_5_dfcf,
            "seis": self.g_6_dfcf,
            "siete": self.g_7_dfcf,
            "ocho": self.g_8_dfcf,
            "nueve": self.g_9_dfcf,
            "diez": self.g_10_dfcf,
            "once": self.g_11_dfcf,
            "doce": self.g_12_dfcf,
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "uno":
            self.a_dfcf.setText("0")
            self.radio_dfcf.setText("0")
        elif geometria_seleccionada == "ocho":
            self.l_dfcf.setText("0")
            self.a_dfcf.setText("0")
        else:
            self.radio_dfcf.setText("0")

        # Cálculo de la pierna del cordón de soldadura

        # Verificar si se seleccionó carga estática
        try:

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_dfcf.text()),
                "sut_mb1": float(self.sut_mb1_dfcf.text()),
                "sy_mb2": float(self.sy_mb2_dfcf.text()),
                "sut_mb2": float(self.sut_mb2_dfcf.text()),
                "sy_e": float(self.sy_e_dfcf.text()),
                "sut_e": float(self.sut_e_dfcf.text()),
                "e": float(self.e_dfcf.text()),
                "l": float(self.l_dfcf.text()),
                "a": float(self.a_dfcf.text()),
                "r": float(self.radio_dfcf.text()),
                "fmax": float(self.fmax_dfcf.text()),
                "fmin": float(self.fmin_dfcf.text()),
                "b": float(self.b_dfcf.text())
                }

            if self.cestatica_dfcf.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfcf.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Unión T"
                fmax = diccionario_datos["fmax"]
                brazo = diccionario_datos["b"]
                carga = {"Fmax": fmax, "b": brazo}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, largo, ancho, radio, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                print(0)

                # Instancia para el diseño por estática de la pierna del cordón de soldadura
                resultados = diseno.DisenoPiernaFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo, geometria,
                                                       parametros_geometricos, espesor)

                print(1)

                # Mostrar valores en interfaz
                x, y = resultados.obtener_coordenadas_centroide()
                c = str(round(resultados.obtener_rx_ry()[1], 3))
                self.x_dfcf.setText(str(round(x, 3)))
                self.y_dfcf.setText(str(round(y, 3)))
                self.c_dfcf.setText(c)

                print(2)

                # Extraer diccionario con resultados de diseño por estática
                dic_resultados_estatica = resultados.pierna_cflex_estatica()

                print(3)

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_h_filete_cf(nombre_proyecto, "estática", {},
                                                                           {}, dic_resultados_estatica,
                                                                           self.sist_und_dfcf.currentText(),
                                                                           self.und_fuerza_dfcf_1.text(),
                                                                           self.und_distancia_dfcf_1.text(),
                                                                           self.und_esfuerzo_dfcf_1.text(),
                                                                           self.mb1_dfcf.currentText(),
                                                                           self.mb2_dfcf.currentText(),
                                                                           self.electrodo_dfcf.currentText()
                                                                           )

                print(4)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfcf.setText(info_resum[0])
                self.resumen_resultados_dfcf.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_dfcf.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfcf.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Unión T"
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                brazo = diccionario_datos["b"]
                carga = {"Fmax": fmax, "Fmin": fmin, "b": brazo}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, largo, ancho, radio, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el diseño por fatiga de la pierna del cordón de soldadura
                resultados = diseno.DisenoPiernaFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo, geometria,
                                                       parametros_geometricos, espesor)

                # Mostrar valores en interfaz
                x, y = resultados.obtener_coordenadas_centroide()
                c = str(round(resultados.obtener_rx_ry()[1], 3))
                self.x_dfcf.setText(str(round(x, 3)))
                self.y_dfcf.setText(str(round(y, 3)))
                self.c_dfcf.setText(c)

                # Extraer diccionario con resultados de diseño por estática
                dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica = resultados.pierna_cflex()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_h_filete_cf(nombre_proyecto, "de fatiga", dic_diseno_fatiga,
                                                                           dic_comprobacion, dic_diseno_estatica,
                                                                           self.sist_und_dfcf.currentText(),
                                                                           self.und_fuerza_dfcf_1.text(),
                                                                           self.und_distancia_dfcf_1.text(),
                                                                           self.und_esfuerzo_dfcf_1.text(),
                                                                           self.mb1_dfcf.currentText(),
                                                                           self.mb2_dfcf.currentText(),
                                                                           self.electrodo_dfcf.currentText()
                                                                           )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfcf.setText(info_resum[0])
                self.resumen_resultados_dfcf.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_dfcf.setEnabled(True)

    def calcular_h_dfctor(self):

        self.informe_resultados_dfctor.clear()
        self.resumen_resultados_dfctor.clear()

        if self.iden_proyecto_dfctor is not None:
            nombre_proyecto = self.iden_proyecto_dfctor.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_dfctor,
            "tres": self.g_3_dfctor,
            "cinco": self.g_5_dfctor,
            "seis": self.g_6_dfctor,
            "siete": self.g_7_dfctor,
            "ocho": self.g_8_dfctor,
            "nueve": self.g_9_dfctor,
            "diez": self.g_10_dfctor,
            "once": self.g_11_dfctor,
            "doce": self.g_12_dfctor,
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "uno":
            self.a_dfctor.setText("0")
            self.radio_dfctor.setText("0")
        elif geometria_seleccionada == "ocho":
            self.l_dfctor.setText("0")
            self.a_dfctor.setText("0")
        else:
            self.radio_dfctor.setText("0")

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Intermedia": self.union_interm_dfctor,
            "Unión T": self.union_t_dfctor
        }

        union_seleccionada = None

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Cálculo de la pierna del cordón de soldadura

        # Verificar si se seleccionó carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_dfctor.text()),
                "sut_mb1": float(self.sut_mb1_dfctor.text()),
                "sy_mb2": float(self.sy_mb2_dfctor.text()),
                "sut_mb2": float(self.sut_mb2_dfctor.text()),
                "sy_e": float(self.sy_e_dfctor.text()),
                "sut_e": float(self.sut_e_dfctor.text()),
                "e": float(self.e_dfctor.text()),
                "l": float(self.l_dfctor.text()),
                "a": float(self.a_dfctor.text()),
                "r": float(self.radio_dfctor.text()),
                "fmax": float(self.fmax_dfctor.text()),
                "fmin": float(self.fmin_dfctor.text()),
                "b": float(self.b_dfctor.text())
            }

            if self.cestatica_dfctor.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfctor.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                brazo = diccionario_datos["b"]
                carga = {"Fmax": fmax, "b": brazo}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, largo, ancho, radio, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el diseño por estática de la pierna del cordón de soldadura
                resultados = diseno.DisenoPiernaFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo, geometria,
                                                       parametros_geometricos, espesor)

                x, y = resultados.obtener_coordenadas_centroide()
                rx, ry = resultados.obtener_rx_ry()[0:2]
                r = str(round((rx ** 2 + ry ** 2) ** 0.5, 3))
                self.x_dfctor.setText(str(round(x, 3)))
                self.y_dfctor.setText(str(round(y, 3)))
                self.r_dfctor.setText(r)

                # Extraer diccionario con resultados de diseño por estática
                dic_resultados_estatica = resultados.pierna_ctor_estatica()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_h_filete_ctor(nombre_proyecto, "estática", {},
                                                                             {}, dic_resultados_estatica,
                                                                             self.sist_und_dfctor.currentText(),
                                                                             self.und_fuerza_dfctor_1.text(),
                                                                             self.und_distancia_dfctor_1.text(),
                                                                             self.und_esfuerzo_dfctor_1.text(),
                                                                             self.mb1_dfctor.currentText(),
                                                                             self.mb2_dfctor.currentText(),
                                                                             self.electrodo_dfctor.currentText()
                                                                             )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfctor.setText(info_resum[0])
                self.resumen_resultados_dfctor.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_dfctor.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfctor.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                brazo = diccionario_datos["b"]
                carga = {"Fmax": fmax, "Fmin": fmin, "b": brazo}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, largo, ancho, radio, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el diseño por fatiga de la pierna del cordón de soldadura
                resultados = diseno.DisenoPiernaFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo, geometria,
                                                       parametros_geometricos, espesor)

                # Mostrar valores en campos de interfaz
                x, y = resultados.obtener_coordenadas_centroide()
                rx, ry = resultados.obtener_rx_ry()[0:2]
                r = str(round((rx ** 2 + ry ** 2) ** 0.5, 3))
                self.x_dfctor.setText(str(round(x, 3)))
                self.y_dfctor.setText(str(round(y, 3)))
                self.r_dfctor.setText(r)

                # Extraer diccionario con resultados de diseño por estática
                dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica = resultados.pierna_ctor()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_h_filete_ctor(nombre_proyecto, "de fatiga", dic_diseno_fatiga,
                                                                             dic_comprobacion, dic_diseno_estatica,
                                                                             self.sist_und_dfctor.currentText(),
                                                                             self.und_fuerza_dfctor_1.text(),
                                                                             self.und_distancia_dfctor_1.text(),
                                                                             self.und_esfuerzo_dfctor_1.text(),
                                                                             self.mb1_dfctor.currentText(),
                                                                             self.mb2_dfctor.currentText(),
                                                                             self.electrodo_dfctor.currentText()
                                                                             )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfctor.setText(info_resum[0])
                self.resumen_resultados_dfctor.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_dfctor.setEnabled(True)

    def calcular_h_dfcc(self):

        self.informe_resultados_dfcc.clear()
        self.resumen_resultados_dfcc.clear()

        if self.iden_proyecto_dfcc is not None:
            nombre_proyecto = self.iden_proyecto_dfcc.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_dfcc,
            "cinco": self.g_5_dfcc,
            "seis": self.g_6_dfcc,
            "ocho": self.g_8_dfcc,
            "nueve": self.g_9_dfcc,
            "once": self.g_11_dfcc,
            "doce": self.g_12_dfcc,
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "uno":
            self.a_dfcc.setText("0")
            self.radio_dfcc.setText("0")
        elif geometria_seleccionada == "ocho":
            self.l_dfcc.setText("0")
            self.a_dfcc.setText("0")
        else:
            self.radio_dfcc.setText("0")

        # Cálculo de la pierna del cordón de soldadura

        # Verificar si se seleccionó carga estática
        try:

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_dfcc.text()),
                "sut_mb1": float(self.sut_mb1_dfcc.text()),
                "sy_mb2": float(self.sy_mb2_dfcc.text()),
                "sut_mb2": float(self.sut_mb2_dfcc.text()),
                "sy_e": float(self.sy_e_dfcc.text()),
                "sut_e": float(self.sut_e_dfcc.text()),
                "e": float(self.e_dfcc.text()),
                "l": float(self.l_dfcc.text()),
                "a": float(self.a_dfcc.text()),
                "r": float(self.radio_dfcc.text()),
                "fmax": float(self.fmax_dfcc.text()),
                "fmin": float(self.fmin_dfcc.text()),
                "bl": float(self.bl_dfcc.text()),
                "bt": float(self.bt_dfcc.text())
            }

            print(diccionario_datos)

            if self.cestatica_dfcc.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfcc.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Unión T"
                fmax = diccionario_datos["fmax"]
                bl = diccionario_datos["bl"]
                bt = diccionario_datos["bt"]
                carga = {"Fmax": fmax, "bl": bl, "bt": bt}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, bl, bt)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, largo, ancho, radio, bl, bt, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                print(sist_und, tipo_union, carga, mb1, mb2, electrodo, geometria,
                                                       parametros_geometricos, espesor)

                # Instancia para el diseño por estática de la pierna del cordón de soldadura
                resultados = diseno.DisenoPiernaFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo, geometria,
                                                       parametros_geometricos, espesor)

                # Mostrar valores en campos de interfaz
                x, y = resultados.obtener_coordenadas_centroide()
                rx, ry = resultados.obtener_rx_ry()[0:2]
                r = str(round((rx ** 2 + ry ** 2) ** 0.5, 3))
                c = str(round(resultados.obtener_rx_ry()[1], 3))
                self.c_dfcf.setText(c)
                self.x_dfcc.setText(str(round(x, 3)))
                self.y_dfcc.setText(str(round(y, 3)))
                self.r_dfcc.setText(r)

                print(0)

                # Extraer diccionario con resultados de diseño por estática
                dic_resultados_estatica = resultados.pierna_ccomb_estatica()

                print(1)

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_h_filete_cc(nombre_proyecto, "estática", {},
                                                                           {}, dic_resultados_estatica,
                                                                           self.sist_und_dfcc.currentText(),
                                                                           self.und_fuerza_dfcc_1.text(),
                                                                           self.und_distancia_dfcc_1.text(),
                                                                           self.und_esfuerzo_dfcc_1.text(),
                                                                           self.mb1_dfcc.currentText(),
                                                                           self.mb2_dfcc.currentText(),
                                                                           self.electrodo_dfcc.currentText()
                                                                           )

                print(2)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfcc.setText(info_resum[0])
                self.resumen_resultados_dfcc.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_dfcc.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_dfcc.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Unión T"
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                bl = diccionario_datos["bl"]
                bt = diccionario_datos["bt"]
                carga = {"Fmax": fmax, "Fmin": fmin, "bl": bl, "bt": bt}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                ancho = diccionario_datos["a"]
                radio = diccionario_datos["r"]
                parametros_geometricos = {"largo": largo, "ancho": ancho, "radio": radio}
                espesor = diccionario_datos["e"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, espesor, bl, bt)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    espesor, largo, ancho, radio, bl, bt, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el diseño por fatiga de la pierna del cordón de soldadura
                resultados = diseno.DisenoPiernaFilete(sist_und, tipo_union, carga, mb1, mb2, electrodo, geometria,
                                                       parametros_geometricos, espesor)

                # Mostrar valores en campos de interfaz
                x, y = resultados.obtener_coordenadas_centroide()
                rx, ry = resultados.obtener_rx_ry()[0:2]
                r = str(round((rx ** 2 + ry ** 2) ** 0.5, 3))
                c = str(round(resultados.obtener_rx_ry()[1], 3))
                self.c_dfcc.setText(c)
                self.x_dfcc.setText(str(round(x, 3)))
                self.y_dfcc.setText(str(round(y, 3)))
                self.r_dfcc.setText(r)

                print(0)

                # Extraer diccionario con resultados de diseño por estática
                dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica = resultados.pierna_ccomb()

                print(1)

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_h_filete_cc(nombre_proyecto, "de fatiga", dic_diseno_fatiga,
                                                                           dic_comprobacion, dic_diseno_estatica,
                                                                           self.sist_und_dfcc.currentText(),
                                                                           self.und_fuerza_dfcc_1.text(),
                                                                           self.und_distancia_dfcc_1.text(),
                                                                           self.und_esfuerzo_dfcc_1.text(),
                                                                           self.mb1_dfcc.currentText(),
                                                                           self.mb2_dfcc.currentText(),
                                                                           self.electrodo_dfcc.currentText()
                                                                           )

                print(2)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_dfcc.setText(info_resum[0])
                self.resumen_resultados_dfcc.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_dfcc.setEnabled(True)


class VentanaDisenoRanura(QMainWindow, ui_ventana_diseno_ranura):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Heredar metodos de clase de la clase VentanaAnalisisFilete
        self.ventana_analisis_filete = VentanaAnalisisFilete()

        # Conexión de señales y slots

        ############################################################################################################

        # Señal para cambiar las etiquetas de sistema de unidades
        comboboxes_sist_und = [self.sist_und_drcp, self.sist_und_drct, self.sist_und_drcf,
                               self.sist_und_drctor, self.sist_und_drcc]

        for combobox in comboboxes_sist_und:
            combobox.currentIndexChanged.connect(self.evento_actualizar_etiquetas)

        ############################################################################################################

        # Señal para copiar nombre del acero y resistencias para piezas de igual material
        checkboxes_material_base = [self.mb_iguales_drcp, self.mb_iguales_drct, self.mb_iguales_drcf,
                                    self.mb_iguales_drctor, self.mb_iguales_drcc]

        for checkbox in checkboxes_material_base:
            checkbox.toggled.connect(self.evento_copiar_resistenias_mb)

        ############################################################################################################

        # Señal para extraer de la base de datos las resistencias del material base
        comboboxes_material_base = [self.mb1_drcp, self.mb1_drct, self.mb1_drcf, self.mb1_drctor, self.mb1_drcc,
                                    self.mb2_drcp, self.mb2_drct, self.mb2_drcf, self.mb2_drctor, self.mb2_drcc]

        for combobox in comboboxes_material_base:
            combobox.currentIndexChanged.connect(self.evento_resistencias_materiales_base)

        ############################################################################################################

        # Señal para extraer de la base de datos las resistencias del material de aporte
        comboboxes_material_aporte = [self.electrodo_drcp, self.electrodo_drct, self.electrodo_drcf,
                                      self.electrodo_drctor, self.electrodo_drcc]

        for combobox in comboboxes_material_aporte:
            combobox.currentIndexChanged.connect(self.resistencias_material_aporte)

        ############################################################################################################

        # Diccionario de qlineedits de ingreso de datos
        qlineedit_datos_entrada = {
            "Carga paralela": [self.sy_mb1_drcp, self.sut_mb1_drcp,
                               self.sy_mb2_drcp, self.sut_mb2_drcp,
                               self.sy_e_drcp, self.sut_e_drcp,
                               self.t_drcp, self.l_drcp,
                               self.relacionf_drcp],
            "Carga transversal": [self.sy_mb1_drct, self.sy_mb2_drct,
                                  self.sut_mb1_drct, self.sut_mb2_drct,
                                  self.sy_e_drct, self.sut_e_drct,
                                  self.t_drct, self.l_drct,
                                  self.radio_drct, self.relacionf_drct],
            "Carga de flexión": [self.sy_mb1_drcf, self.sy_mb2_drcf,
                                 self.sut_mb1_drcf, self.sut_mb2_drcf,
                                 self.sy_e_drcf, self.sut_e_drcf,
                                 self.t_drcf, self.l_drcf,
                                 self.radio_drcf,
                                 self.relacionf_drcf, self.b_drcf],
            "Carga de torsión": [self.sy_mb1_drctor, self.sy_mb2_drctor,
                                 self.sut_mb1_drctor, self.sut_mb2_drctor,
                                 self.sy_e_drctor, self.sut_e_drctor,
                                 self.t_drctor, self.l_drctor,
                                 self.radio_drctor,
                                 self.relaciont_drctor],
            "Carga combinada": [self.sy_mb1_drcc, self.sy_mb2_drcc,
                                self.sut_mb1_drcc, self.sut_mb2_drcc,
                                self.sy_e_drcc, self.sut_e_drcc,
                                self.t_drcc, self.l_drcc,
                                self.radio_drcc,
                                self.relacionf_drcc,
                                self.bl_drcc, self.bt_drcc]
        }

        # Asignar validador en qlineedits para permitir sólo ingreso de floats
        for tipo_carga, qlineedits in qlineedit_datos_entrada.items():
            for qlineedit in qlineedits:
                qlineedit.setValidator(QDoubleValidator())

        ############################################################################################################

        # Señal de boton en barra menu de volver a inicio
        self.actionVolver_al_inicio.triggered.connect(self.cerrar_y_volver_a_inicio)

        # Señal de boton en barra menu de cerrar
        self.actionCerrar.triggered.connect(self.cerrar_ventana)

        # Señal de boton en barra menú para cálculo nuevo
        self.actionNuevo_calculo.triggered.connect(self.evento_limpiar_tab_actionnuevocalculo)

        # Señal de boton para calcular carga permisible para soldadura sometida a carga transversal
        self.boton_calcular_carga_drcp.clicked.connect(self.calcular_carga_drcp)

        # Señal de boton para calcular carga permisible para soldadura sometida a carga transversal
        self.boton_calcular_carga_drct.clicked.connect(self.calcular_carga_drct)

        # Señal de boton para calcular carga permisible para soldadura sometida a carga de flexión
        self.boton_calcular_carga_drcf.clicked.connect(self.calcular_carga_drcf)

        # Señal de boton para calcular carga permisible para soldadura sometida a carga de torsión
        self.boton_calcular_carga_dfctor.clicked.connect(self.calcular_carga_drctor)

        # Señal de boton para calcular carga permisible para soldadura sometida a carga paralela
        self.boton_calcular_carga_drcc.clicked.connect(self.calcular_carga_drcc)

        # SEÑALES PARA GUARDAR INFORMES

        # Carga paralela
        self.boton_guardar_drcp.clicked.connect(self.evento_guardar)

        # Carga transversal
        self.boton_guardar_drct.clicked.connect(self.evento_guardar)

        # Carga de flexión debido a una fuerza excéntrica
        self.boton_guardar_drcf.clicked.connect(self.evento_guardar)

        # Carga de torsión debido a una fuerza excéntrica
        self.boton_guardar_drctor.clicked.connect(self.evento_guardar)

        # Carga combinada debido a una fuerza excéntrica
        self.boton_guardar_drcc.clicked.connect(self.evento_guardar)

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def evento_guardar(self):
        """
        Método de evento para manejar la señal de clic en un botón de guardar.

        Obtiene el botón que emite la señal y llama al método 'guardar_informe' para guardar el informe asociado al botón.
        """

        dic_botones = {
            self.boton_guardar_drcp: self.informe_resultados_drcp,
            self.boton_guardar_drct: self.informe_resultados_drct,
            self.boton_guardar_drcf: self.informe_resultados_drcf,
            self.boton_guardar_drctor: self.informe_resultados_drctor,
            self.boton_guardar_drcc: self.informe_resultados_drcc
        }

        objeto = self.sender()

        VentanaAnalisisFilete.guardar_informe(self, objeto, dic_botones)

    def evento_actualizar_etiquetas(self):
        """Slot para el evento de cambio de índice de la lista desplegable de sistema de unidades.
       Realiza acciones específicas al seleccionar un índice de la lista desplegable.
       """

        # Diccionario de objetos etiquetas con unidades de esfuerzo, distancia y fuerza
        etiquetas_unidades = {
            self.sist_und_drct: {
                'esfuerzo': [self.und_esfuerzo_drct_1,
                             self.und_esfuerzo_drct_2,
                             self.und_esfuerzo_drct_3,
                             self.und_esfuerzo_drct_4,
                             self.und_esfuerzo_drct_5,
                             self.und_esfuerzo_drct_6],
                'distancia': [self.und_distancia_drct_1,
                              self.und_distancia_drct_2,
                              self.und_distancia_drct_3],
                'fuerza': [],
                'torque': []
            },
            self.sist_und_drcp: {
                "esfuerzo": [self.und_esfuerzo_drcp_1,
                             self.und_esfuerzo_drcp_2,
                             self.und_esfuerzo_drcp_3,
                             self.und_esfuerzo_drcp_4,
                             self.und_esfuerzo_drcp_5,
                             self.und_esfuerzo_drcp_6],
                'distancia': [self.und_distancia_drcp_1,
                              self.und_distancia_drcp_2],
                'fuerza': [],
                'torque': []
            },
            self.sist_und_drcf: {
                "esfuerzo": [self.und_esfuerzo_drcf_1,
                             self.und_esfuerzo_drcf_2,
                             self.und_esfuerzo_drcf_3,
                             self.und_esfuerzo_drcf_4,
                             self.und_esfuerzo_drcf_5,
                             self.und_esfuerzo_drcf_6],
                'distancia': [self.und_distancia_drcf_1,
                              self.und_distancia_drcf_2,
                              self.und_distancia_drcf_3,
                              self.und_distancia_drcf_4],
                'fuerza': [],
                'torque': []
            },
            self.sist_und_drctor: {
                'esfuerzo': [self.und_esfuerzo_drctor_1,
                             self.und_esfuerzo_drctor_2,
                             self.und_esfuerzo_drctor_3,
                             self.und_esfuerzo_drctor_4,
                             self.und_esfuerzo_drctor_5,
                             self.und_esfuerzo_drctor_6],
                'distancia': [self.und_distancia_drctor_1,
                              self.und_distancia_drctor_2,
                              self.und_distancia_drctor_3],
                'fuerza': [],
                'torque': []
            },
            self.sist_und_drcc: {
                'esfuerzo': [self.und_esfuerzo_drcc_1,
                             self.und_esfuerzo_drcc_2,
                             self.und_esfuerzo_drcc_3,
                             self.und_esfuerzo_drcc_4,
                             self.und_esfuerzo_drcc_5,
                             self.und_esfuerzo_drcc_6],
                'distancia': [self.und_distancia_drcc_1,
                              self.und_distancia_drcc_2,
                              self.und_distancia_drcc_3,
                              self.und_distancia_drcc_4,
                              self.und_distancia_drcc_5],
                'fuerza': [],
                'torque': []
            }
        }

        # Código para el evento

        # Obtener objeto que emite la señal y su contenido
        objeto = self.sender()
        contenido_objeto = self.sender().currentText()

        # Uso del método de clase para cambiar contenido sist und de etiquetas
        VentanaAnalisisFilete.cambiar_etiquetas(etiquetas_unidades, objeto, contenido_objeto)

    def evento_copiar_resistenias_mb(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
         Realiza acciones específicas al hacer click en el radiobutton.
         """
        # Código para el evento

        widgets_material_base = [
            {
                "mb_iguales": self.mb_iguales_drcp,
                "mb1": self.mb1_drcp,
                "mb2": self.mb2_drcp,
                "sy_mb1": self.sy_mb1_drcp,
                "sut_mb1": self.sut_mb1_drcp,
                "sy_mb2": self.sy_mb2_drcp,
                "sut_mb2": self.sut_mb2_drcp
            },
            {
                "mb_iguales": self.mb_iguales_drct,
                "mb1": self.mb1_drct,
                "mb2": self.mb2_drct,
                "sy_mb1": self.sy_mb1_drct,
                "sut_mb1": self.sut_mb1_drct,
                "sy_mb2": self.sy_mb2_drct,
                "sut_mb2": self.sut_mb2_drct
            },
            {
                "mb_iguales": self.mb_iguales_drcf,
                "mb1": self.mb1_drcf,
                "mb2": self.mb2_drcf,
                "sy_mb1": self.sy_mb1_drcf,
                "sut_mb1": self.sut_mb1_drcf,
                "sy_mb2": self.sy_mb2_drcf,
                "sut_mb2": self.sut_mb2_drcf
            },
            {
                "mb_iguales": self.mb_iguales_drctor,
                "mb1": self.mb1_drctor,
                "mb2": self.mb2_drctor,
                "sy_mb1": self.sy_mb1_drctor,
                "sut_mb1": self.sut_mb1_drctor,
                "sy_mb2": self.sy_mb2_drctor,
                "sut_mb2": self.sut_mb2_drctor
            },
            {
                "mb_iguales": self.mb_iguales_drcc,
                "mb1": self.mb1_drcc,
                "mb2": self.mb2_drcc,
                "sy_mb1": self.sy_mb1_drcc,
                "sut_mb1": self.sut_mb1_drcc,
                "sy_mb2": self.sy_mb2_drcc,
                "sut_mb2": self.sut_mb2_drcc
            }

        ]

        VentanaAnalisisFilete.copiar_resistencias_mb(widgets_material_base)

    def evento_resistencias_materiales_base(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
        Realiza acciones específicas al cambiar el contenido del combobox.
        """
        # Código para el evento

        # Diccionario de dependecia de objetos (lista desplegable de sistund, lista de materiales, lineas de texto
        mb_comboboxes = {
            self.sist_und_drcp: {
                self.mb1_drcp: (self.sy_mb1_drcp, self.sut_mb1_drcp),
                self.mb2_drcp: (self.sy_mb2_drcp, self.sut_mb2_drcp)
            },
            self.sist_und_drct: {
                self.mb1_drct: (self.sy_mb1_drct, self.sut_mb1_drct),
                self.mb2_drct: (self.sy_mb2_drct, self.sut_mb2_drct)
            },
            self.sist_und_drcf: {
                self.mb1_drcf: (self.sy_mb1_drcf, self.sut_mb1_drcf),
                self.mb2_drcf: (self.sy_mb2_drcf, self.sut_mb2_drcf)
            },
            self.sist_und_drctor: {
                self.mb1_drctor: (self.sy_mb1_drctor, self.sut_mb1_drctor),
                self.mb2_drctor: (self.sy_mb2_drctor, self.sut_mb2_drctor)
            },
            self.sist_und_drcc: {
                self.mb1_drcc: (self.sy_mb1_drcc, self.sut_mb1_drcc),
                self.mb2_drcc: (self.sy_mb2_drcc, self.sut_mb2_drcc)
            }
        }

        # Obtener objeto que emite la señal
        objeto = self.sender()

        # Obtener contenido del objeto que emite la señal (nombre de material seleccionado de lista desplegable)
        contenido_objeto = self.sender().currentText()

        widgets_material_base = [
            {
                "mb_iguales": self.mb_iguales_drcp,
                "mb1": self.mb1_drcp,
                "mb2": self.mb2_drcp,
                "sy_mb1": self.sy_mb1_drcp,
                "sut_mb1": self.sut_mb1_drcp,
                "sy_mb2": self.sy_mb2_drcp,
                "sut_mb2": self.sut_mb2_drcp
            },
            {
                "mb_iguales": self.mb_iguales_drct,
                "mb1": self.mb1_drct,
                "mb2": self.mb2_drct,
                "sy_mb1": self.sy_mb1_drct,
                "sut_mb1": self.sut_mb1_drct,
                "sy_mb2": self.sy_mb2_drct,
                "sut_mb2": self.sut_mb2_drct
            },
            {
                "mb_iguales": self.mb_iguales_drcf,
                "mb1": self.mb1_drcf,
                "mb2": self.mb2_drcf,
                "sy_mb1": self.sy_mb1_drcf,
                "sut_mb1": self.sut_mb1_drcf,
                "sy_mb2": self.sy_mb2_drcf,
                "sut_mb2": self.sut_mb2_drcf
            },
            {
                "mb_iguales": self.mb_iguales_drctor,
                "mb1": self.mb1_drctor,
                "mb2": self.mb2_drctor,
                "sy_mb1": self.sy_mb1_drctor,
                "sut_mb1": self.sut_mb1_drctor,
                "sy_mb2": self.sy_mb2_drctor,
                "sut_mb2": self.sut_mb2_drctor
            },
            {
                "mb_iguales": self.mb_iguales_drcc,
                "mb1": self.mb1_drcc,
                "mb2": self.mb2_drcc,
                "sy_mb1": self.sy_mb1_drcc,
                "sut_mb1": self.sut_mb1_drcc,
                "sy_mb2": self.sy_mb2_drcc,
                "sut_mb2": self.sut_mb2_drcc
            }
        ]

        VentanaAnalisisFilete.obtencion_resistencias_mb(widgets_material_base, mb_comboboxes, objeto, contenido_objeto)

    def resistencias_material_aporte(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
       Realiza acciones específicas al seleccionar un tipo de electrodo de la lista desplegable.
       """

        # Código para el evento

        # Diccionario de dependencia de objetos (lista de electrodos, campos de resistencia para cada ventana)
        """Material de aporte comboboxes"""
        ma_comboboxes = {
            self.sist_und_drcp: {
                self.electrodo_drcp: (self.sy_e_drcp,
                                      self.sut_e_drcp)
            },
            self.sist_und_drct: {
                self.electrodo_drct: (self.sy_e_drct,
                                      self.sut_e_drct)
            },
            self.sist_und_drcf: {
                self.electrodo_drcf: (self.sy_e_drcf,
                                      self.sut_e_drcf)
            },
            self.sist_und_drctor: {
                self.electrodo_drctor: (self.sy_e_drctor,
                                        self.sut_e_drctor)
            },
            self.sist_und_drcc: {
                self.electrodo_drcc: (self.sy_e_drcc,
                                      self.sut_e_drcc)
            }
        }

        # Obtener objeto y contenido del objeto que emite la señal
        objeto = self.sender()
        contenido_objeto = self.sender().currentText()

        VentanaAnalisisFilete.obtencion_resistencias_ma(ma_comboboxes, objeto, contenido_objeto)

    def evento_limpiar_tab_actionnuevocalculo(self):

        # Obtener pestaña activa
        tab_widget = self.tab_widget
        tab_activa_index = tab_widget.currentIndex()
        tab_activa = tab_widget.widget(tab_activa_index)

        # Colocar todos los QlineEdits en 0 (datos de entrada)
        for widget in tab_activa.findChildren(QLineEdit):
            if isinstance(widget, QLineEdit):
                widget.setText("0")

        # Vaciar el contenido de todos los QTextBrowsers (resumen e informe de resultados)
        for widget in tab_activa.findChildren(QTextBrowser):
            if isinstance(widget, QTextBrowser):
                widget.setText("")

        # Deseleccionar el nombre de algún material
        for widget in tab_activa.findChildren(QComboBox):
            if isinstance(widget, QComboBox):
                widget.setCurrentText("")

        # Deseleccionar los QRadioButtons
        for widget in tab_activa.findChildren(QRadioButton):
            if isinstance(widget, QRadioButton):
                widget.setChecked(False)

    def cerrar_y_volver_a_inicio(self):
        """
        Slot para el evento de clic del botón de Volver a inicio en la barra menú.
        Realiza acciones específicas al presionar el botón.
        """

        # Declarar la ventana como una clase
        self.ventana_volver_inicio = VentanaPrincipal()

        # Abrir ventana de análisis de ranura
        self.ventana_volver_inicio.show()

        # Cerrar ventana de análisis de filete
        self.close()

    def cerrar_ventana(self):
        self.close()

    def calcular_carga_drcp(self):

        self.informe_resultados_drcp.clear()
        self.resumen_resultados_drcp.clear()

        if self.iden_proyecto_drcp is not None:
            nombre_proyecto = self.iden_proyecto_drcp.text()
        else:
            nombre_proyecto = "S/I"

        # Cálculo de carga permisible
        try:

            # Casting de los datos ingresados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_drcp.text()),
                "sut_mb1": float(self.sut_mb1_drcp.text()),
                "sy_mb2": float(self.sy_mb2_drcp.text()),
                "sut_mb2": float(self.sut_mb2_drcp.text()),
                "sy_e": float(self.sy_e_drcp.text()),
                "sut_e": float(self.sut_e_drcp.text()),
                "t": float(self.t_drcp.text()),
                "l": float(self.l_drcp.text()),
                "relacion_f": float(self.relacionf_drcp.text())
            }

            if self.cestatica_drcp.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drcp.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Tope"
                geometria = "uno"
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                parametros_geometricos = {"espesor": garganta, "largo": largo}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoCargaPermisibleRanura(sist_und, tipo_union, 0, 0, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_estatica = resultados.carga_permisible_estatica_cp()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_ranura_cp(nombre_proyecto, "estática", {},
                                                                               {}, dic_resultados_estatica,
                                                                               self.sist_und_drcp.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_drcp_1.text(),
                                                                               self.und_esfuerzo_drcp_1.text(),
                                                                               self.mb1_drcp.currentText(),
                                                                               self.mb2_drcp.currentText(),
                                                                               self.electrodo_drcp.currentText()
                                                                               )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_drcp.setText(info_resum[0])
                self.resumen_resultados_drcp.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_drcp.isChecked():

                # Asignacion de datos necesarios a variables
                sist_und = self.sist_und_drcp.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Tope"
                geometria = "uno"
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                parametros_geometricos = {"espesor": garganta, "largo": largo}
                relacionf = diccionario_datos["relacion_f"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, relacionf)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoCargaPermisibleRanura(sist_und, tipo_union, relacionf, 0, mb1, mb2, electrodo,
                                                                geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_fatiga, dic_comprobacion, dic_resultados_estatica = resultados.carga_permisible_cp()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_ranura_cp(nombre_proyecto, "de fatiga",
                                                                               dic_resultados_fatiga, dic_comprobacion,
                                                                               dic_resultados_estatica,
                                                                               self.sist_und_drcp.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_drcp_1.text(),
                                                                               self.und_esfuerzo_drcp_1.text(),
                                                                               self.mb1_drcp.currentText(),
                                                                               self.mb2_drcp.currentText(),
                                                                               self.electrodo_drcp.currentText()
                                                                               )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_drcp.setText(info_resum[0])
                self.resumen_resultados_drcp.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_drcp.setEnabled(True)

    def calcular_carga_drct(self):

        self.informe_resultados_drct.clear()
        self.resumen_resultados_drct.clear()

        if self.iden_proyecto_drct is not None:
            nombre_proyecto = self.iden_proyecto_drct.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_drct,
            "tres": self.g_3_drct
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "tres":
            self.l_drct.setText("0")
        else:
            self.radio_drct.setText("0")

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Tope": self.union_tope_drct,
            "Unión T": self.union_t_drct
        }

        union_seleccionada = None

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Cálculo de carga permisible
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Casting de los datos ingresados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_drct.text()),
                "sut_mb1": float(self.sut_mb1_drct.text()),
                "sy_mb2": float(self.sy_mb2_drct.text()),
                "sut_mb2": float(self.sut_mb2_drct.text()),
                "sy_e": float(self.sy_e_drct.text()),
                "sut_e": float(self.sut_e_drct.text()),
                "t": float(self.t_drct.text()),
                "l": float(self.l_drct.text()),
                "radio": float(self.radio_drct.text()),
                "relacion_f": float(self.relacionf_drct.text())
            }

            print(diccionario_datos)

            if self.cestatica_drct.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drct.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, radio)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                print(0)

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoCargaPermisibleRanura(sist_und, tipo_union, 0, 0, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos)

                print(1)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_estatica = resultados.carga_permisible_estatica_ctrans()

                print(2)

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_ranura_ct(nombre_proyecto, "estática", {},
                                                                               {}, dic_resultados_estatica,
                                                                               self.sist_und_drct.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_drct_1.text(),
                                                                               self.und_esfuerzo_drct_1.text(),
                                                                               self.mb1_drct.currentText(),
                                                                               self.mb2_drct.currentText(),
                                                                               self.electrodo_drct.currentText()
                                                                               )

                print(3)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_drct.setText(info_resum[0])
                self.resumen_resultados_drct.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_drct.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drct.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                relacionf = diccionario_datos["relacion_f"]
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, radio, relacionf)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoCargaPermisibleRanura(sist_und, tipo_union, relacionf, 0, mb1, mb2, electrodo,
                                                                geometria, parametros_geometricos)

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_fatiga, dic_comprobacion, dic_resultados_estatica = resultados.carga_permisible_ctrans()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_ranura_ct(nombre_proyecto, "de fatiga",
                                                                               dic_resultados_fatiga,
                                                                               dic_comprobacion,
                                                                               dic_resultados_estatica,
                                                                               self.sist_und_drct.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_drct_1.text(),
                                                                               self.und_esfuerzo_drct_1.text(),
                                                                               self.mb1_drct.currentText(),
                                                                               self.mb2_drct.currentText(),
                                                                               self.electrodo_drct.currentText()
                                                                               )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_drct.setText(info_resum[0])
                self.resumen_resultados_drct.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_drct.setEnabled(True)

    def calcular_carga_drcf(self):

        self.informe_resultados_drcf.clear()
        self.resumen_resultados_drcf.clear()

        if self.iden_proyecto_drcf is not None:
            nombre_proyecto = self.iden_proyecto_drcf.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrias disponibles
        diccionario_geometrias = {
            "uno": self.g_1_drcf,
            "dos": self.g_2_drcf,
            "tres": self.g_3_drcf,
        }

        geometria_seleccionada = None

        # Obtención de la geometria seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "tres":
            self.l_drcf.setText("0")
        else:
            self.radio_drcf.setText("0")

        # Diccionario de tipos de union disponibles
        diccionario_union = {"Tope": self.union_tope_drcf,
                             "Unión T": self.union_t_drcf}

        union_seleccionada = None

        # Obtencion del tipo de union seleccionado
        for clave, objeto in diccionario_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Cálculo de carga permisible
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Casting de los datos ingresados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_drcf.text()),
                "sut_mb1": float(self.sut_mb1_drcf.text()),
                "sy_mb2": float(self.sy_mb2_drcf.text()),
                "sut_mb2": float(self.sut_mb2_drcf.text()),
                "sy_e": float(self.sy_e_drcf.text()),
                "sut_e": float(self.sut_e_drcf.text()),
                "t": float(self.t_drcf.text()),
                "l": float(self.l_drcf.text()),
                "radio": float(self.radio_drcf.text()),
                "brazo": float(self.b_drcf.text()),
                "relacion_f": float(self.relacionf_drcf.text())
            }

            if self.cestatica_drcf.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drcf.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}
                brazo = diccionario_datos["brazo"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta, brazo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, radio, brazo)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el diseño por estática para carga paralela
                resultados = diseno.DisenoCargaPermisibleRanura(sist_und, tipo_union, 0, brazo, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos)
                print(0)
                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_estatica = resultados.carga_permisible_estatica_cflex()
                print(1)
                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_ranura_cf(nombre_proyecto, "estática", {},
                                                                               {}, dic_resultados_estatica,
                                                                               self.sist_und_drcf.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_drcf_1.text(),
                                                                               self.und_esfuerzo_drcf_1.text(),
                                                                               self.mb1_drcf.currentText(),
                                                                               self.mb2_drcf.currentText(),
                                                                               self.electrodo_drcf.currentText()
                                                                               )
                print(2)
                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_drcf.setText(info_resum[0])
                self.resumen_resultados_drcf.setHtml(resumen)
                print(3)
            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_drcf.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drcf.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}
                brazo = diccionario_datos["brazo"]
                relacionf = diccionario_datos["relacion_f"]

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta, brazo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, radio, brazo, relacionf)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()
                print(0)
                # Instancia para el diseño por fatiga de carga paralela
                resultados = diseno.DisenoCargaPermisibleRanura(sist_und, tipo_union, relacionf, brazo, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos)
                print(1)
                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_fatiga, dic_comprobacion, dic_resultados_estatica = resultados.carga_permisible_cflex()
                print(2)
                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_ranura_cf(nombre_proyecto, "de fatiga",
                                                                               dic_resultados_fatiga,
                                                                               dic_comprobacion,
                                                                               dic_resultados_estatica,
                                                                               self.sist_und_drcf.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_drcf_1.text(),
                                                                               self.und_esfuerzo_drcf_1.text(),
                                                                               self.mb1_drcf.currentText(),
                                                                               self.mb2_drcf.currentText(),
                                                                               self.electrodo_drcf.currentText()
                                                                               )
                print(3)
                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_drcf.setText(info_resum[0])
                self.resumen_resultados_drcf.setHtml(resumen)
                print(4)
            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_drcf.setEnabled(True)

    def calcular_carga_drctor(self):

        self.informe_resultados_drctor.clear()
        self.resumen_resultados_drctor.clear()

        if self.iden_proyecto_drctor is not None:
            nombre_proyecto = self.iden_proyecto_drctor.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrias disponibles
        diccionario_geometrias = {
            "uno": self.g_1_drctor,
            "tres": self.g_3_drctor,
        }

        geometria_seleccionada = None

        # Obtención de la geometria seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        if geometria_seleccionada == "tres":
            self.l_drctor.setText("0")
        else:
            self.radio_drctor.setText("0")

        # Diccionario de tipos de union disponibles
        diccionario_union = {"Tope": self.union_tope_drctor,
                             "Unión T": self.union_t_drctor}

        union_seleccionada = None

        # Obtencion del tipo de union seleccionado
        for clave, objeto in diccionario_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Cálculo de carga permisible
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Casting de los datos ingresados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_drctor.text()),
                "sut_mb1": float(self.sut_mb1_drctor.text()),
                "sy_mb2": float(self.sy_mb2_drctor.text()),
                "sut_mb2": float(self.sut_mb2_drctor.text()),
                "sy_e": float(self.sy_e_drctor.text()),
                "sut_e": float(self.sut_e_drctor.text()),
                "t": float(self.t_drctor.text()),
                "l": float(self.l_drctor.text()),
                "radio": float(self.radio_drctor.text()),
                "relacion_t": float(self.relaciont_drctor.text())
            }

            if self.cestatica_drctor.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drctor.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, radio)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el diseño por estática de carga paralela
                resultados = diseno.DisenoCargaPermisibleRanura(sist_und, tipo_union, 0, 0, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos)

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_estatica = resultados.carga_permisible_estatica_ctor()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_ranura_ctor(nombre_proyecto, "estática", {},
                                                                                 {}, dic_resultados_estatica,
                                                                                 self.sist_und_drctor.currentText(),
                                                                                 und_fuerza,
                                                                                 self.und_distancia_drctor_1.text(),
                                                                                 self.und_esfuerzo_drctor_1.text(),
                                                                                 self.mb1_drctor.currentText(),
                                                                                 self.mb2_drctor.currentText(),
                                                                                 self.electrodo_drctor.currentText()
                                                                                 )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_drctor.setText(info_resum[0])
                self.resumen_resultados_drctor.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_drctor.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drctor.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                relaciont = diccionario_datos["relacion_t"]
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, radio, relaciont)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el diseño por fatiga para carga de torsión
                resultados = diseno.DisenoCargaPermisibleRanura(sist_und, tipo_union, relaciont, 0, mb1, mb2, electrodo,
                                                                geometria, parametros_geometricos)

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_fatiga, dic_comprobacion, dic_resultados_estatica = resultados.carga_permisible_ctor()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_ranura_ctor(nombre_proyecto, "de fatiga",
                                                                                 dic_resultados_fatiga,
                                                                                 dic_comprobacion,
                                                                                 dic_resultados_estatica,
                                                                                 self.sist_und_drctor.currentText(),
                                                                                 und_fuerza,
                                                                                 self.und_distancia_drctor_1.text(),
                                                                                 self.und_esfuerzo_drctor_1.text(),
                                                                                 self.mb1_drctor.currentText(),
                                                                                 self.mb2_drctor.currentText(),
                                                                                 self.electrodo_drctor.currentText()
                                                                                 )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_drctor.setText(info_resum[0])
                self.resumen_resultados_drctor.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_drctor.setEnabled(True)

    def calcular_carga_drcc(self):

        self.informe_resultados_drcc.clear()
        self.resumen_resultados_drcc.clear()

        if self.iden_proyecto_drcc is not None:
            nombre_proyecto = self.iden_proyecto_drcc.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrias disponibles
        diccionario_geometrias = {
            "uno": self.g_1_drcc,
            "dos": self.g_2_drcc,
            "tres": self.g_3_drcc,
        }

        geometria_seleccionada = None

        # Obtención de la geometria seleccionada
        for clave, objeto in diccionario_geometrias.items():
          if objeto.isChecked():
            geometria_seleccionada = clave
            break

        if geometria_seleccionada == "tres":
            self.l_drcc.setText("0")
        else:
            self.radio_drcc.setText("0")

        # Diccionario de tipos de union disponibles
        diccionario_union = {"Tope": self.union_tope_drcc,
                             "Unión T": self.union_t_drcc}

        union_seleccionada = None

        # Obtencion del tipo de union seleccionado
        for clave, objeto in diccionario_union.items():
          if objeto.isChecked():
            union_seleccionada = clave
            break

        # Cálculo de carga permisible
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Casting de los datos ingresados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_drcc.text()),
                "sut_mb1": float(self.sut_mb1_drcc.text()),
                "sy_mb2": float(self.sy_mb2_drcc.text()),
                "sut_mb2": float(self.sut_mb2_drcc.text()),
                "sy_e": float(self.sy_e_drcc.text()),
                "sut_e": float(self.sut_e_drcc.text()),
                "t": float(self.t_drcc.text()),
                "l": float(self.l_drcc.text()),
                "radio": float(self.radio_drcc.text()),
                "bl": float(self.bl_drcc.text()),
                "bt": float(self.bt_drcc.text()),
                "relacion_f": float(self.relacionf_drcc.text())
            }

            if self.cestatica_drcc.isChecked():

                sist_und = self.sist_und_drcc.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}
                bt = diccionario_datos["bt"]
                bl = diccionario_datos["bl"]
                brazo = {"bl": bl, "bt": bt}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta, bl, bt)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, radio, bl, bt)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el diseño por estática para carga combinada
                resultados = diseno.DisenoCargaPermisibleRanura(sist_und, tipo_union, 0, brazo, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos)

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Extraer diccionario con resultados de diseño
                dic_resultados_estatica = resultados.carga_permisible_estatica_ccomb()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_ranura_cc(nombre_proyecto, "estática", {}, {},
                                                                               dic_resultados_estatica,
                                                                               self.sist_und_drcc.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_drcc_1.text(),
                                                                               self.und_esfuerzo_drcc_1.text(),
                                                                               self.mb1_drcc.currentText(),
                                                                               self.mb2_drcc.currentText(),
                                                                               self.electrodo_drcc.currentText()
                                                                               )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_drcc.setText(info_resum[0])
                self.resumen_resultados_drcc.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_drcc.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drcc.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                relacionf = diccionario_datos["relacion_f"]
                geometria = geometria_seleccionada
                garganta = diccionario_datos["t"]
                largo = diccionario_datos["l"]
                radio = diccionario_datos["radio"]
                parametros_geometricos = {"espesor": garganta, "largo": largo, "radio exterior": radio}
                bl = diccionario_datos["bl"]
                bt = diccionario_datos["bt"]
                brazo = {"bl": bl, "bt": bt}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, garganta, bl, bt)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    garganta, largo, radio, bl, bt, relacionf)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el diseño por fatiga de carga paralela
                resultados = diseno.DisenoCargaPermisibleRanura(sist_und, tipo_union, relacionf, brazo, mb1, mb2,
                                                                electrodo, geometria, parametros_geometricos)

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_fatiga, dic_comprobacion, dic_resultados_estatica = resultados.carga_permisible_ccomb()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_carga_ranura_cc(nombre_proyecto, "de fatiga",
                                                                               dic_resultados_fatiga,
                                                                               dic_comprobacion,
                                                                               dic_resultados_estatica,
                                                                               self.sist_und_drcc.currentText(),
                                                                               und_fuerza,
                                                                               self.und_distancia_drcc_1.text(),
                                                                               self.und_esfuerzo_drcc_1.text(),
                                                                               self.mb1_drcc.currentText(),
                                                                               self.mb2_drcc.currentText(),
                                                                               self.electrodo_drcc.currentText()
                                                                               )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_drcc.setText(info_resum[0])
                self.resumen_resultados_drcc.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_drcc.setEnabled(True)


# Clase para ventana de ranura. Hereda de la clase de ventana de filete
class VentanaDisenoEspesorRanura(QMainWindow, ui_ventana_disenoespesor_ranura):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Herencia de la clase de Analisis filete
        self.ventana_analisis_filete = VentanaAnalisisFilete()

        # Conexión de señales y slots

        ############################################################################################################

        # Señal para cambiar las etiquetas de sistema de unidades
        comboboxes_sist_und = [self.sist_und_drcp, self.sist_und_drct, self.sist_und_drcf,
                               self.sist_und_drctor, self.sist_und_drcc]

        for combobox in comboboxes_sist_und:
            combobox.currentIndexChanged.connect(self.evento_actualizar_etiquetas)

        ############################################################################################################

        # Señal para copiar nombre del acero y resistencias para piezas de igual material
        checkboxes_material_base = [self.mb_iguales_drcp, self.mb_iguales_drct, self.mb_iguales_drcf,
                                    self.mb_iguales_drctor, self.mb_iguales_drcc]

        for checkbox in checkboxes_material_base:
            checkbox.toggled.connect(self.evento_copiar_resistenias_mb)

        ############################################################################################################

        # Señal para extraer de la base de datos las resistencias del material base
        comboboxes_material_base = [self.mb1_drcp, self.mb1_drct, self.mb1_drcf, self.mb1_drctor, self.mb1_drcc,
                                    self.mb2_drcp, self.mb2_drct, self.mb2_drcf, self.mb2_drctor, self.mb2_drcc]

        for combobox in comboboxes_material_base:
            combobox.currentIndexChanged.connect(self.evento_resistencias_materiales_base)

        ############################################################################################################

        # Señal para extraer de la base de datos las resistencias del material de aporte
        comboboxes_material_aporte = [self.electrodo_drcp, self.electrodo_drct, self.electrodo_drcf,
                                      self.electrodo_drctor, self.electrodo_drcc]

        for combobox in comboboxes_material_aporte:
            combobox.currentIndexChanged.connect(self.resistencias_material_aporte)

        ############################################################################################################

        # Diccionario de qlineedits de ingreso de datos
        qlineedit_datos_entrada = {
            "Carga paralela": [self.sy_mb1_drcp, self.sut_mb1_drcp,
                               self.sy_mb2_drcp, self.sut_mb2_drcp,
                               self.sy_e_drcp, self.sut_e_drcp,
                               self.l_drcp,
                               self.fmax_drcp, self.fmin_drcp],
            "Carga transversal": [self.sy_mb1_drct, self.sy_mb2_drct,
                                  self.sut_mb1_drct, self.sut_mb2_drct,
                                  self.sy_e_drct, self.sut_e_drct,
                                  self.l_drct,
                                  self.fmax_drct, self.fmin_drct],
            "Carga de flexión": [self.sy_mb1_drcf, self.sy_mb2_drcf,
                                 self.sut_mb1_drcf, self.sut_mb2_drcf,
                                 self.sy_e_drcf, self.sut_e_drcf,
                                 self.l_drcf,
                                 self.fmax_drcf, self.fmin_drcf, self.b_drcf],
            "Carga de torsión": [self.sy_mb1_drctor, self.sy_mb2_drctor,
                                 self.sut_mb1_drctor, self.sut_mb2_drctor,
                                 self.sy_e_drctor, self.sut_e_drctor,
                                 self.l_drctor,
                                 self.tmax_drctor, self.tmin_drctor],
            "Carga combinada": [self.sy_mb1_drcc, self.sy_mb2_drcc,
                                self.sut_mb1_drcc, self.sut_mb2_drcc,
                                self.sy_e_drcc, self.sut_e_drcc,
                                self.l_drcc,
                                self.fmax_drcc, self.fmin_drcc,
                                self.bl_drcc, self.bt_drcc]
        }

        # Asignar validador en qlineedits para permitir sólo ingreso de floats
        for tipo_carga, qlineedits in qlineedit_datos_entrada.items():
            for qlineedit in qlineedits:
                qlineedit.setValidator(QDoubleValidator())

        ############################################################################################################

        # Señal de boton en barra menu de volver a inicio
        self.actionVolver_al_inicio.triggered.connect(self.cerrar_y_volver_a_inicio)

        # Señal de boton en barra menu de cerrar
        self.actionCerrar.triggered.connect(self.cerrar_ventana)

        # Señal de boton en barra menú para cálculo nuevo
        self.actionNuevo_calculo.triggered.connect(self.evento_limpiar_tab_actionnuevocalculo)

        # SEÑALES PARA BOTONES DE CALCULAR FS

        # Carga paralela
        self.boton_calcularespesor_drcp.clicked.connect(self.calcular_espesor_drcp)

        # Carga transversal
        self.boton_calcularespesor_drct.clicked.connect(self.calcular_espesor_drct)

        # Carga de flexion
        self.boton_calcularespesor_drcf.clicked.connect(self.calcular_espesor_drcf)

        # Carga de torsion
        self.boton_calcularespesor_drctor.clicked.connect(self.calcular_espesor_drctor)

        # Carga de torsion
        self.boton_calcularespesor_drcc.clicked.connect(self.calcular_espesor_drcc)

        # SEÑALES PARA GUARDAR INFORMES

        # Carga paralela
        self.boton_guardar_drcp.clicked.connect(self.evento_guardar)

        # Carga transversal
        self.boton_guardar_drct.clicked.connect(self.evento_guardar)

        # Carga de flexion
        self.boton_guardar_drcf.clicked.connect(self.evento_guardar)

        # Carga de torsion
        self.boton_guardar_drctor.clicked.connect(self.evento_guardar)

        # Carga combinada
        self.boton_guardar_drcc.clicked.connect(self.evento_guardar)

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def evento_actualizar_etiquetas(self):
        """Slot para el evento de cambio de indice de la lista desplegable de sistema de unidades.
       Realiza acciones específicas al seleccionar un indice de la lista desplegable.
       """

        # Diccionario de objetos etiquetas con unidades de esfuerzo, distancia y fuerza
        etiquetas_unidades = {
            self.sist_und_drct: {
                'esfuerzo': [self.und_esfuerzo_drct_1,
                             self.und_esfuerzo_drct_2,
                             self.und_esfuerzo_drct_3,
                             self.und_esfuerzo_drct_4,
                             self.und_esfuerzo_drct_5,
                             self.und_esfuerzo_drct_6],
                'distancia': [self.und_distancia_drct_1],
                'fuerza': [self.und_fuerza_drct_1,
                           self.und_fuerza_drct_2],
                'torque': []
            },
            self.sist_und_drcp: {
                "esfuerzo": [self.und_esfuerzo_drcp_1,
                             self.und_esfuerzo_drcp_2,
                             self.und_esfuerzo_drcp_3,
                             self.und_esfuerzo_drcp_4,
                             self.und_esfuerzo_drcp_5,
                             self.und_esfuerzo_drcp_6],
                'distancia': [self.und_distancia_drcp_1],
                'fuerza': [self.und_fuerza_drcp_1,
                           self.und_fuerza_drcp_2],
                'torque': []
            },
            self.sist_und_drcf: {
                "esfuerzo": [self.und_esfuerzo_drcf_1,
                             self.und_esfuerzo_drcf_2,
                             self.und_esfuerzo_drcf_3,
                             self.und_esfuerzo_drcf_4,
                             self.und_esfuerzo_drcf_5,
                             self.und_esfuerzo_drcf_6],
                'distancia': [self.und_distancia_drcf_1,
                              self.und_distancia_drcf_3],
                'fuerza': [self.und_fuerza_drcf_1,
                           self.und_fuerza_drcf_2],
                'torque': []
            },
            self.sist_und_drctor: {
                'esfuerzo': [self.und_esfuerzo_drctor_1,
                             self.und_esfuerzo_drctor_2,
                             self.und_esfuerzo_drctor_3,
                             self.und_esfuerzo_drctor_4,
                             self.und_esfuerzo_drctor_5,
                             self.und_esfuerzo_drctor_6],
                'distancia': [self.und_distancia_drctor_1],
                'fuerza': [],
                'torque': [self.und_torque_drctor_1,
                           self.und_torque_drctor_2]
            },
            self.sist_und_drcc: {
                'esfuerzo': [self.und_esfuerzo_drcc_1,
                             self.und_esfuerzo_drcc_2,
                             self.und_esfuerzo_drcc_3,
                             self.und_esfuerzo_drcc_4,
                             self.und_esfuerzo_drcc_5,
                             self.und_esfuerzo_drcc_6],
                'distancia': [self.und_distancia_drcc_1,
                              self.und_distancia_drcc_3,
                              self.und_distancia_drcc_4],
                'fuerza': [self.und_fuerza_drcc_1,
                           self.und_fuerza_drcc_2],
                'torque': []
            }
        }

        # Código para el evento

        # Obtener objeto que emite la señal y su contenido
        objeto = self.sender()
        contenido_objeto = self.sender().currentText()

        # Uso del método de clase para cambiar contenido sist und de etiquetas
        VentanaAnalisisFilete.cambiar_etiquetas(etiquetas_unidades, objeto, contenido_objeto)

    def evento_copiar_resistenias_mb(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
         Realiza acciones específicas al hacer click en el radiobutton.
         """
        # Código para el evento

        widgets_material_base = [
            {
                "mb_iguales": self.mb_iguales_drcp,
                "mb1": self.mb1_drcp,
                "mb2": self.mb2_drcp,
                "sy_mb1": self.sy_mb1_drcp,
                "sut_mb1": self.sut_mb1_drcp,
                "sy_mb2": self.sy_mb2_drcp,
                "sut_mb2": self.sut_mb2_drcp
            },
            {
                "mb_iguales": self.mb_iguales_drct,
                "mb1": self.mb1_drct,
                "mb2": self.mb2_drct,
                "sy_mb1": self.sy_mb1_drct,
                "sut_mb1": self.sut_mb1_drct,
                "sy_mb2": self.sy_mb2_drct,
                "sut_mb2": self.sut_mb2_drct
            },
            {
                "mb_iguales": self.mb_iguales_drcf,
                "mb1": self.mb1_drcf,
                "mb2": self.mb2_drcf,
                "sy_mb1": self.sy_mb1_drcf,
                "sut_mb1": self.sut_mb1_drcf,
                "sy_mb2": self.sy_mb2_drcf,
                "sut_mb2": self.sut_mb2_drcf
            },
            {
                "mb_iguales": self.mb_iguales_drctor,
                "mb1": self.mb1_drctor,
                "mb2": self.mb2_drctor,
                "sy_mb1": self.sy_mb1_drctor,
                "sut_mb1": self.sut_mb1_drctor,
                "sy_mb2": self.sy_mb2_drctor,
                "sut_mb2": self.sut_mb2_drctor
            },
            {
                "mb_iguales": self.mb_iguales_drcc,
                "mb1": self.mb1_drcc,
                "mb2": self.mb2_drcc,
                "sy_mb1": self.sy_mb1_drcc,
                "sut_mb1": self.sut_mb1_drcc,
                "sy_mb2": self.sy_mb2_drcc,
                "sut_mb2": self.sut_mb2_drcc
            }

        ]

        VentanaAnalisisFilete.copiar_resistencias_mb(widgets_material_base)

    def evento_resistencias_materiales_base(self):
        """Slot para el evento de click en el botón de selección de materiales base iguales.
        Realiza acciones específicas al cambiar el contenido del combobox.
        """
        # Código para el evento

        # Diccionario de dependecia de objetos (lista desplegable de sistund, lista de materiales, lineas de texto
        mb_comboboxes = {
            self.sist_und_drcp: {
                self.mb1_drcp: (self.sy_mb1_drcp, self.sut_mb1_drcp),
                self.mb2_drcp: (self.sy_mb2_drcp, self.sut_mb2_drcp)
            },
            self.sist_und_drct: {
                self.mb1_drct: (self.sy_mb1_drct, self.sut_mb1_drct),
                self.mb2_drct: (self.sy_mb2_drct, self.sut_mb2_drct)
            },
            self.sist_und_drcf: {
                self.mb1_drcf: (self.sy_mb1_drcf, self.sut_mb1_drcf),
                self.mb2_drcf: (self.sy_mb2_drcf, self.sut_mb2_drcf)
            },
            self.sist_und_drctor: {
                self.mb1_drctor: (self.sy_mb1_drctor, self.sut_mb1_drctor),
                self.mb2_drctor: (self.sy_mb2_drctor, self.sut_mb2_drctor)
            },
            self.sist_und_drcc: {
                self.mb1_drcc: (self.sy_mb1_drcc, self.sut_mb1_drcc),
                self.mb2_drcc: (self.sy_mb2_drcc, self.sut_mb2_drcc)
            }
        }

        # Obtener objeto que emite la señal
        objeto = self.sender()

        # Obtener contenido del objeto que emite la señal (nombre de material seleccionado de lista desplegable)
        contenido_objeto = self.sender().currentText()

        widgets_material_base = [
            {
                "mb_iguales": self.mb_iguales_drcp,
                "mb1": self.mb1_drcp,
                "mb2": self.mb2_drcp,
                "sy_mb1": self.sy_mb1_drcp,
                "sut_mb1": self.sut_mb1_drcp,
                "sy_mb2": self.sy_mb2_drcp,
                "sut_mb2": self.sut_mb2_drcp
            },
            {
                "mb_iguales": self.mb_iguales_drct,
                "mb1": self.mb1_drct,
                "mb2": self.mb2_drct,
                "sy_mb1": self.sy_mb1_drct,
                "sut_mb1": self.sut_mb1_drct,
                "sy_mb2": self.sy_mb2_drct,
                "sut_mb2": self.sut_mb2_drct
            },
            {
                "mb_iguales": self.mb_iguales_drcf,
                "mb1": self.mb1_drcf,
                "mb2": self.mb2_drcf,
                "sy_mb1": self.sy_mb1_drcf,
                "sut_mb1": self.sut_mb1_drcf,
                "sy_mb2": self.sy_mb2_drcf,
                "sut_mb2": self.sut_mb2_drcf
            },
            {
                "mb_iguales": self.mb_iguales_drctor,
                "mb1": self.mb1_drctor,
                "mb2": self.mb2_drctor,
                "sy_mb1": self.sy_mb1_drctor,
                "sut_mb1": self.sut_mb1_drctor,
                "sy_mb2": self.sy_mb2_drctor,
                "sut_mb2": self.sut_mb2_drctor
            },
            {
                "mb_iguales": self.mb_iguales_drcc,
                "mb1": self.mb1_drcc,
                "mb2": self.mb2_drcc,
                "sy_mb1": self.sy_mb1_drcc,
                "sut_mb1": self.sut_mb1_drcc,
                "sy_mb2": self.sy_mb2_drcc,
                "sut_mb2": self.sut_mb2_drcc
            }
        ]

        VentanaAnalisisFilete.obtencion_resistencias_mb(widgets_material_base, mb_comboboxes, objeto, contenido_objeto)

    def resistencias_material_aporte(self):
        """Slot para el evento de clic en el botón de selección de materiales base iguales.
           Realiza acciones específicas al seleccionar un tipo de electrodo de la lista desplegable.
           """

        # Código para el evento

        # Diccionario de dependencia de objetos (lista de electrodos, campos de resistencia para cada ventana)
        """Material de aporte comboboxes"""
        ma_comboboxes = {
            self.sist_und_drcp: {
                self.electrodo_drcp: (self.sy_e_drcp,
                                      self.sut_e_drcp)
            },
            self.sist_und_drct: {
                self.electrodo_drct: (self.sy_e_drct,
                                      self.sut_e_drct)
            },
            self.sist_und_drcf: {
                self.electrodo_drcf: (self.sy_e_drcf,
                                      self.sut_e_drcf)
            },
            self.sist_und_drctor: {
                self.electrodo_drctor: (self.sy_e_drctor,
                                        self.sut_e_drctor)
            },
            self.sist_und_drcc: {
                self.electrodo_drcc: (self.sy_e_drcc,
                                      self.sut_e_drcc)
            }
        }

        # Obtener objeto y contenido del objeto que emite la señal
        objeto = self.sender()
        contenido_objeto = self.sender().currentText()

        VentanaAnalisisFilete.obtencion_resistencias_ma(ma_comboboxes, objeto, contenido_objeto)

    # Evento para limpiar los campos necesarios para realizar un nuevo cálculo
    def evento_limpiar_tab_actionnuevocalculo(self):

        # Obtener pestaña activa
        tab_widget = self.tab_widget
        tab_activa_index = tab_widget.currentIndex()
        tab_activa = tab_widget.widget(tab_activa_index)

        # Colocar todos los QlineEdits en 0 (datos de entrada)
        for widget in tab_activa.findChildren(QLineEdit):
            if isinstance(widget, QLineEdit):
                widget.setText("0")

        # Vaciar el contenido de todos los QTextBrowsers (resumen e informe de resultados)
        for widget in tab_activa.findChildren(QTextBrowser):
            if isinstance(widget, QTextBrowser):
                widget.setText("")

        # Deseleccionar el nombre de algún material
        for widget in tab_activa.findChildren(QComboBox):
            if isinstance(widget, QComboBox):
                widget.setCurrentText("")

        # Deseleccionar los QRadioButtons
        for widget in tab_activa.findChildren(QRadioButton):
            if isinstance(widget, QRadioButton):
                widget.setChecked(False)

    def cerrar_y_volver_a_inicio(self):
        """
        Slot para el evento de clic del botón de Volver a inicio en la barra menú.
        Realiza acciones específicas al presionar el botón.
        """

        # Declarar la ventana como una clase
        self.ventana_volver_inicio = VentanaPrincipal()

        # Abrir ventana de análisis de ranura
        self.ventana_volver_inicio.show()

        # Cerrar ventana de análisis de filete
        self.close()

    def cerrar_ventana(self):
        self.close()

    @staticmethod
    def mostrar_msg_error_sinsol():

        # Mensaje de aviso si no se consiguió solución
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Critical)
        message_box.setText(
            "Para las especificaciones de diseño indicadas, no se encontró solución real.\nConsidere cambiar las especificaciones de diseño.")
        message_box.setWindowTitle("Error")
        message_box.exec_()

    # Evento para calcular el espesor mínimo del cordón de ranura para carga paralela
    def calcular_espesor_drcp(self):

        self.informe_resultados_drcp.clear()
        self.resumen_resultados_drcp.clear()

        if self.iden_proyecto_drcp is not None:
            nombre_proyecto = self.iden_proyecto_drcp.text()
        else:
            nombre_proyecto = "S/I"

        # Cálculo de espesor para carga estática

        # Verificar si se seleccionó carga estática
        try:

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_drcp.text()),
                "sut_mb1": float(self.sut_mb1_drcp.text()),
                "sy_mb2": float(self.sy_mb2_drcp.text()),
                "sut_mb2": float(self.sut_mb2_drcp.text()),
                "sy_e": float(self.sy_e_drcp.text()),
                "sut_e": float(self.sut_e_drcp.text()),
                "l": float(self.l_drcp.text()),
                "fmax": float(self.fmax_drcp.text()),
                "fmin": float(self.fmin_drcp.text())
            }

            if self.cestatica_drcp.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drcp.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Tope"
                fmax = diccionario_datos["fmax"]
                carga = {"Fmax": fmax}
                geometria = "uno"
                largo = diccionario_datos["l"]
                parametros_geometricos = {"largo": largo}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, largo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    largo, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # AQUI MODIFICAR

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoEspesorRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                        geometria, parametros_geometricos)

                print(0)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_estatica = resultados.espesor_cp_estatica()

                print(1)

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_espesor_ranura_cp(nombre_proyecto, "estática",
                                                                                 {},
                                                                                 {},
                                                                                 dic_resultados_estatica,
                                                                                 self.sist_und_drcp.currentText(),
                                                                                 self.und_fuerza_drcp_1.text(),
                                                                                 self.und_distancia_drcp_1.text(),
                                                                                 self.und_esfuerzo_drcp_2.text(),
                                                                                 self.mb1_drcp.currentText(),
                                                                                 self.mb2_drcp.currentText(),
                                                                                 self.electrodo_drcp.currentText()
                                                                                 )

                print(2)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI el informe y el resumen
                self.informe_resultados_drcp.setText(info_resum[0])
                self.resumen_resultados_drcp.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_drcp.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drcp.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = "Tope"
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                carga = {"Fmax": fmax, "Fmin": fmin}
                geometria = "uno"
                largo = diccionario_datos["l"]
                parametros_geometricos = {"largo": largo}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, largo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    largo, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoEspesorRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                        geometria, parametros_geometricos)

                print(1)

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga, dic_comprobacion, dic_resultados_estatica = resultados.espesor_cp()

                print(2)

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_espesor_ranura_cp(nombre_proyecto, "de fatiga",
                                                                                 dic_resultados_fatiga, dic_comprobacion,
                                                                                 dic_resultados_estatica,
                                                                                 self.sist_und_drcp.currentText(),
                                                                                 self.und_fuerza_drcp_1.text(),
                                                                                 self.und_distancia_drcp_1.text(),
                                                                                 self.und_esfuerzo_drcp_2.text(),
                                                                                 self.mb1_drcp.currentText(),
                                                                                 self.mb2_drcp.currentText(),
                                                                                 self.electrodo_drcp.currentText()
                                                                                 )

                print(3)

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_drcp.setText(info_resum[0])
                self.resumen_resultados_drcp.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except TypeError:

            VentanaDisenoEspesorRanura.mostrar_msg_error_sinsol()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_drcp.setEnabled(True)

    # Evento para calcular el espesor mínimo del cordón de ranura para carga transversal
    def calcular_espesor_drct(self):

        self.informe_resultados_drct.clear()
        self.resumen_resultados_drct.clear()

        if self.iden_proyecto_drct is not None:
            nombre_proyecto = self.iden_proyecto_drct.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Tope": self.union_tope_drct,
            "Unión T": self.union_t_drct
        }

        union_seleccionada = None

        # Obtención de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Cálculo de espesor para carga estática

        # Verificar si se seleccionó carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_drct.text()),
                "sut_mb1": float(self.sut_mb1_drct.text()),
                "sy_mb2": float(self.sy_mb2_drct.text()),
                "sut_mb2": float(self.sut_mb2_drct.text()),
                "sy_e": float(self.sy_e_drct.text()),
                "sut_e": float(self.sut_e_drct.text()),
                "l": float(self.l_drct.text()),
                "fmax": float(self.fmax_drct.text()),
                "fmin": float(self.fmin_drct.text())
            }

            if self.cestatica_drct.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drct.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                carga = {"Fmax": fmax}
                geometria = "uno"
                largo = diccionario_datos["l"]
                parametros_geometricos = {"largo": largo}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, largo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    largo, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # AQUI MODIFICAR

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoEspesorRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                        geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_estatica = resultados.espesor_ctrans_estatica()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_espesor_ranura_ct(nombre_proyecto, "estática",
                                                                                 {}, {},
                                                                                 dic_resultados_estatica,
                                                                                 self.sist_und_drct.currentText(),
                                                                                 self.und_fuerza_drct_2.text(),
                                                                                 self.und_distancia_drct_1.text(),
                                                                                 self.und_esfuerzo_drct_2.text(),
                                                                                 self.mb1_drct.currentText(),
                                                                                 self.mb2_drct.currentText(),
                                                                                 self.electrodo_drct.currentText()
                                                                                 )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_drct.setText(info_resum[0])
                self.resumen_resultados_drct.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_drct.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drct.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                carga = {"Fmax": fmax, "Fmin": fmin}
                geometria = "uno"
                largo = diccionario_datos["l"]
                parametros_geometricos = {"largo": largo}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, largo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    largo, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoEspesorRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                        geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga, dic_comprobacion, dic_resultados_estatica = resultados.espesor_ctrans()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_espesor_ranura_ct(nombre_proyecto, "de fatiga",
                                                                                 dic_resultados_fatiga,
                                                                                 dic_comprobacion,
                                                                                 dic_resultados_estatica,
                                                                                 self.sist_und_drct.currentText(),
                                                                                 self.und_fuerza_drct_2.text(),
                                                                                 self.und_distancia_drct_1.text(),
                                                                                 self.und_esfuerzo_drct_2.text(),
                                                                                 self.mb1_drct.currentText(),
                                                                                 self.mb2_drct.currentText(),
                                                                                 self.electrodo_drct.currentText()
                                                                                 )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_drct.setText(info_resum[0])
                self.resumen_resultados_drct.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except TypeError:

            VentanaDisenoEspesorRanura.mostrar_msg_error_sinsol()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_drct.setEnabled(True)

    # Evento para calcular el espesor mínimo del cordón de ranura para carga de flexion
    def calcular_espesor_drcf(self):

        self.informe_resultados_drcf.clear()
        self.resumen_resultados_drcf.clear()

        if self.iden_proyecto_drcf is not None:
            nombre_proyecto = self.iden_proyecto_drcf.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_drcf,
            "dos": self.g_2_drcf
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Tope": self.union_tope_drcf,
            "Unión T": self.union_t_drcf
        }

        union_seleccionada = None

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Calculo de FS para carga estática

        # Verificar si se seleccionó carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_drcf.text()),
                "sut_mb1": float(self.sut_mb1_drcf.text()),
                "sy_mb2": float(self.sy_mb2_drcf.text()),
                "sut_mb2": float(self.sut_mb2_drcf.text()),
                "sy_e": float(self.sy_e_drcf.text()),
                "sut_e": float(self.sut_e_drcf.text()),
                "l": float(self.l_drcf.text()),
                "fmax": float(self.fmax_drcf.text()),
                "fmin": float(self.fmin_drcf.text()),
                "brazo": float(self.b_drcf.text())
            }

            if self.cestatica_drcf.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drcf.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                brazo = diccionario_datos["brazo"]
                carga = {"Fmax": fmax, "b": brazo}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                parametros_geometricos = {"largo": largo}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, largo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    largo, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoEspesorRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                        geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_estatica = resultados.espesor_cflex_estatica()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_espesor_ranura_cf(nombre_proyecto, "estática",
                                                                                 {},{},
                                                                                 dic_resultados_estatica,
                                                                                 self.sist_und_drcf.currentText(),
                                                                                 self.und_fuerza_drcf_2.text(),
                                                                                 self.und_distancia_drcf_1.text(),
                                                                                 self.und_esfuerzo_drcf_2.text(),
                                                                                 self.mb1_drcf.currentText(),
                                                                                 self.mb2_drcf.currentText(),
                                                                                 self.electrodo_drcf.currentText()
                                                                                 )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_drcf.setText(info_resum[0])
                self.resumen_resultados_drcf.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_drcf.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drcf.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                brazo = diccionario_datos["brazo"]
                carga = {"Fmax": fmax, "Fmin": fmin, "b": brazo}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                parametros_geometricos = {"largo": largo}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, largo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    largo, fmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoEspesorRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                        geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga, dic_comprobacion, dic_resultados_estatica = resultados.espesor_cflex()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_espesor_ranura_cf(nombre_proyecto, "de fatiga",
                                                                                 dic_resultados_fatiga,
                                                                                 dic_comprobacion,
                                                                                 dic_resultados_estatica,
                                                                                 self.sist_und_drcf.currentText(),
                                                                                 self.und_fuerza_drcf_2.text(),
                                                                                 self.und_distancia_drcf_1.text(),
                                                                                 self.und_esfuerzo_drcf_2.text(),
                                                                                 self.mb1_drcf.currentText(),
                                                                                 self.mb2_drcf.currentText(),
                                                                                 self.electrodo_drcf.currentText()
                                                                                 )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_drcf.setText(info_resum[0])
                self.resumen_resultados_drcf.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except TypeError:

            VentanaDisenoEspesorRanura.mostrar_msg_error_sinsol()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_drcf.setEnabled(True)

    # Evento para calcular el espesor mínimo del cordón de ranura para carga de torsion
    def calcular_espesor_drctor(self):

        self.informe_resultados_drctor.clear()
        self.resumen_resultados_drctor.clear()

        if self.iden_proyecto_drctor is not None:
            nombre_proyecto = self.iden_proyecto_drctor.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Tope": self.union_tope_drctor,
            "Unión T": self.union_t_drctor
        }

        union_seleccionada = None

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Calculo de FS para carga estática

        # Verificar si se seleccionó carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_drctor.text()),
                "sut_mb1": float(self.sut_mb1_drctor.text()),
                "sy_mb2": float(self.sy_mb2_drctor.text()),
                "sut_mb2": float(self.sut_mb2_drctor.text()),
                "sy_e": float(self.sy_e_drctor.text()),
                "sut_e": float(self.sut_e_drctor.text()),
                "l": float(self.l_drctor.text()),
                "tmax": float(self.tmax_drctor.text()),
                "tmin": float(self.tmin_drctor.text())
            }

            if self.cestatica_drctor.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drctor.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                tmax = diccionario_datos["tmax"]
                carga = {"Tmax": tmax}
                geometria = "uno"
                largo = diccionario_datos["l"]
                parametros_geometricos = {"largo": largo}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, largo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    largo, tmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoEspesorRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                        geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_estatica = resultados.espesor_ctor_estatica()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_espesor_ranura_ctor(nombre_proyecto, "estática",
                                                                                   {}, {},
                                                                                   dic_resultados_estatica,
                                                                                   self.sist_und_drctor.currentText(),
                                                                                   und_fuerza,
                                                                                   self.und_distancia_drctor_1.text(),
                                                                                   self.und_esfuerzo_drctor_2.text(),
                                                                                   self.mb1_drctor.currentText(),
                                                                                   self.mb2_drctor.currentText(),
                                                                                   self.electrodo_drctor.currentText()
                                                                                   )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_drctor.setText(info_resum[0])
                self.resumen_resultados_drctor.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_drctor.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drctor.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                tmax = diccionario_datos["tmax"]
                tmin = diccionario_datos["tmin"]
                carga = {"Tmax": tmax, "Tmin": tmin}
                geometria = "uno"
                largo = diccionario_datos["l"]
                parametros_geometricos = {"largo": largo}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, largo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    largo, tmax)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Almacenar unidad de fuerza según sistema de unidades
                if sist_und == "Internacional":
                    und_fuerza = "[N]"
                else:
                    und_fuerza = "[lb]"

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoEspesorRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                        geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga, dic_comprobacion, dic_resultados_estatica = resultados.espesor_ctor()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_espesor_ranura_ctor(nombre_proyecto, "de fatiga",
                                                                                   dic_resultados_fatiga,
                                                                                   dic_comprobacion,
                                                                                   dic_resultados_estatica,
                                                                                   self.sist_und_drctor.currentText(),
                                                                                   und_fuerza,
                                                                                   self.und_distancia_drctor_1.text(),
                                                                                   self.und_esfuerzo_drctor_2.text(),
                                                                                   self.mb1_drctor.currentText(),
                                                                                   self.mb2_drctor.currentText(),
                                                                                   self.electrodo_drctor.currentText()
                                                                                   )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_drctor.setText(info_resum[0])
                self.resumen_resultados_drctor.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except TypeError:

            VentanaDisenoEspesorRanura.mostrar_msg_error_sinsol()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_drctor.setEnabled(True)

    # Evento para calcular el espesor mínimo del cordón de ranura para carga combinada
    def calcular_espesor_drcc(self):

        self.informe_resultados_drcc.clear()
        self.resumen_resultados_drcc.clear()

        if self.iden_proyecto_drcc is not None:
            nombre_proyecto = self.iden_proyecto_drcc.text()
        else:
            nombre_proyecto = "S/I"

        # Diccionario de geometrías disponibles
        diccionario_geometrias = {
            "uno": self.g_1_drcc,
            "dos": self.g_2_drcc
        }

        geometria_seleccionada = None

        # Obtención de geometría seleccionada
        for clave, objeto in diccionario_geometrias.items():
            if objeto.isChecked():
                geometria_seleccionada = clave
                break

        # Diccionario de tipos de uniones disponibles
        tipo_union = {
            "Tope": self.union_tope_drcc,
            "Unión T": self.union_t_drcc
        }

        union_seleccionada = None

        # Obtencion de union seleccionada
        for clave, objeto in tipo_union.items():
            if objeto.isChecked():
                union_seleccionada = clave
                break

        # Calculo de FS para carga estática

        # Verificar si se seleccionó carga estática
        try:

            # Validador de seleccion de tipo de unión
            if union_seleccionada is None:
                error = 1 / 0

            # Diccionarios de inputs casteados
            diccionario_datos = {
                "sy_mb1": float(self.sy_mb1_drcc.text()),
                "sut_mb1": float(self.sut_mb1_drcc.text()),
                "sy_mb2": float(self.sy_mb2_drcc.text()),
                "sut_mb2": float(self.sut_mb2_drcc.text()),
                "sy_e": float(self.sy_e_drcc.text()),
                "sut_e": float(self.sut_e_drcc.text()),
                "l": float(self.l_drcc.text()),
                "fmax": float(self.fmax_drcc.text()),
                "fmin": float(self.fmin_drcc.text()),
                "bl": float(self.bl_drcc.text()),
                "bt": float(self.bt_drcc.text())
            }

            if self.cestatica_drcc.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drcc.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                bl = diccionario_datos["bl"]
                bt = diccionario_datos["bt"]
                carga = {"Fmax": fmax, "bl": bl, "bt": bt}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                parametros_geometricos = {"largo": largo}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, bl, bt, largo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    largo, fmax, bl, bt)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoEspesorRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                        geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis estático y bool de si falla
                dic_resultados_estatica = resultados.espesor_ccomb_estatica()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_espesor_ranura_cc(nombre_proyecto, "estática",
                                                                                 {}, {},
                                                                                 dic_resultados_estatica,
                                                                                 self.sist_und_drcc.currentText(),
                                                                                 self.und_fuerza_drcc_1.text(),
                                                                                 self.und_distancia_drcc_1.text(),
                                                                                 self.und_esfuerzo_drcc_2.text(),
                                                                                 self.mb1_drcc.currentText(),
                                                                                 self.mb2_drcc.currentText(),
                                                                                 self.electrodo_drcc.currentText()
                                                                                 )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_drcc.setText(info_resum[0])
                self.resumen_resultados_drcc.setHtml(resumen)

            # Verificar si se está seleccionado carga cíclica
            elif self.cciclica_drcc.isChecked():

                # Asignación de datos necesarios a variables
                sist_und = self.sist_und_drcc.currentText()
                sy_mb1 = diccionario_datos["sy_mb1"]
                sut_mb1 = diccionario_datos["sut_mb1"]
                sy_mb2 = diccionario_datos["sy_mb2"]
                sut_mb2 = diccionario_datos["sut_mb2"]
                mb1 = {"Sy": sy_mb1, "Sut": sut_mb1}
                mb2 = {"Sy": sy_mb2, "Sut": sut_mb2}
                sy_e = diccionario_datos["sy_e"]
                sut_e = diccionario_datos["sut_e"]
                electrodo = {"Sy": sy_e, "Sut": sut_e}
                tipo_union = union_seleccionada
                fmax = diccionario_datos["fmax"]
                fmin = diccionario_datos["fmin"]
                bl = diccionario_datos["bl"]
                bt = diccionario_datos["bt"]
                carga = {"Fmax": fmax, "Fmin": fmin, "bl": bl, "bt": bt}
                geometria = geometria_seleccionada
                largo = diccionario_datos["l"]
                parametros_geometricos = {"largo": largo}

                VentanaAnalisisFilete.validar_datos('ceros', sy_mb1, sy_mb2, sut_mb1, sut_mb2, sy_e,
                                                    sut_e, bl, bt, largo)

                VentanaAnalisisFilete.validar_datos('negativos', sy_mb1, sy_mb2, sut_mb1, sut_mb2,
                                                    largo, fmax, bl, bt)

                if sut_e < min(sut_mb1, sut_mb2):
                    VentanaAnalisisFilete.mostrar_msg_aviso_electrodo()

                # Instancia para el análisis estático de carga paralela
                resultados = diseno.DisenoEspesorRanura(sist_und, tipo_union, carga, mb1, mb2, electrodo,
                                                        geometria, parametros_geometricos)

                # Extraer diccionario con resultados de análisis de fatiga
                dic_resultados_fatiga, dic_comprobacion, dic_resultados_estatica = resultados.espesor_ccomb()

                # Obtener tupla que contiene el informe y el resumen
                info_resum = generador_informes.informe_diseno_espesor_ranura_cc(nombre_proyecto, "de fatiga",
                                                                                 dic_resultados_fatiga,
                                                                                 dic_comprobacion,
                                                                                 dic_resultados_estatica,
                                                                                 self.sist_und_drcc.currentText(),
                                                                                 self.und_fuerza_drcc_1.text(),
                                                                                 self.und_distancia_drcc_1.text(),
                                                                                 self.und_esfuerzo_drcc_2.text(),
                                                                                 self.mb1_drcc.currentText(),
                                                                                 self.mb2_drcc.currentText(),
                                                                                 self.electrodo_drcc.currentText()
                                                                                 )

                resumen = info_resum[1]
                # Mostrar en los QTextBrowser de la UI
                self.informe_resultados_drcc.setText(info_resum[0])
                self.resumen_resultados_drcc.setHtml(resumen)

            else:

                VentanaAnalisisFilete.mostrar_msg_error()

        except TypeError:

            VentanaDisenoEspesorRanura.mostrar_msg_error_sinsol()

        except:

            VentanaAnalisisFilete.mostrar_msg_error()

        else:

            self.boton_guardar_drcc.setEnabled(True)

    def evento_guardar(self):
        """
        Método de evento para manejar la señal de clic en un botón de guardar.

        Obtiene el botón que emite la señal y llama al método 'guardar_informe' para guardar el informe asociado al botón.
        """

        dic_botones = {
            self.boton_guardar_drcp: self.informe_resultados_drcp,
            self.boton_guardar_drct: self.informe_resultados_drct,
            self.boton_guardar_drcf: self.informe_resultados_drcf,
            self.boton_guardar_drctor: self.informe_resultados_drctor,
            self.boton_guardar_drcc: self.informe_resultados_drcc
        }

        objeto = self.sender()

        VentanaAnalisisFilete.guardar_informe(self, objeto, dic_botones)


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec_()
