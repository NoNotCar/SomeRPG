from Img import img2, fload
from Object import Object
import Moves
import pygame
from random import randint
import BoxManagers
import Weapon
class Jiggle(Moves.Move):
    def use(self,user,target,battle):
        return user.name.capitalize()+(" wobbles happily!" if user.hap>0 else " jiggles angrily!")
class Spare(Moves.Move):
    def use(self,user,target,battle):
        return user.name.capitalize()+" is sparing you."
class NullMove(Moves.Move):
    def __init__(self,msg):
        self.m=msg
    def use(self,user,target,battle):
        return user.name.capitalize()+self.m
class SlimeBullet(BoxManagers.FallingBullet):
    orect = pygame.Rect(2,6,12,8)
    img=img2("SlimeBullet")
    atk = 3
class LeafBullet(BoxManagers.FallingBullet):
    orect = pygame.Rect(2,4,18,6)
    img=img2("LeafBullet")
    atk = 5
    def update(self,manager):
        self.x=(self.x+20)%132-21
        BoxManagers.FallingBullet.update(self,manager)
class SunSpawner(BoxManagers.Bullet):
    orect = pygame.Rect(10,10,12,12)
    img=img2("Bullets/Sun")
    atk = 100
    t=0
    def update(self,manager):
        if self.y:
            self.y+=1
        if self.t<60:
            self.t+=1
        else:
            self.t=0
            offset=randint(0,60)
            for x in range(6):
                manager.bullets.append(BoxManagers.AngBullet(self.x+12,self.y+12,x*60+offset,2))
class BirdBeak(BoxManagers.Bullet):
    orects = [pygame.Rect(0,2,104,12),pygame.Rect(0,8,112,4)]
    atk=6
    dx=2
    img=img2("LongBeak")
    def update(self,manager):
        self.x+=self.dx
        if self.x==0:
            self.dx=-4
        elif self.x==-112:
            manager.bullets.remove(self)
        self.set_rect()
class FBulletAttack(BoxManagers.EnemyAttackManager):
    bchance=20
    bclass=None
    def eup(self,box,events):
        if not randint(0,self.bchance):
            self.bullets.append(self.bclass(randint(0,96),-self.bclass.img.get_height()))
class SlimeAttack(FBulletAttack):
    bclass=SlimeBullet
class LeafAttack(FBulletAttack):
    bclass = LeafBullet
class BeakAttack(BoxManagers.EnemyAttackManager):
    def eup(self,box,events):
        if not self.bullets:
            self.bullets.append(BirdBeak(-112,randint(0,96)))
class SunAttack(BoxManagers.EnemyAttackManager):
    spawned=False
    def eup(self,box,events):
        if not self.spawned:
            self.spawned=True
            self.bullets.append(SunSpawner(randint(0,80),-32))

class SlimeSpray(Moves.EnemyAttack):
    eam=SlimeAttack
class LeafStorm(Moves.EnemyAttack):
    eam = LeafAttack
class BeakPoke(Moves.EnemyAttack):
    eam = BeakAttack
class SunSpray(Moves.EnemyAttack):
    eam = SunAttack

class Enemy(object):
    mhp=1
    name="Enemy"
    img=None
    owimg=None
    hap=0
    moves=[]
    actextras=[]
    loot=None
    desc="A horrid creature"
    singular=False
    def __init__(self):
        self.hp=self.mhp
    def get_img(self,battle):
        return self.img
    def likes_food(self,foodname):
        return False
    def allow_leave(self,battle):
        return False
    def act(self,n,battle):
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
class RSlime(Enemy):
    name="red slime"
    img=img2("RedSlime")
    himg=img2("RedSlimeH")
    moves = [Jiggle(),SlimeSpray(),SlimeSpray()]
    desc = "A small slime. It doesn't look too dangerous, just quite hungry."
    mhp=15
    hap = -1
    def likes_food(self,foodname):
        return True
    def get_img(self,battle):
        return self.himg if self.hap>0 else self.img
class CoolSlime(Enemy):
    name="cool slime"
    img=img2("CoolSlime")
    moves = [NullMove(" is chillin'."),SlimeSpray(),SunSpray()]
    desc = "A RAD COOL slime."
    mhp=15
    hap = 0
    actextras = ["Chill"]
    def act(self,n,battle):
        battle.add_info("You chill with the cool slime. You feel relaxed")
        self.hap=1
class BadFlower(Enemy):
    name="???"
    img=img2("BadFlower")
    moves = [LeafStorm()]
    desc = "A very angry flower."
    mhp=20
    hap = 0
    actextras = ["Taunt","Flirt","Hug"]
    def likes_food(self,foodname):
        return False
    def act(self,n,battle):
        if n!=3:
            battle.add_info(self.name.capitalize()+" makes a very rude gesture with its leaves")
        else:
            battle.add_info(self.name.capitalize()+" is conforted!")
            self.hap+=1
    def allow_leave(self,battle):
        return randint(0,1)
class BirdBrain(Enemy):
    name="???"
    img=img2("BirdBrain")
    moves = [BeakPoke()]
    desc = "Some kind of bird. It's pecking at the ground."
    mhp=8
    hap = 0
    def likes_food(self,foodname):
        if foodname=="wheat":
            return True
    def allow_leave(self,battle):
        return False
class Dad(Enemy):
    name="Dad"
    owimg = img2("Dad")
    img=img2("DadBattle")
    moves=[Spare()]
    desc = "It's your father."
    mhp = 20
    hap=1
    singular = True
    loot = Weapon.Pistol
class OverworldNPC(Object):
    encountered=False
    name="NPC"
    deathtext=None
    o3d=4
    def __init__(self,x,y,enemy=None):
        self.place(x,y)
        if not self.e:
            self.e=enemy
        self.img=self.e.owimg
        self.info=self.e.desc
    def update(self,world,events):
        if self.e.hp==0:
            if self.deathtext:
                world.add_info(self.deathtext)
            world.dest(self)
class DadNPC(OverworldNPC):
    e=Dad()
    tfont = fload("PrStart")
    deathtext = "You feel like you'll regret this."
    def interact(self,world):
        world.add_talk("Hello, son",self)
class OverworldEnemy(Object):
    o3d=4
    name="NPC"
    def __init__(self,x,y,enemy):
        self.place(x,y)
        self.img=enemy.owimg
        self.e=enemy
        self.info="That %s looks dangerous" % self.e.name
    def interact(self,world):
        world.encounter(self.e)
        world.dest(self)