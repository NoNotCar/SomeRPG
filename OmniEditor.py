'''
Created on 22 Sep 2014

@author: NoNotCar
'''
import pygame
pygame.init()
screen=pygame.display.set_mode((480,512))
from Img import img2
import Img
from random import randint,choice
import pygame
import sys
import Tiles
import Plants
import Direction as D
from Overworld import EDITOROBJS
EDITORTILES = Tiles.tiles[1:]
EDITORITEMS = EDITORTILES + EDITOROBJS
class Scroller(object):
    solid=False
    hidden=False
    img=img2("Mouse")
    def __init__(self):
        self.x=0
        self.y=0
        self.ex=0
        self.xoff=0
        self.yoff=0
        self.speed=2
        self.excool=0
        self.moving=False
    def get_img(self):
        return self.img
    def mupdate(self):
        if self.xoff>0:
            self.xoff-=self.speed
        elif self.xoff<0:
            self.xoff+=self.speed
        if self.yoff>0:
            self.yoff-=self.speed
        elif self.yoff<0:
            self.yoff+=self.speed
        if abs(self.xoff)<self.speed and abs(self.yoff)<self.speed and self.moving:
            self.xoff=0
            self.yoff=0
            self.moving=False
    def fill(self,world,t):
        poss=[(self.x,self.y)]
        while poss:
            p=poss.pop(0)
            if world.eworld[p[0]][p[1]][0]!=t:
                world.eworld[p[0]][p[1]][0]=t
                for dx,dy in [[0,1],[1,0],[0,-1],[-1,0]]:
                    if world.inworld(p[0]+dx,p[1]+dy):
                        poss.append((p[0]+dx,p[1]+dy))
    def update(self,world):
        if not self.moving:
            dx=0
            dy=0
            keys=pygame.key.get_pressed()
            if keys[pygame.K_s] and pygame.key.get_mods()&pygame.KMOD_LCTRL:
                world.save()
                sys.exit()
            if not self.moving and keys[pygame.K_SPACE]:
                if pygame.key.get_mods()&pygame.KMOD_LCTRL:
                    if self.ex<len(EDITORTILES):
                        self.fill(world,self.ex+1)
                else:
                    if self.ex<len(EDITORTILES):
                        world.eworld[self.x][self.y][0]=self.ex+1
                    else:
                        world.eworld[self.x][self.y][1]=self.ex+1-len(EDITORTILES)
            elif not self.moving and keys[pygame.K_LSHIFT]:
                if pygame.key.get_mods()&pygame.KMOD_LCTRL:
                    self.fill(world,0)
                else:
                    world.edestroy(self.x,self.y)
            for n,k in enumerate(D.kconv):
                if keys[k]:
                    d=D.get_dir(n)
                    dx+=d[0]
                    dy+=d[1]
            if self.excool:
                self.excool-=1
            else:
                if keys[pygame.K_LEFT]:
                    self.ex=(self.ex-1)%len(EDITORITEMS)
                    self.excool=10
                if keys[pygame.K_RIGHT]:
                    self.ex=(self.ex+1)%len(EDITORITEMS)
                    self.excool=10
            if dx or dy:
                if world.inworld(self.x+dx,self.y+dy):
                    self.x+=dx
                    self.y+=dy
                    self.xoff=-dx*32
                    self.yoff=-dy*32
                    self.moving=True
class World(object):
    done=False
    def __init__(self,lvlsize):
        self.size=lvlsize
        s=self.size
        self.eworld=[[None]*s[1] for n in range(s[0])]
        for x,r in enumerate(self.eworld):
            for y,o in enumerate(r):
                self.eworld[x][y]=[0,0]
        self.player=Scroller()
        self.complete=False
        self.pdone=False
    def update(self,events):
        """Update Everything"""
        self.player.update(self)
        if self.player.moving:
            self.player.mupdate()
    def scrollrender(self,screen):
        """Render Everything in scrolling mode"""
        ply=self.player
        asx=ply.x*32+int(round(ply.xoff))-224
        asx=0 if asx<0 else asx if asx<self.size[0]*32-480 else self.size[0]*32-480
        asy=ply.y*32+int(round(ply.yoff))-224
        asy=0 if asy<0 else asy if asy<self.size[1]*32-480 else self.size[1]*32-480
        sx=7 if ply.x<7 else ply.x if ply.x<self.size[0]-8 else self.size[0]-8
        sy=7 if ply.y<7 else ply.y if ply.y<self.size[1]-8 else self.size[1]-8
        for x,row in enumerate(self.eworld):
            for y,obj in enumerate(row):
                if abs(x-sx)<9 and abs(y-sy)<9:
                    screen.blit(([Tiles.tiles[0]] + EDITORTILES)[obj[0]].img, (x * 32 - asx, y * 32 - asy))
                    if obj[1]:
                        screen.blit(EDITOROBJS[obj[1] - 1].img, (x * 32 - asx, y * 32 - asy - EDITOROBJS[obj[1] - 1].o3d * 2))
        screen.blit(self.player.get_img(),(self.player.x*32-asx+ply.xoff,self.player.y*32-asy+ply.yoff))
        pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,480,480,32))
        for n,x in enumerate(EDITORTILES):
            screen.blit(x.img,(n*32,480))
        for on,x in enumerate(EDITOROBJS):
            screen.blit(x.img,((n+on+1)*32,480-x.o3d*2))
        screen.blit(self.player.img,(self.player.ex*32,480))
    def inworld(self,x,y):
        """Is the coordinate in the world?"""
        return 0<=x<self.size[0] and 0<=y<self.size[1]
    def edestroy(self,x,y):
        self.eworld[x][y]=[0,0]
    def save(self):
        savfile = open(Img.np("areas//save.sav"), "w")
        savfile.write("\n")
        for row in self.eworld:
            savfile.write(" ".join([self.symbconvert(o) for o in row]) + "\n")
        savfile.close
    def symbconvert(self,n):
        if n[1]:
            return str(n[0])+":"+EDITOROBJS[n[1]-1].symb
        else:
            return str(n[0])
    def symbreconvert(self,s):
        for n,e in enumerate(EDITORTILES):
            if n>=len(Tiles.tiles)-1 and e.symb==s:
                return n+1
w=World((30,100))
clock=pygame.time.Clock()
while True:
    es=pygame.event.get()
    for e in es:
        if e.type==pygame.QUIT:
            sys.exit()
    screen.fill((0,200,0))
    w.update(es)
    w.scrollrender(screen)
    pygame.display.flip()
    clock.tick(60)