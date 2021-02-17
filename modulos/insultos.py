import random

class Insultos:

    def __init__(self, db, user):
        self.insultos = []
        self.db = db
        self.user = user


    def cargar_insultos(self):
        insultos = self.db.child("Insultos").get(self.user["idToken"]).each()
        for insulto in insultos:
            self.insultos.append(insulto.val())
        return self.insultos

    def agregar_insulto(self, insulto_nuebo, user):
        self.insultos.append(insulto_nuebo)
        self.db.child("Insultos").set(self.insultos, user["idToken"])

    def insultar(self):
        return self.insultos[random.randint(0, len(self.insultos)-1)]