from werkzeug.security import chreck_password_hash
from flask_login import UserMixin
class User (UserMixin):
    def __init__(self,id,nombre,correo,clave,perfil):
        self.id      =id
        self.nombre  =nombre  
        self.correo  =correo
        self.clave   =clave    
        self.perfil  =perfil

@classmethod
def validarClave(self,claveCifrada,clave):
    return chreck_password_hash(claveCifrada,clave)
    