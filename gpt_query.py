import time
import pyautogui
import pyperclip
import keyboard

def query_gpt():
    # Alt + Tab 키를 사용하여 창 전환
    pyautogui.hotkey('ctrl', 'shift', 'tab')

    # 잠시 대기 (화면 전환이 완료되도록)
    time.sleep(1)

    # 지정된 좌표(1100, 1460) 클릭
    pyautogui.click(1100, 1460)

    # 클립보드에 저장된 텍스트를 붙여넣기
    pyautogui.hotkey('ctrl', 'v')

    time.sleep(0.3)

    # 추가로 지정된 좌표(1830, 1460) 클릭
    pyautogui.click(1830, 1460)

    # 스페이스바 입력 대기
    keyboard.wait('space')

    # 지정된 좌표(1090, 1337) 클릭
    pyautogui.click(1090, 1337)

    # 클립보드에 저장된 내용을 가져옴
    result_text = pyperclip.paste()

    return result_text
