from operator import itemgetter
import win32api as api
import pygame as pg
import numpy as np
from numba import njit
from time import sleep
import random,os
import sqlite3 as sql
def main(name,table):
    running = True
    pg.init()
    screen = pg.display.set_mode((800,600))
    player_name = name
    vocab = []
    db = sql.connect(r"D:\PEEKZ\Documents\ปี 1 เทอม 2\งาน ED251007 S.2\Project\vocab.db")
    cmd = f"SELECT * FROM {table}"
    for i in db.execute(cmd):
        vocab.append([i[0],i[1]])
    question = random.choice(vocab)
    horizontal = 120 #horizontal resolution
    vertical = 100 #vertical resolution/
    size = 25
    maph = np.random.choice([0,0,1,0],(size,size))
    end_posx = random.randint(-21,21)
    end_posy = random.randint(-21,21)
    global timers
    timers = 120.00
    get_answer = ''

    light_gray = (200,200,200)
    red = (255,0,0)
    green = (0,255,0)
    color = light_gray
    game_font = pg.font.Font(r"D:\PEEKZ\Documents\ปี 1 เทอม 2\งาน ED251007 S.2\Project\5011_thE_Little_Uki_noworry.ttf",32)
    font_vocab = pg.font.Font(r"D:\PEEKZ\Documents\ปี 1 เทอม 2\งาน ED251007 S.2\Project\5011_thE_Little_Uki_noworry.ttf",64)

    mod = horizontal/60 #scaling factor (60° fov)
    posx, posy, rot = 0, 0, 0
    frame = np.random.uniform(0,0, (horizontal, vertical*2, 3))
    sky = pg.image.load(r"D:\PEEKZ\Documents\ปี 1 เทอม 2\งาน ED251007 S.2\Project\sky.jpg")
    sky = pg.surfarray.array3d(pg.transform.scale(sky, (360, vertical*2)))/255
    floor = pg.surfarray.array3d(pg.image.load(r"D:\PEEKZ\Documents\ปี 1 เทอม 2\งาน ED251007 S.2\Project\snow_floor2.jpg"))/255
    wall = pg.surfarray.array3d(pg.image.load(r"D:\PEEKZ\Documents\ปี 1 เทอม 2\งาน ED251007 S.2\Project\wall2.jpg"))/255
    bright,bright_start,loadingX,loadingY = 0,0,380,300
    timer_start = 0.00
    time_delay_end,time_delay_end2 = 0,0
    time_delay = 0.01
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type ==pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                timer_start = 000.01
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                bright_start = 1
        bright += bright_start
        sleep(time_delay)
        if bright == 100:
            time_delay = 0
            loadingY = 0
            loadingX = 0
            bright = 255
            bright_start = 0

        frame = new_frame(posx, posy, rot, frame, sky, floor, horizontal, vertical, mod,size,maph,wall,end_posx,end_posy)

        surf = pg.surfarray.make_surface(frame*255)
        surf = pg.transform.scale(surf, (800, 600))
        pg.display.set_caption("THE PROJECT")

        text_load = game_font.render(f"{bright} %",True,light_gray)
        text_posxy = game_font.render(f"x:{int(posx)} y:{int(posy)}",True,light_gray)
        text_time = game_font.render("{:.2f} second".format(timers),True,light_gray)
        text_xy = game_font.render(f"x:{end_posx} y:{end_posy}",True,light_gray)

        time_delay_end += time_delay_end2
        if time_delay_end >= 100:
            running = False

        if int(posx) == end_posx and int(posy) == end_posy:
            center =  text_question.get_rect(center=(800/2,200))
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type ==pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    break
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        get_answer = get_answer[:-1]
                    else:
                        get_answer += event.unicode
                        if get_answer in question:
                            color = green
                            cmd = """INSERT INTO score (player_name,player_time)
                                    VALUES ("{}","{:.2f}")""".format(player_name,120.00-timers)
                            db.execute(cmd)
                            db.commit()
                            os.system("cls")
                            print("\n"*4)
                            print(f"\t\t\tYour name: {name}".rjust(35),f"Your questions: {question[0]}".rjust(40),f"Your Time: {120-timers:.2f} second".rjust(40),
                            f"Your Position X:{end_posx} Y:{end_posy}".rjust(40))
                            No = []
                            for i in db.execute("SELECT * FROM score"):
                                i = list(i)
                                i[1] = float(i[1])
                                No.append(i)
                                No = sorted(No,key = itemgetter(1))
                            print("\n")
                            print("\u001b[43;1m{}Your top: {} \u001b[0m".format("\t"*8,No.index([f"{name}",float(f"{float(120-timers):.2f}")])+1))
                            print(" ")
                            print("\u001b[44;1m{}{:<27}{:<27}{:<9}\n\u001b[0m".format("\t"*8,"No.","Name","Time"))

                            for i in range(len(No)):
                            
                                if i >= 0 and i <= 2 and No.index([f"{name}",float(f"{float(120-timers):.2f}")]) >=3:
                                    print("\u001b[45;1m{} {:<20} {:<30} {:<10}\u001b[0m".format("\t"*8,i+1,No[i][0],No[i][1]))

                                elif No.index([f"{name}",float(f"{float(120-timers):.2f}")]) == i:
                                    print("\u001b[41;1m{} {:<20} {:<30} {:<10}\u001b[0m".format("\t"*8,i+1,No[i][0],No[i][1]))
                                else:
                                    print("{} {:<20} {:<30} {:<10}".format("\t"*8,i+1,No[i][0],No[i][1]))

                            time_delay_end2 = 1
                            
                        else:
                            color = red
                        
        else:
            center = (0,-100)

        text_question = font_vocab.render(f" {question[0]} ",True,color)
        text_answer = game_font.render(f"{get_answer}",False,color)
        timers -= timer_start

        if timers <= 0.00:
            break

        surf.blit(text_answer,(380,380))
        surf.blit(text_question,center)
        surf.blit(text_posxy,(350,10))
        surf.blit(text_time,(320,490))
        surf.blit(text_xy,(30,30))

        surf.blit(text_load,(loadingX,loadingY))
        screen.blit(surf, (0,0))
        pg.display.update()
        
        posx, posy, rot = movement(posx, posy, rot, pg.key.get_pressed())

def movement(posx, posy, rot, keys):
    if keys[pg.K_LEFT] or keys[ord('a')]:
        rot = rot - 0.025

    if keys[pg.K_RIGHT] or keys[ord('d')]:
        rot = rot + 0.025
        
    if keys[pg.K_UP] or keys[ord('w')]:
        posx, posy = posx + np.cos(rot)*0.02,  posy + np.sin(rot)*0.02

    if keys[pg.K_DOWN] or keys[ord('s')]:
        posx, posy = posx - np.cos(rot)*0.02,  posy - np.sin(rot)*0.02
    
    if keys[pg.K_UP] or keys[ord('w')] and keys[pg.K_LSHIFT]:
        posx, posy = posx + np.cos(rot)*0.024,  posy + np.sin(rot)*0.024

    return posx, posy, rot

@njit()
def new_frame(posx, posy, rot, frame, sky, floor, horizontal, vertical, mod,size,maph,wall,end_posx,end_posy):
    
    for i in range(horizontal): #0 - 120
        rot_i = rot + np.deg2rad(i/mod - 30) # หาความกว้างของมุมมองของผู้เล่น i หารด้วย mod - กับครึ่งนึงของ mod จะได้ fov 60 พอดี (fov horizontal)
        # ค่าที่ใช้ในฟังก์ชันตรีโกณนั้นต้องมีหน่วยเป็นเรเดียน ซึ่งถ้าจะใช้มุมในหน่วยองศาก็ต้องมาคูณด้วย π/180
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i/mod - 30)) # ส่วนเกินขอบเขตของระยะสายตาสูตรจาก horizontal 60 fov 
        frame[i][:] = sky[int(np.rad2deg(rot_i)%360)][:]
        x,y = posx,posy
        while maph[int(x)%size-1][int(y)%size-1] == 0: # '== 0' = เช็กว่ามีการชนกำแพงมั้ย หากชน ค่าจะกลายเป็น False 
            x,y = x+0.01*cos,y+0.01*sin # 0.01*cos , 0.01*sin = 'เพื่อที่จะคำนวนได้เร็วขึ้นเพราะมีค่าที่น้อยลง' 
        n = abs((x-posx)/cos) # slow ขาของเราลดลง ลดความเร็วของขาเราลงเมื่ออยู่ใกล้กำแพง
        h = int(vertical/(n*cos2 + 0.01)) # '0.01' = 'ความหนา ของกำแพง'

        xx = int(x*2%1*99) # สร้างค่าความกว้างขอแกน x
        if x%1 < 0.02 or x%1 > 0.98: # '*2' = สร้างขนาดให้เท่ากับแกน y and x, array two dimensions 
            xx = int(y*2%1*99) # สร้างค่าความสูงของแกน y 
        yy = np.linspace(0,198,h*2)%99 # '0' => ตั้งที่พิกัดเริ่มต้น y = 0 , '198' = ความยาวของแกนสุดท้ายของ y , 
        #'%99' = ค่าความละเอียดของรูปผ่าน โดยผ่านค่าที 1:1 pixel

        shade = 0.3 + 0.7*(h/vertical) # '0.3' = fade in shader , '0.7(h/vertical)' = fade out shader gradient 
        if shade > 1:
            shade = 1
            
        for k in range(h*2):
            
            if vertical-h+k >= 0 and vertical-h+k < 2*vertical: # ไม่อยากให้เกินขอบเขตของท้องฟ้า
                frame[i][vertical-h+k] = shade*wall[xx][int(yy[k])] # int(yy[k]) = เพื่อจะให้ row ภาพ มีขนาดตามแกน yy ส่วน k ให้ column มีขนาดที่ขนานกับแกน x

        for j in range(vertical-h):
            n = (vertical/(vertical-j))/cos2 #หาค่าความยาวของด้าน fov vertica ตั้งแต่ 0.01 => 1 ได้ค่าเท่ากับ vertical พอดีนั่นคือ 100
            x, y = posx + cos*n, posy + sin*n # หาองศาของเส้นรังสีที่มันกระทบเข้ากับดวงตา ตั้งแต่ -30 => 30
            xx, yy = int(x*2%1*99), int(y*2%1*99) # ส่วนของการสร้างภาพในแนวนอน และ แนวตั้ง 

            shade = 0.2 + 0.8*(j/vertical)

            frame[i][vertical*2-j-1] = shade*floor[xx][yy] # ขนาดของarrayพื้นมีค่าตามตำแหน่งที่คำนวนไว้
            if int(x) == end_posx and int(y) == end_posy : # สร้างทางออกเท่ากับตำแหน่งที่กำหนดไว้
                ee = j/(10*vertical)  # สร้างความโปร่งของทางออก
                frame[i][j:2*vertical-j] = (ee*np.ones(3)+frame[i][j:2*vertical-j])/(1+ee) # สร้างสี่เหลี่ยมสีขาวกำหนดความเข้มของสีตามการหารของตัวแปร ee
    return frame

def ready():
    color = ("\u001b[41;1m","\u001b[41;1m","\u001b[42;1m","\u001b[43;1m","\u001b[44;1m","\u001b[45;1m","\u001b[46;1m")
    text_start = " W E L C O M E  T O  M Y  G A M E "
    particle = "0"*30
    os.system("cls")
    print("\n"*5)
    for i in particle:
        print("\t"*11+f"{random.choice(color)}{i}\u001b[0m",end="",flush=True)
        sleep(0.02)
    print("\n")
    for i in "\t"*10+text_start:
        print(f"\u001b[44;1m{i}\u001b[0m",end="",flush=True)
        sleep(0.08)
    print("\n"*8)
    print("\u001b[37;1m► click to start ◄".rjust(113))
    while True:
        lc1 = api.GetAsyncKeyState(0x01)
        if lc1 < 0:
            sleep(0.3)
            choice()
            break

def choice():
    db = sql.connect(r"D:\PEEKZ\Documents\ปี 1 เทอม 2\งาน ED251007 S.2\Project\vocab.db")
    os.system("cls")
    print("\n"*15)
    print("\u001b[31;1m {:^200}\n\n\u001b[32;1m{:^200}\n\n\u001b[34;1m {:^200}\u001b[0m ".format("Click to start the game","Press [C] view score","Press [E] Exits"))
    while True:
        lc = api.GetAsyncKeyState(0x01)
        c = api.GetAsyncKeyState(0x43)
        z = api.GetAsyncKeyState(0x5A)
        e = api.GetAsyncKeyState(0x45)
        d = api.GetAsyncKeyState(0x44)
        if lc < 0:
    
            os.system("cls")
            print("\n"*15)
            try:
                print("\u001b[37;1mPress 1 animals\t\t\tPress 2 fruit\u001b[0m".rjust(113))
                print("\n\n")
                v_type = int(input(":".rjust(95)))
                if v_type == 1:
                    table = "vocab"
                elif v_type == 2:
                    table = "vocab_fruit"
                else:
                    print("\n")
                    print("\u001b[31;1mPlease select only 1 or 2.\u001b[0m".rjust(122))
                    sleep(2)
                    choice()
            except ValueError:
                print("\n")
                print("\u001b[31;1mPlease select your number.\u001b[0m".rjust(122))
                sleep(2)
                choice()
            os.system("cls")
            print("\n"*15)
            name = input("YOUR NAME: ".rjust(95))
            for i in db.execute("SELECT * FROM score"):
                if name == i[0]:
                    print("\n")
                    print("\u001b[31;1mYour name is already exists.\u001b[0m".rjust(122))
                    sleep(2)
                    choice()
                else:
                    pass
            os.system("cls")
            print("{}{:^202}\n\n{:^202}\n\n{:^202}\n\n\n".format("\n"*10,"\u001b[36;1mW A S D \u001b[37;1m=  Walk","\u001b[36;1mL SHIFT + W  \u001b[37;1m=  Speed","\u001b[36;1mSPACEBAR  \u001b[37;1m=  start timer"))
            sleep(3)
            print("\u001b[46;1m Have fun :) \u001b[0m".rjust(111))
            main(name,table)
            break
        elif c < 0:

            os.system("cls")
            # db = sql.connect(r"D:\PEEKZ\Documents\ปี 1 เทอม 2\งาน ED251007 S.2\Project\vocab.db")
            No = []
            for i in db.execute("SELECT * FROM score"):
                i = list(i)
                i[1] = float(i[1])
                No.append(i)
                No = sorted(No,key = itemgetter(1))
            print("\n\n")
            # print("\u001b[43;1m{}Your rank: {} \u001b[0m".format("\t"*8,No.index([f"{name}",float(f"{float(timers):.2f}")])+1))
            print("\u001b[44;1m{}{:<27}{:<27}{:<9}\n\u001b[0m".format("\t"*8,"No.","Name","Time"))

            for i in range(len(No)):
            
                if i >= 0 and i <= 2 :
                    print("\u001b[45;1m{} {:<20} {:<30} {:<10}\u001b[0m".format("\t"*8,i+1,No[i][0],No[i][1]))
                else:
                    print("{} {:<20} {:<30} {:<10}".format("\t"*8,i+1,No[i][0],No[i][1]))
            print("\n\n")
            print("\u001b[31;1m {:^189}\n\n\u001b[32;1m{:^190}\n\n\u001b[34;1m {:^188}\n".format("Click to start the game","Press [C] View score","Press [E] Exits"))
            print("\u001b[37;1m[D] Delete all score\u001b[0m".rjust(116))
        elif z < 0:
            choice()
        elif e < 0:
            exit()
        elif d < 0:
            db.execute("DELETE FROM score")
            db.commit()
            os.system("cls")
            print("\n"*15)
            print("\u001b[37;1mDelete all done!\u001b[0m".rjust(115))
            sleep(1.5)
            choice()
if __name__ == '__main__':
    main()
    pg.quit()