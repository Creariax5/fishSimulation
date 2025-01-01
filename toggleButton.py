import pygame

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class ToggleButton:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = RED  # Start with "off" color
        self.text = text
        self.font = pygame.font.Font(None, 16)
        self.active = False  # Toggle state (False = off, True = on)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.text:
            text_surf = self.font.render(self.text, True, "black")
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Toggle state
                self.clicked()
                return self.active
        return None

    def clicked(self):
        # Toggle state
        self.active = not self.active
        self.color = GREEN if self.active else RED
