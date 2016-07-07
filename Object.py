import Img
class Object(object):
    img=Img.blank32
    speed=2
    xoff,yoff=(0,0)
    moving=False
    o3d=0
    solid=True
    info="Nothing to see here"
    symb="O"
    tfont=None
    name="Object"
    def __init__(self,x,y):
        self.place(x,y)
    def place(self,x,y):
        self.x=x
        self.y=y
    def update(self,world,events):
        pass
    def get_img(self,world):
        return self.img
    def mupdate(self,world):
        if self.xoff>0:
            self.xoff-=self.speed
        elif self.xoff<0:
            self.xoff+=self.speed
        if self.yoff>0:
            self.yoff-=self.speed
        elif self.yoff<0:
            self.yoff+=self.speed
        if abs(self.xoff)<self.speed and abs(self.yoff)<self.speed and self.moving:
            self.xoff=0
            self.yoff=0
            self.moving=False
    def move(self,dx,dy,world):
        tx=self.x+dx
        ty=self.y+dy
        if world.is_clear(tx,ty):
            world.move(self,tx,ty)
            self.moving=True
            self.xoff= -dx*32
            self.yoff= -dy*32
            return True
        return False
    def interact(self,world):
        pass
    def get_info(self,world):
        return self.info
    def enter(self,world,d):
        return False
    def offenter(self,mp,world,d):
        pass
class MultiPart(Object):
    def __init__(self,x,y,p):
        self.parent=p
        self.place(x,y)
    def get_info(self,world):
        return self.parent.get_info(world)
    def enter(self,world,d):
        return self.parent.offenter(self,world,d)