import pygame
import Img
import Direction as D
ehit=Img.sndget("enemyhit")
phit=Img.sndget("hit")
pimgs=Img.imgstrip("Man")
class AttackManager(object):
    def update(self,box,events):
        pass
    def render(self,sub):
        pass
    def end(self,box,damage):
        box.damage=damage if damage>0 else 0
        box.done=True
        if damage>0:
            ehit.play()
class EnemyAttackManager(AttackManager):
    px=48
    py=48
    pd=2
    pspd=2
    prect=pygame.Rect(5,1,6,14)
    mi=0
    def __init__(self,p,secs):
        self.p=p
        self.bullets=[]
        self.t=secs*60
    def update(self,box,events):
        keys=pygame.key.get_pressed()
        for n,k in enumerate(D.kconv):
            if keys[k]:
                d=D.get_dir(n)
                self.px+=d[0]*self.pspd
                self.py+=d[1]*self.pspd
                self.pd=n
                break
        if 0>self.px:
            self.px=0
        elif 96<self.px:
            self.px=96
        if 0>self.py:
            self.py=0
        elif 96<self.py:
            self.py=96
        for b in self.bullets[:]:
            b.update(self)
        if self.mi:
            self.mi-=1
        else:
            prect=self.prect.move(self.px,self.py)
            for b in self.bullets:
                if prect.collidelist(b.rects)!=-1:
                    self.p.hp-=b.atk
                    phit.play()
                    if self.p.hp<=0:
                        box.done=True
                    else:
                        self.mi=b.mi
                    break
        self.eup(box,events)
        if self.t:
            self.t-=1
        else:
            box.done=True
    def eup(self,box,events):
        pass
    def render(self,sub):
        self.prerender(sub)
        if not self.mi or (self.t//2)%2:
            sub.blit(pimgs[self.pd],(self.px,self.py))
        for b in self.bullets:
            sub.blit(b.img,(b.x,b.y))
    def prerender(self,sub):
        pass
    def postrender(self,sub):
        pass
    def end(self,box,damage):
        box.damage=damage
        box.done=True
class Bullet(object):
    img=None
    orect=pygame.Rect(0,0,0,0)
    atk=1
    mi=60
    orects=None
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.set_rect()
    def update(self,manager):
        pass
    def set_rect(self):
        if self.orects:
            self.rects=[ore.move(self.x,self.y) for ore in self.orects]
        else:
            self.rects=[self.orect.move(self.x,self.y)]
class FallingBullet(Bullet):
    fspeed=1
    def update(self,manager):
        self.y+=self.fspeed
        if self.y>112:
            manager.bullets.remove(self)
        self.set_rect()
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