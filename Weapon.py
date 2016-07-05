from Item import Item
from Img import img2
from BoxManagers import SlashAttack
class Weapon(Item):
    maxstack = 1
    utype = "weapon"
    action="hit"
    damrange=(1,2)
    am=None
class BasicSword(Weapon):
    img=img2("Sword")
    name="sword"
    action="slash"
    am=SlashAttack
