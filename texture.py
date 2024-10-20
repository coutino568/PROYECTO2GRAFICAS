from mathcou import *
from numpy import arccos, arctan2,pi
import struct

class Texture(object):
    def __init__(self, filename):
        
        if filename != None:    
            with open(filename, "rb") as image:
                image.seek(10)
                headerSize = struct.unpack('=l',image.read(4))[0]
                
                image.seek(18)
                self.width = struct.unpack('=l',image.read(4))[0]
                self.height = struct.unpack('=l',image.read(4))[0]
                
                image.seek(headerSize)
                self.pixels = []
                
                ##lectura de filas de pixeles dentro de la textura
                for y in range (self.height):
                    pixelsrow = []
                    for x in range(self.width):
                        b = ord(image.read(1)) /255
                        g= ord(image.read(1)) /255
                        r= ord(image.read(1)) /255
                        pixelsrow.append([r,g,b])
                        #print("PIXEL ROW APPENDED: (" + str(r)+" ; "+str(g)+" ; "+str(b)+" )")
                    self.pixels.append(pixelsrow)
                    
        
                
    def getColor(self, u, v):
        
        ##tendra un comportamineto de tilling por defecto
        u = u%1
        v= v%1
        # print(" U " + str(u) + "V " + str(v))
    
        x =int(v*(self.width-1))
        y = int(u*(self.height-1))
                      
        return self.pixels[y][x]
      
            
            
    #este metodo deberia retornar los colores basados la direccion desde el centro de la esfera
    def getColorSphere(self, direction):
        
        direction = normalize(direction)

        
        v = arctan2(direction[2],direction[0]) / (2*np.pi)
        u = arccos(-direction[1]) / np.pi
        
        
        x =int(v*(self.width-1))
        y = int(u*(self.height-1))
                       
        return self.pixels[y][x]
        