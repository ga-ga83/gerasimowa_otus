import pytest
import allure
import logging
from allure import severity, severity_level
from playwright.sync_api import Page, expect

from UI.pages.base_page import BasePage
from UI.pages.login_page import LoginPage
from UI.pages.shop_page import ShopPage

# Настройка логгера для быстрой отладки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VALID_CREDENTIALS = {"username": "standard_user", "password": "secret_sauce"}


@allure.feature("Корзина и оформление заказа")
@allure.severity(severity_level.CRITICAL)
class TestCart:

    @pytest.fixture(autouse=True)
    def setup(self, page):
        with allure.step("Выполнить вход в систему"):
            login_page = LoginPage(page)
            login_page.enter_username(VALID_CREDENTIALS["username"])
            login_page.enter_password(VALID_CREDENTIALS["password"])
            login_page.click_login()

        with allure.step("Закрыть возможные алерт-окна"):
            try:
                BasePage(page).close_password_alert_window()
            except Exception:
                logger.warning("Окно-алерт не найдено или не удалось закрыть — продолжаем тест")

        self.page = page
        self.shop_page = ShopPage(page)
        logger.info("Страница магазина инициализирована")

    @allure.title("Успешное оформление покупки и очистка корзины")
    @allure.description(
        "Тест проверяет полный сценарий покупки: добавление товара в корзину, "
        "переход к оформлению, заполнение формы, подтверждение заказа. "
        "В конце проверяется сообщение об успехе и отсутствие товаров в корзине."
    )
    @allure.story("Оформление заказа и проверка результата")
    def test_successful_purchase(self):
        with allure.step("Добавить первый товар в корзину"):
            self.shop_page.add_item_to_cart(index=0)

        with allure.step("Открыть корзину и перейти к оформлению заказа"):
            self.shop_page.open_cart()
            self.shop_page.open_checkout()

        with allure.step("Заполнить форму оформления заказа и завершить покупку"):
            self.shop_page.fill_checkout_form("Anna", "Ivanova", "123456")
            self.shop_page.click_continue()
            self.shop_page.click_finish()

        with allure.step("Проверить сообщение об успехе"):
            success_message = self.page.locator(self.shop_page.SUCCESS_MESSAGE)
            expect(success_message).to_be_visible()

            expected_msg = (
                "Your order has been dispatched, and will arrive just as fast "
                "as the pony can get there!"
            )
            assert expected_msg in self.shop_page.get_success_message_text(), \
                "Текст сообщения не совпадает"

        with allure.step("Проверить, что корзина пуста"):
            # Ждём исчезновения счётчика корзины (аналог wait.until(count == 0))
            badge = self.page.locator(self.shop_page.CART_BADGE)
            expect(badge).to_have_count(0)
            assert self.shop_page.get_cart_count() == 0, "Корзина не пуста после успешного заказа"

    @allure.title("Очистка корзины через кнопки удаления и возврат на страницу магазина")
    @allure.description(
        "Тест добавляет два товара в корзину, затем последовательно удаляет их "
        "с помощью кнопок «Remove» на странице каталога. В конце проверяется, "
        "что корзина пуста, а пользователь находится на странице магазина."
    )
    @allure.story("Очистка корзины и навигация")
    @allure.severity(severity_level.NORMAL)
    def test_clear_cart_and_return_to_shop(self):
        badge = self.page.locator(self.shop_page.CART_BADGE)
        remove_button = self.page.locator(self.shop_page.REMOVE_FROM_CART_BUTTON)

        with allure.step("Добавить два товара в корзину"):
            self.shop_page.add_item_to_cart(index=0)
            self.shop_page.add_item_to_cart(index=1)

        with allure.step("Проверить, что в корзине два товара"):
            # Ждём, пока счётчик реально покажет "2"
            expect(badge).to_have_text("2")
            assert self.shop_page.get_cart_count() == 2, "В корзине не два товара"

        with allure.step("Удалить все товары из корзины по одному"):
            initial_count = self.shop_page.get_cart_badge_count()
            logger.info(f"Начинаем удаление: в корзине {initial_count} товаров")

            while self.shop_page.get_cart_count() > 0:
                count_before = self.shop_page.get_cart_count()
                logger.info(f"Текущий счётчик перед кликом: {count_before}")

                # Скриншот перед кликом для отладки
                self.page.screenshot(path=f"before_remove_click_{count_before}.png")

                remove_button.first.click()

                # Ждём, что счётчик уменьшился ровно на единицу
                expect(badge).to_have_text(str(count_before - 1))
                logger.info(f"Товар удалён. Новый счётчик: {count_before - 1}")

        with allure.step("Убедиться, что корзина пуста и пользователь на странице магазина"):
            expect(badge).to_have_count(0)
            assert "Swag Labs" in self.page.title(), \
                f"Неверный заголовок страницы: {self.page.title()}"
            logger.info("Корзина пуста, тест пройден")
