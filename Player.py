from Object import Object
import Img
import pygame
import Direction as D
import Weapon
class Player(Object):
    imgs=Img.imgstrip2("Man")
    hp=40
    hu=40
    mp=40
    d=0
    o3d=4
    items=[None]*10
    items[0]=Weapon.BasicSword()
    def get_img(self,world):
        return self.imgs[self.d]
    def update(self,world,events):
        if not self.moving:
            keys=pygame.key.get_pressed()
            for n,k in enumerate(D.kconv):
                if keys[k]:
                    d=D.directions[n]
                    self.d=n
                    if self.move(d[0],d[1],world):
                        break
        for e in events:
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_SPACE:
                    tx,ty=D.offset(self.d,self)
                    if world.in_world(tx,ty):
                        o=world.get_o(tx,ty)
                        if o:
                            o.interact(world)
                elif e.key==pygame.K_LSHIFT:
                    tx,ty=D.offset(self.d,self)
                    o=world.get_o(tx,ty)
                    if world.in_world(tx,ty):
                        if o:
                            world.add_info(o.get_info(world))

    def add_item(self,item):
        for n,i in enumerate(self.items):
            if not i:
                self.items[n]=item
                return item.n
            elif i.name==item.name:
                if i.n+item.n<=i.maxstack:
                    i.n+=item.n
                    return item.n
                elif i.n<i.maxstack:
                    diff=i.maxstack-i.n
                    i.n=i.maxstack
                    return diff
        return 0
    def sub_item(self,item):
        if item.n==1:
            self.items.remove(item)
        else:
            item.n-=1
    def move(self,dx,dy,world):
        tx=self.x+dx
        ty=self.y+dy
        if not world.in_world(tx,ty):
            world.get_exit()
            return True
        return Object.move(self,dx,dy,world)