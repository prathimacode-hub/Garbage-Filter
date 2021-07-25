import pygame

#sounds
buzz = pygame.mixer.Sound('sound_buzz.wav')
ding = pygame.mixer.Sound('sound_ding.wav')

# bins
blue_bin_pic=pygame.image.load("bin1.png")
blue_bin_pic=pygame.transform.scale(blue_bin_pic,(90,130))
green_bin_pic=pygame.image.load("bin2.png")
green_bin_pic=pygame.transform.scale(green_bin_pic,(90,130))

# recyclable
cardboard=pygame.image.load("recycle_cardboard.png")
cardboard=pygame.transform.scale(cardboard,(55,40))
can=pygame.image.load("recycle_can.png")
can=pygame.transform.scale(can,(20,35))
egg_carton=pygame.image.load("recycle_egg_carton.png")
egg_carton=pygame.transform.scale(egg_carton,(60,58))
newspaper=pygame.image.load("recycle_newspaper.png")
newspaper=pygame.transform.scale(newspaper,(50,45))
paper=pygame.image.load("recycle_paper.png")
paper=pygame.transform.scale(paper,(25,25))
water=pygame.image.load("recycle_water.png")
water=pygame.transform.scale(water,(20,40))


# compost
apple=pygame.image.load("compost_apple.png")
apple=pygame.transform.scale(apple,(27,39))
banana=pygame.image.load("compost_banana.png")
banana=pygame.transform.scale(banana,(45,35))
chicken=pygame.image.load("compost_chicken.png")
chicken=pygame.transform.scale(chicken,(30,15))
egg_shell=pygame.image.load("compost_egg_shell.png")
egg_shell=pygame.transform.scale(egg_shell,(45,26))
tea=pygame.image.load("compost_tea.png")
tea=pygame.transform.scale(tea,(34,39))
watermelon=pygame.image.load("compost_watermelon.png")
watermelon=pygame.transform.scale(watermelon,(54,23))

recyclable_garbage_pictures = [cardboard,can,egg_carton,newspaper,paper,water]
compost_garbage_pictures = [apple,banana,chicken,egg_shell,tea,watermelon]

# ----------- classes ----------- #
class Garbage(object):
    def __init__(self,x,y, speed, image, score):
        self.x=x
        self.y=y
        self.speed = speed
        self.image=image
        self.visable= True
        self.score=score

    def draw(self,surface):
        if self.visable:
            surface.blit(self.image, (self.x, self.y))

    def visibilty(self):
        if self.y>1000:
            self.visable=False

    def move_down(self):
        self.y = self.y + self.speed

    def move_left(self):
        if self.x>-50:
            self.x = self.x - self.speed

    def move_right(self):
        if self.x<500:
            self.x = self.x + self.speed

    def collides(self,other):
        if self.y > 600 and self.y <650: #at right height
            if self.x > (other.x - 45) and self.x < (other.x + 45): #within bin opening
                if self.image in recyclable_garbage_pictures and other.image == blue_bin_pic:
                    if self.visable == True:
                        self.visable = False
                        print ("in the right bin (recycle)")
                        other.score +=5
                        ding.play()
                elif self.image in compost_garbage_pictures and other.image == green_bin_pic:
                    if self.visable == True:
                        self.visable = False
                        print ("in the right bin (recycle)")
                        other.score +=5
                        ding.play()
                else:
                    if self.visable == True:
                        self.visable = False
                        print ("in the wrong bin")
                        other.score -=1
                        buzz.play()

        if self.y > 999:
            if self.image in recyclable_garbage_pictures and other.image == blue_bin_pic:
                if self.visable == True:
                    self.visable = False
                    other.score-=3
            if self.image in compost_garbage_pictures and other.image == green_bin_pic:
                if self.visable == True:
                    self.visable = False
                    other.score -= 3
