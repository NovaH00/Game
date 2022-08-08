
from time import sleep
from object import *
from UI import*
from game import Game
from math import pi
import pygame
from vector_calutation import distance_between_2_point
from Color import*



game = Game((800, 600), 60)
#-----------------------------------------------r_s

player1 = character([300, 550], 20, 60, 40, 200, pi/30, 100, 100, 10, 5, 20, Color.white)
player1_bullets = []
for i in range(1, player1.magazine_size + 1):
    player1_bullets.append(projectile([200, 200], 1000, 10, 5, (0, 255, 255)))


player2 = character([game.resolution[0] - 200, 300], 20, 60, 40, 200, pi/30, 100, 100, 10, 5, 20, Color.red)
player2_bullets = []
for i in range(1, player2.magazine_size + 1):
    player2_bullets.append(projectile([200, 200], 1000, 10, 5, (0, 255, 255)))


def player2_update():
    if player2.hp > 0:
        player2.pos_update(game.fps)
        player2.acceleration_update(game.fps)
        player2.decelerarion_update(game.fps)
        player2.friction_update(game.fps)
        player2.angle_update()
        player2.dir_vect_update()
        game.draw_gun_barrel(player2)
        game.draw_object(player2)
    else:
        player2.pos = [3000, 3000]

class player2_bullet():
    def bullet_update():
        # Nếu player1 k đang nạp đạn thì mới update đạn
        if player2.is_manual_reload == False and player2.hp > 0:
            for bullet in player2_bullets:
                bullet.position_update(player2.get_pos(), game.fps)
                bullet.angle_update(player2.angle)
                game.draw_object(bullet)

        if player2.hp <= 0:
            for bullet in player2_bullets:
                bullet.pos = [3000, 3000]
        
    def reset_bullet():
        for bullet in player2_bullets:
            bullet.fired = False

    def is_magazine_emty():
        for bullet in player2_bullets:
            if bullet.fired == False:
                return False
        return True

    def auto_reload():
        if player2_bullet.is_magazine_emty() == True and player2.hp >= 0:
            player2.is_auto_reload = True
            player2.reloading = True
            game.tick_counter_player2 += 1
            reset_trigger = False
            if game.tick_counter_player2 % (60*player2.reload_time) == 0: 
                game.tick_counter_player2 = 0 
                player2.reloading = False
                player2.is_magazine_full = True
                reset_trigger = True
                player2.is_auto_reload = False
            if reset_trigger == True:
                # print("hye")
                player2_bullet.reset_bullet()
    def manual_reload():
        if player2.manual_reload_trigger == True and player2.is_auto_reload == False:
            player2.reloading = True
            player2.is_manual_reload = True
            game.tick_counter_player2 += 1
            reset_trigger = False
            if game.tick_counter_player2 % (60*player2.reload_time) == 0:
                reset_trigger = True
                game.tick_counter_player2 = 0 
                player2.manual_reload_trigger = False
                player2.reloading = False
                player2.is_magazine_full = True
                player2.is_manual_reload = False
            if reset_trigger == True:
                player2_bullet.reset_bullet()

    def get_number_of_remaining_bullet():
        count = 0
        for bullet in player2_bullets:
            if bullet.fired == False:
                count += 1
        return count 

    def hit_check():
        for bullet in player2_bullets:
            if distance_between_2_point(bullet.pos, player1.pos) <= (bullet.radius + player1.radius):
                player1.hp -= bullet.dmg
                bullet.pos =  [3000, 3000]        
    
def player1_update():
    if player1.hp > 0:
        player1.pos_update(game.fps)
        player1.acceleration_update(game.fps)
        player1.decelerarion_update(game.fps)
        player1.friction_update(game.fps)
        player1.angle_update()
        player1.dir_vect_update()
        #Draw gun barrel
        game.draw_gun_barrel(player1)
        #Draw player1
        game.draw_object(player1)
    
    elif player1.hp <= 0:
        player1.pos = [3000, 3000]

#----------------------------------------------------------------------------------------------
class player1_bullet():
    def bullet_update():
        # Nếu player1 k đang nạp đạn thì mới update đạn
        if player1.is_manual_reload == False and player1.hp > 0:
            for bullet in player1_bullets:
                bullet.position_update(player1.get_pos(), game.fps)
                bullet.angle_update(player1.angle)
                game.draw_object(bullet)

        if player1.hp <= 0:
            for bullet in player1_bullets:
                bullet.pos =  [3000, 3000]
    #Reset toàn bộ đạn về trạng thái chưa bắn
    def reset_bullet():
        for bullet in player1_bullets:
            bullet.fired = False
    #Check xem băng đạn có rỗng hay k
    def is_magazine_emty():
        for bullet in player1_bullets:
            if bullet.fired == False:
                return False
        return True
    #Tự nạp đạn khi hết đạn
    
    def auto_reload():
        if player1_bullet.is_magazine_emty() == True and player1.hp >= 0:
            player1.is_auto_reload = True
            player1.reloading = True
            game.tick_counter_player1 += 1
            reset_trigger = False
            if game.tick_counter_player1 % (60*player1.reload_time) == 0: 
                game.tick_counter_player1 = 0 
                player1.reloading = False
                player1.is_magazine_full = True
                reset_trigger = True
                player1.is_auto_reload = False
            if reset_trigger == True:
                # print("hye")
                player1_bullet.reset_bullet()
                
    #Nạp đạn thủ công
    def manual_reload():
        if player1.manual_reload_trigger == True and player1.is_auto_reload == False:
            player1.reloading = True
            player1.is_manual_reload = True
            game.tick_counter_player1 += 1
            reset_trigger = False
            if game.tick_counter_player1 % (60*player1.reload_time) == 0:
                reset_trigger = True
                game.tick_counter_player1 = 0 
                player1.manual_reload_trigger = False
                player1.reloading = False
                player1.is_magazine_full = True
                player1.is_manual_reload = False
            if reset_trigger == True:
                player1_bullet.reset_bullet()
    #Lấy số lượng đạn
    def get_number_of_remaining_bullet():
        count = 0
        for bullet in player1_bullets:
            if bullet.fired == False:
                count += 1
        return count
    
    def hit_check():
        for bullet in player1_bullets:
            if distance_between_2_point(bullet.pos, player2.pos) <= (bullet.radius + player2.radius):
                player2.hp -= bullet.dmg
                bullet.pos =  [3000, 3000]
#----------------------------------------------------------------------------------------------

#Giới hạn map
def map_restriction():
    game.map_restriction(player1)
    game.map_restriction(player2)

def prematch_seperate():
    game.premath_counter += 1
    second = 11
    
    if int(second - game.premath_counter / 60) > 0:
        game.prematch_separate(player1, player1_bullets, player2, player2_bullets, int(second - game.premath_counter / 60))
    

def reset():
    player1.pos = [300, 550]
    player1.speed = 0
    player1.hp = player1.max_hp
    player1.reloading = False
    for bullet in player1_bullets:
        bullet.fired = False
    

    player2.pos = [game.resolution[0] - 200, 300]
    player2.speed = 0
    player2.hp = player2.max_hp
    player2.reloading = False
    for bullet in player2_bullets:
        bullet.fired = False
    
    game.premath_counter = 0


'''
==================================================================================================
==================================================================================================
==================================================================================================
'''
def main():
    # game.screen.fill(Color.gray)
    
    #Đạn của player1---------------------------------
    player1_bullet.bullet_update()
    player1_bullet.auto_reload()
    player1_bullet.manual_reload()
    player1_bullet.hit_check()
    #------------------------------------
    #player1
    player1_update()
    #------------------------------------
        
    
    #Đạn của player2
    player2_bullet.bullet_update()
    player2_bullet.auto_reload()
    player2_bullet.manual_reload()
    player2_bullet.hit_check()
    #player2-------------------------------
    player2_update()
    #------------------------------------

    #Game--------------------------------
    map_restriction()
    prematch_seperate()



    game.draw_player1_bullet_status(player1_bullet.get_number_of_remaining_bullet(), player1.magazine_size, game.tick_counter_player1, player1.reload_time)
    game.draw_player1_speed(player1.speed)

    game.draw_player2_bullet_status(player2_bullet.get_number_of_remaining_bullet(), player2.magazine_size, game.tick_counter_player2, player2.reload_time)
    game.draw_player2_speed(player2.speed)
    game.draw_player_hp_bar(player1)
    game.draw_player_hp_bar(player2)
    
    game.collision_handle(player1, player2)
    #------------------------------------

play_button = button(game.screen, (100, 100), "PLAY", 50, Color.white, Color.gray, Color.cyan)
control_button = button(game.screen, (100, 170), "CONTROL", 20, Color.white, Color.gray, Color.cyan)
exit_button = button(game.screen, (100, 200), "EXIT", 20, Color.white, Color.gray, Color.cyan)
back_button = button(game.screen, (50, game.resolution[1] - 50), "BACK", 15, Color.white, Color.gray, Color.cyan)

pause_button = button(game.screen, (20, 20), "PAUSE", 15, Color.white, Color.gray, Color.cyan)
resume_button = button(game.screen, (100, 100), "RESUME", 30, Color.white, Color.gray, Color.cyan)

main_screen_button = button(game.screen, (100, 150), "MAIN SCREEN", 30, Color.white, Color.gray, Color.cyan)
quit_button = button(game.screen, (100, 200), "QUIT", 30, Color.white, Color.gray, Color.cyan)


        
while game.is_running:
    game.clock.tick(game.fps)
    game.screen.fill((Color.gray))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.stop_running()
        if event.type == pygame.KEYDOWN:
            #Player1----------------------------------------
            if event.key == pygame.K_w:
                player1.is_moving_forward = True
            
            if event.key == pygame.K_s:
                player1.is_moving_backward = True
            
            if event.key == pygame.K_d:
                player1.is_deacreasing_angle = True
            
            if event.key == pygame.K_a:
                player1.is_increasing_angle = True

            if event.key == pygame.K_SPACE and player1.reloading == False and player1.hp >= 0:
                player1_bullets[player1.current_bullet_location % player1.magazine_size].fired = True
                player1.is_magazine_full = False
                player1.current_bullet_location += 1
                

            if event.key == pygame.K_r and player1.is_auto_reload == False and player1.hp >= 0:
                if player1.is_magazine_full == False:
                    player1.manual_reload_trigger = True
            #Player2----------------------------------------------
            if event.key == pygame.K_UP:
                player2.is_moving_forward = True
            
            if event.key == pygame.K_DOWN:
                player2.is_moving_backward = True
            
            if event.key == pygame.K_RIGHT:
                player2.is_deacreasing_angle = True
            
            if event.key == pygame.K_LEFT:
                player2.is_increasing_angle = True

            if event.key == pygame.K_RSHIFT and player2.reloading == False and player2.hp >= 0:
                player2_bullets[player2.current_bullet_location % player2.magazine_size].fired = True
                player2.is_magazine_full = False
                player2.current_bullet_location += 1

            if event.key == pygame.K_RCTRL and player2.is_auto_reload == False and player2.hp >= 0:

                if player2.is_magazine_full == False:
                    player2.manual_reload_trigger = True
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player1.is_moving_forward = False
            
            if event.key == pygame.K_s:
                player1.is_moving_backward = False
                
            
            if event.key == pygame.K_d:
                player1.is_deacreasing_angle = False

            if event.key == pygame.K_a:
                player1.is_increasing_angle = False

            #Player2 ------------------------------

            if event.key == pygame.K_UP:
                player2.is_moving_forward = False
            
            if event.key == pygame.K_DOWN:
                player2.is_moving_backward = False
                
            if event.key == pygame.K_RIGHT:
                player2.is_deacreasing_angle = False

            if event.key == pygame.K_LEFT:
                player2.is_increasing_angle = False

    game.screen.fill(Color.gray)
    # main()
    mouse_pos = pygame.mouse.get_pos()
    left_mouse_pressed = pygame.mouse.get_pressed()[0]

    if game.is_main_running == False:
        play_button.draw()

        control_button.draw()
        
        exit_button.draw()  

    if play_button.get_pressed():
        game.is_main_running = True

    if game.is_main_running == True and game.pause == False:
        main()
        pause_button.draw()

    if pause_button.get_pressed() and game.is_main_running:
        game.pause = True

    if game.pause == True:
        resume_button.draw()
        main_screen_button.draw()
        quit_button.draw()
        if resume_button.get_pressed():
            game.pause = False    

        if main_screen_button.get_pressed():
            game.pause = False
            game.is_main_running = False
            reset()
        
        if quit_button.get_pressed():
            game.is_running = False

    if control_button.get_pressed() == True:
        game.is_control_guide_running = True

    if game.is_control_guide_running == True and game.is_main_running == False:
        game.draw_control_guide()
        back_button.draw()

        if back_button.get_pressed() == True:
            game.is_control_guide_running = False
    
    if exit_button.get_pressed():
        game.is_running = False

    pygame.display.flip()

    
    
pygame.quit()

