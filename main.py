# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import random
import sys

from definitions import *
def dcl_around2(cell):
    list = [False]*4
    if (cell[1]>0 and [cell[0],cell[1]-1] in dcl):
        list[0] = True     # Top,Middle
    if (cell[0] >0 and  [cell[0]-1,cell[1]] in dcl):
        list[1] = True # Middle,Left
    if (cell[0] < cell_x_num and [cell[0]+1,cell[1]] in dcl):
        list [2] = True # Middle,Right
    if (cell[1] < cell_y_num and [cell[0],cell[1]+1] in dcl):
        list[3] = True     # Bottom,Middle
    return list
#----------------------------------------
#--------------- Class ------------------
#----------------------------------------pp
class Objects(pygame.sprite.Sprite):
    def image_tasks(self):
        cell_size = 20           
        self.image = pygame.transform.scale(self.image,(cell_size,cell_size))
        self.rect = [self.point[0]*cell_size+self.dx,horizon+self.point[1]*cell_size+self.dy]

    def __init__(self,point):
        self.dx,self.dy = 0,0
        pygame.sprite.Sprite.__init__(self)
        self.point = point

class Mover(Objects):
    def __init__(self,point):
        Objects.__init__(self,point)
        self.spread_flag = True
        
class Monster(Mover):
    def decide_direction(self,direc_prior): # direc_prior は優先順位を記録した4要素のリスト
        around = dcl_around2(self.point)
        for x in direc_prior:
            if around[x] == True:
                self.direc = x
                break

    def __init__(self,point,img_list,direc_prior=[0,3,2,1]):
        Mover.__init__(self,point)
        self.direc_prior = direc_prior # 初期の優先順位はUp,Down,Right,Left
        self.decide_direction(self.direc_prior)
        self.image = img_list[self.direc]
        self.image_tasks()
    def walk_straight(self,around_dead_cell):
        if around_dead_cell[self.direc] != False:
            self.point = around_dead_cell[self.direc]
            return True
        else:
            return False

    def make_spread_nut_list(self):
        list = [False]*8
        cell = self.point[:]
        if cell[1]>0:
            if (cell[0]>1 and [cell[0]-1,cell[1]-1] not in dcl):
                list[0] = [cell[0]-1,cell[1]-1]      # Top,Left
            if [cell[0],cell[1]-1] not in dcl:
                list[1] = [cell[0],cell[1]-1]     # Top,Middle
            if (cell[0]<cell_x_num-1 and  [cell[0]+1,cell[1]-1] not in dcl):
                list[2] = [cell[0]+1,cell[1]] # Top,Right
        if (cell[0]>0 and [cell[0]-1,cell[1]] not in dcl):
            list[3] = [cell[0]-1,cell[1]]          # Middle,Left
        if (cell[0]<cell_x_num-1 and [cell[0]+1,cell[1]] not in dcl):
            list[4] = [cell[0]+1,cell[1]]     # Middle,Right
        if cell[1]<cell_y_num-1:
            if (cell[0]>1 and [cell[0]-1,cell[1]+1] not in dcl):
                list[5] = [cell[0]-1,cell[1]+1]      # Top,Left
            if [cell[0],cell[1]+1] not in dcl:
                list[6] = [cell[0],cell[1]+1]     # Top,Middle
            if (cell[0]<cell_x_num-1 and  [cell[0]+1,cell[1]+1] not in dcl):
                list[7] = [cell[0]+1,cell[1]+1] # Top,Right
        return list

    def spread_nut(self):
        for x in self.make_spread_nut_list():
            if x != False:
                cell_list[x[0]][x[1]].nut +=1
                self.nut -= 1
                if self.nut == 0:
                    break
    def spread_mag(self):
        for x in self.make_spread_nut_list():
            if x != False:
                cell_list[x[0]][x[1]].mag +=1
                self.mag -= 1
                if self.mag == 0:
                    break
        

    def hp_tasks(self,List):
        if game_time %100 == 0:
            self.hp -= 1
        if self.hp <= 0:
            List.pop(List.index(self))
            if self.spread_flag == True:
                pass
            self.spread_nut()

class Koke(Monster):
    def __init__(self,point):
        Monster.__init__(self,point,koke_img)
        self.hp = 15
        self.hpmax = 30
        self.power =10
        self.def_phy = 1
        self.def_mag = 0
        self.nut = 0
    
    def walk(self,around_dead_cell):
        if self.walk_straight(around_dead_cell) == False:
            list_for_choice = []
            # 等しい確率で方向を変える
            for x in range(4):
                if around_dead_cell[x] != False:
                    list_for_choice.append(x)
            self.direc = random.choice(list_for_choice)
            # 変えた方向でもってその方向にまっすぐ歩かせる
            self.walk_straight(around_dead_cell)

    def attack(self,around_dead_cell,Class):
        if Class.exist_flag == True:
            for x in around_dead_cell:
                if Class.point == x:
                    Class.hp -= self.power
                    self.direc = trans_cell_to_direc(self,x)
                    screen.blit(wave_img[0],[(self.rect[0]+Class.rect[0])/2,(self.rect[1]+Class.rect[1])/2])
                    se_attack.play()
                    return True
        return False
        
    def update(self):
        around_alive_cell = around_alive_cell_make(self.point)
        around_dead_cell  = around_dead_cell_make(self.point)
        if self.attack(around_dead_cell,pig):
            if  self.direc == 0:
                self.dy = -20
            elif self.direc == 1:
                self.dx = -20
            elif self.direc == 2:
                self.dx =  20
            elif self.direc == 3:
                self.dy =  20

            if self.direc == 1:
                self.image = koke_left
            elif self.direc == 2:
                self.image = koke_right
        else:
            self.walk(around_dead_cell)
            self.image = koke_img[self.direc]
                # 養分の移動
            for x in range(4):
                if around_alive_cell[x] != False:
                    dest_cell = cell_list[around_alive_cell[x][0]][around_alive_cell[x][1]]
                    if (random.randint(0,9) < 3 and dest_cell.nut >0):
                        if self.nut >= 3:
                            dest_cell.nut += 1
                            self.nut -= 1
                        if (random.randint(0,9) < 3 and dest_cell.nut>0):
                            dest_cell.nut -= 1
                            self.nut += 1
                                        
        self.image_tasks()
        self.hp_tasks(koke_list)

class Gazi(Monster):
    def __init__(self,point):
        Monster.__init__(self,point,gazi_img)
        self.hp = 30
        self.hpmax = 60
        self.power = 15
        self.def_phy = 2
        self.def_mag = 0
        self.nut = 0
        self.se = se_gazi

    def walk(self,around_dead_cell):
        """Koke よりランダム要素高め。1/3 で方向転換"""
        if (self.walk_straight(around_dead_cell) == False 
            or random.randint(0,10)<=3):
            list_for_choice = []
            # 等しい確率で方向を変える
            for x in range(4):
                if around_dead_cell[x] != False:
                    list_for_choice.append(x)
            self.direc = random.choice(list_for_choice)
            # 変えた方向でもってその方向にまっすぐ歩かせる
            self.walk_straight(around_dead_cell)

    def attack(self,around_dead_cell,Class,Koke_list):
        """ぶたに攻撃するだけじゃなくて、コケも捕食するよ"""
        for x in around_dead_cell:
            if Class.exist_flag == True:
                if Class.point == x: # 豚が居たら
                    Class.hp -= self.power
                    self.direc = trans_cell_to_direc(self,x)
                    return True
            elif Koke_list != [] and random.randint(0,2)==0:
                for koke in Koke_list:
                    if koke.point == x:
                        damage = self.power - koke.def_phy
                        koke.hp -= damage
                        koke.spread_flag = False
                        self.hp += damage + 10
                        self.direc = trans_cell_to_direc(self,x)
                        self.nut = koke.nut
                        self.se.play()
                        return True
        return False

    def update(self):
        around_alive_cell = around_alive_cell_make(self.point)
        around_dead_cell  = around_dead_cell_make(self.point)
        if self.attack(around_dead_cell,pig,koke_list):
            pass
        else:
            self.walk(around_dead_cell)
            self.image = gazi_img[self.direc]
            
            # サナギ化
            if self.hp >= self.hpmax:
                new_sanagi = Sanagi(self)
                sanagi_list.append(new_sanagi)
                gazi_list.pop(gazi_list.index(self))
        self.image_tasks()
        self.hp_tasks(gazi_list)

class Sanagi(Gazi):
    def decide_direction(self,direc_prior):
        # 仕方なく再定義
        self.direc = direc_prior[0]

    def __init__(self,Gazi_original):
        Monster.__init__(self,Gazi_original.point,sanagi_img,[0,0,0,0]) # サナギの画像は1枚なので、方向は上のみnp
        self.hp = Gazi_original.hp
        self.hpmax = Gazi_original.hp
        self.power = 0
        self.def_phy = 8
        self.def_mag = 0
        self.time = 0
        self.nut = Gazi_original.nut
    def update(self):
        if self.time == 100:
            fly_list.append(Fly(self))
            sanagi_list.pop(sanagi_list.index(self))
            self.time += 1
        self.image_tasks()
        self.hp_tasks(sanagi_list)
        self.time += 1

class Fly(Gazi):
    """能力を上げただけで、ガジガジと同じ処理をする。"""
    def __init__(self,Sanagi_original):
        Monster.__init__(self,Sanagi_original.point[:],fly_img)
        self.hp = 70
        self.hpmax = 100
        self.power = 30
        self.def_phy = 5
        self.def_mag = 0
        self.nut = Sanagi_original.nut
    def update(self):
        around_alive_cell = around_alive_cell_make(self.point)
        around_dead_cell  = around_dead_cell_make(self.point)
        if self.attack(around_dead_cell,pig,koke_list):
            pass
        else:
            self.walk(around_dead_cell)
            self.image = fly_img[self.direc]
            
        self.image_tasks()
        self.hp_tasks(fly_list)

    def attack(self,around_dead_cell,Class,Koke_list):
        """ぶたに攻撃するだけじゃなくて、コケも捕食するよ"""
        for x in around_dead_cell:
            if Class.exist_flag == True:
                if Class.point == x: # 豚が居たら
                    Class.hp -= self.power
                    self.direc = trans_cell_to_direc(self,x)
                    return True
            elif Koke_list != [] and self.hp < self.hp/3:
                for koke in Koke_list:
                    if koke.point == x:
                        damage = self.power - koke.def_phy
                        koke.hp -= damage
                        koke.spread_flag = False
                        self.hp += damage
                        self.direc = trans_cell_to_direc(self,x)
                        self.nut = koke.nut
                        return True
        return False


class Rappy(Monster):
    def __init__(self,point):
        Monster.__init__(self,point,rappy_img)
        self.hp = 40
        self.hpmax = 80
        self.power = 40
        self.def_phy = 10
        self.def_mag = 0
        self.nut = 0
    def attack(self,around_dead_cell,Class):
        """ぶたに攻撃するだけじゃなくて、ガジも捕食するよ"""
        for x in around_dead_cell:
            if Class.exist_flag == True:
                if Class.point == x: # 豚が居たら
                    Class.hp -= self.power
                    self.direc = trans_cell_to_direc(self,x)
                    return True
            elif self.hp < 50:
                for gfl in gazi_family_list:
                    for indivi in gfl:
                        if indivi.point == x:
                            damage = self.power - indivi.def_phy
                            indivi.hp -= damage
                            indivi.spread_flag = False
                            self.hp += damage
                            self.direc = trans_cell_to_direc(self,x)
                            self.nut = indivi.nut
                            return True
        return False
    def walk(self,around_dead_cell):
        """Koke よりランダム要素高め。
        ガジよりもまっすぐだよ。1/5 で方向転換"""
        if (self.walk_straight(around_dead_cell) == False 
            or random.randint(0,4)==0):
            list_for_choice = []
            # 等しい確率で方向を変える
            for x in range(4):
                if around_dead_cell[x] != False:
                    list_for_choice.append(x)
            self.direc = random.choice(list_for_choice)
            # 変えた方向でもってその方向にまっすぐ歩かせる
            self.walk_straight(around_dead_cell)


    def update(self):
        around_alive_cell = around_alive_cell_make(self.point)
        around_dead_cell  = around_dead_cell_make(self.point)
        if self.attack(around_dead_cell,pig):
            pass
        else:
            self.walk(around_dead_cell)
            self.image = rappy_img[self.direc]
            
        self.image_tasks()
        self.hp_tasks(rappy_list)

class Hitodama(Monster):
    def __init__(self,point):
        Monster.__init__(self,point,hitodama_img)
        self.hp = 30
        self.hpmax = 45
        self.power =5
        self.def_phy = 0
        self.def_mag = 0
        self.nut = 0
        self.mag = 0
    
    def walk(self,around_dead_cell):
        if self.walk_straight(around_dead_cell) == False:
            list_for_choice = []
            # 等しい確率で方向を変える
            for x in range(4):
                if around_dead_cell[x] != False:
                    list_for_choice.append(x)
            self.direc = random.choice(list_for_choice)
            # 変えた方向でもってその方向にまっすぐ歩かせる
            self.walk_straight(around_dead_cell)

    def attack(self,around_dead_cell,Class):
        if Class.exist_flag == True:
            for x in around_dead_cell:
                if Class.point == x:
                    Class.hp -= self.power
                    self.direc = trans_cell_to_direc(self,x)
                    screen.blit(wave_img[0],[(self.rect[0]+Class.rect[0])/2,(self.rect[1]+Class.rect[1])/2])
                    return True
        return False
        
    def update(self):
        around_alive_cell = around_alive_cell_make(self.point)
        around_dead_cell  = around_dead_cell_make(self.point)
        if self.attack(around_dead_cell,pig):
            if self.direc == 1:
                self.image = hitodama_left
            elif self.direc == 2:
                self.image = hitodama_right
        else:
            self.walk(around_dead_cell)
            self.image = hitodama_img[self.direc]
                # 養分の移動
            for x in range(4):
                if around_alive_cell[x] != False:
                    dest_cell = cell_list[around_alive_cell[x][0]][around_alive_cell[x][1]]
                    rand = random.randint(0,9)
                    if rand>=3 and self.mag>=0:
                        dest_cell.mag += 1
                        self.mag -= 1
                    if rand< 3:
                        if dest_cell.mag > 0:
                            dest_cell.mag -= 1
                            self.mag += 1
                    
        self.image_tasks()
        self.hp_tasks(hitodama_list)

class Elice(Monster):
    def __init__(self,point):
        Monster.__init__(self,point,elice_img)
        self.hp = 60
        self.hpmax = 120
        self.power = 15
        self.def_phy = 3
        self.def_mag = 0
        self.nut = 0
        self.mag=5
        
    def walk(self,around_dead_cell):
        """Koke よりランダム要素高め。1/5 で方向転換"""
        if (self.walk_straight(around_dead_cell) == False 
            or random.randint(0,4)==0):
            list_for_choice = []
            # 等しい確率で方向を変える
            for x in range(4):
                if around_dead_cell[x] != False:
                    list_for_choice.append(x)
            self.direc = random.choice(list_for_choice)
            # 変えた方向でもってその方向にまっすぐ歩かせる
            self.walk_straight(around_dead_cell)

    def attack_close(self,around_dead_cell,Class,Monster_list):
        """ぶたに攻撃するだけじゃなくて、人魂も捕食するよ"""
        for x in around_dead_cell:
            if Class.exist_flag == True:
                if Class.point == x: # 豚が居たら
                    Class.hp -= self.power-Class.def_phy
                    self.direc = trans_cell_to_direc(self,x)
                    return True
            elif Monster_list != []:
                for mons_list in Monster_list:
                    for mons in mons_list:
                        if mons.point == x:
                            mons.hp = 0
                            if self.hpmax < self.hp:
                                self.hp += 10
                            self.hp /= 2
                            return True
        return False

    def attack_shot(self):
        if game_time%5 == 0:
            new_eshot = Eshot(self.point,self.direc)
            eshot_list.append(new_eshot)
            return True
        return False

    def update(self):
        around_alive_cell = around_alive_cell_make(self.point)
        around_dead_cell  = around_dead_cell_make(self.point)
        if self.attack_close(around_dead_cell,pig,monster_list_elice):
            pass
        elif self.attack_shot():
            pass
        else:
            self.walk(around_dead_cell)
            self.image = elice_img[self.direc]

            # 分身
        self.image_tasks()
        self.hp_tasks(elice_list)

class Eshot(Objects):
    def move_straight(self,around_dead_cell):
        if around_dead_cell[self.direc] != False:
            self.point = around_dead_cell[self.direc]
            return True
        else:
            return False

    def __init__(self,point,direc):
        Objects.__init__(self,point)
        self.point = point
        self.image = eshot_img
        self.direc = direc
        self.image_tasks()
        
    def update(self):
        around_dead_cell  = around_dead_cell_make(self.point)
        if (not self.move_straight(around_dead_cell)) or self.attack(around_dead_cell):
            eshot_list.pop(eshot_list.index(self))
        self.image_tasks()
        
    def attack(self,around_dead_cell):
        if self.point == pig.point:
            pig.hp -= 20
        for mons_list in monster_list:
            for mons in mons_list:
                if self.point == mons.point:
                    mons.hp -= 5
                    return True
        return False

class Monkey(Objects):
    def __init__(self,point):
        Objects.__init__(self,point)
        self.image = monkey_img
        self.captured_flag = False
        self.se = pygame.mixer.Sound("sound/pickaxe.ogg")

    def setting(self):
        global monkey_confirm
        if monkey_confirm == False:
            if pressed_key[K_LEFT]:
                if self.point[0] >=1:
                    self.point[0] -= 1
                    self.se.play()          
            elif pressed_key[K_RIGHT]:
                if self.point[0] < cell_x_num-1:
                    self.point[0] += 1
                    self.se.play()
            elif pressed_key[K_UP]:
                if self.point[1] >= 1:
                    self.point[1] -= 1
                    self.se.play()
            elif pressed_key[K_DOWN]:
                if self.point[1] < cell_y_num-1:
                    self.point[1] += 1
                    self.se.play()
            if pressed_key[K_SPACE] and self.point in dcl:
                monkey_confirm = True
        elif monkey_confirm == True:
            # draw_str([[u"ここでいいですか？ 'Y'es or 'N'o",(100,70)]])
            if pressed_key[K_y]:
                monkey_confirm = False
                return True
            elif pressed_key[K_n]:
                monkey_confirm = False
        self.image_tasks()
    def update(self,Class):
        if Class.point == self.point:
            pass
        if self.captured_flag == True:
            self.point = Class.prev_point # Class は勇者、勇者の前にいた場所に移動。
        self.image_tasks()

class Cell(Objects):
    def __init__(self,point):
        #Call the parent class (Sprite) constractor
        Objects.__init__(self,point)
        rand = random.randint(0,99)
        if rand < 40:
            self.nut = 1
            self.mag = 0
        elif rand < 45:
            self.nut = 2
            self.mag = 0
        elif rand < 50:
            self.nut = 0
            self.mag = 1
        else:
            self.nut = 0
            self.mag = 0
        self.alive_f = True
        alive_cell_group.add(self)
    def update(self):
        if self.nut >= self.mag:
            # nut によって画像を変更
            if self.nut == 0:
                self.image = cell_nut_img_lv0
            elif self.nut == 1:
                self.image = cell_nut_img_lv1
            elif self.nut <= lv3_line:
                self.image = cell_nut_img_lv2
            elif self.nut > lv3_line:
                self.image = cell_nut_img_lv3
        elif self.mag > 0:
            if self.mag <3:
                self.image = cell_mag_img_lv1
            else:
                self.image = cell_nut_img_lv2

        self.image_tasks()
        
class Pig(Monster):
    def __init__(self,appear_time,hp,mp,power,def_phy,def_mag,img_list):
        Monster.__init__(self,[17,0],img_list)
        self.appear_time = appear_time
        self.exist_flag = False
        self.hp = hp
        self.mp = mp
        self.power = power
        self.def_phy = def_phy
        self.def_mag = def_mag
        self.rote = []
        self.time = 0
        self.junc_list = []
        self.dead_junc_list = []
        self.list_for_stucking_dust = []
        self.exist_flag = False
        self.walk_turns = 0
        self.image_list = img_list
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.prev_point = [17,0]

    def magic_spread(self):
        for x in range(3,6):
            for y in range(3,6):
                if [x,y] not in dcl:
                    cell_list[x][y].mag += 2
                else:
                    pass
    def attack(self,around_dead_cell):
        hoge = False
        for x in around_dead_cell:
            if x != False:
                for mons_list in monster_list:
                    for mons in mons_list:
                        if mons.point == x:
                            mons.hp -= self.power
                            self.direc = trans_cell_to_direc(self,x)
                            hoge = True
        return hoge
        
    def junc_list_tasks(self,path): # junc とは、分岐点(junction)より
        if self.junc_list != []:
            for x in self.junc_list[-1][1:]: #条件部
                if x not in path: # まだ行っていないところがあったら
                    return True
            # すべて行っていたら
            self.dead_junc_list.append(self.junc_list.pop())
            self.junc_list_tasks(path)

    def bf_search(self,start, goal):
            q = [[start]]
            while len(q) > 0:        # < を > に修正 (2011/04/10)
                # dequeu
                path = q.pop(0)
                n = path[-1]
                if n == goal:
                    return path
                else:
                    for x in dead_cell_list[dcl.index(n)][1:]: # 条件部
                        if x not in path:
                            new_path = path[:]
                            new_path.append(x)
                            # enqueue
                            q.append(new_path)
        
    def search(self, path,monkey_pos):    # n は枝分かれ用
        now_pos = dead_cell_list[dcl.index(path[-1])][:] # 現在の座標の情報
        if path[-1] == monkey_pos:
            return path

        # 分岐記録
        if (len(now_pos) >= 4 or now_pos[0] == [17,0]) and now_pos not in self.junc_list :           # 一本道は[現在位置,次の位置,前の位置]の3つの情報を保持している。
            self.junc_list.append(now_pos[:])
            
        for x in now_pos[1:]: # 第0要素(現在の座標)以外
            if x in dcl and x not in path:         # x が dcl に入っていれば移動可能だよね
                path.append(x)                         # 現在座標を x に変更
                return self.search(path,monkey_pos)                      # 現在の座標を加えた path でもって再帰処理
        # 行き場がない
        self.junc_list_tasks(path) # junc_list を整理
        temp_path = self.bf_search(now_pos[0],self.junc_list[-1][0])
        path.extend(temp_path)
        return self.search(path,monkey_pos)
        
    def walk(self):
        if len(self.rote) > self.walk_turns:
            next_pos = self.rote[self.walk_turns] 
            self.direc = trans_cell_to_direc(self,next_pos)
            self.prev_point = self.point
            self.point = next_pos
            self.walk_turns += 1
        if self.point == self.rote[-1] and monkey.captured_flag == False:
            self.rote.reverse()
            self.walk_turns = 0
            pygame.mixer.music.load("sound/bgm_return.ogg")
            monkey.captured_flag = True
        elif self.point == self.rote[-1] and monkey.captured_flag == True:
            global stage_clear
            stage_clear = False
    def rooting(self,monkey_pos):
        make_dead_cell_list_relataion()
        self.rote.extend(self.search([self.point],monkey_pos)) # 座標のリストで渡すよ
        self.exist_flag = True

    def update(self):
        around_dead_cell = around_dead_cell_make(self.point)
        if self.exist_flag:
            around_alive_cell = around_alive_cell_make(self.point)
            around_dead_cell  = around_dead_cell_make(self.point)
            self.dx,self.dy = 0,0
            if self.attack(around_dead_cell):
                if  self.direc == 0:
                    self.dy = -20
                elif self.direc == 1:
                    self.dx = -20
                elif self.direc == 2:
                    self.dx =  20
                elif self.direc == 3:
                    self.dy =  20
            else:
                self.walk()
            self.image = self.image_list[self.direc]
            self.image_tasks()
        self.time += 1
        if self.hp <= 0: # 豚さん死んだら Faulse 返すよ
            self.magic_spread()
            self.exist_flag = False
            global stage_clear
            stage_clear = True
            
class Pickaxe(Objects):
    def __init__(self):
        Objects.__init__(self,[17,0])
        self.se_move = se_move
        self.se_use = se_use
        self.image = pickaxe_img
        self.image.set_colorkey((0,0,0))
        self.hori_power = ini_hori_power
    
    def use(self):
        around = dcl_around2(self.point)
        if (around[0] or around[1] or around[2] or around[3]):
            self.se_use.play()
            self.image = pickaxe2_img
            if(cell_list[self.point[0]][self.point[1]].alive_f == True):
                cell_list[self.point[0]][self.point[1]].alive_f = False
                dcl.append([self.point[0],self.point[1]])
                alive_cell_group.remove(cell_list[self.point[0]][self.point[1]])
                self.hori_power -= 1
                if cell_list[self.point[0]][self.point[1]].nut >= cell_list[self.point[0]][self.point[1]].mag:
                    if cell_list[self.point[0]][self.point[1]].nut == 0:
                        pass
                    elif cell_list[self.point[0]][self.point[1]].nut == 1: # 消した cell の栄養が 1 なら
                        new_koke = Koke(self.point[:])
                        koke_list.append(new_koke)
                    elif cell_list[self.point[0]][self.point[1]].nut <= lv3_line: # 同じく 2 なら
                        new_gazi = Gazi(self.point[:])
                        gazi_list.append(new_gazi)
                    elif cell_list[self.point[0]][self.point[1]].nut > lv3_line: # lv3_line 以上なら
                        new_rappy = Rappy(self.point[:])
                        rappy_list.append(new_rappy)
                else:
                    if cell_list[self.point[0]][self.point[1]].mag > 1:
                        new_hitodama = Hitodama(self.point[:])
                        hitodama_list.append(new_hitodama)
                    else:
                        new_elice = Elice(self.point[:])
                        elice_list.append(new_elice)
            elif monster_list != []:
                for mons_list in monster_list:
                    for x in mons_list:
                        if x.point == self.point:
                            x.hp -= 5

    def update(self):
        self.image = pickaxe_img
        #Figure out if it was an arrow key.
        #If so adjust velocity.
        if pressed_key[K_LEFT]:
            if self.point[0] >=1:
                self.point[0] -= 1
                self.se_move.play()          
        elif pressed_key[K_RIGHT]:
            if self.point[0] < cell_x_num-1:
                self.point[0] += 1
                self.se_move.play()
        elif pressed_key[K_UP]:
            if self.point[1] >= 1:
                self.point[1] -= 1
                self.se_move.play()
        elif pressed_key[K_DOWN]:
            if self.point[1] < cell_y_num-1:
                self.point[1] += 1
                self.se_move.play()
        if pressed_key[K_SPACE] and self.hori_power>0:
            self.use()
        self.image_tasks()
#-----------------------------------------
#----------- Pre Settings ----------------
#-----------------------------------------
# Make cell_list
for i in range (cell_x_num):
    cell_list_y = []
    for j in range (cell_y_num):
        cell_list_y.append(Cell((i,j)))
    cell_list.append(cell_list_y)
for x in [[17,0],[17,1]]:
    cell_list[x[0]][x[1]].alive_f = False
    dcl.append(x[:])
    alive_cell_group.remove(cell_list[x[0]][x[1]])

# Class
pickaxe = Pickaxe()
butasan_list=[Pig(500,5000,150,5,5,5,butasan_img),Pig(150,5000,0,10,10,10,butasan2_img)]

#-----------------------------------------
#------------- Functions -----------------
#-----------------------------------------
def make_dead_cell_list_relataion():
    for x in dcl:
        dead_cell_list.append([x])
    for x in range(len(dcl)):        
        s_dcl = dcl[x]
        if [s_dcl[0],s_dcl[1]+1] in dcl: # Down
            dead_cell_list[x].append([s_dcl[0],s_dcl[1]+1])
        if [s_dcl[0]+1,s_dcl[1]] in dcl: # Right
            dead_cell_list[x].append([s_dcl[0]+1,s_dcl[1]])
        if [s_dcl[0]-1,s_dcl[1]] in dcl: # Left
            dead_cell_list[x].append([s_dcl[0]-1,s_dcl[1]])
        if [s_dcl[0],s_dcl[1]-1] in dcl: # Up
            dead_cell_list[x].append([s_dcl[0],s_dcl[1]-1])


def around_dead_cell_make(cell):
    around = dcl_around2(cell)
    list = [False]*4
    if around[0] == True:
        list[0] = [cell[0],cell[1]-1]
    if around[1] == True:
        list[1] = [cell[0]-1,cell[1]]
    if around[2] == True:
        list[2] = [cell[0]+1,cell[1]]
    if around[3] == True:
        list[3] = [cell[0],cell[1]+1]
    return list

def around_alive_cell_make(cell):
    around = dcl_around2(cell)
    list = [False]*4
    if (cell[1]>0 and around[0] == False):
        list[0] = [cell[0],cell[1]-1]
    if (cell[0]>0 and around[1] == False):
        list[1] = [cell[0]-1,cell[1]]
    if (cell[0]<cell_x_num-1 and around[2] == False):
        list[2] = [cell[0]+1,cell[1]]
    if (cell[1]<cell_y_num-1 and around[3] == False):
        list[3] = [cell[0],cell[1]+1]
    return list

def trans_cell_to_direc(Class,cell2): # 中心、比較するセル
    point = Class.point
    if ([point[0],point[1]-1] == cell2): # 上向き
        return 0
    elif ([point[0]-1,point[1]] == cell2): # 左向き
        return 1
    elif ([point[0]+1,point[1]] == cell2): # 右向き
        return 2
    elif ([point[0],point[1]+1] == cell2): # 下向き
        return 3
    else:
        return 0

def do_update(List):
    if len(List) > 0:
        for Class in List:
            Class.update()

def do_draw(List):
    if len(List) > 0:
        for Class in List:
            screen.blit(Class.image,Class.rect)

def draw_str(list):
    for x in list:
        screen.blit(font_game.render(x[0],False,white),x[1])

def draw_str_game():
    Pig_hp_txt = "HP:"+str(pig.hp)
    Hori_power_txt="Count"+str(pickaxe.hori_power)
    Now_pickaxe = "Coordination"+str(pickaxe.point)
    draw_str([[Pig_hp_txt,(0,0)],[Hori_power_txt,(0,35)],[Now_pickaxe,(0,70)]])
    if monkey_confirm == True:
        draw_str([["Are you ready? 'Y'es or 'N'o",(200,100)]])

#-----------------------------------------
#----------- Main Function ---------------
#-----------------------------------------
while done == False:
    # Clear the screen
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == KEYDOWN:
            if event.key == K_RETURN and game_cond == "OP":
                pig = butasan_list[0]
                pygame.mixer.music.load("sound/bgm_main.ogg")
                game_cond = "GAME"
            elif event.key == K_RETURN and game_cond=="NT":
                now_stage += 1
                pig = butasan_list[now_stage-1]
                monkey_set_flag = False
                monkey = False
                stage_clear = None
                dead_cell_list = []
                pygame.mixer.music.load("bgm_main.ogg")
                game_cond = "GAME"

            elif event.key == K_RETURN and game_cond =="GAME":
                monkey = Monkey([17,0]) # 初期座標
                monkey_set_flag = not monkey_set_flag

            if event.key == K_ESCAPE:
                done = True

    if stage_clear == True:
        if now_stage < Max_stage:
            game_cond = "NT"
        elif now_stage == Max_stage:
            screen.blit(stage_clear2_img,(0,0))
    if stage_clear == False:
        screen.blit(gameover_img,(0,0))
    # Receive condition of keys
    pressed_key = pygame.key.get_pressed()
    if game_cond == "OP":
        screen.blit(opening_img,(0,0))
    elif game_cond =="NT":
        screen.blit(stage_clear_img,(0,0))
    elif game_cond == "GAME" and stage_clear == None:
        if monkey_set_flag == True:
            if monkey.setting():
                print(("monkey.point",monkey.point))
                pig.rooting(monkey.point)
                pig.exist_flag = True
                monkey_set_flag = None
        # Updates
        if monkey_set_flag != True:
            pickaxe.update()
        if monkey != False:
            monkey.update(pig)
        for i in range (len(cell_list)):
            for j in range (len(cell_list[i])):
                cell_list[i][j].update()
        if game_time % 3 == 0:
            do_update(koke_list)
            do_update(gazi_list)
            do_update(sanagi_list)
            do_update(fly_list)
            do_update(rappy_list)
            do_update(hitodama_list)
            do_update(elice_list)
            do_update(eshot_list)
            pig.update()
        # Draw back_ground
        screen.blit(back_ground,(0,0))
        # Draw the all sprites
        do_draw(koke_list)
        do_draw(gazi_list)
        do_draw(sanagi_list)
        do_draw(fly_list)
        do_draw(rappy_list)
        do_draw(hitodama_list)
        do_draw(elice_list)
        do_draw(eshot_list)
        alive_cell_group.draw(screen)
        if pig.exist_flag == True:
            screen.blit(pig.image,pig.rect)
        if monkey_set_flag != True:
            screen.blit(pickaxe.image,pickaxe.rect)
        if monkey_set_flag != False:
            screen.blit(monkey.image,monkey.rect)
        draw_str_game()
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
        game_time += 1
    # Limit to 50 frames per second
    clock.tick(15)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
pygame.quit()
