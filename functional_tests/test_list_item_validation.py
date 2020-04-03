from unittest import skip
from functional_tests.base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Mark goes to the home page and accidently tries to submit an empty list item
        self.browser.get(self.live_server_url)
        self.inputItem('')

        # wait for homepage to refresh
        # He submits and the page refreshes saying there cannot be an empty item
        self.wait_for(lambda: 
            self.browser.find_element_by_css_selector('#id_text:invalid')
        )

        # He tries again with some text and it works
        self.inputItem("Bananzas")

        # He then writes another blank message and gets the similar warning 
        self.inputItem('')
        self.wait_for(lambda :
            self.browser.find_element_by_css_selector('#id_text:invalid')
        )

        # He can then correct it by writing some text
        self.wait_for(lambda: self.inputItem("Hola"))
        self.wait_for_item_in_list_table('1: Bananzas')
        self.wait_for_item_in_list_table('2: Hola')

    def test_cannot_duplicate_items(self):
        # Mark goes to the homepage and starts a new list
        self.browser.get(self.live_server_url)
        self.inputItem("hello")
        self.wait_for_item_in_list_table("1: hello")

        # Mark accidently tries to enter a duplicate item
        self.inputItem("hello")

        # Mark sees a helpful error message
        self.wait_for(lambda: self.assertEqual(self.get_error_element().text, "You've already got this item in your list."))

    def test_error_messages_are_cleared_on_input(self):
        # Mark starts a list and causes a validation error
        self.browser.get(self.live_server_url)
        self.inputItem('abc')
        self.wait_for_item_in_list_table('1: abc')
        self.inputItem('abc')
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))
        # He starts typing in the input box to clear the error
        inputbox = self.wait_for(lambda: self.browser.find_element_by_id('id_text'))
        inputbox.send_keys('a')

        # He is pleased to see the error message disappears 
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
      



        
