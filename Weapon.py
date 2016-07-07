from Item import Item
from Img import img2
from BoxManagers import SlashAttack, PistolAttack
class Weapon(Item):
    maxstack = 1
    utype = "weapon"
    action="hit"
    damrange=(1,2)
    am=None
    def use(self,world):
        tx,ty=world.get_p_look()
        for o in world.get_os(tx,ty):
            if o.name=="NPC":
                world.encounter(o.e,True)
class BasicSword(Weapon):
    img=img2("Sword")
    name="sword"
    action="slash"
    am=SlashAttack
    desc = "An old blunt sword your father gave you. It's a family heirloom"
class Pistol(Weapon):
    img=img2("Pistol")
    name="pistol"
    action = "shoot"
    am=PistolAttack
    desc = "A pistol you looted from your father's body. You can still see the bloodstains."
