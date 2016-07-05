from Object import Object, MultiPart
from Img import img2
class Building(Object):
    footprint=(1,1)
    def __init__(self,x,y,world):
        self.place(x,y)
        for tx in range(x,x+self.footprint[0]):
            for ty in range(y,y+self.footprint[1]):
                if (tx,ty)!=(x,y):
                    world.spawn(MultiPart(tx,ty,self))
class SHouse(Building):
    img=img2("House")
    o3d = 30
    footprint = (2,1)
    checked=-1
    def get_info(self,world):
        self.checked+=1
        if not self.checked:
            return "It's your house, you idiot"
        elif self.checked<5:
            return "It hasn't stopped being your house yet"
        elif self.checked==5:
            return "Oh wait it's been taken over by fierce pirates!"
        elif self.checked<9:
            return "Happy now?"
        elif self.checked<20:
            return "Seriously. It's your house, just go with it."
        else:
            return "YOUR HOUSE."