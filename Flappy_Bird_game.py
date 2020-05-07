import pygame
import random
import os
import time



WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730


#STAT_FONT = pygame.font.SysFont("comicsans", 50)
#END_FONT = pygame.font.SysFont("comicsans", 50)

#pygame.init()
#WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
#pygame.display.set_caption("Flappy Bird")

#background = pygame.image.load("imgs/bg.png").convert()
#pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
#bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 800))
#bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
#base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())
#clock = pygame.time.Clock()

class FlappyBird:
    def __init__(self, action_callback = None, reward_callback = None, tick_speed = 30):
        self.WIN_WIDTH = 600
        self.WIN_HEIGHT = 800
        self.FLOOR = 730
        
        self.edge_penatly = -10
        self.pipe_penalty = -5
        self.pipe_reward = 1
        self.score = 0

        self.action_fn = action_callback
        self.reward_fn = reward_callback
        self.tick_speed = tick_speed


    #STAT_FONT = pygame.font.SysFont("comicsans", 50)
    #END_FONT = pygame.font.SysFont("comicsans", 50)
        pygame.init()
        self.WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")

        self.background = pygame.image.load("imgs/bg.png").convert()
        self.pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
        self.bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 800))
        self.bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
        self.base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())
        self.clock = pygame.time.Clock()

        self.bird = Bird(230, 350, self.bird_images)
        self.base = Base(self.FLOOR, self.base_img)
        self.pipes = [Pipe(700, self.pipe_img)]

        self.bird_left = self.bird.x
        self.bird_right = self.bird.x + self.bird_images[0].get_width()
    
    def get_state(self):

        next_pipe = None
        pipe_width = self.pipe_img.get_width()
        for pipe in self.pipes:
            if pipe.x + pipe_width >= self.bird.x:
                next_pipe = pipe
                break

        if not next_pipe:
            next_pipe = self.pipes[0]
        #for pipe in self.pipes: 
        #    if pipe[]
        return { 'score': self.score,
                 'pipe' : { 'distance': next_pipe.x + pipe_width - self.bird_left,
                            'top': self.WIN_HEIGHT - (next_pipe.top + next_pipe.pipe_top.get_height()),
                            'bottom': self.WIN_HEIGHT - next_pipe.bottom},
                     #'distance_left': next_pipe - self.bird_right,
                            #'distance_right': next},
                 'bird': { 'displacement' : self.bird.get_diplacement(),
                           'top' : self.WIN_HEIGHT - self.bird.y,
                           'bottom' : self.WIN_HEIGHT - self.bird.y - self.bird_images[0].get_height()}}

    def game_loop(self):
        self.clock.tick(self.tick_speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # game_running = False    
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.jump()
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        
        if self.action_fn is not None and self.action_fn(self.get_state()):
            #print("jump")
            self.bird.jump()
                    

        edge_hit = False
        pipe_hit = False
        add_pipe = False
        pass_pipe = False
        for pipe in self.pipes:
            pipe.move()

            if pipe.collide(self.bird, self.WIN):
                pipe_hit = True
            
            if pipe.x + pipe.pipe_top.get_width() < 0:
                self.pipes.remove(pipe)

            if not pipe.passed and pipe.x < self.bird.x: 
                pipe.passed = True
                add_pipe = True
                pass_pipe = True
                self.score += 1
        #for pipe in pipes: 
        #    pipe.draw(win)
        if add_pipe:
            #score +=1 
            #print(score)
            self.pipes.append(Pipe(WIN_WIDTH, self.pipe_img))
        
        if self.bird.y + self.bird.img.get_height() - 10 >= self.FLOOR or self.bird.y < -50:
            edge_hit = True
            
        if edge_hit:
            if self.reward_fn is not None:
                self.reward_fn(self.edge_penatly)
            if self.action_fn is not None:
                self.action_fn(self.get_state())
            return False
        if pipe_hit:
            if self.reward_fn is not None: 
                self.reward_fn(self.pipe_penalty)
            if self.action_fn is not None:
                self.action_fn(self.get_state())
            return False
        if self.reward_fn is not None:
            if pass_pipe:
                self.reward_fn(self.pipe_reward)
            else:
                self.reward_fn(0)


        self.base.move()
        self.bird.move()
        draw_simple(self.WIN, self.base, self.bird, self.pipes, self.bg_img)

        print(self.get_state())
        return True





class Bird:
    MAX_ROTATION = 25
    #IMGS = bird_images
    ANIMATION_TIME = 5
    rotation_vel = 20

    def __init__(self, x, y, IMGS):
        self.x = x
        self.y = y
        self.IMGS = IMGS
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.tilt = 0
        self.displacement = 0


    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        self.displacement = self.vel*self.tick_count + 1.5*self.tick_count**2

        if self.displacement >= 16:
            self.displacement = (self.displacement/abs(self.displacement)) * 16

        if self.displacement < 0:
            self.displacement -= 2

        self.y = self.y + self.displacement

        if self.displacement < 0: #or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION: 
                self.tilt = self.MAX_ROTATION
        else: 
            if self.tilt > -90:
                self.tilt -= self.rotation_vel

    def draw(self, win):

        self.img_count += 1

        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        # win.blit(self.img, (self.x,self.y))
        RotateImage(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def get_diplacement(self):
        return self.displacement

def RotateImage(surface, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surface.blit(rotated_image, new_rect.topleft)



class Pipe:
    VEL = 5
    GAP = 200

    def __init__(self, x, pipe_img):
        self.x = x
        self.height = 0
        self.pipe_img = pipe_img

        self.top = 0
        self.bottom = 0

        self.pipe_top = pygame.transform.flip(self.pipe_img, False, True)
        self.pipe_bottom = self.pipe_img
        
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL
    
    def draw(self, win):
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pipe_bottom, (self.x, self.bottom))
    
    def collide(self, bird, win):

        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False

class Base:
    VEL = 5
    #IMG = base_img
    #WIDTH = IMG.get_width()

    def __init__(self, y, IMG):
        self.y = y
        self.x1 = 0
        self.IMG = IMG
        self.WIDTH = self.IMG.get_width()
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def draw_simple(window, base, bird, pipes, background_image):
    window.blit(background_image, (0,0))
    for pipe in pipes:
        pipe.draw(window)
    bird.draw(window)
    base.draw(window)

    pygame.display.update()
"""
def draw_window(win, base, bird, pipes):
    clock.tick(30)
    win.blit(bg_img, (0,0))
    score = 0
    edge_penatly = -10
    pipe_penalty = -5
    pipe_reward = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
            if event.key == pygame.K_ESCAPE:
                game_running = False

    edge_hit = False
    pipe_hit = False
    add_pipe = False
    for pipe in pipes:
        pipe.move()

        if pipe.collide(bird, win):
            pipe_hit = True
        
        if pipe.x + pipe.pipe_top.get_width() < 0:
            pipes.remove(pipe)

        if not pipe.passed and pipe.x < bird.x: 
            pipe.passed = True
            add_pipe = True
    for pipe in pipes: 
        pipe.draw(win)
    if add_pipe:
        score +=1 
        print(score)
        pipes.append(Pipe(WIN_WIDTH))
    
    if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
        edge_hit = True
    



    #pipe.draw(win)

    base.move()
    bird.move()
    #pipes[0].move()
    #pipes[0].draw(win)
    base.draw(win)
    bird.draw(win)

    pygame.display.update()


def main():
    draw_window(WIN, base, bird, pipes)

    #pygame.display.update()
"""
if __name__ == '__main__':
    """
    bird = Bird(230, 350)
    base = Base(FLOOR)
    pipes = [Pipe(700)]


    while True:
        #WIN.fill((0,0,0))
        #WIN.blit(bg_img, (0,0))
        #pygame.display.update()
        main()

    """
    game = FlappyBird()

    while game.game_loop():
        pass
