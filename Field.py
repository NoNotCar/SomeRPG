import Overworld
import Enemies
class OverField(Overworld.World):
    music = "ChOrDs"
    entrances=["FIELDB","FIELDT"]
    ranencounters=[Enemies.RSlime,Enemies.BadFlower,Enemies.BirdBrain,Enemies.CoolSlime]
    save="Fields"
    def enter(self,entrance):
        self.remusic()
        if entrance=="FIELDB":
            return (17,99)
    def get_exit(self):
        if self.p.y==99:
            self.exit("HOME")