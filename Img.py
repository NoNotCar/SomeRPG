__author__ = 'NoNotCar'
import pygame
import os

np = os.path.normpath
loc = os.getcwd() + "/Assets/"
pygame.mixer.init()
dfont=pygame.font.Font(np(loc+"PressStart2P.ttf"),16)

def img(fil):
    return pygame.image.load(np(loc + fil + ".png")).convert_alpha()
def img2(fil):
    i=img(fil)
    return pygame.transform.scale(i,(i.get_width()*2,i.get_height()*2)).convert_alpha()


def img32(fil):
    return pygame.transform.scale(pygame.image.load(np(loc + fil + ".png")), (32, 32)).convert_alpha()


def imgsz(fil, sz):
    return pygame.transform.scale(pygame.image.load(np(loc + fil + ".png")), sz).convert_alpha()

def imgstrip2(fil):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // h):
        imgs.append(pygame.transform.scale(img.subsurface(pygame.Rect(n * h, 0, h, h)), (h*2, h*2)).convert_alpha())
    return imgs
def imgstrip(fil):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // h):
        imgs.append(img.subsurface(pygame.Rect(n * h, 0, h, h)).convert_alpha())
    return imgs
def imgstrip2f(fil,w):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // w):
        imgs.append(pygame.transform.scale(img.subsurface(pygame.Rect(n * w, 0, w, h)), (w*2, h*2)).convert_alpha())
    return imgs
def imgrot(i):
    imgs=[i]
    for n in range(3):
        imgs.append(pygame.transform.rotate(i,-90*n-90))
    return imgs


def musplay(fil):
    pygame.mixer.music.load(np(loc+"Music/" + fil+".ogg"))
    pygame.mixer.music.play(-1)


def bcentre(font, text, surface, offset=0, col=(0, 0, 0), xoffset=0):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx + xoffset
    textrect.centery = surface.get_rect().centery + offset
    return surface.blit(render, textrect)

def bcentrex(font, text, surface, y, col=(0, 0, 0), xoffset=0):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx + xoffset
    textrect.top = y
    return surface.blit(render, textrect)
def bcentrerect(font, text, surface, rect, col=(0, 0, 0)):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = rect.centerx
    textrect.centery = rect.centery
    return surface.blit(render, textrect)

def sndget(fil):
    return pygame.mixer.Sound(np(loc+"Sounds/"+fil+".wav"))

def hflip(img):
    return pygame.transform.flip(img,1,0)
def gradback(t,b):
    back=pygame.Surface((480,480))
    for n in range(480):
        pygame.draw.line(back,[(t[x]*(480-n)+b[x]*n)//480 for x in range(3)],(0,n),(480,n),1)
    return back

def x2(img):
    return pygame.transform.scale(img,(img.get_width()*2,img.get_height()*2))

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawTextRect(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

blank32=img2("Trans")