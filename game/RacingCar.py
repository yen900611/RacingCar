import pygame

from .playingMode import PlayingMode
from .coinPlayMode import CoinMode
from .env import *
from .sound_controller import *

'''need some fuction same as arkanoid which without dash in the name of fuction'''

class RacingCar:
    def __init__(self, user_num: int, difficulty,sound):
        self.is_sound = sound
        self.sound_controller = SoundController(self.is_sound)
        if difficulty == "NORMAL":
            self.game_mode = PlayingMode(user_num,self.sound_controller)
            self.game_type = "NORMAL"
        elif difficulty == "COIN":
            self.game_mode = CoinMode(user_num,self.sound_controller)
            self.game_type = "COIN"

        self.user_num = user_num

    def get_player_scene_info(self) -> dict:
        scene_info = self.get_scene_info
        # print(scene_info)
        return {
            "ml_1P" : scene_info,
            "ml_2P" : scene_info,
            "ml_3P" : scene_info,
            "ml_4P" : scene_info
        }

    def update(self, commands):
        self.game_mode.handle_event()
        self.game_mode.detect_collision()
        self.game_mode.update_sprite(commands)
        self.draw()
        if not self.isRunning():
            return "QUIT"

    def reset(self):
        self.__init__(self.user_num,self.game_type,self.is_sound)
        pass

    def isRunning(self):
        return self.game_mode.isRunning()
        pass

    def draw(self):
        self.game_mode.draw_bg()
        self.game_mode.drawAllSprites()
        self.game_mode.flip()

    @property
    def get_scene_info(self) -> dict:
        """
        Get the scene information
        """

        cars_pos = []
        computer_cars_pos = []
        lanes_pos = []

        scene_info = {
            "frame": self.game_mode.frame,
            "status": self.game_mode.status,
            "line":[(self.game_mode.line.rect.left,self.game_mode.line.rect.top)]}

        for car in self.game_mode.cars_info:
            cars_pos.append(car["pos"])
            if car["id"] <= 4:
                scene_info["player_"+str(car["id"])+"_pos"] = car["pos"]
            elif car["id"] > 100:
                computer_cars_pos.append(car["pos"])
        scene_info["computer_cars"] = computer_cars_pos
        scene_info["cars_pos"] = cars_pos

        for lane in self.game_mode.lanes:
            lanes_pos.append((lane.rect.left, lane.rect.top))
        scene_info["lanes"] = lanes_pos

        if self.game_type == "COIN":
            coin_pos = []
            for coin in self.game_mode.coins:
                coin_pos.append(coin.get_position())
            scene_info["coin"] = coin_pos

        result = {}
        for user in self.game_mode.winner:
            result["Rank" + str(self.game_mode.winner.index(user) + 1)] = "Player " + str(user.car_no + 1)
        scene_info["game_result"] = result
        return scene_info

    def get_game_info(self):
        """
        Get the scene and object information for drawing on the web
        """
        return {
            "scene": {
                "size": [WIDTH, HEIGHT]
            },
            "game_object": [
                {"name": "lane", "size": lane_size, "color": WHITE},
                {"name": "coin", "size": coin_size, "color": YELLOW},
                {"name": "computer_car", "size": car_size, "color": BLACK},
                {"name": "player1_car", "size": car_size, "color": WHITE},
                {"name": "player2_car", "size": car_size, "color": YELLOW},
                {"name": "player3_car", "size": car_size, "color": BLUE},
                {"name": "player4_car", "size": car_size, "color": RED},
                {"name": "line", "size": (5,450), "color": WHITE}
            ]
        }

    def get_game_progress(self):
        """
        Get the position of game objects for drawing on the web
        """
        scene_info = self.get_scene_info
        game_progress = {}

        if self.game_type == "NORMAL":
            game_progress = {"game_object": {
        "lane": scene_info["lanes"],
        "line":scene_info["line"],
        "computer_car": scene_info["computer_cars"],
        "player1_car": [scene_info["player1_pos"]],
        "player2_car": [scene_info["player2_pos"]],
        "player3_car": [scene_info["player3_pos"]],
        "player4_car": [scene_info["player4_pos"]]}
    }


        if self.game_type == "COIN":
            game_progress = {"game_object": {
        "lane": scene_info["lanes"],
        "line":scene_info["line"],
        "coin": scene_info["coin"],
        "computer_car": scene_info["computer_cars"],
        "player1_car": [scene_info["player1_pos"]],
        "player2_car": [scene_info["player2_pos"]],
        "player3_car": [scene_info["player3_pos"]],
        "player4_car": [scene_info["player4_pos"]],}
    }


        return game_progress

    def get_game_result(self):
        """
        Get the game result for the web
        """
        scene_info = self.get_scene_info
        result = []
        ranking = []
        for user in scene_info["game_result"]:
            result.append("GAME_DRAW")
            ranking.append(str(user.car_no + 1) + "P")

        return {
            "frame_used": scene_info["frame"],
            "result": result,
            "ranking": ranking
        }

    def get_keyboard_command(self):
        """
        Get the command according to the pressed keys
        """
        key_pressed_list = pygame.key.get_pressed()
        cmd_1P = []
        cmd_2P = []

        if key_pressed_list[pygame.K_LEFT]: cmd_1P.append(BRAKE_cmd)
        if key_pressed_list[pygame.K_RIGHT]:cmd_1P.append(SPEED_cmd)
        if key_pressed_list[pygame.K_UP]:cmd_1P.append(LEFT_cmd)
        if key_pressed_list[pygame.K_DOWN]:cmd_1P.append(RIGHT_cmd)

        if key_pressed_list[pygame.K_a]: cmd_2P.append(BRAKE_cmd)
        if key_pressed_list[pygame.K_d]:cmd_2P.append(SPEED_cmd)
        if key_pressed_list[pygame.K_w]:cmd_2P.append(LEFT_cmd)
        if key_pressed_list[pygame.K_s]:cmd_2P.append(RIGHT_cmd)

        return [cmd_1P, cmd_2P]

if __name__ == '__main__':
    pygame.init()
    display = pygame.display.init()
    game = Game(4)

    while game.isRunning():
        game.update(commands)
        game.draw()

    pygame.quit()
