import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestAddToCart(unittest.TestCase):

    def setUp(self):
        """Инициализация драйвера перед каждым тестом"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://goldapple.ru/")
        self.wait = WebDriverWait(self.driver, 10)

    def test_add_product_to_cart(self):
        """Тест: Добавление товара в корзину с главной страницы"""

        driver = self.driver

        # Находим первый товар
        first_product = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__layout"]/div/main/section[3]/div/section/div/div[2]/div[1]')
        ))

        # Прокручиваем страницу вниз на 5% для отображения элемента
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight * 0.05);")

        # Нажимаем кнопку "Добавить в корзину"
        add_to_cart_button = first_product.find_element(
            By.XPATH, '//*[@id="__layout"]/div/main/section[3]/div/section/div/div[2]/div[1]/div/div/div/div/article/div/div/div/div[3]/button'
        )
        add_to_cart_button.click()

        # Ожидаем добавления, иначе иногда падает
        time.sleep(8)

        # Переходим в корзину
        cart_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="__layout"]/div/header/div[2]/div[2]/button[5]')
        ))
        cart_button.click()

        # Проверяем, что товар появился в корзине
        cart_items = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__layout"]/div/div[4]/aside[4]/div[2]/div/div[1]/div/div/div/div[2]/article/div/section[2]/div/div/section/div/div/div[1]')
        ))

        self.assertTrue(cart_items, "Тест провален: Товар отсутствует в корзине.")

    def tearDown(self):
        """Закрываем браузер после выполнения теста"""
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()