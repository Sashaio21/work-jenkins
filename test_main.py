from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/hovers")

# находим первый блок пользователя
user = driver.find_element(By.CLASS_NAME, "figure")

# hover
ActionChains(driver).move_to_element(user).perform()

# маленькая пауза (чтобы UI успел отрисоваться)
time.sleep(1)

# получаем текст
caption = driver.find_element(By.CLASS_NAME, "figcaption")
print(caption.text)

driver.quit()