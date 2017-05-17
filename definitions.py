# -*- coding: utf-8 -*-
import pygame, os
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

#Define some colors
black = (0,0,0)
white = (255,255,255)
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)

# Define 
screenwidth = 700
screenheight= 800
done = False
cell_x_num  = 35
cell_y_num  = 30
horizon = 200
clock = pygame.time.Clock()
game_time = 0
update_rate = 20
lv3_line = 5
ini_hori_power = 340
game_cond = "OP"
now_stage = 1
stage_clear = None
Max_stage = 2
# Status
# Lists
cell_list = []
alive_cell_group = pygame.sprite.RenderUpdates()
dead_cell_list = []
dcl = []                                # dead_cell_listの第0要素のリスト

koke_list =[]
gazi_list = []
sanagi_list = []
fly_list = []
rappy_list = []
hitodama_list = []
elice_list = []
eshot_list = []
gazi_family_list = [gazi_list,sanagi_list,rappy_list]
monster_list = [koke_list,gazi_list,sanagi_list,fly_list,rappy_list,hitodama_list,elice_list]
monster_list_elice=[koke_list,gazi_list,sanagi_list,fly_list,rappy_list,hitodama_list]
# Others
back_ground = False
monkey_confirm = False
monster_group = pygame.sprite.RenderUpdates()
monkey = False
monkey_set_flag = False
pig_create_flag = False
pointer = [17,0]
# Screen settings
screen_width = screenwidth
screen_height= screenheight
screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption('ぶたさんのくせになまいきだ')

# Images
opening_img = pygame.image.load("op.png").convert()
stage_clear_img = pygame.image.load("clear.png").convert()
stage_clear2_img = pygame.image.load("clear2.png").convert()
eshot_img = pygame.image.load("eshot.png").convert()
gameover_img = pygame.image.load("GAME_OVER.png")
back_ground = pygame.image.load("butagoya.png").convert()
butasan_front = pygame.image.load("butasan/butasan_front.png").convert()
butasan_left=pygame.image.load("butasan/butasan_left.png").convert()
butasan_right=pygame.image.load("butasan/butasan_right.png").convert()
butasan_back = pygame.image.load("butasan/butasan_back.png").convert()
butasan2_front = pygame.image.load("butasan/butasan2_front.png").convert()
butasan2_left = pygame.image.load("butasan/butasan2_left.png").convert()
butasan2_right = pygame.image.load("butasan/butasan2_right.png").convert()
butasan2_back = pygame.image.load("butasan/butasan2_back.png").convert()
monkey_img   = pygame.image.load("monkey/monkey.png").convert()
cell_nut_img_lv0 = pygame.image.load("cell/cell_lv0.png").convert()
cell_nut_img_lv1 = pygame.image.load("cell/cell_lv1.png").convert()
cell_nut_img_lv2 = pygame.image.load("cell/cell_lv2.png").convert()
cell_nut_img_lv3 = pygame.image.load("cell/cell_lv3.png").convert()
cell_mag_img_lv1 = pygame.image.load("cell/cell_mag_lv1.png").convert()
koke_front = pygame.image.load("koke/koke_front.png").convert()
koke_left  = pygame.image.load("koke/koke_left.png").convert()
koke_right = pygame.image.load("koke/koke_right.png").convert()
koke_back  = pygame.image.load("koke/koke_back.png").convert()
gazi_front = pygame.image.load("gazi/gazi_front.png").convert()
gazi_left = pygame.image.load("gazi/gazi_left.png").convert()
gazi_right = pygame.image.load("gazi/gazi_right.png").convert()
gazi_back = pygame.image.load("gazi/gazi_back.png").convert()
sanagi_front = pygame.image.load("gazi/sanagi.png").convert()
fly_front = pygame.image.load("gazi/fly_front.png").convert()
fly_left = pygame.image.load("gazi/fly_left.png").convert()
fly_right = pygame.image.load("gazi/fly_right.png").convert()
fly_back = pygame.image.load("gazi/fly_back.png").convert()
rappy_front = pygame.image.load("rappy/rappy_front.png").convert()
rappy_left = pygame.image.load("rappy/rappy_left.png").convert()
rappy_left_attack = pygame.image.load("rappy/rappy_left_atack.png").convert()
rappy_right = pygame.image.load("rappy/rappy_right.png").convert()
rappy_right_attack = pygame.image.load("rappy/rappy_right_atack.png").convert()
rappy_back = pygame.image.load("rappy/rappy_back.png").convert()
hitodama_front = pygame.image.load("hitodama/hitodama_front.png").convert()
hitodama_left = pygame.image.load("hitodama/hitodama_left.png").convert()
hitodama_right = pygame.image.load("hitodama/hitodama_right.png").convert()
hitodama_back = pygame.image.load("hitodama/hitodama_back.png").convert()
elice_front = pygame.image.load("elice/elice_front.png").convert()
elice_left = pygame.image.load("elice/elice_left.png").convert()
elice_right = pygame.image.load("elice/elice_right.png").convert()
elice_back = pygame.image.load("elice/elice_back.png").convert()
pickaxe_img = pygame.image.load("pickaxe.png").convert()
pickaxe2_img= pygame.transform.rotate(pickaxe_img,60).convert()
wave_left = pygame.image.load("effect/wave_left.png").convert()
wave_right = pygame.image.load("effect/wave_right.png").convert()
# Image lists
butasan_img = [butasan_back,butasan_left,butasan_right,butasan_front]
butasan2_img = [butasan2_back,butasan2_left,butasan2_right,butasan2_front]
koke_img = [koke_back,koke_left,koke_right,koke_front]
gazi_img = [gazi_back,gazi_left,gazi_right,gazi_front]
sanagi_img = [sanagi_front]
fly_img  = [fly_back,fly_left,fly_right,fly_front]
rappy_img= [rappy_back,rappy_left,rappy_right,rappy_front]
hitodama_img = [hitodama_back,hitodama_left,hitodama_right,hitodama_front]
elice_img = [elice_back,elice_left,elice_right,elice_front]
wave_img = [wave_left,wave_right]
# Transparent settings
monkey_img.set_colorkey((1,1,1))
sanagi_front.set_colorkey((1,1,1))
def set_colorkey_func(img_list,key):
    for img in img_list:
        img.set_colorkey(key)

set_colorkey_func(butasan_img,(1,1,1))
set_colorkey_func(butasan2_img,(1,1,1))
set_colorkey_func(koke_img,(0,0,255))
set_colorkey_func(gazi_img,(0,0,255))
set_colorkey_func(fly_img,(1,1,1))
set_colorkey_func(rappy_img,(1,1,1))
set_colorkey_func(hitodama_img,(0,0,255))
set_colorkey_func(elice_img,(1,1,1))
set_colorkey_func(wave_img,(1,1,1))

# SEs

se_move = pygame.mixer.Sound("sound/pickaxe.ogg")
se_use  = pygame.mixer.Sound("sound/pickaxe_use.ogg")
se_attack = pygame.mixer.Sound("sound/attack.ogg")
se_gazi = pygame.mixer.Sound("sound/gazi.ogg")
# 文字列関係
font_OP = pygame.font.Font("mikachan.ttf",30)
font_game = pygame.font.Font( "mikachan.ttf", 20) # フォント読み込み
