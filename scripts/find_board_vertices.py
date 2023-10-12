import pygame, json, sys, random
from pygame.time import Clock

sys.path.extend("../")
from spirit_island import launcher
from spirit_island.ui.inside_land import is_point_inside_polygon

pygame.init()


FPS = 60
WIDTH = 800
HEIGHT = 600
BOARD_IMAGE = pygame.image.load("./spirit_island/resources/board_d.png")

def add(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]

class BoardViewer():

    def __init__(self):
        self.clock = Clock()
        self.offset = [0, 0]

    def keys_pressed(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.offset[1] += 10
        if keys[pygame.K_s]:
            self.offset[1] -= 10
        if keys[pygame.K_a]:
            self.offset[0] += 10
        if keys[pygame.K_d]:
            self.offset[0] -= 10

    def run(self):
        display = pygame.display.set_mode((WIDTH, HEIGHT))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_button_up()
                if event.type == pygame.KEYUP:
                    self.key_up(event.key)
            self.keys_pressed()
            self.render(display)
            pygame.display.flip()
            self.clock.tick(FPS)

    def render(self):
        # No-op for override
        pass
    
    def mouse_button_up(self):
        # No-op for override
        pass

    def key_up(self, key):
        # No-op for override
        pass

class FindVertices(BoardViewer):

    def __init__(self):
        super().__init__()
        self.vertices = []

    def render(self, display):
        display.fill((0, 0, 0))
        rect = BOARD_IMAGE.get_rect()
        rect.topleft = self.offset
        display.blit(BOARD_IMAGE, rect)
        
        for i in range(len(self.vertices) - 1):
            pygame.draw.line(
                display, 
                (255, 0, 0),
                add(self.vertices[i], self.offset),
                add(self.vertices[i + 1], self.offset), 3)
    
    def mouse_button_up(self):
        mouse_pos = pygame.mouse.get_pos()
        self.vertices.append([
            mouse_pos[0] - self.offset[0],
            mouse_pos[1] - self.offset[1]])

    def key_up(self, key):
        if key == pygame.K_z:
            self.vertices = self.vertices[:-1]
        elif key == pygame.K_p:
            with open("./coords_d.txt", "w") as f:
                for vertex in self.vertices:
                    f.write(f"{vertex[0]},{vertex[1]}\n")

    def render(self, display):
        display.fill((0, 0, 0))
        rect = BOARD_IMAGE.get_rect()
        rect.topleft = self.offset
        display.blit(BOARD_IMAGE, rect)
        
        for i in range(len(self.vertices) - 1):
            pygame.draw.line(
                display, 
                (255, 0, 0),
                add(self.vertices[i], self.offset),
                add(self.vertices[i + 1], self.offset), 3)

class CreateLands(BoardViewer):

    def __init__(self):
        super().__init__()
        with open("./coords_d_all.txt") as f:
            contents = f.read()
        self.vertices = [(int(line.split(",")[0]), int(line.split(",")[1])) for line in contents.split("\n")]
        self.selected_vertices = []
        self.land_number = 0

    def get_nearest_vertex(self, target):
        closest_vertex = None
        min_distance = 100000
        for vertex in self.vertices:
            distance =  abs(target[0] - vertex[0]) + abs(target[1] - vertex[1])
            if distance < min_distance:
                min_distance = distance
                closest_vertex = vertex
        return closest_vertex
        
    def mouse_button_up(self):
        self.selected_vertices.append(self.get_nearest_vertex((pygame.mouse.get_pos()[0] - self.offset[0], pygame.mouse.get_pos()[1] - self.offset[1])))

    def key_up(self, key):
        if key == pygame.K_p:
            with open(f"./board_d_land_{self.land_number}.csv", "w") as f:
                for vertex in self.selected_vertices:
                    f.write(f"{vertex[0]},{vertex[1]}\n")
            self.selected_vertices = []
            self.land_number += 1

    def render(self, display):
        display.fill((0, 0, 0))
        rect = BOARD_IMAGE.get_rect()
        rect.topleft = self.offset
        display.blit(BOARD_IMAGE, rect)
        
        for vertex in self.vertices:
            pygame.draw.circle(
                display,
                (0, 255, 0) if vertex in self.selected_vertices else (255, 0, 0),
                add(vertex, self.offset),
                3
            )

        for vertex in range(len(self.selected_vertices)):
            pygame.draw.line(
                display,
                (0, 255, 0),
                add(self.selected_vertices[vertex], self.offset),
                add(self.selected_vertices[(vertex + 1) % len(self.selected_vertices)], self.offset),
                2)

class TestLands(BoardViewer):
    def __init__(self):
        super().__init__()
        self.lands = launcher.read_json("./spirit_island/resources/board_d_coords.json")
        self.inside_points_image = BOARD_IMAGE
        for land in range(9):
            colour = [int(random.random() * 255) for _ in range(3)]
            for point in self.get_inside_coords(land):
                pygame.draw.circle(self.inside_points_image, colour, point, 5)

    def get_inside_coords(self, land):
        inside_points = []
        for i in range(200):
            for j in range(200):
                if is_point_inside_polygon(self.lands[f"{land}"], (10 * i, 10 * j)):
                    inside_points.append((10 * i, 10 * j))
        return inside_points

    def render(self, display):
        display.fill((0, 0, 0))
        rect = self.inside_points_image.get_rect()
        rect.topleft = self.offset
        display.blit(self.inside_points_image, rect)

class PickLandLocations(BoardViewer):

    def __init__(self):
        super().__init__()
        self.selected_locations = []
        self.location_width = 50

    def mouse_button_up(self):
        self.selected_locations.append([pygame.mouse.get_pos()[0] - self.offset[0], pygame.mouse.get_pos()[1] - self.offset[1]])

    def key_up(self, key):
        if key == pygame.K_z:
            self.selected_locations = self.selected_locations[:-1]
        if key == pygame.K_p:
            with open(f"./board_d_land_locations.csv", "w") as f:
                for vertex in self.selected_locations:
                    f.write(f"{vertex[0]},{vertex[1]}\n")
            
    def render(self, display):
        display.fill((0, 0, 0))
        rect = BOARD_IMAGE.get_rect()
        rect.topleft = self.offset
        display.blit(BOARD_IMAGE, rect)
        for location in self.selected_locations:
            pygame.draw.rect(display, (255, 0, 0), pygame.rect.Rect(location[0] + self.offset[0], location[1] + self.offset[1], self.location_width, self.location_width))

def write_to_json():
    with open("./board_d.json", "w") as board_json:
        board = {}
        for i in range(9):
            with open(f"./board_d_land_{i}.csv", "r") as f:
                contents = f.read()
            board[i] = [(int(line.split(",")[0]), int(line.split(",")[1])) for line in contents.split("\n") if line]
        board_json.write(json.dumps(board))

def write_land_locations_json():
    lands = launcher.read_json("./spirit_island/resources/board_d_coords.json")
    with open("./board_d_land_locations.csv", "r") as f:
        locations = f.read().split("\n")[:-1]
    location_by_land = {}
    for raw_location in locations:
        location = [int(raw_location.split(",")[0]), int(raw_location.split(",")[1])]
        land_found = False
        for i in range(9):
            if is_point_inside_polygon(lands[str(i)], location):
                if land_found:
                    print("Problem")
                land_found = True
                if str(i) in location_by_land:
                    location_by_land[str(i)].append(location)
                else:
                    location_by_land[str(i)] = [location]
        if not land_found:
            print(f"{location} not in any land")
    with open("./board_d_land_locations.json", "w") as dest:
        dest.write(json.dumps(location_by_land))

if __name__ == "__main__":
    # FindVertices().run() # Click all the vertices, pan with wasd and click p to save (z to remove a vertex, you can ignore the red lines)
    # CreateLands().run() # Click round the vertices of a land and click p to save and move on to th next land
    # TestLands().run() # Check visually that all the lands look right
    # PickLandLocations().run() # Choose places within lands to draw things
    write_land_locations_json()
    # write_to_json()