from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Mark has heard of a new lists app and goes to the website to check it out
        self.browser.get("http://localhost:8000")

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        headerText = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', headerText)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), "Enter a to-do item")

        # He types Buy feathers into the text box
        inputbox.send_keys('Buy feathers')
        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)

        # He types another input
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Clean feathers')
        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy feathers', [row.text for row in rows])
        self.assertIn('2: Clean feathers', [row.text for row in rows])

        # There is still a textbox initing him to add another item
        
        # Mark enters "Use feathers for mask"
        self.fail("Finish the test")


if __name__ == "__main__":
    unittest.main(warnings='ignore')