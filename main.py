# imports
import time
from utility.window_capture import window_capture
import cv2
import numpy as np
from utility.controller import controller

class Application_Status:
    Wait = "Wait"
    CHARACTER_SELECT = "Character Select"
    Game = "In Game"

# 定数
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 360
IMAGE_CHANNEL = 4
ALL_PIXEL_DATA_LENGTH = IMAGE_WIDTH * IMAGE_HEIGHT * IMAGE_CHANNEL

SIMILARITY_THRESHOLD = 0.7
TEMPLATE_THRESHOLD = 0.9

# グローバル変数
ppt = window_capture("PuyoPuyoTetris2")
application_status = Application_Status.Wait
previous_time = time.time()

go_image = cv2.imread("./image/Go.png", cv2.IMREAD_UNCHANGED)
ready_image = cv2.imread("./image/Ready.png", cv2.IMREAD_UNCHANGED)
character_image = cv2.imread("./image/Character.png", cv2.IMREAD_UNCHANGED)

# メインループ
def update():
    global application_status

    # スクリーンショットを取って変形
    screenshot_array = ppt.get_screenshot()
    screenshot_array = cv2.resize(src=screenshot_array, dsize=(IMAGE_WIDTH, IMAGE_HEIGHT))


    if application_status is Application_Status.Wait:
        # print("game")
        # print(character_image.shape)
        # print(screenshot_array.shape)
        # print(screenshot_array)
        # print(abs(character_image - screenshot_array) < 10)
        # print(np.count_nonzero(character_image == screenshot_array) / (IMAGE_WIDTH * IMAGE_HEIGHT * 4))
        
        # キャラ選択画面判定
        character_select_similarity = get_similarity(screenshot_array, character_image)
        if character_select_similarity > SIMILARITY_THRESHOLD:
            print("キャラ選択")
            controller.chose_character()
            time.sleep(3)
            application_status = Application_Status.CHARACTER_SELECT

        # ゲーム開始判定
        else:
            ready_match_result = cv2.matchTemplate(screenshot_array, ready_image, cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(ready_match_result)
            if max_val > TEMPLATE_THRESHOLD:
                """
                top_left = max_loc
                bottom_right = (top_left[0] + ready_image.shape[1], top_left[1] + ready_image.shape[0])
                cv2.rectangle(screenshot_array, top_left, bottom_right, (255, 255, 0), 2)
                cv2.imwrite("screenshot.png", screenshot_array)
                """

                application_status = Application_Status.Game
            """
            go_match_result = cv2.matchTemplate(screenshot_array, go_image, cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(go_match_result)
            if max_val > SIMILARITY_THRESHOLD:
                print("ゲーム開始")
                application_status = Application_Status.Game
            """
            


    elif application_status is Application_Status.CHARACTER_SELECT:
        character_select_similarity = get_similarity(screenshot_array, character_image)
        if character_select_similarity < SIMILARITY_THRESHOLD:
            print("キャラ選び終了")
            application_status = Application_Status.Wait


    elif application_status is Application_Status.Game:
        game_update(screenshot_array=screenshot_array)
    
def game_update(screenshot_array):
    pass

def get_similarity(a, b):
    return np.count_nonzero(np.isclose(a=a, b=b, atol=20)) / ALL_PIXEL_DATA_LENGTH


# メイン実行部分
if __name__ == "__main__":
    # コントローラー接続
    controller.connect()

    counter = 0
    while True:

        update()

        current_time = time.time()
        delta_time = current_time - previous_time    
        if counter % 10 == 0:
            pass
            # print(str(round(1 / delta_time)) + "fps")
        previous_time = current_time
        counter += 1
