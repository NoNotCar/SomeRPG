import Battle
import Overworld
import pygame
import Field
from Internals import buildings
class ArchWorld(object):
    battling=False
    internal=False
    def __init__(self):
        self.worlds=[Overworld.Home(self),Field.OverField(self)]
        self.home=self.worlds[0]
        self.p=self.home.p
        self.wstack=[self.home]
        self.infos=[]
        for n,b in enumerate(buildings):
            buildings[n]=b(self)
            buildings[n].p=self.p
    def update(self,events):
        self.wstack[-1].update(events)
        self.infos=self.wstack[-1].infos
        if not self.battling and self.internal and self.wstack[-1].exiting:
            self.wstack[-1].exiting=False
            del self.wstack[-1]
            self.p.place(self.px,self.py)
            self.internal=False
    def render(self,screen):
        self.wstack[-1].render(screen)
    def encounter(self,enemy,bad):
        self.wstack.append(Battle.Battle(enemy,self.p,self,self.wstack[-1].backcolour,bad))
        self.battling=True
    def use_item(self,n):
        self.wstack[-1].use_item(n)
    def endbattle(self):
        del self.wstack[-1]
        self.battling=False
        pygame.mixer_music.stop()
    def battle_action(self,n):
        self.wstack[-1].battle_action(n)
    def add_info(self,info):
        self.wstack[-1].add_info(info)
    def add_internal(self,internal):
        for b in buildings:
            if b.name==internal:
                self.wstack.append(b)
                self.px=self.p.x
                self.py=self.p.y
                self.p.place(b.ex,b.size[1]-1)
                b.spawn(self.p)
                self.internal=True
                break
    def turn(self):
        if self.battling:
            self.wstack[-1].turn=0