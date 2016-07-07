from Img import blank32,img2
class Item(object):
    name="Item"
    maxstack=10
    utype="normal"
    img=blank32
    desc="Some kind of item"
    def __init__(self,n=1):
        self.n=n
    def get_img(self):
        return self.img
    def use(self,world):
        pass

class WheatItem(Item):
    img=img2("WheatItem")
    name="wheat"
    utype="mfood"
    def use(self,world):
        world.add_info("This isn't really edible")