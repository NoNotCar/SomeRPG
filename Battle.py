import Text, Img
import pygame
from random import choice
import sys
pback=Img.img2("BattleBack")
bactions=Img.img2("BattleBar")
pactions=Img.img2("BattleBarP")
class Battle(object):
    turn=1
    end=False
    resultbox=None
    restype=None
    def __init__(self,foe,player,arch,backcolour=(0,0,0),bad=False):
        pygame.mixer_music.stop()
        Img.musplay("GlitchBattle" if bad else "Battle 1")
        self.f=foe
        self.p=player
        self.infos=[]
        self.backcolour=backcolour
        self.add_info(foe.name.upper()+" appears!")
        if foe.name=="???":
            self.restype="Name"
            self.add_resbox(Text.EntryBox("Choose your foe's name!"))
        self.a=arch
    def update(self,events):
        if not self.infos:
            if self.end:
                if self.end=="DEAD":
                    sys.exit()
                self.a.endbattle()
            if self.p.hp<=0:
                self.p.hp=0
                self.add_info("You died...")
                self.end="DEAD"
            if self.turn==0:
                self.turn=1
                chuse=choice(self.f.moves).use(self.f,self.p,self)
                if chuse:
                    self.add_info(chuse)
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
                        if self.f.hap>0:
                            self.add_info("YOU WON!")
                            self.end="won"
                        else:
                            self.add_info(self.f.name.capitalize()+" wants to keep fighting!")
                elif self.restype=="Act":
                    if self.resultbox.n:
                        self.f.act(self.resultbox.n,self)
                    else:
                        self.add_info(self.f.desc)
                elif self.restype=="Fight":
                    self.f.damage(self.resultbox.damage)
                    if self.f.hp==0:
                        self.add_info(self.f.name.capitalize()+" died!")
                        if self.f.loot:
                            if self.p.add_item(self.f.loot()):
                                self.add_info("You got a "+self.f.loot.name)
                            else:
                                self.add_info("Your inventory is too full to pick up any loot!")
                        self.end="won"
                        override=True
                elif self.restype=="Name":
                    self.f.__class__.name=self.resultbox.ebox.value.lower()
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
        screen.blit(pactions if self.f.hap>0 else bactions,(0,480))
    def add_info(self,info):
        self.infos.append(Text.Ibox(info))
    def add_talk(self,talk,talker):
        self.infos.append(Text.TalkBox(talk,talker.tfont,talker.owimg))
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
            if self.f.singular:
                self.add_info("You %s %s with your %s" % (i.action,self.f.name,i.name))
            else:
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
            self.resultbox=Text.MultiBox(["Spare","Flee"],[(255,255,0),(64,64,64)] if self.f.hap>0 else None)
            self.restype="Mercy"
            self.add_obox(self.resultbox)

