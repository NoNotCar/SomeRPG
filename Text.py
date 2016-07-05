import Img
import pygame
infobox=Img.img2("InfoBox")
multibox=Img.img2("MultiBox")
wabox=Img.img2("AtkBoxWide")
sabox=Img.img2("AtkBoxSquare")
cursor=Img.img2("Selector")
class Tbox(object):
    img=None
    interactive=False
    def render(self,screen,iloc):
        screen.blit(self.img,iloc)
class Ibox(Tbox):
    def __init__(self,info):
        self.img=infobox.copy()
        Img.drawTextRect(self.img," "*3+info,(64,64,64),pygame.Rect(10,10,492,108),Img.dfont)
class MultiBox(Tbox):
    interactive = True
    done=False
    def __init__(self,texts):
        self.img=multibox.copy()
        for n,t in enumerate(texts):
            Img.bcentrerect(Img.dfont,t,self.img,pygame.Rect(254 if n%2 else 4,38*(n//2)+4,254,42),(64,64,64))
        self.maxn=len(texts)
        self.n=0
    def update(self,events):
        for e in events:
            if e.type==pygame.KEYDOWN:
                if e.key in (pygame.K_d,pygame.K_a):
                    self.n=(self.n+(1 if e.key==pygame.K_d else -1))%self.maxn
                elif e.key==pygame.K_LSHIFT:
                    self.done=True
    def render(self,screen,iloc):
        screen.blit(self.img,iloc)
        screen.blit(cursor,((375 if self.n%2 else 125)+iloc[0],38*(self.n//2)+iloc[1]+2))
class AttackBox(Tbox):
    interactive = True
    done=False
    def __init__(self,weapon):
        self.img=wabox.copy()
        self.am=weapon.am()
        self.sub=self.img.subsurface(pygame.Rect(8,8,496,112))
    def update(self,events):
        self.am.update(self,events)
    def render(self,screen,iloc):
        self.sub.fill((0,0,0))
        self.am.render(self.sub)
        screen.blit(self.img,iloc)
class EAttackBox(Tbox):
    interactive = True
    done=False
    def __init__(self,eam):
        self.img=sabox.copy()
        self.am=eam
        self.sub=self.img.subsurface(pygame.Rect(200,8,112,112))
    def update(self,events):
        self.am.update(self,events)
    def render(self,screen,iloc):
        self.sub.fill((0,0,0))
        self.am.render(self.sub)
        screen.blit(self.img,iloc)

