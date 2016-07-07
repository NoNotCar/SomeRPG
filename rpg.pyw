import pygame
import sys
pygame.init()
screen=pygame.display.set_mode((512,512))
import Img, ArchWorld
clock=pygame.time.Clock()
toolbar=Img.img2("Toolbar")
numerals=Img.imgstrip2f("Numbers",5)+[Img.img2("Ten")]
itemrects=[pygame.Rect(10,10,76,76)]+[pygame.Rect(90+n*44,4,40,40) for n in range(9)]
battlerects=[pygame.Rect(0,480,166,32),pygame.Rect(166,480,180,32),pygame.Rect(346,480,166,32)]
w=ArchWorld.ArchWorld()
t=0
while True:
    events=pygame.event.get()
    for event in events:
        if event.type==pygame.QUIT:
            sys.exit()
        elif w.infos and not w.infos[0].interactive and event.type==pygame.KEYDOWN and event.key==pygame.K_LSHIFT:
            del w.infos[0]
            events.remove(event)
        elif event.type==pygame.MOUSEBUTTONDOWN and not w.infos:
            mx,my=pygame.mouse.get_pos()
            kmods=pygame.key.get_mods()
            if event.button==1:
                for n,rect in enumerate(itemrects):
                    if rect.collidepoint(mx,my) and w.p.items[n]:
                        if kmods&pygame.KMOD_LCTRL:
                            slot1=w.p.items[0]
                            if n:
                                slot1=w.p.items[0]
                                w.p.items[0]=w.p.items[n]
                                w.p.items[n]=slot1
                                w.add_info("You equip the "+w.p.items[0].name)
                            elif w.p.items[1]:
                                slot1=w.p.items[0]
                                w.p.items[0]=w.p.items[1]
                                w.p.items[1]=slot1
                                w.add_info("You equip the "+w.p.items[0].name)
                            w.turn()
                        else:
                            w.use_item(n)
                        break
                else:
                    if w.battling:
                        for n,rect in enumerate(battlerects):
                            if rect.collidepoint(mx,my):
                                w.battle_action(n)
                                break
            elif event.button==3:
                for n,rect in enumerate(itemrects):
                    if rect.collidepoint(mx,my) and w.p.items[n]:
                        w.add_info(w.p.items[n].desc)
    screen.fill(w.wstack[-1].backcolour)
    w.update(events)
    w.render(screen)
    screen.blit(toolbar,(0,0))
    if w.p.hp:
        pygame.draw.rect(screen,(255,0,0),pygame.Rect(154,56,w.p.hp*2,10))
    if w.p.hu:
        pygame.draw.rect(screen,(255,216,0),pygame.Rect(252,56,w.p.hu*2,10))
    if w.p.mp:
        pygame.draw.rect(screen,(0,255,255),pygame.Rect(354,56,w.p.mp*2,10))
    for n,i in enumerate(w.p.items):
        if i:
            if n:
                screen.blit(i.get_img(),(94+(n-1)*44,8))
                if i.n>1:
                   screen.blit(numerals[i.n-2],(116+(n-1)*44-(4 if i.n==10 else 0),26))
            else:
                screen.blit(Img.x2(i.get_img()),(16,16))
                if i.n>1:
                   screen.blit(numerals[i.n-2],(72-(4 if i.n==10 else 0),68))
    if w.infos:
        if w.infos[0].interactive:
            w.infos[0].update(events)
        w.infos[0].render(screen,(0,384 if not w.battling else 352))
        if w.infos[0].interactive and w.infos[0].done:
            del w.infos[0]
    pygame.display.flip()
    clock.tick(60)
