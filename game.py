import pygame, math
pygame.init()

RED = 255, 0, 0
RECT_WIDTH = 23
RECT_HEIGHT = 15
BLACK = 0, 0, 0
WHITE = 255, 255, 255
SCREEN = pygame.display.set_mode([800, 600])
SPEED = 1
top = 25

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
  """ This class is the ball that breaks rectangles and bounces off the player class """
  def __init__(self):
    super(Ball, self).__init__()
    self.width, self.height = 15, 15
    self.image = pygame.Surface([self.width, self.height])
    self.rect = self.image.get_rect()
    self.image.fill(WHITE)
    self.screen_width = pygame.display.get_surface().get_width()
    self.screen_height = pygame.display.get_surface().get_height()
    self.x = self.screen_width / 2 - 15 / 2
    self.y = self.screen_height - 47
    self.speed = 0.5
    self.direction = 0

  def bounce(self, diff):
    """ This function will bounce the ball
        off a horizontal surface (not a vertical one) """

    self.direction = (180 - self.direction) % 360
    self.direction -= diff

  def update(self):
    # Determine speed and direction of ball movement
    direction_radians = math.radians(self.direction)
    self.x += self.speed * math.sin(direction_radians)
    self.y -= self.speed * math.cos(direction_radians)

    # Move the image to where our x and y are
    self.rect.x = self.x
    self.rect.y = self.y

    # Do we bounce off the top of the screen?
    if self.y <= 0:
      self.bounce(0)
      self.y = 1

    # Do we bounce off the left of the screen?
    if self.x <= 0:
      self.direction = (360 - self.direction) % 360
      self.x = 1

    # Do we bounce of the right side of the screen?
    if self.x > self.screen_width - self.width:
      self.direction = (360 - self.direction) % 360
      self.x = self.screen_width - self.width - 1

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

  def update(self):
    if pygame.key.get_pressed()[pygame.K_LEFT] and self.rect.x != 0:
      self.rect.x -= SPEED
    if pygame.key.get_pressed()[pygame.K_RIGHT] and self.rect.x != 800 - self.width:
      self.rect.x += SPEED


# Sprite group for rectangles
rects = pygame.sprite.Group()

# Initialize player
player = Player()

# Initialize ball
balls = pygame.sprite.Group()
ball = Ball()
balls.add(ball)

# Group to render all sprites
allsprites = pygame.sprite.Group()
allsprites.add(player)
allsprites.add(ball)

# Font for game messages
font = pygame.font.Font(None, 36)

score = 0

# Create the rectangles to be rendered
for row in range(16):
  for column in range(32):
    rect = Rect(column * (RECT_WIDTH + 2) + 1, top, RED)
    rects.add(rect)
    allsprites.add(rect)
  top += RECT_HEIGHT + 2

game_over = False

while 1:

  SCREEN.fill(BLACK)

  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

  # While game isn't over update player and ball position
  if not game_over:
    ball.update()
    player.update()

  # If game is over render "Game Over"
  if game_over:
    text = font.render("Game Over!", True, WHITE)
    text_pos = text.get_rect(centerx=800/2)
    text_pos.top = 300
    SCREEN.blit(text, text_pos)

  # If ball collides with player change the direction, takes into account left and right sides for diagonal movement
  if pygame.sprite.spritecollide(player, balls, False):
    diff = (player.rect.x + player.width / 2) - (ball.rect.x + ball.width / 2)
    ball.bounce(diff)

  # Add rects that ball collides with to new group
  dead_rects = pygame.sprite.spritecollide(ball, rects, True)

  # Keep moving ball as long as there are rects
  if len(dead_rects) > 0:
    ball.bounce(0)
  # End game if rects are 0 or if ball falls off bottom of screen
  if len(rects) == 0 or ball.y >= 600:
    game_over = True

  # Increase speed of ball as more rects get hit for difficulty
  for rect in dead_rects:
    ball.speed += 0.001
    score += 2

  score_text = font.render("Score: {0}".format(score), True, WHITE)
  score_pos = [1, 1]
  SCREEN.blit(score_text, score_pos)

  allsprites.draw(SCREEN)
  pygame.display.flip()
