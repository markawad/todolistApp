from unittest import skip
from functional_tests.base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Mark goes to the home page and accidently tries to submit an empty list item
        self.browser.get(self.live_server_url)
        self.inputItem('')

        # wait for homepage to refresh
        # He submits and the page refreshes saying there cannot be an empty item
        self.wait_for(lambda: 
        self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item."
        ))

        # He tries again with some text and it works
        self.inputItem("Bananzas")

        # He then writes another blank message and gets the similar warning 
        self.inputItem('')
        self.wait_for(lambda :
        self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item."
        ))

        # He can then correct it by writing some text
        self.inputItem("Hola")
        self.wait_for_item_in_list_table('1: bananza')
        self.wait_for_item_in_list_table('2: Hola')

        self.fail("finish this test!")
        
