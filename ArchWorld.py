import Battle
import Overworld
import pygame
import Field
class ArchWorld(object):
    battling=False
    def __init__(self):
        self.worlds=[Overworld.Home(self),Field.OverField(self)]
        self.home=self.worlds[0]
        self.p=self.home.p
        self.wstack=[self.home]
        self.infos=[]
    def update(self,events):
        self.wstack[-1].update(events)
        self.infos=self.wstack[-1].infos
    def render(self,screen):
        self.wstack[-1].render(screen)
    def encounter(self,enemy):
        self.wstack.append(Battle.Battle(enemy,self.p,self))
        self.battling=True
    def use_item(self,n):
        self.wstack[-1].use_item(n)
    def endbattle(self):
        del self.wstack[-1]
        self.battling=False
        pygame.mixer_music.stop()
    def battle_action(self,n):
        self.wstack[-1].battle_action(n)