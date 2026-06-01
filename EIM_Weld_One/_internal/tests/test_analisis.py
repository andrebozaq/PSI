from src.main import analisis


"""prueba = analisis.AnalisisSoldaduraFilete("Internacional", "Intermedia",{"Fmax": 2000, "Fmin": 1500, "b": 100}, {"Sy": 279, "Sut": 415},
                                 {"Sy": 279, "Sut": 415}, {"Sy": 280, "Sut": 450},
                                 "uno", {"pierna": 5, "largo": 80}, 8)


if not prueba.analisis_fatiga_cflex():
    prueba.analisis_estatico_cflex()
prueba.verificar_tamano_minimo_pierna_analisis()"""

"""prueba = analisis.AnalisisSoldaduraFilete("Internacional", "Unión T", {"Fmax": 2000, "Fmin": 1500, "b": 150}, {"Sy": 250, "Sut": 400},
                                 {"Sy": 250, "Sut": 400}, {"Sy": 345, "Sut": 415},
                                 "uno", {"pierna": 8, "largo": 80, "ancho": 0, "radio": 0}, 10)
falla, resultados = prueba.analisis_fatiga_ctor()

print(resultados)"""

"""if prueba.analisis_estatico_cp()[0]:
    print("La junta falló")
else:
    print("La junta está buena")
"""


"""prueba_mott = analisis.AnalisisSoldaduraFilete("Inglés", "Intermedia", {"Fmax": 3500, "b": 10.86},
                                        {"Sy": 36000, "Sut": 58000}, {"Sy": 36000, "Sut": 58000}, {"Sy": 50000, "Sut": 60000},
                                        "siete", {"pierna": 0.188, "largo": 4, "ancho": 6}, 0.5)
prueba_mott.analisis_estatico_ctor()"""



"""prueba_ejemplo_resuelto = AnalisisSoldaduraFilete("Internacional", "Unión T",
                                                {"Fmax": 25000, "Fmin": 5000, "b": 100},
                                                  {"Sy": 250, "Sut": 400}, {"Sy": 259, "Sut": 469},
                                                  {"Sy": 345, "Sut": 415},
                                                  "nueve", {"pierna": 6, "largo": 76, "ancho": 203},
                                                  7.1)

prueba_ejemplo_resuelto.analisis_estatico_ctor()
prueba_ejemplo_resuelto.analisis_fatiga_ctor()
print(verificar_tamano_minimo_pierna("Internacional", 7.1, 6))"""

prueba_analisis_ranura = analisis.AnalisisSoldaduraRanura("Internacional", "Unión T", {"Tmax": 276.28},
                                                         {"Sy": 250, "Sut": 415}, {"Sy": 250, "Sut": 415},
                                                         {"Sy": 345, "Sut": 415}, "dos",
                                                         {"espesor": 8, "largo": 80, "radio exterior": 0})
resultados = prueba_analisis_ranura.analisis_estatico_ctor()[1]
print(resultados)

"""ejemplo_fatiga_shigley = AnalisisSoldaduraFilete("Inglés", "Unión T", {"Fmax": 500, "Fmin": 0, "b": 6},
                                                 {"Sy": 32000, "Sut": 58000}, {"Sy": 32000, "Sut": 58000},
                                                 {"Sy": 50000, "Sut": 62000}, "cinco", {"pierna": 3/8, "largo": 2, "ancho": 3/8},
                                                 3/8)
ejemplo_fatiga_shigley.analisis_estatico_cflex()
print(verificar_tamano_minimo_pierna("Inglés", 0.5, 3/8))"""