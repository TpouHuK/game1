import sys
import pygame
import pygame.locals as pc
import pymunk.pygame_util
import pymunk
import pygame.joystick
import time

def add_ball(space):
    """Add a ball to the given space at a random position"""
    mass = 1
    radius = 14
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    x = random.randint(120,380)
    body.position = x, 550
    shape = pymunk.Circle(body, radius, (0,0))
    space.add(body, shape)
    return shape

def add_L(space):
    """Add a inverted L shape with two joints"""
    rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    rotation_center_body.position = (300,300)

    rotation_limit_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    rotation_limit_body.position = (210,300)

    body = pymunk.Body(10, 10000)
    body.position = (300,300)
    l1 = pymunk.Segment(body, (-100, 0), (255.0, 0.0), 5.0)
    l2 = pymunk.Segment(body, (-150.0, 0), (-150.0, 50.0), 5.0)

    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,0), (0,0))
    joint_limit = 25
    rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-100,0), (0,0), 0, joint_limit)

    space.add(l1, l2, body, rotation_center_joint, rotation_limit_joint)
    return l1,l2


def main():
    pygame.joystick.init()
    #controller = pygame.joystick.Joystick(0)
    #controller.init()
    global restart
    restart = True
    while restart:
        restart = False
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render('Some Text', False, (0, 0, 0))


        pygame.init()
        screen = pygame.display.set_mode((1200, 680))
        pygame.display.set_caption("Joints. Just wait and the L will tip over")
        clock = pygame.time.Clock()

        space = pymunk.Space()
        global is_end
        is_end = False
        def set_tru(a, b, c):
            global is_end
            is_end = True

        def set_tru2(a, b, c):
            global restart
            restart = True
        space.add_collision_handler(1, 2).begin = set_tru
        space.add_collision_handler(1, 9).begin = set_tru2
        space.gravity = (0.0, -900.0)
        space.sleep_time_threshold = 1

        balls = []
        draw_options = pymunk.pygame_util.DrawOptions(screen)

        body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, (0, 0), (2000, 0),5)
        body.position = (0, 0)

        shape6 = pymunk.Segment(body, (500, 200), (900, 200), 5)
        shape6.friction = 0.9
        space.add(shape6)

        shape6 = pymunk.Segment(body, (500, 200), (500, 690), 5)
        shape6.friction = 0.9
        space.add(shape6)

        shape6 = pymunk.Segment(body, (1100, 0), (1200, 100), 5)
        shape6.friction = 0.9
        #space.add(shape6)
        shape6.color = (250, 0, 0)
        shape6.collision_type = 9

        shape6 = pymunk.Segment(body, (0, 0), (0, 800), 5)
        shape6.friction = 0.9
        space.add(shape6)
        shape6 = pymunk.Segment(body, (0, 0), (1200, 0), 5)
        shape6.friction = 0.9
        space.add(shape6)
        shape6 = pymunk.Segment(body, (1200, 0), (1200, 800), 5)
        shape6.friction = 0.9
        space.add(shape6)
        shape6 = pymunk.Segment(body, (0, 800), (1200, 800), 5)
        shape6.friction = 0.9
        space.add(shape6)

        segments = [(-10/2, 100/2), (10/2, 100/2), (-100/2, 0/2), (100/2, 0/2)]
        body1 = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.DYNAMIC)
        shape1 = pymunk.Poly(body1, segments)
        shape1.density = 1
        shape1.collision_type = 1

        body2 = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.DYNAMIC)
        shape2 = pymunk.Poly(body2, segments)
        shape2.density = 1
        #shape2.color = (255, 0, 0)
        shape2.collision_type = 1

        shape1.friction = 1
        shape2.friction = 1
        shape.friction = 1

        body1.position = (200, 150)
        body2.position = (200, 100)
        body2.angle = 3.1415926535897932

        space.add(body1, shape1)
        space.add(body2, shape2)

        body3 = pymunk.Body(mass=1, moment=1, body_type=pymunk.Body.STATIC)
        body3.position = (800, 400)
        crl = pymunk.Circle(body3, 80)
        crl.collision_type = 2
        space.add(body3, crl)


        #cs = pymunk.constraint.SlideJoint(body1, body2, (-10,0), (10,0), 0, 100)
        #cs4 = pymunk.constraint.SlideJoint(body1, body2, (10,0), (-10,0), 0, 100)
        spring_f = 100000 * 2 * 2 * 2 * 2 * 2
        spring_d = 10000 * 2 
        cs2 = pymunk.constraint.DampedSpring(body1, body2, (-50,0), (50,0), 30, spring_f, spring_d)
        cs3 = pymunk.constraint.DampedSpring(body1, body2, (50,0), (-50,0), 30, spring_f, spring_d)
        cs5 = pymunk.constraint.GrooveJoint(body1, body2, (10, 0), (10, -100), (-10,0))
        cs6 = pymunk.constraint.GrooveJoint(body1, body2, (-10, 0), (-10, -100), (10,0))
        #space.add(cs, cs2)
        space.add(cs2, cs3, cs5, cs6)
        
        space.add(body, shape)

        ticks_to_next_ball = 10
        max_jump = 150

        start_time = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pc.QUIT:
                    sys.exit(0)
                elif event.type == pc.KEYDOWN and event.key == pc.K_ESCAPE:
                    sys.exit(0)

                elif event.type == pc.KEYDOWN and event.key == 97:
                    cs2.rest_length = 15
                elif event.type == pc.KEYDOWN and event.key == 100:
                    cs3.rest_length = 15
                elif event.type == pc.KEYUP and event.key == 97:
                    cs2.rest_length = 50 + 10
                elif event.type == pc.KEYUP and event.key == 100:
                    cs3.rest_length = 50 + 10
                elif event.type == pc.KEYDOWN and event.key == 98:
                    cs3.rest_length = 50 + 30
                    cs2.rest_length = 50 + 30
                elif event.type == pc.KEYDOWN and event.key == 114:
                    restart = True
                    break
                elif event.type == 7 and event.axis == 5:
                    #right
                    jv = 1-(event.value + 1)/2
                    cs2.rest_length = 15 + jv*65
                elif event.type == 7 and event.axis == 2:
                    #left
                    jv = 1-(event.value + 1)/2
                    cs3.rest_length = 15 + jv*65
                else:
                    pass
                    #print(event.type)
                    #print(event.value)
            if restart:
                break
            #if event.type == pc
            #print(pc.JOYAXISMOTION)
            #print(event)
            #print(event.type)
            #print(event.value)
            #print(event.axis)
            #5/3


            space.step(1/50.0)
            #space.step(1/500.0)
            cur_max = max(body1.position[1], body2.position[1])
            #if  cur_max > max_jump:
                #print("NEW MAX JUMP:", cur_max)
                #max_jump = cur_max

            screen.fill((255,255,255))
            space.debug_draw(draw_options)
            finished_time = time.time()
            textsurface = myfont.render(f"TIME: {finished_time-start_time:.3f}", False, (0, 0, 0))
            screen.blit(textsurface,(0,0))
            pygame.display.flip()
            clock.tick(50)
            if is_end:
                print("end")
                break
    #finished_time = time.time()
    print("FINISHED FOR:", (finished_time - start_time))

if __name__ == '__main__':
    main()

