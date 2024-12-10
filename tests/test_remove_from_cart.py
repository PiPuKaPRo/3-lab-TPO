import time
import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.test_add_to_cart import TestAddToCart


class TestDeleteFromCart(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://goldapple.ru/")
        self.wait = WebDriverWait(self.driver, 10)

    def test_remove_from_cart(self):
        """Тест: Удаление товара из корзины"""

        driver = self.driver

        # Предусловие (товар в корзине)
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

        time.sleep(8)

        change_element = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="__layout"]/div/div[4]/aside[4]/div[2]/div/div[1]/div/div/div/div[2]/article/div/section[2]/div/div/section/div/div/div/div/article')
        ))
        ActionChains(driver).move_to_element(change_element).perform()
        time.sleep(8)

        # Находим кнопку удаления
        delete_button = change_element.find_element(
            By.XPATH,
            '//*[@id="__layout"]/div/div[4]/aside[4]/div[2]/div/div[1]/div/div/div/div[2]/article/div/section[2]/div/div/section/div/div/div/div/article/div[2]/div[1]/button')
        delete_button.click()

        # Находим фразу о пустой корзине
        empty_cart = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="__layout"]/div/div[4]/aside[4]/div[2]/div/div[1]/div/div/div/div[1]/article/div/section/h2')))

        self.assertEqual(empty_cart.text, 'в корзине\nничего нет...', "Тест провален: Корзина не пустая.")


    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()