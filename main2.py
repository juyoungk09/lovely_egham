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
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'instant', block: 'center' });", msg)
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
            buttons = msg.find_elements(By.XPATH, ".//*[contains(@class, 'hoverBarButton')]")
            for btn in buttons:
                label = btn.get_attribute("aria-label")
                if label == "반응 추가하기":  # 또는 영어 UI면 "Add Reaction"4
                    ActionChains(driver).move_to_element(btn).perform()
                    # btn.click()
                    driver.execute_script("arguments[0].click();", btn)
                    # break
            if not buttons: 
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