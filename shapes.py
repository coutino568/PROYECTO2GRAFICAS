
from mathcou import *



class Intercept(object):
    def __init__(self,distance, point,normal,obj):
        self.distance= distance
        self.point= point
        self.normal = normal
        self.obj= obj








class Shape(object):
    
    def __init__( self, position, material ):
        self.position = position
        self.material= material
        
        
        
    def ray_intersect(self, origin, dir):
        return False
    
    def moveObject(self, movement):
        self.position= add(self.position,movement)
        
    
class Sphere (Shape):
    
    def __init__(self, position, radius ,material):
        self.radius =radius
        # self.material= material
        super().__init__( position,material)
        
    def ray_intersect(self, origin, direction):
        
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
        
        return Intercept(distance=t0,
                         point=point,
                         normal=normal,
                         obj = self)
        
class Plane (Shape):
    
    def __init__(self, position, material , normal):
        self.normal = normal
        # self.material= material
        super().__init__( position,material)
        
    def ray_intersect(self, origin, direction):
        
        
        denom= dotProduct( direction, self.normal)
        if abs(denom) <= 0.0001 :
            return None
        num = subtract(self.position, origin)
        num = dotProduct(num, self.normal)
        
        
        t = num / denom
        if t< 0 :
            return None
        
        point = add(origin , vectorAndScalarMultiplication(direction, t) )
        
        return Intercept(distance=t,
                         point=point,
                         normal=self.normal,
                         obj = self)
    
    
    
    
    
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