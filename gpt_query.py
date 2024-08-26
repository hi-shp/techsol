import time
import pyautogui
import pyperclip
import keyboard

"챗 지피티를 미리 크롬으로 띄워놓고 alt+tab으로 넘어가서 요청하도록 구현한거라, api를 사용하려면 따로 코드 짜야합니다."

def query_gpt():
    # Alt + Tab 키를 사용하여 창 전환
    pyautogui.hotkey('ctrl', 'shift', 'tab')

    # 잠시 대기 (화면 전환이 완료되도록)
    time.sleep(1)

    # 지정된 좌표(1100, 1460) 클릭 (input)
    pyautogui.click(1100, 1460)

    # 클립보드에 저장된 텍스트를 붙여넣기
    pyautogui.hotkey('ctrl', 'v')

    time.sleep(0.3)

    # 추가로 지정된 좌표(1830, 1460) 클릭 (요청 버튼)
    pyautogui.click(1830, 1460)

    # 스페이스바 입력 대기
    keyboard.wait('space')

    # 지정된 좌표(1090, 1337) 클릭 (복사 버튼)
    pyautogui.click(1090, 1337)

    # 클립보드에 저장된 내용을 가져옴
    result_text = pyperclip.paste()

    return result_text
