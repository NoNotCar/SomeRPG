import Overworld
import Enemies
import Img
exitimg=Img.img2("Exit")
class BuildingInternals(Overworld.World):
    ex=0
    size=(1,1)
    floor=4
    exiting=False
    name="building"
    backcolour = (100,100,100)
    def __init__(self,arch):
        self.arch=arch
        s=self.size
        self.t=[[self.floor]*s[1] for _ in range(s[0])]
        self.o=[[None]*s[1] for _ in range(s[0])]
        self.oconvert()
        self.build()
    def build(self):
        pass
    def get_exit(self):
        if self.p.x==self.ex and self.p.y==self.size[1]-1:
            self.exiting=True
            self.dest(self.p)
    def erender(self,screen,asx,asy):
        screen.blit(exitimg,(self.ex*32-asx,self.size[1]*32-asy))
class PHouse(BuildingInternals):
    size=(4,3)
    ex=3
    name="phouse"
    def build(self):
        self.spawn(Enemies.DadNPC(0,0))
buildings=[PHouse]