
import pygame
import random
from gl import Raytracer
from shapes import Sphere , Plane
from lights import *
from materials import *

height = 600
width = 800

pixels= []


pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True


# pixels= [[self.bgColor for x in range(self.width)] for y in range(self.height)]

myRaytracer =  Raytracer(screen)
myRaytracer.rtClearColor(0.09,0.2,0.5)

brick = Material(difuse = (0.5,0.1,0),specular=0.2)
snow= Material(difuse=(0.8,0.8,0.8),specular=0.99)
black= Material(difuse=(0.1,0.1,0.1),specular=0.5)
carrot = Material(difuse=(0.9,0.5,0.2), specular=0.5)

materials= [brick,snow,black,carrot]

#Esferas de cuerpo

myRaytracer.objects.append(Plane (position=(0,0,0) , normal=(0,1,0), material=snow))

# myRaytracer.objects.append( Sphere(position=(0,-2,-7), radius =1.5, material = snow))
# myRaytracer.objects.append( Sphere(position=(0,0.5,-7), radius =1, material = snow))
# myRaytracer.objects.append( Sphere(position=(0,2,-7), radius =0.7, material = snow))


# #botones
# myRaytracer.objects.append( Sphere(position=(0,-1,-4), radius =0.15, material = black))
# myRaytracer.objects.append( Sphere(position=(0,0,-4), radius =0.15, material = black))
# myRaytracer.objects.append( Sphere(position=(0,0.5,-4), radius =0.15, material = black))


# #esferas de la cara
# myRaytracer.objects.append( Sphere(position=(0,1.1,-4), radius =0.1, material = carrot))
# myRaytracer.objects.append( Sphere(position=(-0.1,1.3,-4), radius =0.05, material = black))
# myRaytracer.objects.append( Sphere(position=(0.1,1.3,-4), radius =0.05, material = black))



# myRaytracer.objects.append( Sphere(position=(0.1,0.99,-4.1), radius =0.03, material = black))
# myRaytracer.objects.append( Sphere(position=(0.19,1.1,-4.1), radius =0.03, material = black))

# myRaytracer.objects.append( Sphere(position=(-0.1,0.99,-4.1), radius =0.03, material = black))
# myRaytracer.objects.append( Sphere(position=(-0.19,1.1,-4.1), radius =0.03, material = black))




numofspheres = 30

# for x in range (numofspheres):
#     minx=-2
#     miny=-2
#     maxx=2
#     maxy=2
#     maxz=-2
#     minz=-7
    
#     x= random.randint(minx,maxx)
#     y= random.randint(miny,maxy)
#     z= random.randint(minz,maxz)
    
#     myRaytracer.objects.append( Sphere(position=(x,y,z), radius =random.random(), material = materials[random.randint(0,len(materials)-1)]))


# myRaytracer.objects.append( Sphere(position=(3,0,-5), radius =1.5, material = brick))
# myRaytracer.objects.append( Sphere(position=(-2,0,-5), radius =1.5, material = brick))

# myRaytracer.Lights.append( AmbientLight(intensity = 0.1))
myRaytracer.Lights.append (DirectionalLight(direction=(-0.9,-1,-2),intensity=0.4))


# myRaytracer.Lights.append (PointLight(point = (0,0,-5),intensity=1, decayEffect=0.9) )
# myRaytracer.Lights.append (PointLight(point = (0,0,-5),intensity=1, decayEffect=0.9) )



while running:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

   
    # screen.fill("black")
    # pygame.draw.circle(screen, "white", [width/2, height/2] , 40)

    myRaytracer.rtClear()
    
    # myRaytracer.rtPoint(random.randint(0,width),random.randint(0,height),(1,1,0))
    
    time= pygame.time.get_ticks()
    # print(time)
    factor=6
    # for light in myRaytracer.Lights:
    #     if light.LightType =="Directional":  
    #         movement = [math.sin(time)/factor,0,0]
    #         light.moveObject(movement)
    myRaytracer.rtRender()
    pygame.display.flip()

    # clock.tick(60) 

pygame.quit()