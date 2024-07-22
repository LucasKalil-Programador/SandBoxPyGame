import random
import threading
import time

import pygame
import sys
import SandBox


def handle_actions(keys_pressed: dict[any, bool], on_key_click):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            keys_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            if keys_pressed.get(event.key, False):
                keys_pressed[event.key] = False
                on_key_click(event)


class Game:
    def __init__(self, size=(160, 160), scale=4.0, fps=60, font_size=30, test_mode=False):
        # Start variables
        self.performance_str = None
        self.size, self.scale, self.fps = size, scale, fps
        self.selected_item, self.spawn_radius = SandBox.Types.SAND, 10
        self.screen_size = (self.size[0] * self.scale, self.size[1] * self.scale)
        self.test_mode, self.performance_data, self.performance_str = test_mode, {}, ""
        self.paused = False
        self.keys_pressed = {}

        # Start
        self.sandBox = SandBox.SandBox(self.size)

        # Start pygame
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        pygame.display.set_caption("Sand box game")

        # Start pygame utils
        self.font = pygame.font.Font(None, font_size)
        self.fps_clock = pygame.time.Clock()

    def handle_key_inputs(self, event):
        key_to_item = {
            pygame.K_1: SandBox.Types.BG,
            pygame.K_2: SandBox.Types.SAND,
            pygame.K_3: SandBox.Types.WATER,
            pygame.K_4: SandBox.Types.STONE,
            pygame.K_5: SandBox.Types.VACUUM,
            pygame.K_6: SandBox.Types.CLONER,
        }

        if event.key == pygame.K_KP_PLUS and self.spawn_radius < min(self.size[0], self.size[1]):
            self.spawn_radius += 10 if pygame.key.get_pressed()[pygame.K_LCTRL] else 1
        elif event.key == pygame.K_KP_MINUS and self.spawn_radius > 1:
            self.spawn_radius -= 10 if pygame.key.get_pressed()[pygame.K_LCTRL] else 1
        elif event.key == pygame.K_p:
            self.paused = not self.paused
        elif event.key == pygame.K_r:
            self.performance_data = {}
            self.selected_item = SandBox.Types.SAND
            self.spawn_radius = 10
            self.sandBox.reset()
        elif event.key in key_to_item:
            for key, item in key_to_item.items():
                if key == event.key:
                    self.selected_item = item
                    break

    def handle_mouse_inputs(self):
        buttons_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if buttons_pressed[0]:
            pos = (int(mouse_pos[0] / self.scale), int(mouse_pos[1] / self.scale))
            self.sandBox.spawn(pos, self.spawn_radius, type_b=self.selected_item)

    def perform_random_spawn(self):
        type_b = random.choice(list(SandBox.Types))
        x, y = random.randint(0, self.size[0]), random.randint(0, self.size[1])
        self.sandBox.spawn((x, y), self.spawn_radius, type_b)

    def performance_monitor(self):
        current_fps = int(self.fps_clock.get_fps())
        if current_fps in self.performance_data:
            self.performance_data[current_fps] = self.performance_data[current_fps] + 1
        else:
            self.performance_data[current_fps] = 1

        fps_sum, occurrences_count = 0, 0
        for fps, count in self.performance_data.items():
            occurrences_count += count
            fps_sum += count * fps
        sorted_keys = sorted(self.performance_data.keys())
        self.performance_str = f"MIN: {sorted_keys[0]}, MAX: {sorted_keys[-1]}, AVG: {fps_sum // occurrences_count}"

    def run(self):
        self.__loading()

        while True:
            handle_actions(self.keys_pressed, self.handle_key_inputs)
            self.handle_mouse_inputs()

            if self.test_mode and not self.paused:
                self.performance_monitor()
                self.perform_random_spawn()

            self.__render_sand_box()
            self.__render_gui()
            pygame.display.flip()

            self.fps_clock.tick(self.fps)

    def __loading(self):
        # First run to force numba compilation
        thread1 = threading.Thread(target=self.sandBox.spawn, args=((0, 0), 10))
        thread2 = threading.Thread(target=self.sandBox.run_physics)
        thread1.start()
        thread2.start()
        while thread1.is_alive() or thread2.is_alive():
            for i in range(4):
                self.__render_message("Loading" + "".ljust(i, "."), (50, 255, 50))
                time.sleep(.25)

    def __render_message(self, text="", color=(0, 0, 0)):
        fps_text = self.font.render(text, True, color)
        self.screen.fill((0, 0, 0))
        self.screen.blit(fps_text, (5, 5))
        pygame.display.flip()

    def __render_sand_box(self):
        if not self.paused:
            self.sandBox.run_physics()
        sb_surface = pygame.transform.scale(self.sandBox.get_surface(), self.screen_size)
        self.screen.blit(sb_surface, (0, 0))

    def __render_gui(self):
        fps_str = f'Item: {self.selected_item.name}, Pencil size: {self.spawn_radius},  Fps: {int(self.fps_clock.get_fps())} '
        if self.test_mode:
            fps_str += self.performance_str
        fps_text = self.font.render(fps_str, True, (50, 255, 50))
        self.screen.blit(fps_text, (5, 5))


if __name__ == '__main__':
    game = Game(size=(1000, 1000), fps=300, scale=1, test_mode=True)
    game.run()
