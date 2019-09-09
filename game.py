import sys, pygame, math
pygame.init()

RED = 255, 0, 0
RECT_WIDTH = 23
RECT_HEIGHT = 15
BLACK = 0, 0, 0
WHITE = 255, 255, 255
SCREEN = pygame.display.set_mode([800, 600])
SPEED = [1, 1]
top = 1

class Rect(pygame.sprite.Sprite):
  """ This class is the boxes that need to be destroyed in order to win """
  def __init__(self, x, y, color):
    super(Rect, self).__init__()
    self.image = pygame.Surface([RECT_WIDTH, RECT_HEIGHT])
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y


class Ball(pygame.sprite.Sprite):
  """ This class is the ball that breaks blocks and bounces off the player class """
  def __init__(self):
    super(Ball, self).__init__()
    self.width, self.height = 15, 15
    self.image = pygame.Surface([self.width, self.height])
    self.rect = self.image.get_rect()
    self.image.fill(WHITE)
    self.rect.x = pygame.display.get_surface().get_width() / 2 - 15 / 2
    self.rect.y = pygame.display.get_surface().get_height() - 47

class Player(pygame.sprite.Sprite):
  """ This class is the bar at the bottom of the screen that the player controls """
  def __init__(self):
    super(Player, self).__init__()
    self.height = 10
    self.width = 100
    self.image = pygame.Surface([self.width, self.height])
    self.image.fill(WHITE)
    self.rect = self.image.get_rect()
    self.screen_width = pygame.display.get_surface().get_width()
    self.screen_height = pygame.display.get_surface().get_height()
    self.rect.x = (self.screen_width / 2) - 50
    self.rect.y = self.screen_height - 30


clock = pygame.time.Clock()
# Sprite group for rectangles
rects = pygame.sprite.Group()
# Initialize player
player = Player()
# Initialize ball
ball = Ball()

# Group to render all sprites
allsprites = pygame.sprite.Group()
allsprites.add(player)
allsprites.add(ball)

# Create the rectangles to be rendered
for row in range(16):
  for column in range(32):
    rect = Rect(column * (RECT_WIDTH + 2) + 1, top, RED)
    rects.add(rect)
    allsprites.add(rect)
  top += RECT_HEIGHT + 2



def main():

  while 1:
    
    if ball.rect.y == 0:
      ball.rect.y += 0.5

    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()

    SCREEN.fill(BLACK)
    allsprites.draw(SCREEN)

    # Player movement
    if pygame.key.get_pressed()[pygame.K_LEFT] and player.rect.x != 0:
      player.rect.x -= SPEED[0]
    if pygame.key.get_pressed()[pygame.K_RIGHT] and player.rect.x != 800 - player.width:
      player.rect.x += SPEED[0]

    pygame.display.flip()

main()