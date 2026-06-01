from src.calculos.generador_informes import *
from src.calculos import diseno, analisis


"""prueba_cargapermisible = diseno.DisenoCargaPermisibleFilete("Internacional", "Intermedia", 0,
                                                            200,
                                          {"Sy": 250, "Sut": 400}, {"Sy": 345, "Sut": 415},
                                                   {"Sy": 393, "Sut": 482} , "ocho",
                                          {"pierna": 5, "largo": 0, "ancho": 0, "radio": 40}, 15)

dic_diseno_estatica = prueba_cargapermisible.carga_permisible_estatica_ctor()
resultado, resumen = informe_diseno_carga_filete_ctor("estática", {}, {},
                                                dic_diseno_estatica, "Internacional","N",
                                                "mm", "MPa", "ASTM A36",
                                                "ASTM A36", "E70XX")

print(dic_diseno_estatica)"""



"""prueba_pierna = diseno.DisenoPiernaFilete("Internacional", "Unión T", {"Fmax": 7000, "Fmin": 1500, "bl": 150, "bt":100},
                                          {"Sy": 250, "Sut": 400},
                                          {"Sy": 250, "Sut": 400}, {"Sy": 345, "Sut": 415},
                                   "nueve", {"largo": 150, "ancho": 80, "radio": 0},
                                          15)"""

"""dic_diseno_fatiga, dic_comprobracion, dic_diseno_estatica = prueba_pierna.pierna_ccomb()

resultado, resumen = informe_diseno_h_filete_cc("de fatiga", dic_diseno_fatiga, dic_comprobracion,
                                                dic_diseno_estatica, "Internacional","N",
                                                "mm", "MPa", "ASTM A36",
                                                "ASTM A36", "E60XX")

print(resultado)
print(resumen)"""

"""dic_diseno_estatica = prueba_pierna.pierna_ccomb_estatica()

resultado, resumen = informe_diseno_h_filete_cc("estática", {}, {},
                                                dic_diseno_estatica, "Internacional","N",
                                                "mm", "MPa", "ASTM A36",
                                                "ASTM A36", "E60XX")
print(resultado)
print(resumen)"""

prueba_carga_ranura = diseno.DisenoCargaPermisibleRanura("Internacional", "Unión T", 3, 150,
                                                         {"Sy": 250, "Sut": 415}, {"Sy": 250, "Sut": 415},
                                                         {"Sy": 345, "Sut": 415}, "dos",
                                                         {"espesor": 8, "largo": 80, "radio exterior": 0})

dic_diseno_fatiga, dic_comprobacion, dic_diseno_estatica = prueba_carga_ranura.carga_permisible_cflex()

resultado, resumen = informe_diseno_carga_ranura_cf("lol", "de fatiga", dic_diseno_fatiga, dic_comprobacion,
                                                    dic_diseno_estatica, "Internacional", "N",
                                                    "mm", "MPa", "ASTM A36", "ASTM A36",
                                                    "E60XX")

"""dic_diseno_estatica = prueba_carga_ranura.carga_permisible_estatica_ccomb()

resultado, informe = informe_diseno_carga_ranura_cc("estática", {}, {},
                                                    dic_diseno_estatica, "Internacional", "N",
                                                    "mm", "MPa", "ASTM A36", "ASTM A36",
                                                    "E60XX")

print(resultado)
print(informe)"""

"""prueba_analisis_filete = analisis.AnalisisSoldaduraFilete("Internacional", "Unión T",{"Fmax": 7000, "Fmin": 1500, "bl": 100, "bt": 100}, {"Sy": 250, "Sut": 415},
                                 {"Sy": 250, "Sut": 415}, {"Sy": 345, "Sut": 415},
                                 "nueve", {"pierna": 5, "largo": 80, "ancho": 50, "radio": 0}, 8)"""

"""falla, dic_analisis_estatica = prueba_analisis_filete.analisis_estatico_cflex()

resultado, resumen_est, resumen_fat = informe_analisis_filete_cf("estática", dic_analisis_estatica, {}, falla,
                                                "Internacional", "N", "mm", "MPa",
                                                "ASTM A36", "ASTM A36", "E60XX")
print(resultado)
print(resumen_est)"""

"""dic_analisis_fat = prueba_analisis_filete.analisis_fatiga_ccomb()[1]
falla, dic_analisis_est = prueba_analisis_filete.analisis_estatico_ccomb()

resultado, resumen_est, resumen_fat = informe_analisis_filete_cc("de fatiga", dic_analisis_est, dic_analisis_fat, falla,
                                                "Internacional", "N", "mm", "MPa",
                                                "ASTM A36", "ASTM A36", "E60XX")
print(resultado)
print(resumen_fat)
"""

"""prueba_analisis_ranura = analisis.AnalisisSoldaduraRanura("Internacional", "Unión T", {"Fmax": 10000, "Fmin": 0, "bl": 100, "bt": 50},
                                                 {"Sy": 250, "Sut": 400}, {"Sy": 250, "Sut": 400},
                                                 {"Sy": 345, "Sut": 415}, "uno",
                                                          {"espesor": 10, "largo": 100, "radio exterior": 0})

dic_analisis_fat = prueba_analisis_ranura.analisis_fatiga_ccomb()[1]
falla, dic_analisis_est = prueba_analisis_ranura.analisis_estatico_ccomb()

resultado, resumen_est, resumen_fat = informe_analisis_ranura_ccomb("de fatiga", dic_analisis_est, dic_analisis_fat, falla,
                                                "Internacional", "N", "mm", "MPa",
                                                "ASTM A36", "ASTM A36", "E60XX")
print(resultado)
print(resumen_est)
print(resumen_fat)
"""

"""prueba_cargapermisible = diseno.DisenoCargaPermisibleFilete("Internacional", "Unión T", 2,
                                                            {"bl": 150, "bt": 50},
                                          {"Sy": 250, "Sut": 400}, {"Sy": 345, "Sut": 415},
                                                   {"Sy": 345, "Sut": 415} , "nueve",
                                          {"pierna": 7, "largo": 150, "ancho": 80, "radio": 0}, 15)
"""
"""dic_diseno_estatica = prueba_cargapermisible.carga_permisible_estatica_ccomb()
resultado, resumen = informe_diseno_carga_filete_cc("estática", {}, {},
                                                dic_diseno_estatica, "Internacional","N",
                                                "mm", "MPa", "ASTM A36",
                                                "ASTM A36", "E60XX")"""

"""dic_diseno_fatiga, dic_comprobracion, dic_diseno_estatica = prueba_cargapermisible.carga_permisible_ccomb()
resultado, resumen = informe_diseno_carga_filete_cc("de fatiga", dic_diseno_fatiga, dic_comprobracion,
                                                dic_diseno_estatica, "Internacional","N",
                                                "mm", "MPa", "ASTM A36",
                                                "ASTM A36", "E60XX")"""


