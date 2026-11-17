from .base_page import BasePage

class LoginPage(BasePage):
    URL = "https://www.saucedemo.com"

    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = ".error-message-container"

    def open(self):
        self.page.goto(self.URL)

    def enter_username(self, username):
        self.find_element(self.USERNAME_INPUT).fill(username)

    def enter_password(self, password):
        self.find_element(self.PASSWORD_INPUT).fill(password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def close_password_alert_window(self):
        selectors = [
            "div[role='alert']",
            "div.notification",
            "div.toast",
        ]

        for selector in selectors:
            for el in self.page.locator(selector).all():
                if "Смените пароль" in (el.inner_text() or ""):
                    self.page.keyboard.press("Escape")
                    return  # закрыли первый подходящий алерт и выходим

    def get_error_message(self):
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
