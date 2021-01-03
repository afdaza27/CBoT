import random

class Insultos:

    def __init__(self):
        self.insultos = []

    def cargar_insultos(self):
        ruta_archivo = "./data/insultos.txt"
        archivo_insultos = open(ruta_archivo, "r", encoding="utf-8")
        insultos = []
        for insulto in archivo_insultos:
            insulto = insulto.strip()
            insultos.append(insulto)
        archivo_insultos.close()
        self.insultos = insultos
        return self.insultos

    def agregar_insulto(self, insulto_nuebo):
        ruta_archivo = "./data/insultos.txt"
        archivo_insultos = open(ruta_archivo, "r", encoding="utf-8")
        lineas = archivo_insultos.readlines()
        archivo_insultos.close()
        lineas.append("\n" + insulto_nuebo)
        self.insultos.append(insulto_nuebo)
        with open('./data/insultos.txt', 'w', encoding="utf-8") as janarchibo:
            janarchibo.writelines(lineas)
            janarchibo.close()

    def insultar(self):
        return self.insultos[random.randint(0, len(self.insultos)-1)]