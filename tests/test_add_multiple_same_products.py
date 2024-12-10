import time
import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestChangeCount(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://goldapple.ru/")
        self.wait = WebDriverWait(self.driver, 10)

    def test_add_multiple_same_products(self):
        """Тест: Проверка обновления количества товара в корзине"""

        driver = self.driver

        first_product = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__layout"]/div/main/section[3]/div/section/div/div[2]/div[1]')
        ))

        driver.execute_script("window.scrollBy(0, document.body.scrollHeight * 0.05);")

        add_to_cart_button = first_product.find_element(
            By.XPATH,
            '//*[@id="__layout"]/div/main/section[3]/div/section/div/div[2]/div[1]/div/div/div/div/article/div/div/div/div[3]/button'
        )
        add_to_cart_button.click()

        # Ожидаем добавления, иначе иногда падает
        time.sleep(5)

        # Переходим в корзину
        cart_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="__layout"]/div/header/div[2]/div[2]/button[5]')
        ))
        cart_button.click()

        time.sleep(7)

        # Находим элемент изменения количества
        change_count_element = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="__layout"]/div/div[4]/aside[4]/div[2]/div/div[1]/div/div/div/div[2]/article/div/section[2]/div/div/section/div/div/div/div/article')
        ))
        ActionChains(driver).move_to_element(change_count_element).perform()
        time.sleep(5)

        # Находим количество
        count = change_count_element.find_element(
            By.XPATH,
            '//*[@id="__layout"]/div/div[4]/aside[4]/div[2]/div/div[1]/div/div/div/div[2]/article/div/section[2]/div/div/section/div/div/div/div/article/div[2]/div[1]/div/input')
        old_count = count.get_attribute('_value')
        # Находим кнопку добавления
        add_count_button = change_count_element.find_element(
            By.XPATH,
            '//*[@id="__layout"]/div/div[4]/aside[4]/div[2]/div/div[1]/div/div/div/div[2]/article/div/section[2]/div/div/section/div/div/div/div/article/div[2]/div[1]/div/button[2]')

        add_count_button.click()
        time.sleep(5)

        new_count = (count.get_attribute('_value'))
        self.assertGreater(new_count, old_count, "Тест провален: Количество товара меньше минимального измененного.")

    def tearDown(self):
        """Закрываем браузер после выполнения теста"""
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()