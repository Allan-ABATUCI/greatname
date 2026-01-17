from game import WIDTH, HEIGHT
class GameObject:
    def __init__(self, image, height, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)

    def move(self, up=False, down=False, left=False, right=False):
        if right:
            self.pos.right += self.speed
        if left:
            self.pos.right -= self.speed
        if down:
            self.pos.top += self.speed
        if up:
            self.pos.top -= self.speed
        if self.pos.right > WIDTH:
            self.pos.left = 0
        if self.pos.top > HEIGHT-self.image.get_height():
            self.pos.top = 0
        if self.pos.right < self.image.get_width():
            self.pos.right = WIDTH
        if self.pos.top < 0:
            self.pos.top = HEIGHT-self.image.get_height()

