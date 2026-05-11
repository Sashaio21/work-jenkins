import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

USERNAME = sys.argv[1] if len(sys.argv) > 1 else "standard_user"
PASSWORD = sys.argv[2] if len(sys.argv) > 2 else "secret_sauce"

class TestSauceDemo(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()


    # =========================
    # 🔐 LOGIN + ПРОВЕРКА
    # =========================
    def login_and_verify(self):
        self.driver.get("https://www.saucedemo.com/")

        self.driver.find_element(By.ID, "user-name").send_keys(USERNAME)
        self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
        self.driver.find_element(By.ID, "login-button").click()

        self.wait.until(EC.url_contains("inventory.html"))

        inventory = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list"))
        )
        self.assertTrue(inventory.is_displayed())

    # =========================
    # 🧪 CART TESTS
    # =========================

    def test_add_to_cart(self):
        self.login_and_verify()

        self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item button")[0].click()

        badge = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        self.assertEqual(badge.text, "1")

        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertEqual(len(items), 1)

    def test_add_multiple_items(self):
        self.login_and_verify()

        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item button")

        for i in range(3):
            buttons[i].click()

        badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(badge.text, "3")

    def test_remove_item(self):
        self.login_and_verify()

        self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item button")[0].click()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        self.driver.find_element(By.CLASS_NAME, "cart_button").click()

        items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertEqual(len(items), 0)

    def test_add_all_items(self):
        self.login_and_verify()

        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item button")
        count = len(buttons)

        for i in range(count):
            buttons[i].click()

        badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(badge.text, str(count))

        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertEqual(len(items), count)

    # =========================
    # 🧪 SORT TESTS
    # =========================

    def test_sort_price_low_to_high(self):
        self.login_and_verify()

        self.driver.find_element(By.CLASS_NAME, "product_sort_container") \
            .send_keys("Price (low to high)")

        prices = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")

        price_list = []
        for p in prices:
            price = float(p.text.replace("$", ""))
            price_list.append(price)

        self.assertEqual(price_list, sorted(price_list))


if __name__ == "__main__":
    unittest.main()
