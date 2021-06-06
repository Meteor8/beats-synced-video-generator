import pygame
import os
import sys
import csv

from  beat1 import beat_track
from  beat2 import onset_detect
from  beat3 import hpss_beats

W = 600
H = 600
size = (W, H)
color_bg = (0, 0, 0)

class Game(object):
    def __init__(self):
        self.gametime = 0
        self.musictime = 0
        self.name = ""
        self.fps = 10
        self.beat = [0,0,0]
        self.beat_ls = [[],[],[]]
        self.color = [(50, 5, 118),(130, 5, 118),(255, 5, 118)]
        self.pos = [(150, 300),(300,300),(450,300)]

    def restart(self):
        self.gametime = 0
        self.musictime = 0
        self.fps = 10
        self.beat = [0,0,0]

    def beat_det(self):
        beat_track("./music/"+self.name+".mp3","./beats/"+self.name+"1.csv" )
        onset_detect("./music/"+self.name+".mp3","./beats/"+self.name+"2.csv" )
        hpss_beats("./music/"+self.name+".mp3","./beats/"+self.name+"3.csv" )
        
    def load_beat(self):
        for i in range(3):
            with open('./beats/'+self.name+str(i+1)+'.csv') as f:
                f_csv = csv.reader(f)
                for row in f_csv:
                    beat_time = int(float(row[0])*10.0)
                    self.beat_ls[i].append(beat_time)
                
def game_loop():
    game.restart()
    pygame.mixer.music.load(r"./music/"+game.name+".mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1, game.musictime)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        window.fill(color_bg)
        
        # 检测节奏
        for i in range(3):
            if game.gametime == game.beat_ls[i][game.beat[i]]:
                pygame.draw.circle(window, game.color[i], game.pos[i], 20, 0) 
                game.beat[i] += 1

        # 画图
        textImage = myfont.render(str(game.gametime), True, (255,255,255))
        window.blit(textImage, (300, 100))

        # 更新
        clock.tick(game.fps)
        game.gametime += 1
        pygame.display.update()
    



pygame.init()
game = Game()
game.name="a"
# game.beat_det()
game.load_beat()

os.environ['SDL_VIDEO_CENTERED'] = '1'
window = pygame.display.set_mode(size)
pygame.display.set_caption('Retrowave Snake')
clock = pygame.time.Clock()
myfont = pygame.font.Font(None, 30)


game_loop()
