from .base_page import BasePage

class ShopPage(BasePage):
    CART_ICON = ".shopping_cart_link"
    ADD_TO_CART_BUTTONS = "//button[contains(@class, 'btn_primary')]"
    REMOVE_FROM_CART_BUTTON = "//button[normalize-space()='Remove']"
    REMOVE_FROM_CART_BUTTONS = "//button[normalize-space()='Remove']"
    CHECKOUT_BUTTON = "#checkout"
    ITEM_TITLE = ".inventory_item_name"
    LOGO_TITLE = "//*[@class='app_logo']"
    CART_BADGE = ".shopping_cart_badge"
    CART_ICON_BADGE = ".shopping_cart_badge"

    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    ZIP_CODE_INPUT = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    FINISH_BUTTON = "#finish"

    SUCCESS_MESSAGE = ".complete-text"
    BACK_TO_PRODUCTS_LINK = "//button[contains(@class, 'back')]"  # см. примечание ниже

    def add_item_to_cart(self, index=0):
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        buttons[index].click()

    def remove_item_from_cart(self, index=0):
        buttons = self.find_elements(self.REMOVE_FROM_CART_BUTTON)
        if index < len(buttons):
            buttons[index].click()
        else:
            raise IndexError(f"Нет кнопки удаления с индексом {index}, всего кнопок: {len(buttons)}")

    def open_cart(self):
        self.click(self.CART_ICON)

    def get_cart_count(self):
        if self.is_element_present(self.CART_BADGE):
            badge = self.find_element(self.CART_BADGE)
            return int(badge.inner_text()) if badge.inner_text() else 0
        return 0

    def get_cart_badge_count(self):
        # счетчик количества товаров в корзине
        try:
            badge = self.find_element(self.CART_ICON_BADGE)
            return int(badge.inner_text())
        except Exception:
            return 0

    def open_checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def fill_checkout_form(self, first_name, last_name, zip_code):
        self.find_element(self.FIRST_NAME_INPUT).fill(first_name)
        self.find_element(self.LAST_NAME_INPUT).fill(last_name)
        self.find_element(self.ZIP_CODE_INPUT).fill(zip_code)

    def click_continue(self):
        self.click(self.CONTINUE_BUTTON)

    def click_finish(self):
        self.click(self.FINISH_BUTTON)

    def is_success_message_present(self):
        return self.is_element_present(self.SUCCESS_MESSAGE)

    def get_success_message_text(self):
        return self.get_text(self.SUCCESS_MESSAGE)

    def go_back_to_products(self):
        self.click(self.BACK_TO_PRODUCTS_LINK)

    def clear_cart(self):
        while True:
            buttons = self.find_elements_no_wait(self.REMOVE_FROM_CART_BUTTON)
            if not buttons:
                break
            buttons[0].click()
