from hyperboloid_utilities import *
import math
import time

key_movement_bindings = {
    'a': (lambda rot_amount, trans_amount: unit_3_vector_and_distance_to_O13_hyperbolic_translation(
            [ -1.0,  0.0,  0.0 ], trans_amount)),
    'd': (lambda rot_amount, trans_amount: unit_3_vector_and_distance_to_O13_hyperbolic_translation(
            [ +1.0,  0.0,  0.0 ], trans_amount)),
    's': (lambda rot_amount, trans_amount: unit_3_vector_and_distance_to_O13_hyperbolic_translation(
            [  0.0, -1.0,  0.0 ], trans_amount)),
    'w': (lambda rot_amount, trans_amount: unit_3_vector_and_distance_to_O13_hyperbolic_translation(
            [  0.0, +1.0,  0.0 ], trans_amount)),
    'e': (lambda rot_amount, trans_amount: unit_3_vector_and_distance_to_O13_hyperbolic_translation(
            [  0.0,  0.0, -1.0 ], trans_amount)),
    'c': (lambda rot_amount, trans_amount: unit_3_vector_and_distance_to_O13_hyperbolic_translation(
            [  0.0,  0.0, +1.0 ], trans_amount)),
    'Left': (lambda rot_amount, trans_amount: O13_y_rotation(-rot_amount)),
    'Right': (lambda rot_amount, trans_amount: O13_y_rotation(rot_amount)),
    'Up': (lambda rot_amount, trans_amount: O13_x_rotation(-rot_amount)),
    'Down': (lambda rot_amount, trans_amount: O13_x_rotation(rot_amount))
}

class HyperboloidNavigation:
    def __init__(self):
        self.smooth_movement = True
        self.refresh_delay = 10

        self.current_key_pressed = None
        self.mouse = None
        self.view_state_mouse = None

        self.time_key_release_received = None

        self.bind('<KeyPress>', self.tkKeyPress)
        self.bind('<KeyRelease>', self.tkKeyRelease)
        self.bind('<Button-1>', self.tkButton1)
        self.bind('<ButtonRelease-1>', self.tkButtonRelease1)
        self.bind('<B1-Motion>', self.tkButtonMotion1)
        self.bind('<Control-Button-1>', self.tkButton1)
        self.bind('<Control-ButtonRelease-1>', self.tkButtonRelease1)
        self.bind('<Control-B1-Motion>', self.tkCtrlButtonMotion1)

        self.ui_parameter_dict['translationVelocity'] = ('float', 0.4)
        self.ui_parameter_dict['rotationVelocity']    = ('float', 0.4)
        
    def do_movement(self):
        current_time = time.time()

        if self.time_key_release_received:
            if current_time - self.time_key_release_received > 0.005:
                self.current_key_pressed = None

        if not self.current_key_pressed in key_movement_bindings:
            return

        self.last_time, diff_time = current_time, current_time - self.last_time

        m = key_movement_bindings[self.current_key_pressed](
            diff_time * self.ui_parameter_dict['rotationVelocity'][1],
            diff_time * self.ui_parameter_dict['translationVelocity'][1])

        self.view_state = self.raytracing_data.update_view_state(
            self.view_state, m)

        self.redraw_if_initialized()

        self.after(self.refresh_delay, self.do_movement)

    def tkKeyRelease(self, event):
        self.time_key_release_received = time.time()

    def tkKeyPress(self, event):
        if event.keysym in key_movement_bindings:
            if self.smooth_movement:
                self.time_key_release_received = None

                if self.current_key_pressed is None:
                    self.last_time = time.time()
                    self.current_key_pressed = event.keysym
                    self.after(1, self.do_movement)
            else:
                m = key_movement_bindings[event.keysym](self.angle_size, self.step_size)

                self.view_state = self.update_view_state(
                    self.view_state, m)

                self.redraw_if_initialized()

        if event.keysym == 'u':
            print(self.view_state)

        if event.keysym == 'v':
            self.view = (self.view + 1) % 3
            self.redraw_if_initialized()
            
        if event.keysym == 'n':
            self.perspectiveType = 1 - self.perspectiveType
            self.redraw_if_initialized()

    def tkButton1(self, event):
        self.mouse = (event.x, event.y)
        self.view_state_mouse = self.view_state

    def tkButtonMotion1(self, event):
        if self.mouse is None:
            return

        delta_x = event.x - self.mouse[0]
        delta_y = event.y - self.mouse[1]

        amt = math.sqrt(delta_x ** 2 + delta_y ** 2)

        if amt == 0:
            self.view_state = self.view_state_mouse
        else:
            m = unit_3_vector_and_distance_to_O13_hyperbolic_translation(
                [-delta_x / amt, delta_y / amt, 0.0], amt * 0.01)

            self.view_state = self.raytracing_data.update_view_state(
                self.view_state_mouse, m)

        self.redraw_if_initialized()

    def tkButtonRelease1(self, event):
        self.mouse = None

    def tkCtrlButtonMotion1(self, event):
        if self.mouse is None:
            return

        delta_x = event.x - self.mouse[0]
        delta_y = event.y - self.mouse[1]

        m = O13_y_rotation(-delta_x * 0.01) * O13_x_rotation(-delta_y * 0.01)

        self.view_state = self.raytracing_data.update_view_state(
            self.view_state, m)

        self.mouse = (event.x, event.y)

        self.redraw_if_initialized()
