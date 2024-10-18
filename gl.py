
from mathcou import *
from math import tan 
from lights import *


class Raytracer(object):
    def __init__(self, screen):
        self.screen = screen
        _,_, self.width,self.height = screen.get_rect()

        
        self.rtClearColor(0,0,0)
        self.rtColor(1,1,1)
        self.rtClear()
        self.objects = []
        self.Lights=[]
        self.rtViewport (0,0,self.width,self.height)
        self.rtProjection()
        self.camPosition = [0,0,0]
        
        
        
    
    
    def rtViewport(self,posX,posY,width,height):
        self.vpX= posX
        self.vpY=posY
        self.vpWidth=width
        self.vpHeigth= height
    
    def rtClearColor(self,r,g,b):
        self.clearColor=(r,g,b)
    
    
    def rtClear(self):
        self.screen.fill((self.clearColor[0]*255,
                         self.clearColor[1]*255,
                         self.clearColor[2]*255))
        
    def rtColor(self,r,g,b):
        self.currentColor = (r,g,b)
        
    def rtPoint(self,x,y, color= None):
        # print(color)
        y= self.height -y
        
        if(0<=x<self.width) and (0<=y<self.height):
            
            if color!= None:
                color = (int(color[0]*255),
                         int(color[1]*255),
                         int(color[2]*255))
                self.screen.set_at((x,y),color)
                
            else :
                self.screen.set_at((x,y),self.currentColor)
                # print("point")
    def rtProjection (self, fov= 60, n= 0.1):
        aspectRatio = self.vpWidth / self.vpHeigth
        self.nearPlane = n 
        self.topEdge = tan( degreesToRad(fov) )/2 * self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio
        
        
        
    def rtCastRay(self, origin, direction, sceneObj=None):
        depth = float ('inf')
        intercept = None
        hit= None
        for object in self.objects:
            if sceneObj != object:
                
                intercept=  object.ray_intersect(origin,direction)
                    
                if intercept != None:
                    if intercept.distance < depth:
                        hit = intercept
                        depth=intercept.distance
                    
        return hit
        
        
       
        
    def rtRender(self):
        
        for x in range(self.vpX, self.vpX+self.vpWidth+1):
            for y in range(self.vpY, self.vpY+self.vpHeigth+1):
                if 0<=x<self.width and 0<=y<self.height:
                    px = ((x + 0.5 - self.vpX) / self.width ) *2  -1
                    py =  ((y + 0.5 - self.vpY) / self.height ) *2  -1
                    
                    px = px*self.rightEdge
                    py = py*self.topEdge
                    
                    direction = normalize((px,py, -self.nearPlane))
                    
                    intercept = self.rtCastRay(self.camPosition,direction)
                    
                        # print("dibujare pues")
                    if intercept != None:
                            
                        surfaceColor = intercept.obj.material.difuse
                        
                        ambientLightColor = [0,0,0]
                        diffuselightColor = [0,0,0]
                        specularLightColor = [0,0,0]
                            
                            
                        for light in self.Lights:
                            if light.LightType == "Ambient":
                                ambientLightColor[0] += light.getLightColor()[0]
                                ambientLightColor[1] += light.getLightColor()[1]
                                ambientLightColor[2] += light.getLightColor()[2]
                            else:
                                shadowIntersect= None
                                
                                if light.LightType =="Directional":
                                    lightDir = vectorAndScalarMultiplication(light.direction, -1)
                                    shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)
                                
                                if shadowIntersect == None:
                                    diffuselightColor[0] = (diffuselightColor[0]+light.getDifuseColor(intercept)[0])
                                    diffuselightColor[1] = (diffuselightColor[1]+light.getDifuseColor(intercept)[1])
                                    diffuselightColor[2] = (diffuselightColor[2]+light.getDifuseColor(intercept)[2])
                                    
                                    specularLightColor[0] += specularLightColor[0] + light.getSpecularColor(intercept, self.camPosition)[0]
                                    specularLightColor[1] += specularLightColor[1] +light.getSpecularColor(intercept, self.camPosition)[1]
                                    specularLightColor[2] += specularLightColor[2] +light.getSpecularColor(intercept, self.camPosition)[2]
                            
                            if light.LightType == "Directional":
                                diffuselightColor[0] += light.getDifuseColor(intercept)[0]
                                diffuselightColor[1] += light.getDifuseColor(intercept)[1]
                                diffuselightColor[2] += light.getDifuseColor(intercept)[2]

                                
                                specularLightColor[0] += light.getSpecularColor(intercept, self.camPosition)[0]
                                specularLightColor[1] += light.getSpecularColor(intercept, self.camPosition)[1]
                                specularLightColor[2] += light.getSpecularColor(intercept, self.camPosition)[2]
                                
                                
                            
                            lightColor = add(add(diffuselightColor,ambientLightColor),specularLightColor)
                            
                            finalColor = [ min(1,surfaceColor[0] * lightColor[0]),
                                          min(1,surfaceColor[1] * lightColor[1]),
                                          min(1,surfaceColor[1] * lightColor[2])
                                          ]
                            # elif light.LightType =="Directional":
                            self.rtPoint(x,y,finalColor)
                    
                
        
        