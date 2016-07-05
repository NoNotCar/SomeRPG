import Tiles, Player, Plants,Buildings, Crops, Text, Battle, Enemies, Img, pygame
from random import randint, choice
EDITOROBJS=[Plants.Tree,Plants.Flowers]
encounter=Img.sndget("encounter")
class World(object):
    entrances=[]
    ranencounters=[]
    def __init__(self,arch):
        self.arch=arch
        savfile=open(Img.np("areas/%s.sav" % self.save))
        savr = savfile.readlines()
        self.size=(len(savr),len(savr[1].split()))
        s=self.size
        self.t=[[0]*s[1] for _ in range(s[0])]
        self.o=[[None]*s[1] for _ in range(s[0])]
        self.oconvert()
        for x,row in enumerate(savr):
            for y,n in enumerate(row.split()):
                try:
                    n=int(n)
                    self.t[x][y]=n
                except ValueError:
                    n=n.split(":")
                    n=(int(n[0]),n[1])
                    self.t[x][y]=n[0]
                    for o in EDITOROBJS:
                        if o.symb==n[1]:
                            self.o[x][y]=[o(x,y)]
    def oconvert(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.o[x][y]=[]
        self.infos=[]
        self.nextencounter=randint(10,20)
    def update(self,events):
        cencounter=self.p.moving and self.ranencounters
        if not self.infos:
            for row in self.o:
                for os in row:
                    for o in os:
                        o.update(self,events)
                        o.mupdate(self)
        if cencounter and not self.p.moving:
            if self.nextencounter:
                self.nextencounter-=1
            else:
                self.nextencounter=randint(10,20)
                self.encounter(choice(self.ranencounters)())

    def render(self,screen):
        ply=self.p
        asx=ply.x*32+int(round(ply.xoff))-240
        #asx=0 if asx<0 else asx if asx<self.size[0]*32-480 else self.size[0]*32-480
        asy=ply.y*32+int(round(ply.yoff))-240
        #asy=0 if asy<0 else asy if asy<self.size[1]*32-480 else self.size[1]*32-480
        #sx=7 if ply.x<7 else ply.x if ply.x<self.size[0]-8 else self.size[0]-8
        #sy=7 if ply.y<7 else ply.y if ply.y<self.size[1]-8 else self.size[1]-8
        sx=ply.x
        sy=ply.y
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if abs(x-sx)<11 and abs(y-sy)<11:
                    screen.blit(Tiles.tiles[self.t[x][y]].get_img(),(x*32-asx,y*32-asy))
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if abs(x-sx)<11 and abs(y-sy)<11:
                    objs=self.o[x][y]
                    for o in objs:
                        screen.blit(o.get_img(self),(x*32+o.xoff-asx,y*32+o.yoff-asy-o.o3d*2))
    def spawn(self,o):
        self.o[o.x][o.y].append(o)
    def in_world(self,x,y):
        return 0<=x<self.size[0] and 0<=y<self.size[1]
    def is_clear(self,x,y):
        if not self.in_world(x,y):
            return False
        for o in self.get_os(x,y):
            if o.solid:
                return False
        return Tiles.tiles[self.t[x][y]].passable
    def dest(self,o):
        self.o[o.x][o.y].remove(o)
    def move(self,o,tx,ty):
        self.dest(o)
        o.x=tx
        o.y=ty
        self.spawn(o)
    def get_os(self,x,y):
        return self.o[x][y]
    def get_o(self,x,y):
        os=self.get_os(x,y)
        if os:
            return os[0]
    def add_info(self,info):
        self.infos.append(Text.Ibox(info))
    def encounter(self,enemy):
        encounter.play()
        pygame.time.wait(500)
        self.arch.encounter(enemy)
    def use_item(self,n):
        self.p.items[n].use(self)
    def get_exit(self):
        pass
    def exit(self,exit):
        for w in self.arch.worlds:
            if exit in w.entrances:
                self.arch.wstack[0]=w
                self.dest(self.p)
                self.p.place(*w.enter(exit))
                w.spawn(self.p)
                w.p=self.p
    def enter(self,entrance):
        return (0,0)
class Home(World):
    entrances=["HOME"]
    def __init__(self,arch):
        self.size=(16,13)
        self.arch=arch
        size=self.size
        self.t=[[0]*size[1] for _ in range(size[0])]
        self.o=[[None]*size[1] for _ in range(size[0])]
        self.oconvert()
        self.p=Player.Player(8,7)
        self.spawn(self.p)
        for x in range(16):
            for y in range(13):
                if x in (0,15) or y in (0,12):
                    if x not in (7,8) or y:
                        self.spawn(Plants.Tree(x,y))
        self.spawn(Buildings.SHouse(2,2,self))
        fx=9
        fy=9
        for x in range(5):
            for y in range(2):
                self.t[fx+x][fy+y]=1
                crop=Crops.Wheat(fx+x,fy+y)
                self.spawn(crop)
                crop.growthlevel=4
        self.spawn(Enemies.OverworldEnemy(11,11,Enemies.Slime()))
    def get_exit(self):
        self.exit("FIELDB")
    def enter(self,entrance):
        return (7,0)
