# import pyautogui
# import cv2
# import numpy as np
# from PIL import ImageGrab
# import time

# # 이미지 경로 설정
# USER_ICON_PNG = "user_icon.png"
# HEART_PNG = "heart_icon.png"

# # 여러 크기 스케일에서 이미지 찾기 함수
# def find_image_on_screen_multiscale(image_path, threshold=0.8, scales=[1.0, 0.9, 0.8, 0.7]):
#     target_original = cv2.imread(image_path, 0)
#     screen = np.array(ImageGrab.grab())
#     screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

#     for scale in scales:
#         target = cv2.resize(target_original, (0, 0), fx=scale, fy=scale)
#         result = cv2.matchTemplate(screen_gray, target, cv2.TM_CCOEFF_NORMED)
#         loc = np.where(result >= threshold)
#         for pt in zip(*loc[::-1]):
#             return pt
#     return None

# # 하트 아이콘 찾기 함수 (이미 화면에 마우스 올린 상태에서 호출)
# def find_heart_icon(threshold=0.9, scales=[1.0, 0.9, 0.8]):
#     # 하트는 보통 메시지 근처에만 뜨므로 화면 일부만 캡처해도 됨
#     screen = np.array(ImageGrab.grab())
#     screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
#     heart_img = cv2.imread(HEART_PNG, 0)

#     for scale in scales:
#         resized_heart = cv2.resize(heart_img, (0, 0), fx=scale, fy=scale)
#         result = cv2.matchTemplate(screen_gray, resized_heart, cv2.TM_CCOEFF_NORMED)
#         loc = np.where(result >= threshold)
#         for pt in zip(*loc[::-1]):
#             return pt
#     return None

# # 여러 메시지에 순서대로 하트 클릭 함수
# def react_multiple_messages(message_count=3, message_height=60, icon_x_offset=30, icon_y_offset=30, heart_x_offset=5, heart_y_offset=5):
#     print("[INFO] 유저 아이콘 찾는 중...")
#     icon_pos = find_image_on_screen_multiscale(USER_ICON_PNG, threshold=0.85)

#     if icon_pos is None:
#         print("[WARN] 아이콘을 찾지 못했습니다.")
#         return

#     x, y = icon_pos
#     print(f"[INFO] 아이콘 위치 발견: {x}, {y}")

#     for i in range(message_count):
#         # 메시지 위치 예측 (아이콘 기준 아래로 내려가면서)
#         msg_x = x + icon_x_offset
#         msg_y = y + i * message_height + icon_y_offset

#         print(f"[INFO] 메시지 {i+1} 위치에 마우스 이동: {msg_x}, {msg_y}")
#         pyautogui.moveTo(msg_x, msg_y, duration=0.1)
#         time.sleep(0.5)  # 하트 아이콘 뜨도록 대기

#         heart_pos = find_heart_icon()
#         if heart_pos is None:
#             print(f"[WARN] 메시지 {i+1} 하트 아이콘을 찾지 못했습니다.")
#             continue

#         hx, hy = heart_pos
#         print(f"[INFO] 메시지 {i+1} 하트 아이콘 위치 발견: {hx}, {hy} 클릭 중...")
#         pyautogui.moveTo(hx + heart_x_offset, hy + heart_y_offset, duration=0.1)
#         pyautogui.click()
#         time.sleep(0.3)

# if __name__ == "__main__":
#     input("▶ 디스코드 창 준비 후 엔터를 누르세요...")
#     while True:
#         react_multiple_messages(message_count=4)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get("https://discord.com/login")

print("로그인 후 Enter 키를 누르세요.")
input()
time.sleep(3)
target_username = "20616 이은교"  # 원하는 유저명
prev_author = None
messages = driver.find_elements(By.CLASS_NAME, "messageListItem__5126c")

print(f"총 메시지 수: {len(messages)}")
for msg in messages:
    try:
        author_elements = msg.find_elements(By.XPATH, ".//span[starts-with(@class, 'username')]")
        if author_elements:
            author = author_elements[0].text
            prev_author = author  # 이전 작성자 갱신
        else:
            author = prev_author  # 이전 작성자 이름 그대로 사용

        if author == target_username:
            # 이미 하트 리액션이 달렸는지 검사
            reactions = msg.find_elements(By.XPATH, ".//*[contains(@class, 'reactionInner')]")
            has_heart = False
            for r in reactions:
                emoji = r.find_element(By.XPATH, ".//*[contains(@class, 'emoji')]").get_attribute("aria-label")
                # aria-label에 하트가 포함된 이모지가 있는지 체크
                if "heart" in emoji.lower() or "❤️" in emoji:
                    has_heart = True
                    break

            if has_heart:
                print(f"이미 하트가 달린 메시지, 건너뜁니다.")
                continue

            print(f"✅ {author}의 메시지에 하트 달기 시작")

            ActionChains(driver).move_to_element(msg).perform()
            clicked = False
            buttons = msg.find_elements(By.XPATH, ".//*[contains(@class, 'hoverBarButton')]")
            for btn in buttons:
                label = btn.get_attribute("aria-label")
                if label == "반응 추가하기":  # 또는 영어 UI면 "Add Reaction"4
                    ActionChains(driver).move_to_element(btn).perform()
                    btn.click()
                    clicked = True  
                    # break
            if not clicked:
                print("❌ '반응 추가하기' 버튼을 찾을 수 없습니다.")
                continue    
            emojis = driver.find_elements(By.XPATH, ".//*[contains(@class, 'emojiItem')]")
            if emojis:
                emojis[0].click()
                print("❤️ 하트를 달았습니다.")
            else:
                print("❌ 이모지 리스트를 찾을 수 없습니다.")
            # break

    except Exception as e:
        print("오류:", e)

input("작업 완료. Enter 키 누르면 종료합니다.")
driver.quit()
