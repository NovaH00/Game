import pygame
from vector_calutation import rad_to_deg, find_other_point, distance_between_2_point
from Color import Color

pygame.init()

class Game:
    def __init__(self, screen_resolution: tuple[int, int], fps: int):
        self.resolution = screen_resolution
        self.screen = pygame.display.set_mode(self.resolution)
        self.is_running = True
        self.is_main_running = False
        self.is_control_guide_running = False
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.tick_counter_player1 = 0
        self.tick_counter_player2 = 0
        self.premath_counter = 0
        self.pause = False
        
    #Test only
    def draw_plus_sign(self, coordinate):
        pygame.draw.line(self.screen, (255,255,255), (coordinate[0] - 30, coordinate[1]), (coordinate[0] + 30, coordinate[1]))
        pygame.draw.line(self.screen, (255,255,255), (coordinate[0], coordinate[1] - 30), (coordinate[0], coordinate[1] + 30))
        
    
              
    #--------------------------------------------------------------------------------------------------------------------------------
    def draw_gun_barrel(self, object: object):
        pygame.draw.line(self.screen, object.color, object.pos, find_other_point(object.dir_vect, object.pos), 8)

    def draw_object(self, object: object):
        pygame.draw.circle(self.screen, object.color, object.pos, object.radius)

        
    def stop_running(self):
        self.is_running = False
        pygame.quit()

    def is_inside_screen(self, position: list):
        if position[0] > 0 and position[0] < self.resolution[0]:
            if position[1] > 0 and position[1] < self.resolution[1]:
                return True

    def draw_player1_bullet_status(self, current_number_of_bullet: int, max_number_of_bullet: int, reload_tick: int, reload_time: int):
        font = pygame.font.Font('freesansbold.ttf', 18)
        bullet_text = font.render(f"{current_number_of_bullet}/{max_number_of_bullet}", True, (255,255,255))
        self.screen.blit(bullet_text, (50, self.resolution[1] - 60))
        #Vẽ thanh nạp đạn
        pygame.draw.rect(self.screen, Color.white, (50, self.resolution[1] - 40, 102, 6), 1)

        progress = ((reload_tick / 60)/reload_time)*100
        

        pygame.draw.rect(self.screen, Color.blue, (51, self.resolution[1] - 39, progress, 4))
    
    def draw_player1_speed(self, speed):
        font = pygame.font.Font('freesansbold.ttf', 18)
        speed_text = font.render(f"Speed: {int(speed)}", True, Color.white)
        self.screen.blit(speed_text, (50, self.resolution[1] - 25))
    
    
    
    def draw_player2_bullet_status(self, current_number_of_bullet: int, max_number_of_bullet: int, reload_tick: int, reload_time: int):
        font = pygame.font.Font('freesansbold.ttf', 18)
        bullet_text = font.render(f"{current_number_of_bullet}/{max_number_of_bullet}", True, Color.red)
        self.screen.blit(bullet_text, (self.resolution[0] - 150, 60))
        #Vẽ thanh nạp đạn
        pygame.draw.rect(self.screen, Color.red, (self.resolution[0] - 150, 50 , 102, 6), 1)

        progress = ((reload_tick / 60)/reload_time)*100
        
        pygame.draw.rect(self.screen, Color.blue, (self.resolution[0] - 150, 51 , progress, 4))

    def draw_player2_speed(self, speed):
        font = pygame.font.Font('freesansbold.ttf', 18)
        speed_text = font.render(f"Speed: {int(speed)}", True, Color.red)
        self.screen.blit(speed_text, (self.resolution[0] - 150, 30))


    def map_restriction(self, object: object):
        x = object.pos[0]
        y = object.pos[1]
        if x >= self.resolution[0] - object.radius:
            object.pos[0] = self.resolution[0] - object.radius
        if x <= object.radius:
            object.pos[0] = object.radius

        if y >= self.resolution[1] - object.radius:
            object.pos[1] = self.resolution[1] - object.radius
        if y <= object.radius:
            object.pos[1] = object.radius
    

    def collision_handle(self, object1: object, object2: object):
        distance = distance_between_2_point(object1.pos, object2.pos) or 1
        #Player1
        x_distance = object1.pos[0] - object2.pos[0]
        y_distance = object1.pos[1] - object2.pos[1]
        radii_sum = object1.radius + object2.radius
        
        x_unit = x_distance / distance
        y_unit = y_distance / distance
        if distance <= radii_sum:
            object1.pos[0] = object2.pos[0] + (radii_sum + 1)*x_unit
            object1.pos[1] = object2.pos[1] + (radii_sum + 1)*y_unit

        #Player2
        x_distance = object2.pos[0] - object1.pos[0]
        y_distance = object2.pos[1] - object1.pos[1]
        
        x_unit = x_distance / distance
        y_unit = y_distance / distance
        if distance <= radii_sum:
            object2.pos[0] = object1.pos[0] + (radii_sum + 1)*x_unit
            object2.pos[1] = object1.pos[1] + (radii_sum + 1)*y_unit
    

    def draw_player_hp_bar(self, player: object):
        remaining_percentage = (player.hp / player.max_hp)
        pygame.draw.rect(self.screen, player.color, (player.pos[0] - player.radius, player.pos[1] + 25, player.radius*2, 4), 1)
        
        pygame.draw.rect(self.screen, Color.green, (player.pos[0] - player.radius, player.pos[1] + 25, player.radius*2*remaining_percentage, 4))

    
    def prematch_separate(self, player1: object, player1_bullets: list, player2: object, player2_bullets: list, second: int):
        pygame.draw.line(self.screen, Color.yellow, (self.resolution[0]/2, 0), (self.resolution[0]/2, self.resolution[1]), 15)

        if player1.pos[0] + player1.radius >= self.resolution[0]/2 - 7:
            player1.pos [0] = self.resolution[0]/2 - 6 - player1.radius
        
        if player2.pos[0] - player2.radius <= self.resolution[0]/2 + 7:
            player2.pos[0] = self.resolution[0]/2 + 6 + player2.radius
        
        for bullet in player1_bullets:
            if bullet.pos[0] + bullet.radius >= self.resolution[0]/2 - 7:
                bullet.pos = [3000, 3000]
        
        for bullet in player2_bullets:
            if bullet.pos[0] - bullet.radius <= self.resolution[0]/2 + 7:
                bullet.pos = [3000, 3000]
        
        font = pygame.font.Font('freesansbold.ttf', 50)
        remaining_sec = font.render(f"{second}", True, Color.yellow)
        self.screen.blit(remaining_sec, (200, 200))
        self.screen.blit(remaining_sec, (self.resolution[0] - 200, self.resolution[1] - 200))


    
    def draw_control_guide(self):
        self.screen.fill(Color.gray)
        font = pygame.font.Font('freesansbold.ttf', 15)

        shoot_text = font.render("SHOOT", True, Color.white)
        reload_text = font.render("RELOAD", True, Color.white)
        up_text = font.render("UP", True, Color.white)
        down_text = font.render("DOWN", True, Color.white)
        right_text = font.render("RIGHT", True, Color.white)
        left_text = font.render("LEFT", True, Color.white)

        white_player_text = font.render("WHITE PLAYER", True, Color.white)
        space_text = font.render("SPACE", True, Color.white)
        r_text = font.render("R", True, Color.white)
        w_text = font.render("W", True, Color.white)
        a_text = font.render("A", True, Color.white)
        s_text = font.render("S", True, Color.white)
        d_text = font.render("D", True, Color.white)
        
        red_player_text = font.render("RED PLAYER", True, Color.white)
        right_shift_text = font.render("RIGHT SHIFT", True, Color.white)
        right_ctrl_text = font.render("RIGHT CTRL", True, Color.white)
        arrowUp_text = font.render("ARROW UP", True, Color.white)
        arrowDown_text = font.render("ARROW DOWN", True, Color.white)
        arrowRight_text = font.render("ARROW RIGHT", True, Color.white)
        arrowLeft_text = font.render("ARROW LEFT", True, Color.white)


        self.screen.blit(white_player_text, (self.resolution[0]/3 , 100))
        self.screen.blit(red_player_text, (2*self.resolution[0]/3 , 100))

        self.screen.blit(shoot_text, (100, 200))
        self.screen.blit(reload_text, (100, 250))
        self.screen.blit(up_text, (100, 300))
        self.screen.blit(down_text, (100, 350))
        self.screen.blit(left_text, (100, 400))
        self.screen.blit(right_text, (100, 450))

        self.screen.blit(space_text, (self.resolution[0]/3 + 30, 200))
        self.screen.blit(r_text, (self.resolution[0]/3 + 50, 250))
        self.screen.blit(w_text, (self.resolution[0]/3 + 50, 300))
        self.screen.blit(s_text, (self.resolution[0]/3 + 50, 350))
        self.screen.blit(a_text, (self.resolution[0]/3 + 50, 400))
        self.screen.blit(d_text, (self.resolution[0]/3 + 50, 450))

        self.screen.blit(right_shift_text, (2*self.resolution[0]/3 , 200))
        self.screen.blit(right_ctrl_text, (2*self.resolution[0]/3 , 250))
        self.screen.blit(arrowUp_text, (2*self.resolution[0]/3 , 300))
        self.screen.blit(arrowDown_text, (2*self.resolution[0]/3 , 350))
        self.screen.blit(arrowLeft_text, (2*self.resolution[0]/3 , 400))
        self.screen.blit(arrowRight_text, (2*self.resolution[0]/3 , 450))

        
        
        