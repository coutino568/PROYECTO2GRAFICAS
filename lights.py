
from mathcou import *
class Light(object):
    def __init__(self,intensity=1, color= (1,1,1),LightType="None"):
        self.intensity= intensity
        self.color=color
        self.LightType=LightType
        
    def getLightColor(self):
        return [self.color[0]* self.intensity,
                self.color[1]* self.intensity,
                self.color[2]* self.intensity]

    def getDifuseColor(self,intercept):
        return self.getLightColor()
    
    
    def getSpecularColor(self,intercept,viewPos):
        return self.getLightColor()
    
    

class AmbientLight(Light):
    def __init__(self,intensity=1, color= (1,1,1)):
        super().__init__(intensity,color,"Ambient")
        
        
class DirectionalLight(Light):      
    def __init__(self,direction = (0,-1,0),intensity=1, color= (1,1,1)):
        self.direction=normalize(direction)
        super().__init__(intensity,color,"Directional")
        
    def getDifuseColor(self,intercept):
        # lightColor= super().getLightColor(intercept)
        direction = vectorAndScalarMultiplication (self.direction,-1)
        
        intensity = ( dotProduct(intercept.normal, direction)* self.intensity)
        intensity = max (0, min(1 , intensity))
        
        difusecolor = vectorAndScalarMultiplication(self.color,intensity)
        
        return difusecolor
        
    def getSpecularColor(self,intercept,viewPos):
         
        direction = vectorAndScalarMultiplication(self.direction, -1)
        reflect = reflectVector(intercept.normal, direction)
        # print(intercept.point)
        viewDir = subtract(viewPos, intercept.point)
        # print(viewDir)
        viewDir = normalize(viewDir)
         
        specIntensity = max(0, dotProduct(viewDir,reflect)) ** intercept.obj.material.specular
        specIntensity  *= self.intensity
        
        specColor = vectorAndScalarMultiplication(self.color, specIntensity)
        return specColor
   
    
class PointLight(Light):      
    def __init__(self,point = (0,0,0),intensity=1, color= (1,1,1), decayEffect=1):
        
        self.point= point
        self.decayEffect= decayEffect
        super().__init__(intensity,color,"Point")
    
    def moveLight(self, movement):
        self.point= add(self.point,movement)
    
    def getDifuseColor(self,intercept):
        # lightColor= super().getLightColor(intercept)
        direction = subtract( intercept.point, self.point)
        direction = vectorAndScalarMultiplication (direction,-1)
        distance = getmagnitude(direction)
        direction = normalize(direction)
        
        
        intensity = ( dotProduct(intercept.normal, direction)* self.intensity)
        intensity = max (0, min(1 , intensity))
        
        intensity = intensity / ((distance*distance) * self.decayEffect)
        
        
        difusecolor = vectorAndScalarMultiplication(self.color,intensity)
        
        return difusecolor
        
    def getSpecularColor(self,intercept,viewPos):
        direction = subtract( intercept.point, self.point)
        direction = vectorAndScalarMultiplication(direction, -1)
        distance =getmagnitude(direction)
        direction = normalize(direction) 
        
        
        reflect = reflectVector(intercept.normal, direction)
        viewDir = subtract(viewPos, intercept.point)
        viewDir = normalize(viewDir)
         
        specIntensity = max(0, dotProduct(viewDir,reflect)) ** intercept.obj.material.specular
        decayEffect= 0.5
        specIntensity = specIntensity / ((distance*distance) * self.decayEffect)
        specColor = vectorAndScalarMultiplication(self.color, specIntensity)
        return specColor