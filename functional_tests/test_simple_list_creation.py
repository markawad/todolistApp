from functional_tests.base import FunctionalTest
from selenium import webdriver

class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Mark has heard of a new lists app and goes to the website to check it out
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_text')
        self.assertEqual(inputbox.get_attribute('placeholder'), "Enter a to-do item")

        # He types Buy feathers into the text box
        self.inputItem('Buy feathers')
        self.wait_for_item_in_list_table('1: Buy feathers')

        # He types another input
        self.inputItem('Clean feathers')
        self.wait_for_item_in_list_table('1: Buy feathers')
        self.wait_for_item_in_list_table('2: Clean feathers')

        # satisfied
    
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Mark starsts a new todo list
        self.browser.get(self.live_server_url)
        self.inputItem("Buy machinessss")
        self.wait_for_item_in_list_table("Buy machinessss")

        # He notices that his list has a unique url
        mark_list_url = self.browser.current_url
        self.assertRegex(mark_list_url, '/lists/.*')

        # now Daniel comes along to the site
        # we use a new browser login ofc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Daniel vists the homepage, no sign of mark's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Buy machinessss", page_text)


        # Daniel starts a new list by entering item
        self.inputItem("Spend all of my excess money")
        self.wait_for_item_in_list_table("Spend all of my excess money")

        # Daniel gets his own unique url
        daniel_list_url = self.browser.current_url
        self.assertRegex(daniel_list_url, '/lists/.*')
        self.assertNotEqual(mark_list_url, daniel_list_url)

        # Again no trace of Mark's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Buy machinessss", page_text)

        # satisfied

