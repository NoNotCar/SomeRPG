from Object import Object
from Img import imgstrip2f, blank32, img2
from random import randint
from Item import WheatItem
class Crop(Object):
    imgs=[blank32]
    growthlevel=0
    gtr=(0,60)
    gt=0
    harvestcrop=None
    def __init__(self,x,y):
        self.place(x,y)
        self.cgt=randint(*self.gtr)
    def get_img(self,world):
        return self.imgs[self.growthlevel]
    def update(self,world,events):
        if self.growthlevel!=len(self.imgs)-1:
            if self.gt==self.cgt:
                self.gt=0
                self.growthlevel+=1
                self.cgt=randint(*self.gtr)
            else:
                self.gt+=1
    def interact(self,world):
        if self.growthlevel==len(self.imgs)-1 and world.p.add_item(self.harvestcrop(1)):
            self.growthlevel=0
    def get_info(self,world):
        if self.growthlevel==len(self.imgs)-1:
            return "Some wheat, fully grown"
        else:
            return "Some wheat, not grown yet"
class Wheat(Crop):
    imgs=imgstrip2f("Wheat",16)
    o3d=5
    gtr=(60,120)
    harvestcrop = WheatItem