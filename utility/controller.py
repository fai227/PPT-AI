import time
from multiprocessing import Process, Queue
import vgamepad as vg

class controller:
    process = None
    interval = 0.05
    control_queue = Queue()

    def connect():
        global process
        print("コントローラーを接続")
        
        process = Process(target=controller.main, daemon=True, args=(controller.control_queue, ))
        process.start()

    def move(*args):
        for arg in args:
            controller.control_queue.put(arg)

    def chose_character():
        controller.move(0.2, "l","l","l","l","l","d", "h", 0.2, "h", 0.4, "h")

    def disconnect():
        global process
        print("コントローラーを切断")
        process.terminate()

    def main(queue):
        gamepad = vg.VX360Gamepad()
        while True:

            # ゲームパッドを動かさなくていいときはスキップ
            if queue.qsize() == 0:
                continue

            # ゲームパッドを押す
            key = queue.get()
            # 秒数分待機
            if type(key) is not str:
                time.sleep(key)
            # ボタン押下
            else:
                if key == "u":
                    controller.press(gamepad, vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
                elif key == "d":
                    controller.press(gamepad, vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
                elif key == "r":
                    controller.press(gamepad, vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
                elif key == "l":
                    controller.press(gamepad, vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
                elif key == "t":
                    controller.press(gamepad, vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                elif key == "h":
                    controller.press(gamepad, vg.XUSB_BUTTON.XUSB_GAMEPAD_A)



    def press(gp, bt):
        # 押す
        gp.press_button(bt)
        gp.update()
        
        # 待つ
        time.sleep(controller.interval)
        
        # 押す
        gp.release_button(bt)
        gp.update()

        # 待つ
        time.sleep(controller.interval)