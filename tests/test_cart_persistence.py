import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCartPersistence(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://goldapple.ru/")
        self.wait = WebDriverWait(self.driver, 10)

    def test_cart_persistence(self):
        """Тест: Сохранится ли товар в корзине после обновления страницы"""

        driver = self.driver

        # Находим первый товар
        first_product = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__layout"]/div/main/section[3]/div/section/div/div[2]/div[1]')
        ))

        driver.execute_script("window.scrollBy(0, document.body.scrollHeight * 0.05);")

        add_to_cart_button = first_product.find_element(
            By.XPATH,
            '//*[@id="__layout"]/div/main/section[3]/div/section/div/div[2]/div[1]/div/div/div/div/article/div/div/div/div[3]/button'
        )
        add_to_cart_button.click()

        time.sleep(8)

        cart_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="__layout"]/div/header/div[2]/div[2]/button[5]')
        ))
        cart_button.click()

        driver.refresh()
        time.sleep(8)

        # Переходим в корзину
        cart_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="__layout"]/div/header/div[2]/div[2]/button[5]')
        ))
        cart_button.click()

        cart_items = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="__layout"]/div/div[4]/aside[4]/div[2]/div/div[1]/div/div/div/div[2]/article/div/section[2]/div/div/section/div/div/div[1]')
        ))
        self.assertTrue(cart_items.is_displayed(), "Тест провален: товар пропал из корзины после перезагрузки.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
