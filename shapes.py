
from mathcou import *
from numpy import arccos, arctan2,pi,cos,sin
import numpy as np

class Intercept(object):
    def __init__(self,distance, point,normal,obj , texcoords):
        self.distance= distance
        self.point= point
        self.normal = normal
        self.obj= obj
        self.texcoords = texcoords








class Shape(object):
    
    def __init__( self, position, material ):
        self.position = position
        self.material= material
        
        
        
    def ray_intersect(self, origin, dir):
        return False
    
    def moveObject(self, movement):
        self.position= add(self.position,movement)
        
    
class Sphere (Shape):
    
    def __init__(self, position,  material ,radius):
        self.radius =radius
        # self.material= material
        super().__init__( position,material)
        
    def ray_intersect(self, origin, direction):
        direction = normalize(direction)
        Lr = subtract(self.position, origin)
        # print(L)
        # print(direction)
        magnitudL = getmagnitude(Lr)
        tca= dotProduct(Lr, direction)
        d = math.sqrt((magnitudL * magnitudL ) - (tca * tca ) )
        
        if d> self.radius:
            
            return None
        
        thc = math.sqrt((self.radius* self.radius) - (d*d) )
        t0 = tca-thc
        t1 = tca+ thc
        
        if (t0<0):
            t0=t1
        if (t0<0):     
            return None
        # print(t0)
        # print(direction)
        res1= vectorAndScalarMultiplication(direction,t0)
        point = add(origin,  res1 )
        normal = normalize(subtract(point, self.position))
        
        
        
        
        
        texcoords= None
        
        ##si tiene material con textura entonces se devuelve
        if self.material.texture != None:
            
            directionFromInside = normalize(subtract(self.position, point))
            # print(directionFromInside)
            v = arctan2(directionFromInside[2],directionFromInside[0]) / (2*np.pi)
            u = arccos(-directionFromInside[1]) / np.pi
        
        
            # x =int(v*(self.material.texture.width-1))
            # y = int(u*(self.material.texture.height-1))
            
            texcoords= [u,v]
            # print(texcoords)
        
        
        
        
        
        return Intercept(distance=t0,
                         point=point,
                         normal=normal,
                         obj = self,
                         texcoords=texcoords)
        
class Plane (Shape):
    
    def __init__(self, position, normal , material):
        
        self.normal = normalize(normal)
        self.material= material
        super().__init__(position,material)
        
    def ray_intersect(self, origin, direction):
        
       
        
        denom= dotProduct( direction, self.normal)
        
       
        
        if abs(denom) <= 0.0001 :
            return None
        
        num = dotProduct(subtract(self.position, origin), self.normal)
        
        t = num / denom
       
        if t< 0 :
            return None
        
        point = add(origin , vectorAndScalarMultiplication(direction, t) )
        
        if self.material.texture!=None:
            
            
            distancenormalized= getmagnitude(subtract(self.position, point))
            delta=subtract(point, self.position)
            # delta = vectorAndScalarMultiplication(direction, t)
            
            angle= dotProduct(delta,vectorAndScalarMultiplication(direction, t))
            x= cos(angle)*distancenormalized
            y= sin(angle)*distancenormalized
            texcoords = [y/5,x/5]
            
        else:
            texcoords = [0.5,0.5]
            
        
        
        # print ( point)
        return Intercept(distance=t,
                         point=point,
                         normal=self.normal,
                         obj = self,
                         texcoords=texcoords)
    
    
class Disk(Plane):
    def __init__(self, position, material , normal,radius):
        self.radius = radius
        super().__init__( position,  normal , material)
        
    def ray_intersect(self, origin, direction):
        
        planeIntersect = super().ray_intersect(origin,direction)
        
        if planeIntersect == None:
            return None
        
        contactDistance = subtract(planeIntersect.point,self.position)
        contactDistance = getmagnitude(contactDistance)
        
        if contactDistance > self.radius:
            return None
        
        if self.material.texture!= None:
            
            angle= dotProduct(self.position, planeIntersect.point)
            magnitude= getmagnitude(subtract(self.position, planeIntersect.point))
            x= cos(angle)* magnitude
            y= sin(angle)*magnitude
            
            
            texcoords = [x*self.material.texture.width, y*self.material.texture.height]
        else:
            texcoords = None        
        
        return Intercept(distance=planeIntersect.distance,
                         point=planeIntersect.point,
                         texcoords = texcoords,
                         normal=self.normal,
                         obj = self
                         )
        
        
        
class AABB(Shape):
    def __init__(self ,position,size,material):
        super().__init__(position,material)
        self.planes=[]
        
        self.legthnx = size[0]
        self.lengthy = size[1]
        self.lengthz = size[2]
        
        texcoords = None
        ##asigna las caras con sus nurmales+el desplzamiento de cada cara para ue sea simetrico 
        leftplane= Plane(add(self.position, [-size[0]/2,0,0]),[-1,0,0], material )
        rightplane=Plane(add(self.position, [size[0]/2,0,0]),[1,0,0], material )
        
        bottomplane=Plane(add(self.position, [0,-size[0]/2,0]),[0,-1,0], material )
        topplane=Plane(add(self.position, [0,size[0]/2,0]),[1,1,0], material )
        
        backplane=Plane(add(self.position, [0,0,-size[0]/2]),[0,0,-1], material )
        frontplane= Plane(add(self.position, [0,0,size[0]/2]),[0,0,1], material )
        
        
        self.planes.append(leftplane)
        self.planes.append(rightplane)
        self.planes.append(bottomplane)
        self.planes.append(topplane)
        self.planes.append(backplane)
        self.planes.append(frontplane)
        
        self.boundsMin  = [0,0,0]
        self.boundsMax = [0,0,0]
        
        bias= 0.001
        
        for i in range(3):
            self.boundsMin[i]=self.position[i] - (bias + size[i]/2)
            self.boundsMax[i]=self.position[i] + (bias + size[i]/2)
        
        
        
        def ray_intersect ( self , origin, direction):
            intersect = None
            t = float['inf']
            
            for plane in self.planes:
                planeIntersect = plane.ray_intersect(origin, direction)
                if planeIntersect != None:
                    planePoint= planeIntersect.point
                    
                    #osea que el point este comprendido dentro de los limites del bloque
                    if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                        if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                            if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                                if planeIntersect.distance < t :
                                    t = planeIntersect.distance
                                    intersect = planeIntersect
                
                if intersect == None:
                    return None
                
                return Intercept(distance=t,
                         point=intersect.point,
                         texcoords = texcoords,
                         normal=intersect.normal,
                         obj = self
                         )        
    
    
    
    
    
           
        
    
class Triangle(Shape):
    
    def __init__(self, vertices , position, material):
        self.vertices =vertices
        
        # self.material= material
        super().__init__( position,material)
        
    def ray_intersect(self, origin, direction):
        
        v0=self.vertices[0]
        v1=self.vertices[1]
        v2=self.vertices[2]
        
        
        
        
        return None