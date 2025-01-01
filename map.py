import pygame
from bob import Bob
from food import Food


class Map:
    def __init__(self, width, height, chunk_size=50):
        self.width, self.height = width, height
        self.chunk_size = chunk_size
        self.border_color = "gray"
        self.border_thickness = 5
        self.show_grid = False
        self.grid = self.create_grid()

    def create_grid(self):
        # Créer une grille où chaque cellule est une liste de Bobs (au début vide)
        grid = []
        for y in range(0, self.height, self.chunk_size):
            row = []
            for x in range(0, self.width, self.chunk_size):
                row.append([])  # Liste vide pour chaque cellule
            grid.append(row)
        return grid

    def assign_bob_to_grid(self, bob):
        # Calculer la position de la cellule dans laquelle le Bob se trouve
        grid_x = int(bob.pos.x // self.chunk_size)
        grid_y = int(bob.pos.y // self.chunk_size)

        # Vérifier que les coordonnées sont valides dans la grille
        if grid_x < len(self.grid[0]) and grid_y < len(self.grid):
            self.grid[grid_y][grid_x].append(bob)

    def get_bobs_around(self, x, y):
        bobs = []
        foods = []

        # Parcourir les chunks autour de (x, y) dans un rayon de 1
        for dx in range(-1, 2):  # -1, 0, 1
            for dy in range(-1, 2):  # -1, 0, 1
                new_x = x + dx
                new_y = y + dy

                # Vérifier que new_x et new_y sont dans les limites de la grille
                if 0 <= new_x < len(self.grid[0]) and 0 <= new_y < len(self.grid):
                    # Assuming you want to access map.grid[new_y][new_x] and check its type:
                    objs = self.grid[new_y][new_x]

                    for obj in objs:
                        # Check if it's an instance of Bob
                        if isinstance(obj, Bob):
                            bobs.append(obj)  # or += depending on what you're trying to achieve

                        # Check if it's an instance of Food
                        elif isinstance(obj, Food):
                            # Do whatever you need to do with Food objects
                            foods.append(obj)

        return bobs, foods

    def draw(self, screen):
        # Draw the border
        pygame.draw.rect(screen, self.border_color, (0, 0, self.width, self.height), self.border_thickness)

        if self.show_grid:
            # Draw vertical grid lines
            for x in range(0, self.width, self.chunk_size):
                pygame.draw.line(screen, self.border_color, (x, 0), (x, self.height), 1)

            # Draw horizontal grid lines
            for y in range(0, self.height, self.chunk_size):
                pygame.draw.line(screen, self.border_color, (0, y), (self.width, y), 1)
