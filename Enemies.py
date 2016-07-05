from Img import img2
from Object import Object
import Moves
class Jiggle(Moves.Move):
    def use(self,user,target,battle):
        return user.name.capitalize()+(" wobbles happily!" if user.hap else " jiggles angrily!")
class Enemy(object):
    mhp=1
    name="Enemy"
    img=None
    owimg=None
    hap=0
    moves=[]
    actextras=[]
    desc="A horrid creature"
    def __init__(self):
        self.hp=self.mhp
    def get_img(self,battle):
        return self.img
    def likes_food(self,foodname):
        return False
    def allow_leave(self,battle):
        return False
    def act(self,n):
        pass
    def damage(self,dam):
        self.hp-=dam
        if self.hp<0:
            self.hp=0
class Slime(Enemy):
    name="slime"
    img=img2("Slime")
    himg=img2("SlimeH")
    owimg=img2("OWSlime")
    moves = [Jiggle()]
    desc = "A small slime. It doesn't look very dangerous, just hungry."
    mhp=10
    def likes_food(self,foodname):
        return True
    def get_img(self,battle):
        return self.himg if self.hap else self.img
    def allow_leave(self,battle):
        return True
class OverworldEnemy(Object):
    encountered=False
    def __init__(self,x,y,enemy):
        self.place(x,y)
        self.img=enemy.owimg
        self.e=enemy
        self.info="That %s looks dangerous" % self.e.name
    def interact(self,world):
        world.encounter(self.e)
        world.dest(self)