import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


class TestWebUI:
    def setup_method(self):
        chrome_options = ChromeOptions()
        prefs = {
            "profile.password_manager_leak_detection": False,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)

    def teardown_method(self):
        self.driver.quit()

    def test_open_page_and_find_elements(self):
        self.driver.get("https://www.saucedemo.com/")

        username_field = self.driver.find_element(By.ID, "user-name")
        password_field = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.CLASS_NAME, "submit-button")

        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        login_button.click()

        assert "inventory" in self.driver.current_url
        print("Авторизация прошла успешно!")

    def test_add_item_to_cart(self):
        self.test_open_page_and_find_elements()

        add_button = self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        add_button.click()

        cart_icon = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()

        cart_item = self.driver.find_element(By.CLASS_NAME, "cart_item")
        assert cart_item.is_displayed()
        print("Товар успешно добавлен в корзину!")

    def test_delete_item_from_cart(self):
        self.test_open_page_and_find_elements()

        add_button = self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        add_button.click()

        cart_icon = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()

        cart_item = self.driver.find_element(By.CLASS_NAME, "cart_item")
        assert cart_item.is_displayed()
        print("Товар успешно добавлен в корзину!")

        remove_button = self.driver.find_element(By.ID, "remove-sauce-labs-backpack")
        remove_button.click()

        cart_items_after_removal = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items_after_removal) == 0, f"Ожидалось 0 товаров в корзине, но найдено {len(cart_items_after_removal)}"
        print("Товар успешно удален из корзины!")

if __name__ == "__main__":
    test = TestWebUI()
    test.setup_method()
    try:
        test.test_open_page_and_find_elements()
        test.test_add_item_to_cart()
        test.test_delete_item_from_cart()
        print("Все тесты прошли успешно!")
    except Exception as e:
        print(f"Тест упал с ошибкой: {e}")
        test.driver.save_screenshot("error_screenshot.png")
        print("Скриншот ошибки сохранен как error_screenshot.png")
    finally:
        test.teardown_method()