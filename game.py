import pygame
import time
import random
from settings import *
from background import Background
from hand import Hand
from hand_tracking import HandTracking
import cv2
import ui
import image
import numpy as np

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.background = Background()

        # Load camera
        self.cap = cv2.VideoCapture(0)


        self.brush_right_status = "None"
        self.brush_left_status = "None"


        dsize = (400, 400)
        self.Overlayer = []
        self.Overlayer.append(image.load("Assets/Rock.png", size=dsize, convert="default"))
        self.Overlayer.append(image.load("Assets/Paper.jpg", size=dsize, convert="default"))
        self.Overlayer.append(image.load("Assets/Scissor.png", size=dsize, convert="default"))
        self.Overlayer.append(image.load("Assets/nothing.png", size=dsize, convert="default"))

        self.start_time = time.time()
        self.time_count = time.time()
        self.player_choice = 3
        self.computer_choice = 3
        self.count = 0 #count turn
        self.c_win = 0 
        self.c_lose = 0

        self.H=[]
        self.S=[]
        self.V=[]

    def reset_game1(self): 
        for i in range (SCREEN_WIDTH):
            for j in range(SCREEN_HEIGHT):
                    self.background.image.set_at((i,j), (255,255,255))
        self.hand_tracking = HandTracking()
        self.hand = Hand()
        self.side = 0

    def update_game1(self):

        _, self.frame = self.cap.read()
        self.frame = self.hand_tracking.scan_hands(self.frame)

        self.background.draw(self.surface)

        if (self.hand_tracking.results.multi_hand_landmarks):
            for i in range (len(self.hand_tracking.results.multi_hand_landmarks)):
                if self.hand_tracking.results.multi_handedness[i].classification[0].label=="Right":
                    x1 = self.hand_tracking.right_hand_pos1[0]
                    y1 = self.hand_tracking.right_hand_pos1[1]
                    x2 = self.hand_tracking.right_hand_pos2[0]
                    y2 = self.hand_tracking.right_hand_pos2[1]
                    x3 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[12].x
                    y3 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[12].y
                    x4 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[9].x
                    y4 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[9].y
                    x5 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[16].x
                    y5 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[16].y
                    x6 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[20].x
                    y6 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[20].y
                    if y3 > y4:
                        if self.brush_right_status == "Draw" or self.brush_right_status == "Continue_Draw":
                            self.brush_right_status = "Continue_Draw"
                        else:
                            self.brush_right_status = "Draw"
                    elif y5<y4 and y6<y4:
                        if self.brush_right_status == "Eraser" or self.brush_right_status == "Continue_Eraser":
                            self.brush_right_status = "Continue_Eraser"
                        else:
                            self.brush_right_status = "Eraser"
                    else:
                        self.brush_right_status = "None"
                    if self.brush_right_status == "Draw":
                        image.draw(self.surface, self.hand.image_smaller_pen_right, self.hand_tracking.right_hand_pos2, pos_mode="down_left")
                        for k in range (-10,11):
                            for j in range(-10,11):
                                if (k**2+j**2<101):
                                    self.background.image.set_at((x2+k,y2+j), (0,0,0))
                    elif self.brush_right_status == "Continue_Draw":
                        image.draw(self.surface, self.hand.image_smaller_pen_right, self.hand_tracking.right_hand_pos2, pos_mode="down_left")
                        for k in range (-10,11):
                            for j in range(-10,11):
                                if (k**2+j**2<101):
                                    self.background.image.set_at((x2+k,y2+j), (0,0,0))
                        if x1<x2:
                            for la in range (x2-x1+1):
                                for j in range(-10,11):
                                    self.background.image.set_at((x1+la,la*y2//(x2-x1)+(x2-x1-la)*y1//(x2-x1)+j), (0,0,0))
                        elif x1>x2:
                            for la in range (x1-x2+1):
                                for j in range(-10,11):
                                    self.background.image.set_at((x2+la,la*y1//(x1-x2)+(x1-x2-la)*y2//(x1-x2)+j), (0,0,0))
                        if y1<y2:
                            for la in range (y2-y1+1):
                                for j in range(-10,11):
                                    self.background.image.set_at((la*x2//(y2-y1)+(y2-y1-la)*x1//(y2-y1)+j, y1+la), (0,0,0))
                        elif y1>y2:
                            for la in range (y1-y2+1):
                                for j in range(-10,11):
                                    self.background.image.set_at((la*x1//(y1-y2)+(y1-y2-la)*x2//(y1-y2)+j, y2+la), (0,0,0))
                    elif self.brush_right_status == "Eraser":
                        image.draw(self.surface, self.hand.orig_image_eraser_right, self.hand_tracking.right_hand_pos2, pos_mode="top_left")
                        for k in range (-100,101):
                            for j in range(-100,101):
                                if (k**2+j**2<10001):
                                    self.background.image.set_at((x2+k,y2+j), (255,255,255))
                    elif self.brush_right_status == "Continue_Eraser":  
                        image.draw(self.surface, self.hand.image_smaller_eraser_right, self.hand_tracking.right_hand_pos2, pos_mode="top_left")
                        for k in range (-100,101):
                            for j in range(-100,101):
                                if (k**2+j**2<10001):
                                    self.background.image.set_at((x2+k,y2+j), (255,255,255))
                        if x1<x2:
                            for la in range (x2-x1+1):
                                for j in range(-100,101):
                                    self.background.image.set_at((x1+la,la*y2//(x2-x1)+(x2-x1-la)*y1//(x2-x1)+j), (255,255,255))
                        elif x1>x2:
                            for la in range (x1-x2+1):
                                for j in range(-100,101):
                                    self.background.image.set_at((x2+la,la*y1//(x1-x2)+(x1-x2-la)*y2//(x1-x2)+j), (255,255,255))
                        if y1<y2:
                            for la in range (y2-y1+1):
                                for j in range(-100,101):
                                    self.background.image.set_at((la*x2//(y2-y1)+(y2-y1-la)*x1//(y2-y1)+j, y1+la), (255,255,255))
                        elif y1>y2:
                            for la in range (y1-y2+1):
                                for j in range(-100,101):
                                    self.background.image.set_at((la*x1//(y1-y2)+(y1-y2-la)*x2//(y1-y2)+j, y2+la), (255,255,255))
                    else :
                        image.draw(self.surface, self.hand.orig_image_pen_right, self.hand_tracking.right_hand_pos2, pos_mode="down_left")
                if self.hand_tracking.results.multi_handedness[i].classification[0].label=="Left":
                    x1 = self.hand_tracking.left_hand_pos1[0]
                    y1 = self.hand_tracking.left_hand_pos1[1]
                    x2 = self.hand_tracking.left_hand_pos2[0]
                    y2 = self.hand_tracking.left_hand_pos2[1]
                    x3 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[12].x
                    y3 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[12].y
                    x4 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[9].x
                    y4 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[9].y
                    x5 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[16].x
                    y5 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[16].y
                    x6 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[20].x
                    y6 = self.hand_tracking.results.multi_hand_landmarks[i].landmark[20].y
                    if y3 > y4:
                        if self.brush_left_status == "Draw" or self.brush_left_status == "Continue_Draw":
                            self.brush_left_status = "Continue_Draw"
                        else:
                            self.brush_left_status = "Draw"
                    elif y5<y4 and y6<y4:
                        if self.brush_left_status == "Eraser" or self.brush_left_status == "Continue_Eraser":
                            self.brush_left_status = "Continue_Eraser"
                        else:
                            self.brush_left_status = "Eraser"
                    else:
                        self.brush_left_status = "None"
                    if self.brush_left_status == "Draw":
                        image.draw(self.surface, self.hand.image_smaller_pen_left, self.hand_tracking.left_hand_pos2, pos_mode="down_right")
                        for k in range (-10,11):
                            for j in range(-10,11):
                                if (k**2+j**2<101):
                                    self.background.image.set_at((x2+k,y2+j), (0,0,0))
                    elif self.brush_left_status == "Continue_Draw":
                        image.draw(self.surface, self.hand.image_smaller_pen_left, self.hand_tracking.left_hand_pos2, pos_mode="down_right")
                        for k in range (-10,11):
                            for j in range(-10,11):
                                if (k**2+j**2<101):
                                    self.background.image.set_at((x2+k,y2+j), (0,0,0))
                        if x1<x2:
                            for la in range (x2-x1+1):
                                for j in range(-10,11):
                                    self.background.image.set_at((x1+la,la*y2//(x2-x1)+(x2-x1-la)*y1//(x2-x1)+j), (0,0,0))
                        elif x1>x2:
                            for la in range (x1-x2+1):
                                for j in range(-10,11):
                                    self.background.image.set_at((x2+la,la*y1//(x1-x2)+(x1-x2-la)*y2//(x1-x2)+j), (0,0,0))
                        if y1<y2:
                            for la in range (y2-y1+1):
                                for j in range(-10,11):
                                    self.background.image.set_at((la*x2//(y2-y1)+(y2-y1-la)*x1//(y2-y1)+j, y1+la), (0,0,0))
                        elif y1>y2:
                            for la in range (y1-y2+1):
                                for j in range(-10,11):
                                    self.background.image.set_at((la*x1//(y1-y2)+(y1-y2-la)*x2//(y1-y2)+j, y2+la), (0,0,0))
                    elif self.brush_left_status == "Eraser":
                        image.draw(self.surface, self.hand.orig_image_eraser_left, self.hand_tracking.left_hand_pos2, pos_mode="top_right")
                        for k in range (-50,51):
                            for j in range(-50,51):
                                if (k**2+j**2<2501):
                                    self.background.image.set_at((x2+k,y2+j), (255,255,255))
                    elif self.brush_left_status == "Continue_Eraser":  
                        image.draw(self.surface, self.hand.image_smaller_eraser_left, self.hand_tracking.left_hand_pos2, pos_mode="top_right")
                        for k in range (-50,51):
                            for j in range(-50,51):
                                if (k**2+j**2<2501):
                                    self.background.image.set_at((x2+k,y2+j), (255,255,255))
                        if x1<x2:
                            for la in range (x2-x1+1):
                                for j in range(-50,51):
                                    self.background.image.set_at((x1+la,la*y2//(x2-x1)+(x2-x1-la)*y1//(x2-x1)+j), (255,255,255))
                        elif x1>x2:
                            for la in range (x1-x2+1):
                                for j in range(-50,51):
                                    self.background.image.set_at((x2+la,la*y1//(x1-x2)+(x1-x2-la)*y2//(x1-x2)+j), (255,255,255))
                        if y1<y2:
                            for la in range (y2-y1+1):
                                for j in range(-50,51):
                                    self.background.image.set_at((la*x2//(y2-y1)+(y2-y1-la)*x1//(y2-y1)+j, y1+la), (255,255,255))
                        elif y1>y2:
                            for la in range (y1-y2+1):
                                for j in range(-50,51):
                                    self.background.image.set_at((la*x1//(y1-y2)+(y1-y2-la)*x2//(y1-y2)+j, y2+la), (255,255,255))
                    else :
                        image.draw(self.surface, self.hand.orig_image_pen_left, self.hand_tracking.left_hand_pos2, pos_mode="down_right")
                    
        if ui.button(self.surface, 0, "Menu", pos_x = SCREEN_WIDTH-150, b_size = (150, 50)):
            return "menu"
        if ui.button(self.surface, 0, "Help", pos_x = 0, b_size = (150, 50)):
            return "help_game1"
        if ui.button(self.surface, SCREEN_HEIGHT-50, "Blank", pos_x = SCREEN_WIDTH-150, b_size = (150, 50)):
            for i in range (SCREEN_WIDTH):
                for j in range(SCREEN_HEIGHT):
                    self.background.image.set_at((i,j), (255,255,255))
         
        cv2.imshow("Frame", self.frame)
        cv2.waitKey(1)

    def reset_help_game1(self): 
        for i in range (SCREEN_WIDTH):
            for j in range(SCREEN_HEIGHT):
                    self.background.image.set_at((i,j), (0,0,0))

    def update_help_game1(self): 
        self.background.draw(self.surface)
        if ui.button(self.surface, 0, "<- Return", pos_x = 0, b_size = (250, 50)):
            return "game1"
        ui.draw_text(self.surface, "Use two fingers to point", (SCREEN_WIDTH//2,SCREEN_HEIGHT//2-100), (255,255,255), pos_mode = "center")
        ui.draw_text(self.surface, "Use one finger to draw", (SCREEN_WIDTH//2,SCREEN_HEIGHT//2), (255,255,255), pos_mode = "center")
        ui.draw_text(self.surface, "Open your hand to erase", (SCREEN_WIDTH//2,SCREEN_HEIGHT//2+100), (255,255,255), pos_mode = "center")


    def reset_game3(self): 
        for i in range (SCREEN_WIDTH):
            for j in range(SCREEN_HEIGHT):
                    self.background.image.set_at((i,j), (0,0,0))
        self.hand_tracking = HandTracking()
        self.hand = Hand()
        self.side = 0

        self.start_time = time.time()
        self.time_count = time.time()
        self.player_choice = 3
        self.computer_choice = 3
        self.count = 0 #count turn
        self.c_win = 0 
        self.c_lose = 0

    def update_game3(self):

        _, self.frame = self.cap.read()
        self.frame = self.hand_tracking.scan_hands(self.frame)

        self.background.draw(self.surface)

        ui.draw_text(self.surface, "Round "+str(self.count), (SCREEN_WIDTH//2,50), (255,255,255), pos_mode="center")
        if self.c_win==3:
            ui.draw_text(self.surface, "You win!!! :))))", (SCREEN_WIDTH//2-100, SCREEN_HEIGHT-100), (255,255,255), pos_mode="center")
            if ui.button(self.surface, SCREEN_HEIGHT-100, "Restart", pos_x = SCREEN_WIDTH//2+100, b_size = (200, 50)):
                return "game3"
        elif self.c_lose==3:
            ui.draw_text(self.surface, "You lose :(((", (SCREEN_WIDTH//2-100, SCREEN_HEIGHT-100), (255,255,255), pos_mode="center") 
            if ui.button(self.surface, SCREEN_HEIGHT-100, "Restart", pos_x = SCREEN_WIDTH//2+100, b_size = (200, 50)):
                return "game3" 
        
        ui.draw_text(self.surface, "Score:", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50), (255,255,255),pos_mode="center")
        ui.draw_text(self.surface, str(self.c_win), (SCREEN_WIDTH//2-50, SCREEN_HEIGHT//2), (255,255,255),pos_mode="center")
        ui.draw_text(self.surface, "-", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), (255,255,255),pos_mode="center")
        ui.draw_text(self.surface, str(self.c_lose), (SCREEN_WIDTH//2+50, SCREEN_HEIGHT//2), (255,255,255),pos_mode="center")
        # count 3 2 1 before every turn
        if( time.time() - self.time_count < 1 and self.c_win<3 and self.c_lose<3):
            ui.draw_text(self.surface, "3", (SCREEN_WIDTH//2, 150), (255,255,255), pos_mode="center")
        elif(time.time() - self.time_count < 2 and self.c_win<3 and self.c_lose<3):
            ui.draw_text(self.surface, "2", (SCREEN_WIDTH//2, 150), (255,255,255), pos_mode="center")
        elif(time.time() - self.time_count < 3 and self.c_win<3 and self.c_lose<3):
            ui.draw_text(self.surface, "1", (SCREEN_WIDTH//2, 150), (255,255,255), pos_mode="center")
        elif( time.time() - self.time_count >= 3 and self.c_win<3 and self.c_lose<3): # Process every second
            self.computer_choice = random.randint(0,2) 
            self.player_choice = 3
            # 0:rock; 1:paper, 2:scissors
            if (self.hand_tracking.results.multi_hand_landmarks):
                x_orig = self.hand_tracking.results.multi_hand_landmarks[0].landmark[0].x
                y_orig = self.hand_tracking.results.multi_hand_landmarks[0].landmark[0].y
                x_base_index = self.hand_tracking.results.multi_hand_landmarks[0].landmark[6].x
                y_base_index = self.hand_tracking.results.multi_hand_landmarks[0].landmark[6].y
                x_tip_index = self.hand_tracking.results.multi_hand_landmarks[0].landmark[8].x
                y_tip_index = self.hand_tracking.results.multi_hand_landmarks[0].landmark[8].y
                x_base_middle = self.hand_tracking.results.multi_hand_landmarks[0].landmark[10].x
                y_base_middle = self.hand_tracking.results.multi_hand_landmarks[0].landmark[10].y
                x_tip_middle = self.hand_tracking.results.multi_hand_landmarks[0].landmark[12].x
                y_tip_middle = self.hand_tracking.results.multi_hand_landmarks[0].landmark[12].y
                x_base_ring = self.hand_tracking.results.multi_hand_landmarks[0].landmark[14].x
                y_base_ring = self.hand_tracking.results.multi_hand_landmarks[0].landmark[14].y
                x_tip_ring = self.hand_tracking.results.multi_hand_landmarks[0].landmark[16].x
                y_tip_ring = self.hand_tracking.results.multi_hand_landmarks[0].landmark[16].y
                x_base_little = self.hand_tracking.results.multi_hand_landmarks[0].landmark[18].x
                y_base_little = self.hand_tracking.results.multi_hand_landmarks[0].landmark[18].y
                x_tip_little = self.hand_tracking.results.multi_hand_landmarks[0].landmark[20].x
                y_tip_little = self.hand_tracking.results.multi_hand_landmarks[0].landmark[20].y

                firstOpen = ((x_orig-x_base_index)*(x_base_index-x_tip_index)+(y_orig-y_base_index)*(y_base_index-y_tip_index)>0)
                secondOpen = ((x_orig-x_base_middle)*(x_base_middle-x_tip_middle)+(y_orig-y_base_middle)*(y_base_middle-y_tip_middle)>0)
                thirdOpen = ((x_orig-x_base_ring)*(x_base_ring-x_tip_ring)+(y_orig-y_base_ring)*(y_base_ring-y_tip_ring)>0)
                fourthOpen = ((x_orig-x_base_little)*(x_base_little-x_tip_little)+(y_orig-y_base_little)*(y_base_little-y_tip_little)>0)  
                if not firstOpen and not secondOpen and not thirdOpen and not fourthOpen:
                    self.player_choice = 0
                    self.count += 1
                    if self.computer_choice == 1:
                        self.c_lose += 1
                    elif self.computer_choice == 2:
                        self.c_win += 1
                        
                elif firstOpen and secondOpen and thirdOpen and fourthOpen:
                    self.player_choice = 1
                    self.count += 1
                    if self.computer_choice == 0:
                        self.c_win += 1
                    elif self.computer_choice == 2:
                        self.c_lose += 1
                    
                elif firstOpen and secondOpen and not thirdOpen and not fourthOpen:
                    self.player_choice = 2
                    self.count += 1
                    if self.computer_choice == 0:
                        self.c_lose += 1
                    elif self.computer_choice == 1:
                        self.c_win += 1
                    
                else:
                    self.player_choice = 3
                    self.computer_choice = 3
            else:
                self.computer_choice = 3
            
            self.time_count = time.time()
        
        image.draw(self.surface, self.Overlayer[self.player_choice], (300,SCREEN_HEIGHT//2), pos_mode="center")
        image.draw(self.surface, self.Overlayer[self.computer_choice], (SCREEN_WIDTH - 300,SCREEN_HEIGHT//2), pos_mode="center")
        
        ui.draw_text(self.surface, "Player", (300,SCREEN_HEIGHT//2-250), (255,255,255), pos_mode = "center")
        ui.draw_text(self.surface, "Computer", (SCREEN_WIDTH - 300, SCREEN_HEIGHT//2-250), (255,255,255), pos_mode = "center")

        if ui.button(self.surface, 0, "Menu", pos_x = SCREEN_WIDTH-150, b_size = (150, 50)):
            return "menu"
        if ui.button(self.surface, 0, "Help", pos_x = 0, b_size = (150, 50)):
            return "help_game3"

        cv2.imshow("Frame", self.frame)
        cv2.waitKey(1)

    def reset_help_game3(self): 
        for i in range (SCREEN_WIDTH):
            for j in range(SCREEN_HEIGHT):
                    self.background.image.set_at((i,j), (0,0,0))
        
    def update_help_game3(self):   
        self.background.draw(self.surface)
        if ui.button(self.surface, 0, "<- Return", pos_x = 0, b_size = (250, 50)):
            return "game3"
        ui.draw_text(self.surface, "Play Rock-Paper-Scissor normally", (SCREEN_WIDTH//2,SCREEN_HEIGHT//2), (255,255,255), pos_mode = "center")    
      
    
