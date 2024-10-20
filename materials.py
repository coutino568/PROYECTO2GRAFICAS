
from texture import Texture
DIFUSE =0
REFLECTIVE = 1
TRANSPARENT = 2

class Material (object):
    def __init__(self, difuse = (1,1,1), specular = 1, ks= 1 ,type = DIFUSE , texture= None):
        self.difuse = difuse
        self.specular= specular
        self.ks= ks
        self.type= type
        if texture != None:
            self.texture = Texture(texture)
        else:
            self.texture = None
    
    
    
    