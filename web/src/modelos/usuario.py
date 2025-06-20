from flask_login import UserMixin

class Usuario(UserMixin):

    def __init__(self, usuario:str, nombre:str, imagen_perfil:str)->None:

        self.id=usuario
        self.nombre=nombre
        self.imagen_perfil=imagen_perfil