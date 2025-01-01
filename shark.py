import heapq
import math

import pygame
import random


class Shark:
    def __init__(self, map, champ_de_vision=330, distance_de_vue=25):
        self.pos = pygame.Vector2(random.randint(0, map.width), random.randint(0, map.height))
        self.size = 8
        self.speed = 180
        self.direction = pygame.Vector2(
            (random.random() * 2 - 1),
            (random.random() * 2 - 1)
        ).normalize()
        self.champ_de_vision = champ_de_vision
        self.distance_de_vue = distance_de_vue
        self.show_direction = False
        self.show_vision = False

    def draw(self, screen, map, dt):
        pygame.draw.circle(screen, "red", self.pos, self.size)

        self.draw_vision(screen)

        self.pos.y += self.direction.y * dt * self.speed
        self.pos.x += self.direction.x * dt * self.speed

        self.border_touched(map)

    def draw_vision(self, screen):
        size = self.distance_de_vue
        line_width = 1

        # Calculer la position finale de la ligne directionnelle
        direction_vector = pygame.Vector2(self.direction.x, self.direction.y).normalize()
        end_pos = self.pos + direction_vector * size

        if self.show_direction:
            # Dessiner la ligne directionnelle en bleu
            pygame.draw.line(screen, "blue", self.pos, end_pos, line_width)

        # Calculer les angles pour le champ de vision
        angle_offset = math.radians(self.champ_de_vision / 2)  # Convertir en radians la moitié de l'angle
        direction_angle = math.atan2(direction_vector.y, direction_vector.x)

        if self.show_vision:
            # Ligne de champ de vision gauche
            left_angle = direction_angle - angle_offset
            left_vector = pygame.Vector2(math.cos(left_angle), math.sin(left_angle))
            left_end_pos = self.pos + left_vector * size
            pygame.draw.line(screen, "green", self.pos, left_end_pos, line_width)

            # Ligne de champ de vision droite
            right_angle = direction_angle + angle_offset
            right_vector = pygame.Vector2(math.cos(right_angle), math.sin(right_angle))
            right_end_pos = self.pos + right_vector * size
            pygame.draw.line(screen, "green", self.pos, right_end_pos, line_width)

    def border_touched(self, map):

        if self.pos.y - self.size / 2 < map.border_thickness:
            self.pos.y = map.height - map.border_thickness * 2
            return True
        elif self.pos.y + self.size / 2 > map.height - map.border_thickness:
            self.pos.y = map.border_thickness * 2
            return True

        if self.pos.x - self.size / 2 < map.border_thickness:
            self.pos.x = map.width - map.border_thickness * 2
            return True
        elif self.pos.x + self.size / 2 > map.width - map.border_thickness:
            self.pos.x = map.border_thickness * 2
            return True

        return False

    def get_grid_coordinates(self, chunk_size):
        # Calculer les coordonnées de la cellule de la grille
        grid_x = int(self.pos.x // chunk_size) - 1
        grid_y = int(self.pos.y // chunk_size) - 1
        return grid_x, grid_y

    def get_sorted_neighbors(self, other_bobs, max_n=8):
        # Filter out 'self' from the list of bobs and calculate distances only for those in the distance range
        filtered_bobs = []

        # Define the minimum and maximum distance thresholds
        # min_distance = self.size * 8
        min_distance = 0
        max_distance = self.distance_de_vue

        # Iterate over the other bobs
        for other_bob in other_bobs:

            # Skip if the other bob is the same as 'self'
            if other_bob == self:
                continue

            # Calculate the distance between the two bobs
            distance = self.pos.distance_to(other_bob.pos)

            # Check if the distance is within the defined range
            if min_distance <= distance <= max_distance:
                # If so, add the other bob and the distance to the filtered list
                filtered_bobs.append((other_bob, distance))

        # Obtenir les 6 Bobs les plus proches sans trier toute la liste
        filtered_bobs = heapq.nsmallest(max_n, filtered_bobs, key=lambda x: x[1])

        # Extract just the bobs (not distances) from the sorted list
        sorted_bobs = [bob for bob, _ in filtered_bobs]

        return sorted_bobs

    def get_closest_neighbors_in_vision(self, sorted_bobs, top_n=6):
        # Liste pour stocker les voisins dans le champ de vision
        neighbors_in_vision = []

        # Parcourir les Bobs triés pour trouver ceux dans le champ de vision
        for other_bob in sorted_bobs:
            if self.is_in_vision(other_bob):
                neighbors_in_vision.append(other_bob)
                # Arrêter si nous avons atteint le nombre désiré de voisins
                if len(neighbors_in_vision) >= top_n:
                    break

        return neighbors_in_vision

    def is_in_vision(self, other_bob):
        """# Calculer le vecteur directionnel de Bob
        direction_vector = pygame.Vector2(self.direction.x, self.direction.y).normalize()

        # Calculer le vecteur entre Bob et l'autre Bob
        vector_to_other = other_bob.pos - self.pos

        # Calculer l'angle entre le vecteur directionnel et le vecteur vers l'autre Bob
        angle_to_other = math.atan2(vector_to_other.y, vector_to_other.x)
        direction_angle = math.atan2(direction_vector.y, direction_vector.x)
        angle_diff = (angle_to_other - direction_angle) % (2 * math.pi)

        # Vérifier si cet angle est dans le champ de vision
        half_fov = math.radians(self.champ_de_vision / 2)
        if -half_fov <= angle_diff <= half_fov:"""
        distance = self.pos.distance_to(other_bob.pos)
        if distance <= self.distance_de_vue:
            return True

        return False

    def turn_towards(self, target_bob, degrees=5.0):
        if target_bob is None:
            return False
        if target_bob.pos == self.pos:
            return False

        # Calculer le vecteur directionnel actuel de Bob
        current_direction = pygame.Vector2(self.direction.x, self.direction.y).normalize()

        # Calculer le vecteur directionnel vers l'autre Bob
        direction_to_target = (target_bob.pos - self.pos).normalize()

        # Convertir les vecteurs en angles en radians
        current_angle = math.atan2(current_direction.y, current_direction.x)
        target_angle = math.atan2(direction_to_target.y, direction_to_target.x)

        # Calculer l'angle de rotation en radians
        angle_difference = (target_angle - current_angle) % (2 * math.pi)
        if angle_difference > math.pi:
            angle_difference -= 2 * math.pi  # S'assurer que l'angle est dans [-π, π]

        # Limiter la rotation à `degrees`
        rotation_radians = math.radians(degrees)
        if abs(angle_difference) <= rotation_radians:
            # Si l'angle de différence est petit, ajuster directement la direction
            new_angle = target_angle
        else:
            # Sinon, tourner progressivement vers la cible
            new_angle = current_angle + rotation_radians * (1 if angle_difference > 0 else -1)

        # Mettre à jour la direction de Bob avec le nouvel angle
        self.direction.x = math.cos(new_angle)
        self.direction.y = math.sin(new_angle)

        return True

    def manage(self, map, bobs_list):
        if len(bobs_list) != 0:
            sorted_bobs = self.get_sorted_neighbors(bobs_list)
            bobs_to_follow = self.get_closest_neighbors_in_vision(sorted_bobs, 1)
            for other_bob in bobs_to_follow:
                self.turn_towards(other_bob, 6)
            for bob in bobs_list:
                distance = self.pos.distance_to(bob.pos)
                if distance < bob.size + self.size:
                    if bob in bobs_list:
                        bobs_list.remove(bob)