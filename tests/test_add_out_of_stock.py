import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestAddEndedToCartFromProduct(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://goldapple.ru/19000165305-eros-man-eau-de-parfume")
        self.wait = WebDriverWait(self.driver, 15)

    def test_add_out_of_stock(self):
        """Тест: Добавление товара, которого нет в наличии в корзину со страницы товара"""

        driver = self.driver

        # Ищем кнопку "Добавить в корзину"
        add_to_cart_button = self.wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="__layout"]/div/main/article/div[1]/div[1]/form/div[4]/div/button'
        )))


        self.assertEqual(add_to_cart_button.text, 'УЗНАТЬ О ПОСТУПЛЕНИИ', "Тест провален: Товар отсутствует в корзине.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()