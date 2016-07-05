import pygame
class AttackManager(object):
    def update(self,box,events):
        pass
    def render(self,sub):
        pass
    def end(self,box,damage):
        box.damage=damage
        box.done=True
class SlashAttack(AttackManager):
    sx=0
    dsx=8
    def update(self,box,events):
        self.sx+=self.dsx
        if self.sx>494:
            self.sx=494
            self.dsx=-self.dsx
        elif self.sx<0:
            self.sx=0
            self.dsx=-self.dsx
        for e in events:
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
                self.end(box,5-abs(self.sx-248)//8)
    def render(self,sub):
        pygame.draw.rect(sub,(255,255,0),pygame.Rect(216,0,64,112))
        pygame.draw.rect(sub,(255,0,0),pygame.Rect(232,0,32,112))
        pygame.draw.rect(sub,(255,255,255),pygame.Rect(self.sx,0,2,112))