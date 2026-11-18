import math
import random
import pygame

# Initialize Pygame
pygame.init()

# Screen & Pixel Grid Setup (160x160 grid scaled up 4x to 640x640)
SCALE = 4
GRID_W, GRID_H = 160, 160
WIDTH, HEIGHT = GRID_W * SCALE, GRID_H * SCALE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loves Me, Loves Me Not")
pixel_surface = pygame.Surface((GRID_W, GRID_H))

# Night Sky Color Palette
night_sky_palette = [
    ("Void Black", "#070B19"),  # 0
    ("Midnight Navy", "#0F172A"),  # 1
    ("Deep Indigo", "#1E1B4B"),  # 2
    ("Twilight Blue", "#1E3A8A"),  # 3
    ("Nebula Violet", "#3B0764"),  # 4
    ("Cosmic Purple", "#581C87"),  # 5
    ("Starlight Blue", "#3B82F6"),  # 6
    ("Moonlight Silver", "#CBD5E1"),  # 7
    ("Starry Gold", "#FDE047"),  # 8
]

# Palette Assignments
SKY_BANDS = [
    night_sky_palette[0][1],  # Void Black (top)
    night_sky_palette[1][1],  # Midnight Navy
    night_sky_palette[2][1],  # Deep Indigo
    night_sky_palette[4][1],  # Nebula Violet (horizon glow)
]
MOON_COLOR = night_sky_palette[7][1]  # Moonlight Silver
STAR_GOLD = night_sky_palette[8][1]  # Starry Gold
STAR_BLUE = night_sky_palette[6][1]  # Starlight Blue
TEXT_LIGHT = night_sky_palette[7][1]  # Moonlight Silver

# Purple & Lavender Tones for the Petals (matching Cosmic Purple & Nebula Violet)
PETAL_MAIN = (168, 85, 247)  # Glowing Cosmic Lavender
PETAL_HIGHLIGHT = (216, 180, 254)  # Soft Starlit Lilac
PETAL_SHADOW = night_sky_palette[5][1]  # Cosmic Purple (#581C87)

# Night-adjusted grass, stem, and center colors
GRASS_DARK = (18, 48, 32)
GRASS_GREEN = (28, 72, 45)
STEM_GREEN = (38, 98, 72)
STEM_DARK = (20, 55, 40)
CENTER_YELLOW = night_sky_palette[8][1]  # Starry Gold
CENTER_ORANGE = (217, 119, 6)

# Fonts
font = pygame.font.SysFont("couriernew", 26, bold=True)
small_font = pygame.font.SysFont("couriernew", 16, bold=True)

# Twinkling Stars: (x, y, color, twinkle_speed, phase_offset)
stars = [
    (
        random.randint(4, GRID_W - 4),
        random.randint(4, 128),
        random.choice([STAR_GOLD, STAR_BLUE, MOON_COLOR]),
        random.uniform(0.04, 0.12),
        random.uniform(0, math.pi * 2),
    )
    for _ in range(42)
]


class ShootingStar:

  def __init__(self):
    self.active = False
    self.timer = random.randint(120, 300)
    self.x = 0.0
    self.y = 0.0
    self.vx = 0.0
    self.vy = 0.0
    self.life = 0

  def update(self):
    if not self.active:
      self.timer -= 1
      if self.timer <= 0:
        self.spawn()
    else:
      self.x += self.vx
      self.y += self.vy
      self.life -= 1
      if self.life <= 0 or self.x > GRID_W or self.y > 125:
        self.active = False
        self.timer = random.randint(180, 420)

  def spawn(self):
    self.active = True
    self.x = random.randint(10, 90)
    self.y = random.randint(6, 35)
    self.vx = random.uniform(1.8, 2.6)
    self.vy = random.uniform(0.7, 1.2)
    self.life = random.randint(22, 35)

  def draw(self, surf):
    if not self.active:
      return
    # Draw bright head and fading tail
    head_x, head_y = int(self.x), int(self.y)
    tail_x, tail_y = int(self.x - self.vx * 4), int(self.y - self.vy * 4)
    pygame.draw.line(surf, STAR_BLUE, (tail_x, tail_y), (head_x, head_y), 1)
    surf.set_at((head_x, head_y), STAR_GOLD)


class Petal:

  def __init__(self, angle_deg):
    self.angle = math.radians(angle_deg)
    self.attached = True
    self.falling = False
    self.x = 80.0
    self.y = 82.0
    self.vx = 0.0
    self.vy = 0.0
    self.rot_speed = 0.0

  def pluck(self):
    if self.attached:
      self.attached = False
      self.falling = True
      self.vx = math.cos(self.angle) * 0.4 + random.uniform(-0.2, 0.2)
      self.vy = -0.6
      self.rot_speed = random.uniform(-0.06, 0.06)

  def update(self):
    if self.falling:
      self.x += self.vx
      self.y += self.vy
      self.vy += 0.04
      self.vx += math.sin(self.y * 0.15) * 0.03
      self.angle += self.rot_speed

      if self.y > GRID_H + 25:
        self.falling = False

  def draw(self, surf):
    if not self.attached and not self.falling:
      return

    cos_a = math.cos(self.angle)
    sin_a = math.sin(self.angle)

    # Cosmic Purple shadow layer
    for dist in range(10, 25, 3):
      px = int(self.x + cos_a * dist)
      py = int(self.y + sin_a * dist)
      radius = 4 if dist < 21 else 3
      pygame.draw.circle(surf, PETAL_SHADOW, (px, py + 1), radius)

    # Glowing Lavender main petal layer
    for dist in range(10, 25, 3):
      px = int(self.x + cos_a * dist)
      py = int(self.y + sin_a * dist)
      radius = 4 if dist < 21 else 3
      pygame.draw.circle(surf, PETAL_MAIN, (px, py), radius)

    # Inner lilac highlight
    for dist in range(12, 20, 4):
      px = int(self.x + cos_a * dist)
      py = int(self.y + sin_a * dist)
      pygame.draw.circle(surf, PETAL_HIGHLIGHT, (px, py - 1), 1)

  def is_clicked(self, gx, gy):
    if not self.attached:
      return False
    tip_x = self.x + math.cos(self.angle) * 18
    tip_y = self.y + math.sin(self.angle) * 18
    return math.hypot(gx - tip_x, gy - tip_y) < 7


def create_flower():
  num_petals = random.randint(9, 14)
  return [Petal(i * (360 / num_petals)) for i in range(num_petals)]


def draw_sky_gradient(surf):
  # Pixel-art style banded gradient with subtle dithering lines
  band_heights = [40, 40, 35, 25]
  y_cursor = 0
  for idx, color in enumerate(SKY_BANDS):
    h = band_heights[idx]
    pygame.draw.rect(surf, color, (0, y_cursor, GRID_W, h))
    # Add pixel dither transition at the bottom edge of each band
    if idx < len(SKY_BANDS) - 1:
      next_color = SKY_BANDS[idx + 1]
      for x in range(0, GRID_W, 2):
        surf.set_at((x, y_cursor + h - 1), next_color)
        surf.set_at((x + 1, y_cursor + h), color)
    y_cursor += h


def draw_moon(surf):
  # Crescent Moon in top-right corner
  moon_x, moon_y = 132, 24
  pygame.draw.circle(surf, MOON_COLOR, (moon_x, moon_y), 10)
  # Carve crescent shadow using top sky color (Void Black)
  pygame.draw.circle(surf, SKY_BANDS[0], (moon_x - 4, moon_y - 3), 9)


def draw_scene(surf, petals, shooting_star, frame_tick):
  # 1. Sky Gradient & Moon
  draw_sky_gradient(surf)
  draw_moon(surf)

  # 2. Twinkling Stars
  for sx, sy, color, speed, phase in stars:
    pulse = math.sin(frame_tick * speed + phase)
    if pulse > -0.4:  # Briefly blink out when pulse is very low
      surf.set_at((sx, sy), color)
      # Add a tiny cross-sparkle on brightest stars
      if pulse > 0.85 and sy < 110:
        surf.set_at((sx - 1, sy), SKY_BANDS[2])
        surf.set_at((sx + 1, sy), SKY_BANDS[2])

  # 3. Shooting Star
  shooting_star.draw(surf)

  # 4. Ground with top grass edge
  pygame.draw.rect(surf, GRASS_DARK, (0, 138, GRID_W, 22))
  pygame.draw.rect(surf, GRASS_GREEN, (0, 138, GRID_W, 4))

  # 5. Stem & Leaves
  pygame.draw.rect(surf, STEM_DARK, (78, 82, 5, 58))
  pygame.draw.rect(surf, STEM_GREEN, (79, 82, 3, 58))

  pygame.draw.ellipse(surf, STEM_DARK, (63, 112, 16, 8))
  pygame.draw.ellipse(surf, STEM_GREEN, (64, 112, 14, 6))
  pygame.draw.ellipse(surf, STEM_DARK, (82, 104, 16, 8))
  pygame.draw.ellipse(surf, STEM_GREEN, (83, 104, 14, 6))

  # 6. Petals (attached first, falling on top)
  for p in petals:
    if p.attached:
      p.draw(surf)
  for p in petals:
    if p.falling:
      p.draw(surf)

  # 7. Flower Center (Starry Gold pistil)
  pygame.draw.circle(surf, CENTER_ORANGE, (80, 82), 10)
  pygame.draw.circle(surf, CENTER_YELLOW, (80, 81), 8)
  for dx, dy in [(-3, -2), (3, -3), (0, 2), (-4, 3), (4, 2)]:
    surf.set_at((80 + dx, 81 + dy), CENTER_ORANGE)


# Game State
petals = create_flower()
shooting_star = ShootingStar()
status_text = "Click a petal..."
plucked_count = 0
frame_tick = 0
clock = pygame.time.Clock()
running = True

while running:
  frame_tick += 1
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      mx, my = pygame.mouse.get_pos()
      gx, gy = mx // SCALE, my // SCALE

      attached_petals = [p for p in petals if p.attached]

      if attached_petals:
        clicked_petal = next(
            (p for p in attached_petals if p.is_clicked(gx, gy)), None
        )
        target = (
            clicked_petal if clicked_petal else random.choice(attached_petals)
        )

        target.pluck()
        plucked_count += 1
        status_text = (
            "Loves me!" if plucked_count % 2 == 1 else "Loves me not..."
        )
      else:
        petals = create_flower()
        status_text = "Click a petal..."
        plucked_count = 0

  # Update animations & physics
  shooting_star.update()
  for p in petals:
    p.update()

  # Render pixel art to low-res surface, then scale up cleanly
  draw_scene(pixel_surface, petals, shooting_star, frame_tick)
  scaled_surf = pygame.transform.scale(pixel_surface, (WIDTH, HEIGHT))
  screen.blit(scaled_surf, (0, 0))

  # Draw UI Text
  text_color = (
      STAR_GOLD
      if status_text == "Loves me!"
      else (STAR_BLUE if status_text == "Loves me not..." else TEXT_LIGHT)
  )
  text_surf = font.render(status_text, True, text_color)
  text_rect = text_surf.get_rect(center=(WIDTH // 2, 48))
  screen.blit(text_surf, text_rect)

  if not any(p.attached for p in petals):
    sub_surf = small_font.render(
        "Click anywhere for a new flower", True, TEXT_LIGHT
    )
    sub_rect = sub_surf.get_rect(center=(WIDTH // 2, 85))
    screen.blit(sub_surf, sub_rect)

  pygame.display.flip()
  clock.tick(60)

pygame.quit()

