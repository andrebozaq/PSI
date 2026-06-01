from src.calculos import diseno
"""
prueba_carga_permisible_filete = diseno.DisenoCargaPermisibleFilete("Internacional", "Intermedia", 2,
                                                                    0, {"Sy": 250, "Sut": 400},
                                                                    {"Sy": 250, "Sut": 400}, {"Sy": 345, "Sut": 415},
                                                                    "cinco",
                                                                    {"pierna": 7, "largo": 100, "ancho": 50},
                                                                    15)

resultados = prueba_carga_permisible_filete.carga_permisible_estatica_cp()
print(resultados)"""





"""prueba_pierna = diseno.DisenoPiernaFilete("Internacional", "Unión T", {"Fmax": 10000, "Fmin": 1000, "b": 200},
                                          {"Sy": 250, "Sut": 400}, {"Sy": 250, "Sut": 400},
                                          {"Sy": 345, "Sut": 415}, "ocho",
                                          {"largo": 200, "ancho": 80, "radio": 50}, 15)

diseno_fatiga, comprobacion_estatica, rediseno_estatica = prueba_pierna.pierna_ctor()
print(diseno_fatiga)
print(comprobacion_estatica)
print(rediseno_estatica)"""



"""ejercicio_tubular_mott = analisis.AnalisisSoldaduraFilete("Inglés", "Unión T", {"Fmax": 2500, "Fmin": 0, "bl": 14, "bt": 8},
                                            {"Sy": 36000, "Sut": 58000}, {"Sy": 36000, "Sut": 58000},
                                            {"Sy": 50000, "Sut": 60000}, "ocho", {"pierna": 1/4, "radio": 2.25}, 0.5)
ejercicio_tubular_mott.analisis_estatico_ccomb()"""

"""ejericio_tira_mott = diseno.DisenoPiernaFilete("Inglés", "Intermedia", {"Fmax": 3500, "Fmin": 3500, "b": 10.86},
                                        {"Sy": 36000, "Sut": 58000}, {"Sy": 36000, "Sut": 58000}, {"Sy": 50000, "Sut": 60000},
                                        "siete", {"largo": 4, "ancho": 6}, 0.5)

ejericio_tira_mott.pierna_ctor_estatica()"""

"""ejercicio_mensula_mott = DisenoPiernaFilete("Inglés", "Intermedia", {"Fmax": 3500, "Fmin": 3500, "b": 10.86},
                                        {"Sy": 36000, "Sut": 58000}, {"Sy": 36000, "Sut": 58000}, {"Sy": 50000, "Sut": 60000},
                                        "siete", {"largo": 4, "ancho": 6}, 0.5)

pierna = ejercicio_mensula_mott.pierna_ctor_estatica()
print(pierna)
if pierna is not None:
    analisis.verificar_tamano_minimo_pierna("Inglés", 0.5, pierna)

Se me ocurrió que de esta manera se puede incluir la verificacion del tamaño mínimo de la pierna del cordón para los casos de 
diseño por estática"""

"""prueba_pierna_filete = diseno.DisenoPiernaFilete("Internacional", "Unión T", {"Fmax": 5000, "Fmin": 1000,  "b": 150},
                                          {"Sy": 250, "Sut": 400}, {"Sy": 250, "Sut": 400},
                                          {"Sy": 345, "Sut": 415}, "ocho",
                                          {"largo": 0, "ancho": 0, "radio": 50}, 20)
prueba_pierna_filete.pierna_ctor()"""


"""prueba_pierna_filete = diseno.DisenoPiernaFilete("Internacional", "Unión T", {"Fmax": 5000, "Fmin": 1000, "b": 300},
                                          {"Sy": 250, "Sut": 400}, {"Sy": 250, "Sut": 400},
                                          {"Sy": 345, "Sut": 415}, "ocho",
                                          {"largo": 0, "ancho": 0, "radio": 50}, 20)
prueba_pierna_filete.pierna_cflex()"""

"""prueba_pierna_filete = diseno.DisenoPiernaFilete("Internacional", "Unión T", {"Fmax": 5000, "Fmin": 1000, "b": 150},
                                          {"Sy": 250, "Sut": 400}, {"Sy": 250, "Sut": 400},
                                          {"Sy": 345, "Sut": 415}, "ocho",
                                          {"largo": 0, "ancho": 0, "radio": 50}, 20)
prueba_pierna_filete.pierna_ctor()"""

"""prueba_carga_ranura = diseno.DisenoCargaPermisibleRanura("Internacional", "Tope", 3, 150,
                                                         {"Sy": 250, "Sut": 415}, {"Sy": 250, "Sut": 415},
                                                         {"Sy": 345, "Sut": 415}, "dos",
                                                         {"espesor": 8, "largo": 70, "radio exterior": 50})
diseno_fatiga, comprobacion_estatica, rediseno_estatica = prueba_carga_ranura.carga_permisible_ctor()
print(diseno_fatiga)
print(comprobacion_estatica)
print(rediseno_estatica)"""

prueba_espesor_ranura = diseno.DisenoEspesorRanura("Internacional", "Tope", {"Tmax": 2500, "Tmin": 0},
                                                   {"Sy": 240, "Sut": 415}, {"Sy": 240, "Sut": 415},
                                                   {"Sy": 345, "Sut": 415}, "tres", {"largo": 0, "radio exterior": 12})
"""resultados, comprobacion_estatica, rediseno_estatica = prueba_espesor_ranura.espesor_ctor()
print(resultados)
print(comprobacion_estatica)
print(rediseno_estatica)"""

diseno_estatica = prueba_espesor_ranura.espesor_ctor_estatica()
print(diseno_estatica)


