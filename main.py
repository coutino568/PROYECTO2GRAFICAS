
import pygame
import random
from gl import Raytracer
from shapes import Sphere , Plane, Disk , AABB
from lights import *
from materials import *

height = 600
width = 800

pixels= []


pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

envMapFile = "env4.bmp"
metalTexture="metal.bmp"
waveTexture="env4.bmp"
snowTextureFile="snow.bmp"
clayTextureFile = "clay.bmp"
brickTextureFile = "bricks.bmp"
# pixels= [[self.bgColor for x in range(self.width)] for y in range(self.height)]

myRaytracer =  Raytracer(screen,envMapFile)
myRaytracer.rtClearColor(0.09,0.2,0.5)

DIFUSE =0
REFLECTIVE = 1
TRANSPARENT = 2

brick = Material(difuse = (0.5,0.1,0),specular=0.2,type=DIFUSE ,texture= brickTextureFile)
snow= Material(difuse=(1,1,1),specular=0.99,type=DIFUSE , texture=snowTextureFile)
water= Material(difuse=(1,1,1),specular=0.99,type=DIFUSE , texture=waveTexture)
black= Material(difuse=(0.1,0.1,0.1),specular=0.5,type=DIFUSE)
carrot = Material(difuse=(0.9,0.5,0.2), specular=0.5,type=DIFUSE)
mirror = Material(difuse=(0.9,0.5,0.2), specular=0.5,type=REFLECTIVE)
metal = Material(difuse=(0.9,0.5,0.2), specular=0.5,type=DIFUSE, texture=metalTexture)
black = Material(difuse=(0,0,0,),specular=0.5,type=DIFUSE)
sun = Material(difuse= (224/255, 166/255, 58/255), specular=0.5 ,type=DIFUSE)

clay= Material(difuse=(1,1,1),specular=0.99,type=DIFUSE , texture=clayTextureFile)




materials= [brick,snow,black,carrot, mirror , sun, metal]


myRaytracer.materials = materials


# myRaytracer.objects.append( Sphere(position=(18 ,5,-25), radius =3, material = metal))
# myRaytracer.objects.append( Sphere(position=(-15,5,-25), radius =3, material = sun))
# myRaytracer.objects.append( Sphere(position=(-8,4,-25), radius =2, material = sun))
# myRaytracer.objects.append( Sphere(position=(5,-10,-25), radius =5, material = clay))

# # # myRaytracer.objects.append( Plane(position=(-5,0,-50),normal=(1,0,0), material= snow))

# myRaytracer.objects.append( Plane(position=(0,-10,-0),normal=(0,1,0), material= clay))

# myRaytracer.objects.append( Disk(position=(4.5,-10,-20), normal = (0,0,-1) , material= black  ,radius=2))


# myRaytracer.objects.append( Disk(position=(13,-9,-25), normal = (-1,0,0) , material= mirror  ,radius=10))


myRaytracer.Lights.append (DirectionalLight(direction=(-0.2,-1,-0.5),intensity=0.4))

myRaytracer.Lights.append (DirectionalLight(direction=(-0.2,-1,2),intensity=1))



numofspheres = 10

for x in range (numofspheres):
    minx=-2
    miny=-2
    maxx=2
    maxy=2
    maxz=-2
    minz=-7
    
    x= random.randint(minx,maxx)
    y= random.randint(miny,maxy)
    z= random.randint(minz,maxz)
    
    myRaytracer.objects.append( Sphere(position=(x,y,z), radius =random.random(), material = materials[random.randint(0,len(materials)-1)]))



myRaytracer.rtClear()
while running:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

   
   
    time= pygame.time.get_ticks()
    
    factor=6
   
    myRaytracer.rtRender()
    pygame.display.flip()
    
    # clock.tick(60) 

pygame.quit()