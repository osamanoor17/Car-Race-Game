import random
import pygame
from pathlib import Path
from time import sleep

class CarRacing:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.screen = None
        self.asset_path = Path(__file__).parent / "img"
        self.score_file = Path(__file__).parent / "scores.txt"

        self.road_left = 280
        self.road_right = 520

        self.font_large = pygame.font.SysFont("comicsansms", 72, True)
        self.font_medium = pygame.font.SysFont("comicsansms", 36, True)
        self.font_small = pygame.font.SysFont("lucidaconsole", 20)

        self.load_assets()
        pygame.display.set_icon(self.icon_image)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Car Race')

        self.player_name = self.ask_player_name()
        self.show_start_menu()
        self.start_game()

    def load_assets(self):
        try:
            self.car_image = pygame.image.load(self.asset_path / "car.png")
            enemy_raw = pygame.image.load(self.asset_path / "enemy_car_2.png")
            self.enemy_car_image = pygame.transform.flip(enemy_raw, False, True)
            self.background_image = pygame.image.load(self.asset_path / "back_ground.jpg")
            self.icon_image = pygame.image.load(self.asset_path / "icon.png")
        except FileNotFoundError as e:
            print(f"Error loading images: {e}")
            pygame.quit()
            exit()

    def ask_player_name(self):
        name = ""
        active = True
        input_rect = pygame.Rect(self.screen_width // 2 - 150, 250, 300, 50)

        while active:
            self.screen.fill(self.black)
            title = self.font_large.render("Enter Your Name", True, self.white)
            name_text = self.font_medium.render(name, True, self.white)
            pygame.draw.rect(self.screen, self.white, input_rect, 2)

            self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 150))
            self.screen.blit(name_text, (input_rect.x + 10, input_rect.y + 1))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name.strip():
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 15:
                            name += event.unicode

        return name.strip()

    def setup_game(self):
        self.is_crashed = False
        self.car_x = self.screen_width * 0.45
        self.car_y = self.screen_height * 0.8
        self.car_width = 49

        self.enemy_car_x = random.randrange(self.road_left, self.road_right - 50)
        self.enemy_car_y = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        self.bg_x1 = (self.screen_width / 2) - (360 / 2)
        self.bg_x2 = self.bg_x1
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.score = 0

    def draw_car(self):
        self.screen.blit(self.car_image, (self.car_x, self.car_y))

    def show_start_menu(self):
        waiting = True
        while waiting:
            self.screen.fill(self.black)
            title_text = self.font_large.render("Car Racing", True, self.white)
            start_text = self.font_medium.render("Press [SPACE] to Start", True, self.white)

            self.screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 200))
            self.screen.blit(start_text, (self.screen_width // 2 - start_text.get_width() // 2, 300))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def start_game(self):
        self.setup_game()
        self.run_game()

    def run_game(self):
        while not self.is_crashed:
            self.handle_events()
            self.update_game_state()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_crashed = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.car_x > self.road_left:
            self.car_x -= 5
        if keys[pygame.K_RIGHT] and self.car_x + self.car_width < self.road_right:
            self.car_x += 5

    def update_game_state(self):
        self.enemy_car_y += self.enemy_car_speed

        if self.enemy_car_y > self.screen_height:
            self.enemy_car_y = -self.enemy_car_height
            self.enemy_car_x = random.randrange(self.road_left, self.road_right - 50)

        if self.detect_collision():
            self.is_crashed = True
            self.save_score()
            self.show_game_over_menu()

        if self.score % 100 == 0 and self.score != 0:
            self.enemy_car_speed += 1
            self.bg_speed += 1

        self.score += 1

    def detect_collision(self):
        return (
            self.car_y < self.enemy_car_y + self.enemy_car_height and
            (
                (self.car_x > self.enemy_car_x and self.car_x < self.enemy_car_x + self.enemy_car_width) or
                (self.car_x + self.car_width > self.enemy_car_x and self.car_x + self.car_width < self.enemy_car_x + self.enemy_car_width)
            )
        )

    def render(self):
        self.screen.fill(self.black)
        self.render_background()
        self.screen.blit(self.enemy_car_image, (self.enemy_car_x, self.enemy_car_y))
        self.draw_car()
        self.display_score()
        pygame.display.update()

    def render_background(self):
        self.screen.blit(self.background_image, (self.bg_x1, self.bg_y1))
        self.screen.blit(self.background_image, (self.bg_x2, self.bg_y2))

        pygame.draw.line(self.screen, (255, 255, 0), (self.road_left, 0), (self.road_left, self.screen_height), 4)
        pygame.draw.line(self.screen, (255, 255, 0), (self.road_right, 0), (self.road_right, self.screen_height), 4)

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.screen_height:
            self.bg_y1 = -600
        if self.bg_y2 >= self.screen_height:
            self.bg_y2 = -600

    def save_score(self):
        try:
            with open(self.score_file, "a") as file:
                file.write(f"{self.player_name},{self.score}\n")
        except Exception as e:
            print("Error saving score:", e)

    def read_top_scores(self):
        try:
            if not self.score_file.exists():
                return []

            with open(self.score_file, "r") as file:
                lines = file.readlines()

            scores = [line.strip().split(",") for line in lines]
            scores = sorted(scores, key=lambda x: int(x[1]), reverse=True)
            return scores[:5]
        except:
            return []

    def show_game_over_menu(self):
        top_scores = self.read_top_scores()
        waiting = True
        while waiting:
            self.screen.fill(self.black)
            over_text = self.font_large.render("Game Over", True, self.white)
            score_text = self.font_medium.render(f"Score: {self.score}", True, self.white)
            restart_text = self.font_medium.render("Press [R] to Restart or [Q] to Quit", True, self.white)

            self.screen.blit(over_text, (self.screen_width // 2 - over_text.get_width() // 2, 100))
            self.screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, 200))
            self.screen.blit(restart_text, (self.screen_width // 2 - restart_text.get_width() // 2, 300))

            y = 380
            self.screen.blit(self.font_medium.render("Top Scores", True, self.white), (self.screen_width // 2 - 100, y))
            y += 60
            col_name_x = self.screen_width // 2 - 100
            col_score_x = self.screen_width // 2 + 50
            for name, score in top_scores:
                name_surface = self.font_small.render(name, True, self.white)
                score_surface = self.font_small.render(score, True, self.white)
                self.screen.blit(name_surface, (col_name_x, y))
                self.screen.blit(score_surface, (col_score_x, y))
                y += 25
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                        self.start_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()

    def display_score(self):
        text = self.font_small.render(f"{self.player_name} - Score: {self.score}", True, self.white)
        self.screen.blit(text, (10, 10))

if __name__ == '__main__':
    CarRacing()
