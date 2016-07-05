class Move(object):
    def use(self,user,target,battle):
        return "..."

class Attack(Move):
    astr=1
    def use(self,user,target,battle):
        if target.hp>=self.astr:
            target.hp-=self.astr
        else:
            target.hp=0