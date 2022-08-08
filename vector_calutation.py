def find_other_point(vector, first_point):
    '''
    Tìm điểm còn lại của vector
    '''
    return (first_point[0] - vector[0], first_point[1] - vector[1])

def rad_to_deg(rad):
    '''
    Đổi rad sang độ
    '''
    from math import pi
    return rad*180/pi

def convert_to_vector(start_point, end_point):
    '''
    Trả về vector tạo bởi 2 điểm
    '''
    return (end_point[0] - start_point[0], end_point[1] - start_point[1])

def rotate_vector(angle, vector):
    '''
    Quay vector \n
    Góc ở dạng rad và đo ngược chiều kim đồng hồ
    '''
    from math import sin, cos
 
    x2 = cos(angle)*vector[0] - sin(angle)*vector[1]
    y2 = sin(angle)*vector[0] + cos(angle)*vector[1]

    return (x2, y2)

def dot_product(*vector):
    '''
    Tích vô hướng
    '''
    product_x = 1
    product_y = 1

    for vect in vector:
        product_x *= vect[0]
        product_y *= vect[1]

    return product_x + product_y

def angle_between(*vector):
    '''
    Return angle between 2 vectors in radians
    '''
    from math import acos, sqrt

    length_vect1 =  sqrt(vector[0][0]**2 + vector[0][1]**2)
    lenght_vect2 =  sqrt(vector[1][0]**2 + vector[1][1]**2)
  
    
    return acos((dot_product(vector[0], vector[1])/(length_vect1 * lenght_vect2)))


def trig_angle(vector):
    '''
    Trả về góc lượng giác của 1 vector dạng rad
    '''
    from math import pi
    unit_vector = (20, 0)
    alpha = angle_between(vector, unit_vector)
    if vector[1] > 0:
        return float(alpha)
    elif vector[1] < 0:
        return float(pi + alpha)

def distance_between_2_point(p1, p2):
    '''
    Return the distance between 2 points
    '''
    vector = convert_to_vector(p1, p2)
    
    return (vector[0]**2 + vector[1]**2)**0.5