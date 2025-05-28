from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
#782167918452146176 은교햄 아이디
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get("https://discord.com/login")

print("로그인 후 Enter 키를 누르세요.")
input()
time.sleep(1)
target_username = "kkkk"  # 원하는 유저명
prev_author = None
processed_messages = set()
while True:
    try:
        messages = driver.find_elements(By.CLASS_NAME, "messageListItem__5126c")
        print(f"총 메시지 수: {len(messages)}")

        for msg in messages:  # 최신 메시지부터 역순으로 확인
            msg_id = msg.get_attribute("id")
            if msg_id in processed_messages:
                continue

            author_elements = msg.find_elements(By.XPATH, ".//span[starts-with(@class, 'username')]")
            if author_elements:
                author = author_elements[0].text
                prev_author = author
            else:
                author = prev_author

            if author == target_username:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", msg)

                reactions = msg.find_elements(By.XPATH, ".//*[contains(@class, 'reactionInner')]")
                has_heart = False
                for r in reactions:
                    emoji = r.find_element(By.XPATH, ".//*[contains(@class, 'emoji')]").get_attribute("aria-label")
                    if emoji and ("heart" in emoji.lower() or "❤️" in emoji):
                        has_heart = True
                        break
                if has_heart:
                    print("이미 하트 있음, 스킵")
                    processed_messages.add(msg_id)
                    continue

                print(f"💖 {author}의 메시지에 하트 달기")
                ActionChains(driver).move_to_element(msg).perform()

                # hoverBarButton 찾기
                buttons = msg.find_elements(By.XPATH, ".//*[contains(@class, 'hoverBarButton')]")
                found = False
                for btn in buttons:
                    label = btn.get_attribute("aria-label")
                    if label and ("반응 추가하기" in label or "Add Reaction" in label):
                        driver.execute_script("arguments[0].click();", btn)
                        found = True
                        break

                if not found:
                    print("❌ '반응 추가하기' 버튼 못 찾음")
                    continue

                emojis = driver.find_elements(By.XPATH, ".//*[contains(@class, 'emojiItem')]")
                if emojis:
                    emojis[0].click()
                    print("❤️ 하트 완료")
                else:
                    print("❌ 이모지 목록 못 찾음")

                processed_messages.add(msg_id)


    except Exception as e:
        print("오류 발생:", e)