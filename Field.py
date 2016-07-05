import Overworld
import Enemies
class OverField(Overworld.World):
    entrances=["FIELDB","FIELDT"]
    ranencounters=[Enemies.RSlime,Enemies.BadFlower,Enemies.BirdBrain]
    save="Fields"
    def enter(self,entrance):
        if entrance=="FIELDB":
            return (17,99)
    def get_exit(self):
        if self.p.y==99:
            self.exit("HOME")