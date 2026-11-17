import allure
from allure import severity, severity_level

from UI.pages.login_page import LoginPage

# Данные для тестов
VALID_CREDENTIALS = {"username": "standard_user", "password": "secret_sauce"}
INVALID_USERNAME = "wrong_user"
INVALID_PASSWORD = "wrong_password"
EXPECTED_ERROR_MSG = "Epic sadface: Username and password do not match any user in this service"
EXPECTED_ERROR_MSG_EMPTY = "Epic sadface: Username is required"


@allure.feature("Авторизация пользователя")
@allure.severity(severity_level.BLOCKER)
class TestLogin:

    @allure.title("Успешная авторизация с корректными учётными данными")
    @allure.description(
        "Проверяется успешный вход пользователя со стандартными учётными данными. "
        "После входа проверяется URL страницы инвентаря и наличие логотипа приложения."
    )
    @allure.story("Успешный вход в систему")
    def test_successful_login(self, page):
        with allure.step("Ввести логин и пароль, нажать кнопку входа"):
            login_page = LoginPage(page)
            login_page.enter_username(VALID_CREDENTIALS["username"])
            login_page.enter_password(VALID_CREDENTIALS["password"])
            login_page.click_login()

        assert "/inventory.html" in page.url
        with allure.step("Проверить, что пользователь на странице инвентаря"):
            assert login_page.is_element_present(".app_logo")

    @allure.title("Неуспешная авторизация при неверных учётных данных")
    @allure.description(
        "Проверяется поведение системы при попытке входа с некорректными логином и паролем. "
        "Ожидается сообщение об ошибке, указывающее на несоответствие учётных данных."
    )
    @allure.story("Обработка неверных учётных данных")
    @allure.severity(severity_level.CRITICAL)
    def test_unsuccessful_login_wrong_credentials(self, page):
        with allure.step("Ввести неверные логин и пароль, нажать кнопку входа"):
            login_page = LoginPage(page)
            login_page.enter_username(INVALID_USERNAME)
            login_page.enter_password(INVALID_PASSWORD)
            login_page.click_login()

        error_msg = login_page.get_error_message()
        assert error_msg == EXPECTED_ERROR_MSG, (
            f"Expected error '{EXPECTED_ERROR_MSG}', got '{error_msg}'"
        )

    @allure.title("Проверка обработки пустых полей при входе")
    @allure.description(
        "Проверяется реакция системы на попытку входа без ввода логина и пароля. "
        "Ожидается сообщение о том, что поле имени пользователя обязательно для заполнения."
    )
    @allure.story("Валидация обязательных полей")
    @allure.severity(severity_level.CRITICAL)
    def test_unsuccessful_login_empty_fields(self, page):
        with allure.step("Нажать кнопку входа без заполнения полей"):
            login_page = LoginPage(page)
            login_page.click_login()

        error_msg = login_page.get_error_message()
        assert error_msg == EXPECTED_ERROR_MSG_EMPTY, (
            f"Expected error '{EXPECTED_ERROR_MSG_EMPTY}', got '{error_msg}'"
        )
