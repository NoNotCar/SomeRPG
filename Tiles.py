from Img import img2
def timg2(fil):
    return img2("Tiles/"+fil)
class Tile(object):
    img=None
    passable=True
    def get_img(self):
        return self.img
class Grass(Tile):
    img=timg2("Grass")
class Field(Tile):
    img = timg2("Farmland")
class Sand(Tile):
    img = timg2("Sand")
class Water(Tile):
    passable = False
    img = timg2("Wasser")
class HFloor(Tile):
    img = img2("HouseFloor")
tiles=[Grass,Field,Sand,Water,HFloor]
tiles=[t() for t in tiles]