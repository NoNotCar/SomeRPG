import Text
class Move(object):
    def use(self,user,target,battle):
        return "..."

class EnemyAttack(Move):
    eam=None
    time=10
    def use(self,user,target,battle):
        battle.add_obox(Text.EAttackBox(self.eam(target,self.time)))

