import Text, Img
import pygame
from random import choice
pback=Img.img2("BattleBack")
bactions=Img.img2("BattleBar")
class Battle(object):
    turn=1
    end=False
    resultbox=None
    restype=None
    def __init__(self,foe,player,arch):
        pygame.mixer_music.stop()
        Img.musplay("Battle 1")
        self.f=foe
        self.p=player
        self.infos=[]
        self.add_info(foe.name.upper()+" appears!")
        self.a=arch
    def update(self,events):
        if not self.infos:
            if self.end:
                self.a.endbattle()
            if self.turn==0:
                self.turn=1
                self.add_info(choice(self.f.moves).use(self.f,self.p,self))
            if self.resultbox:
                override=False
                if self.restype=="Mercy":
                    if self.resultbox.n:
                        if self.f.allow_leave(self):
                            self.add_info("You ran away...")
                            self.end="flee"
                        else:
                            self.add_info("Can't escape!")
                    else:
                        if self.f.hap:
                            self.add_info("YOU WON!")
                            self.end="won"
                        else:
                            self.add_info(self.f.name.capitalize()+" wants to keep fighting!")
                elif self.restype=="Act":
                    if self.resultbox.n:
                        self.f.act(self.resultbox.n)
                    else:
                        self.add_info(self.f.desc)
                elif self.restype=="Fight":
                    self.f.damage(self.resultbox.damage)
                    if self.f.hp==0:
                        self.add_info(self.f.name.capitalize()+" died!")
                        self.end="won"
                        override=True

                self.resultbox=None
                self.restype=None
                if override:
                    self.turn=1
                else:
                    self.turn=0
    def render(self,screen):
        screen.blit(pback,(128,256))
        fimg=self.f.get_img(self)
        screen.blit(fimg,(256,128))
        pygame.draw.rect(screen,(255,0,0),pygame.Rect(256,128+fimg.get_height(),64,8))
        if self.f.hp:
            pygame.draw.rect(screen,(0,255,0),pygame.Rect(256,128+fimg.get_height(),self.f.hp*64//self.f.mhp,8))
        screen.blit(bactions,(0,480))
    def add_info(self,info):
        self.infos.append(Text.Ibox(info))
    def add_obox(self,box):
        self.infos.append(box)
    def add_resbox(self,box):
        self.resultbox=box
        self.add_obox(box)
    def use_item(self,n):
        i=self.p.items[n]
        self.turn=0
        if i.utype=="mfood":
            if self.f.likes_food(i.name):
                self.f.hap+=1
                self.add_info(self.f.name.capitalize()+" likes your "+i.name)
                self.p.sub_item(i)
        elif i.utype=="weapon":
            self.add_info("You %s the %s with your %s" % (i.action,self.f.name,i.name))
            self.restype="Fight"
            self.add_resbox(Text.AttackBox(i))
            self.turn=1
    def battle_action(self,n):
        if n==0:
            self.resultbox=Text.MultiBox(["Check"]+self.f.actextras)
            self.restype="Act"
            self.add_obox(self.resultbox)
        elif n==1:
            pass
        elif n==2:
            self.resultbox=Text.MultiBox(["Spare","Flee"])
            self.restype="Mercy"
            self.add_obox(self.resultbox)

