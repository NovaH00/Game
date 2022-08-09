
import math

from vector_calutation import convert_to_vector, rotate_vector, angle_between, trig_angle

# class Object:
class character():
    def __init__(self, position: list[int, int], acceleration: int, deceleration: int, friction_deceleration: int,  max_speed: int, rotation_speed: float, hp: int, max_hp: int,  magazine_size: int, reload_time: int, radius: int, color: tuple) -> None:
        '''
        Angle measure in radian which determinant the character direction
        '''
        self.pos = position
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.speed = 0
        self.max_speed = max_speed
        self.hp  = hp
        self.max_hp = max_hp
        self.angle = math.pi/2
        self.radius = radius
        self.dir_vect = rotate_vector(self.angle, convert_to_vector(self.pos, (self.pos[0] + self.radius + 10, self.pos[1])))
        self.color = color
        self.is_moving_forward = False
        self.is_moving_backward = False
        self.is_increasing_angle = False
        self.is_deacreasing_angle = False
        self.rotation_speed = rotation_speed
        self.magazine_size = magazine_size
        self.current_bullet_location = 0
        self.reload_time = reload_time
        self.manual_reload_trigger = False
        self.reloading = False
        self.is_magazine_full = True
        self.is_auto_reload = False
        self.is_manual_reload = False
        self.friction_deceleration = friction_deceleration
        

    def pos_update(self, fps: int):
        
        delta_t = 1/fps
        
        from math import sin, cos
        #delta_t : thời gian mỗi frame
        #delta_d : khoảng cách đi đc mỗi frame
        #delta_x, delta_y: sự thay đổi toạ độ x,y theo delta_d và angle
        delta_d = self.speed * delta_t
        delta_x = cos(self.angle) * delta_d
        delta_y = sin(self.angle) * delta_d
        self.pos[0] += delta_x
        self.pos[1] -= delta_y
    def acceleration_update(self, fps):
        delta_t = 1/fps
        if self.is_moving_forward == True and self.speed < self.max_speed and self.is_moving_backward == False:
            self.speed += self.acceleration*delta_t

    def decelerarion_update(self, fps):
        delta_t = 1/fps
        if self.is_moving_forward == False and self.speed > 0 and self.is_moving_backward == True:
            self.speed -= self.deceleration*delta_t

        if self.speed < 0:
            self.speed = 0
    def friction_update(self, fps):
        delta_t = 1/fps
        if self.is_moving_forward == False:
            if self.speed > 0:
                self.speed -= self.friction_deceleration*delta_t
    def angle_update(self):
        if self.is_increasing_angle == True and self.is_deacreasing_angle == False:
            self.angle += self.rotation_speed
        if self.is_deacreasing_angle == True and self.is_increasing_angle == False:
            self.angle -= self.rotation_speed
        #keep the angle in interval of [0, 2pi]
        self.angle = self.angle % (2*math.pi)

    def dir_vect_update(self):

        if self.is_increasing_angle == True and self.is_deacreasing_angle == False:
            self.dir_vect = rotate_vector(-self.rotation_speed, self.dir_vect)

        if self.is_deacreasing_angle == True and self.is_increasing_angle == False:
            self.dir_vect = rotate_vector(self.rotation_speed, self.dir_vect)

    def get_pos(self):
        return [self.pos[0], self.pos[1]]
    
    



class projectile(object):
    def __init__(self, position: list[int, int], speed: int, damage: int, radius: int, color: tuple) -> None:
        self.pos = position
        self.speed = speed
        self.dmg = damage
        self.angle = math.pi/2
        self.color = color
        self.radius = radius
        self.fired = False
        self.bullet_location = 0
    
    def position_update(self, initial_pos, fps):
        from math import sin, cos
        delta_t = 1/fps
        delta_d = delta_t * self.speed
        if self.fired == True:
            delta_x = cos(self.angle) * delta_d
            delta_y = sin(self.angle) * delta_d
            self.pos[0] += delta_x
            self.pos[1] -= delta_y
        else:
            self.pos = initial_pos
    
    def angle_update(self, angle):
        if self.fired == False:
            self.angle = angle
    

class button(object):
    
    def __init__(self, screen, position: tuple, text: str, text_size: int, text_color: tuple, text_bg_color: tuple, text_color_change: tuple) -> None:
        
        self.screen = screen
        self.pos = position
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.text_bg_color = text_bg_color
        self.text_color_change = text_color_change
        
        
        self.clicked = False
        

    
    def draw(self):
        import pygame
        pygame.init ()
        font = pygame.font.Font('freesansbold.ttf', self.text_size)
        text_surface = font.render(self.text, True, self.text_color, self.text_bg_color)
        text_rect = text_surface.get_rect()
        text_rect[0], text_rect[1] = self.pos[0], self.pos[1]

        mouse_pos = pygame.mouse.get_pos()
        
        if text_rect.collidepoint(mouse_pos):
            text_surface = font.render(self.text, True, self.text_color_change, self.text_bg_color)
             
        self.screen.blit(text_surface, text_rect)

        
    
    def get_pressed(self):
        import pygame
        pygame.init ()
        pressed = False

        font = pygame.font.Font('freesansbold.ttf', self.text_size)
        text_surface = font.render(self.text, True, self.text_color, self.text_bg_color)
        text_rect = text_surface.get_rect()
        text_rect[0], text_rect[1] = self.pos[0], self.pos[1]

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if text_rect.collidepoint(mouse_pos): 
            if mouse_pressed[0] == True and self.clicked == False:
                self.clicked = True
                pressed = True

        if mouse_pressed[0] == False:
            self.clicked = False
        
        return pressed
