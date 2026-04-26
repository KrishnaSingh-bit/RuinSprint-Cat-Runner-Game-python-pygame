import pygame
from sys import exit
from random import choice

class Animator:
    def __init__(self, sprite_sheet, frame_count, scale=1, flip=False, speed=0.15):
        self.frames = []
        self.index = 0
        self.speed = speed

        # slice sprite sheet
        w = sprite_sheet.get_width() // frame_count
        h = sprite_sheet.get_height()

        for i in range(frame_count):
            frame = sprite_sheet.subsurface((i * w, 0, w, h))

            if scale != 1:
                frame = pygame.transform.scale_by(frame, scale)

            if flip:
                frame = pygame.transform.flip(frame, True, False)

            self.frames.append(frame)

    def update(self, dt=1):
        dt /= 1000  

        self.index += self.speed * dt

        if self.index >= len(self.frames):
            self.index = 0

        return self.frames[int(self.index)]
    
class AnimatedSprite:
    def __init__(self, x, y):
        self.animations = {}
        self.current = None

        self.image = None
        self.rect = pygame.Rect(x, y, 0, 0)

    def add_animation(self, name, animator):
        self.animations[name] = animator
        if self.current is None:
            self.current = name
            self.image = animator.frames[0]
            self.rect.size = self.image.get_size()

    def set_animation(self, name):
        if name in self.animations:
            self.current = name

    def update(self, dt=1,X = 0):
        animator = self.animations[self.current]

        self.image = animator.update(dt)

        # KEEP RECT UPDATED WITH IMAGE SIZE
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)
        self.hitbox = pygame.Rect(0, 0, 120, 80)
        if X == 0:
             self.hitbox.center = self.rect.center
        elif X == 1:
             self.hitbox = pygame.Rect(0, 0, 100, 130)
             self.hitbox.center = self.rect.center
             self.rect.bottom = 510
             

             

    def draw(self, surface):
        surface.blit(self.image, self.rect)

pygame.init()
Display = pygame.display.set_mode((1400,600), pygame.RESIZABLE)
pygame.display.set_caption("Krishna")
clock = pygame.time.Clock()

def Score_counter(CTime,x,y):
    Font = pygame.font.Font("font/Minecraft.ttf", 50)
    Score = Font.render(f"Score: {CTime}", False, "Grey")
    RScore = Score.get_rect(topleft = (x,y))  
    Display.blit(Score,RScore)

MCount = 1

class Button():
	def __init__(self, normal_image, hover_image, x_pos, y_pos, size=(50, 50)):
		self.normal_image = pygame.transform.scale(normal_image, size)
		self.hover_image = pygame.transform.scale(hover_image, size)

		self.image = self.normal_image
		self.x_pos = x_pos
		self.y_pos = y_pos

		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

	def update(self):
		Display.blit(self.image, self.rect)

	def playGame(self, position):
		if self.rect.collidepoint(position):
			global ActiveGame, start_time
			ActiveGame = True
			start_time = pygame.time.get_ticks()

	def exitGame(self, position, ):
		if self.rect.collidepoint(position): 
			pygame.quit()
			exit()

	def StopMusic(self, position, ):
		global MCount
		if self.rect.collidepoint(position): 
			MCount += 1
			if MCount %2 == 0:
				BGM.set_volume(0.5)
				self.image = self.normal_image
			else:
				BGM.set_volume(0)
				self.image = self.hover_image

	def changeFrame(self, position):
		if self.rect.collidepoint(position):
			self.image = self.hover_image
		else:
			self.image = self.normal_image

		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))


# Sound

JumpSound = pygame.mixer.Sound("audio/jump.mp3")
JumpSound.set_volume(0.5)
GameOver = pygame.mixer.Sound("audio/gameover.mp3")
GameOver.set_volume(0.5)
Dash = pygame.mixer.Sound("audio/dash.wav")
Dash.set_volume(0.6)
Score50 = pygame.mixer.Sound("audio/score50.wav")
Score50.set_volume(0.5)
BGM = pygame.mixer.Sound("audio/bgm.mp3")
BGM.set_volume(0.5)
BGM.play(loops = -1)


#Buttons

P1 = pygame.image.load("Buttons/PlayButton.png").convert_alpha()
P2 = pygame.image.load("Buttons/RestartButton.png").convert_alpha()
Play = Button(P1, P2, 700,260,(75,75))

E1 = pygame.image.load("Buttons/CancelButton.png").convert_alpha()
E2 = pygame.image.load("Buttons/ExitButton.png").convert_alpha()
Exit = Button(E1, E2, 1360,40)

M1 = pygame.image.load("Buttons/MuteButton.png").convert_alpha()
M2 = pygame.image.load("Buttons/UnMuteButton.png").convert_alpha()
MusicB = Button(M1, M2, 1360,100)

#Titles

Font = pygame.font.Font("font/Minecraft.ttf", 100)
Game_Title = Font.render("RuinSprint", False, "White")
GName = Game_Title.get_rect(center = (700,100))  

Font = pygame.font.Font("font/Minecraft.ttf", 50)
KRI = Font.render("By Krishna Singh", False, "#336600")
SHNA = KRI.get_rect(center = (700,700))

Font2 = pygame.font.Font("font/Minecraft.ttf", 30)
ins1 = Font2.render("Press Space to Start!!", False, "White")
I1 = ins1.get_rect(center = (700,330))

Background = pygame.image.load("background/background_exp3.png").convert()
bg_width = Background.get_width()
BG_move = 0

Ground = pygame.image.load("background/ground_nobg.png").convert_alpha()
Ground_move = 0

CTRL1 = pygame.image.load("controls.png").convert_alpha()
Control_img = pygame.transform.scale_by(CTRL1, 0.1)

#Enemy

Enemy1 = pygame.image.load("sprites/_Roll.png").convert_alpha()
Enemy2 = pygame.image.load("sprites/_Run.png").convert_alpha()
Enemy3 = pygame.image.load("sprites/eagle-attack.png").convert_alpha() 
Enemy4 = pygame.image.load("sprites/DWALK.png").convert_alpha() 
Enemy5 = pygame.image.load("sprites/DLEV.png").convert_alpha() 
Enemy6 = pygame.image.load("sprites/DGWALK.png").convert_alpha() 
Enemy7 = pygame.image.load("sprites/EGWALK.png").convert_alpha() 

Enemy = AnimatedSprite(1600,180)
Enemy.add_animation("ERoll",Animator(Enemy1,12, scale = 4, flip = True, speed = 8))
Enemy.add_animation("ERUN",Animator(Enemy2,10, scale = 4, flip = True, speed = 8))
Enemy.add_animation("EDASH",Animator(Enemy3,4, scale = 3, flip = False, speed = 3))
Enemy.add_animation("DWALK",Animator(Enemy4,8, scale = 4, flip = True, speed = 6))
Enemy.add_animation("DLEV",Animator(Enemy5,6, scale = 4, flip = True, speed = 6))
Enemy.add_animation("DGWALK",Animator(Enemy6,8, scale = 4, flip = True, speed = 6))
Enemy.add_animation("EGWALK",Animator(Enemy7,8, scale = 4, flip = True, speed = 6))

Enemy_List = ["ERoll","ERUN","EDASH","DWALK","DLEV","DGWALK","EGWALK"]

#player

run_sheet = pygame.image.load("sprites/RUN.png").convert_alpha()
jump_sheet = pygame.image.load("sprites/JUMP.png").convert_alpha()
idle_sheet = pygame.image.load("sprites/IDLE.png").convert_alpha()

player = AnimatedSprite(150, 400)

player.add_animation("RUN", Animator(run_sheet, 8, scale=3, flip=True, speed=8))
player.add_animation("JUMP", Animator(jump_sheet, 3, scale=3, flip=True, speed=2))
player.add_animation("IDLE", Animator(idle_sheet, 8, scale=6, flip=True, speed=3))

Gravity = 0
ActiveGame = False
dt = 0
start_time = 0
Final_score = 0

while True:
    dt = clock.tick(60)
    

    #EVENTS 
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            exit()

        if i.type == pygame.KEYDOWN:
            if (i.key == pygame.K_SPACE or i.key == pygame.K_UP or i.key == pygame.K_w)and player.rect.bottom > 500:
                JumpSound.play()
                Gravity = -20  
                if not ActiveGame:
                     start_time = pygame.time.get_ticks()
                     ActiveGame = True   

            if i.key == pygame.K_m or i.key == pygame.K_DOWN or i.key == pygame.K_s:
                Dash.play()
                Gravity += 40

        if i.type == pygame.MOUSEBUTTONDOWN:
             Play.playGame(pygame.mouse.get_pos())
             Exit.exitGame(pygame.mouse.get_pos())
             MusicB.StopMusic(pygame.mouse.get_pos())
             
             
        mouse_pos = pygame.mouse.get_pos()

    #DRAW
    BG_move -= 1
    if BG_move <= -bg_width:
        BG_move = 0

    Display.blit(Background, (BG_move, 0))
    Display.blit(Background, (BG_move + bg_width, 0))

    if ActiveGame:

        score = (pygame.time.get_ticks() - start_time) //100
        Score_counter(score,75,50)

        if score%50 == 0:
             Score50.play()

        #INPUT
        keys = pygame.key.get_pressed()

        if player.rect.bottom < 560:
            player.set_animation("JUMP")

        else:
            player.set_animation("RUN")
            
        Enemy.update(dt,1)

        #PHYSICS 
        Gravity += 0.8
        player.rect.y += Gravity

        if player.rect.bottom > 560:
            player.rect.bottom = 560
            Gravity = 0

        if player.rect.x > 150:
            player.rect.x -= 5

        if Enemy.rect.x > -200:
            Enemy.rect.x -= 10
        else:
             Enemy.rect.x = 1500
             Element = choice(Enemy_List)
             if Element in ["EDASH","DLEV"]:
                  Enemy.hitbox.y -= 10 
             Enemy.set_animation(Element)

            

        #UPDATE 
        player.update(dt)


        #collision
        if player.hitbox.colliderect(Enemy.hitbox): 
            GameOver.play()
            ActiveGame = False
            Final_score = score


    else:
        Display.blit(Control_img,(1130,350))

        Play.changeFrame(mouse_pos)
        Play.update()
        Exit.changeFrame(mouse_pos)
        Exit.update()
        
        MusicB.update()

        score = 0
        Display.blit(Game_Title,GName)
        Display.blit(ins1,I1)
        Score_counter(Final_score,500,150)
        if player.rect.x < 400:
            player.rect.x += 5
        else:
            player.set_animation("IDLE")
            player.rect.y = 240


    # player

    player.update(dt)
    player.draw(Display)
    
    Enemy.update(dt,1)
    Enemy.draw(Display)
    
    # hitboxes
    """ 
    pygame.draw.rect(Display, (0, 255, 0), Enemy.rect, 2)
    pygame.draw.rect(Display, (0, 25, 0), Enemy.hitbox, 2)
    pygame.draw.rect(Display, (255,0,0), player.rect, 2)
    pygame.draw.rect(Display, (0, 0, 255), player.hitbox, 2)
    """
    Display.blit(KRI,SHNA)
    # ground
    Ground_move -= 0.5
    if -(Ground_move) > 400:
        Ground_move = 0
    Display.blit(Ground,(Ground_move,100))


    pygame.display.update()
