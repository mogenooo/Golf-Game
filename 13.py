import py5

# ボールの位置と速度
ball_pos = [0, 100, 0]
ball_speed = [0, 0, 0]

# 穴の位置
hole_pos = [200, 0, 200]
hole_radius = 50

# 重力
gravity = -0.5
is_jumping = False

# CameraControlクラス
class CameraControl:
    def __init__(self):
        self.WH = 500
        self.eye = py5.Py5Vector(0, self.WH/2, 0)
        self.center = py5.Py5Vector(0, 0, 0)
        self.down = py5.Py5Vector(0, 0, -1)
        self.MIN = 100

    def camera(self):
        py5.camera(self.eye.x, self.eye.y, self.eye.z,
                   self.center.x, self.center.y, self.center.z,
                   self.down.x, self.down.y, self.down.z)

    def lights(self):
        py5.directional_light(255, 0, 0, -1, 0, 0)
        py5.directional_light(255, 255, 0, 1, 0, 0)
        py5.directional_light(0, 255, 0, 0, -1, 0)
        py5.directional_light(0, 255, 255, 0, 1, 0)
        py5.directional_light(0, 0, 255, 0, 0, -1)
        py5.directional_light(255, 0, 255, 0, 0, 1)
        
    def mouse_dragged(self):
        s = py5.get_current_sketch()
        if s.is_key_pressed and s.key == py5.CODED:
            if s.key_code == py5.CONTROL:
                self.siten_okuyuki(s)
        else:
            self.siten_yoko(s)
            self.siten_tate(s)

    def siten_okuyuki(self, s):
        v1 = self.eye - self.center
        v1.normalize()
        v1 *= s.mouse_y - s.pmouse_y
        self.eye += v1
        if self.eye.dist(self.center) < self.MIN:
            self.eye -= v1

    def siten_yoko(self, s):
        v1 = self.eye - self.center
        len = v1.mag
        v2 = self.down.cross(v1)
        v2.normalize()
        v2 *= s.mouse_x - s.pmouse_x
        v1 += v2
        v1.mag = len
        self.eye = self.center + v1

    def siten_tate(self, s):
        v1 = self.eye - self.center
        len = v1.mag
        v2 = v1 + self.down * (s.mouse_y - s.pmouse_y)
        v2.mag = len
        self.eye = self.center + v2
        v3 = v2.cross(self.down)
        self.down = v3.cross(v2)
        self.down.normalize()

camera_control = CameraControl()

def setup():
    py5.size(500, 500, py5.P3D)
    py5.frame_rate(30)

def draw():
    py5.background(0)  # 背景を黒に変更
    camera_control.camera()
    camera_control.lights()

    # 床の描画（床の位置を調整して上下反転を修正）
    py5.fill(100, 200, 100)
    py5.rect_mode(py5.CENTER)
    py5.push_matrix()
    py5.translate(0, 0, 0)  # 床の位置を調整
    py5.box(600, 10, 600)
    py5.pop_matrix()

    # 穴の描画（円で代用）
    py5.fill(0, 0, 200)
    py5.push_matrix()
    py5.translate(hole_pos[0], hole_pos[1] + 5, hole_pos[2])
    py5.rotate_x(py5.HALF_PI)  # 円を水平に描画
    py5.ellipse(0, 0, hole_radius * 2, hole_radius * 2)
    py5.pop_matrix()

    # ボールの描画
    py5.fill(255, 0, 0)
    py5.push_matrix()
    py5.translate(ball_pos[0], ball_pos[1], ball_pos[2])
    py5.sphere(20)
    py5.pop_matrix()

    # ボールの物理演算
    update_ball()

    # 勝利判定
    if check_collision():
        py5.fill(255)  # Winの文字を白に設定
        py5.text_size(32)
        py5.text("You Win!", 300, 400)

def mouse_dragged():
    camera_control.mouse_dragged()

def key_pressed():
    global is_jumping
    if py5.key == py5.CODED:
        if py5.key_code == py5.UP:
            ball_speed[2] = -5
        elif py5.key_code == py5.DOWN:
            ball_speed[2] = 5
        elif py5.key_code == py5.LEFT:
            ball_speed[0] = -5
        elif py5.key_code == py5.RIGHT:
            ball_speed[0] = 5
    elif py5.key == ' ' and not is_jumping:
        ball_speed[1] = 10
        is_jumping = True

def key_released():
    if py5.key == py5.CODED:
        if py5.key_code in [py5.UP, py5.DOWN]:
            ball_speed[2] = 0
        elif py5.key_code in [py5.LEFT, py5.RIGHT]:
            ball_speed[0] = 0

def update_ball():
    global is_jumping
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]
    ball_pos[2] += ball_speed[2]

    # 重力の適用
    if ball_pos[1] > 20:
        ball_speed[1] += gravity
    else:
        ball_pos[1] = 20
        ball_speed[1] = 0
        is_jumping = False

def check_collision():
    dist_to_hole = ((ball_pos[0] - hole_pos[0])**2 +
                    (ball_pos[1] - hole_pos[1])**2 +
                    (ball_pos[2] - hole_pos[2])**2)**0.5
    return dist_to_hole < hole_radius

py5.run_sketch()