from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Mark goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # He notices that the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

        self.inputItem('testing')
        self.wait_for_item_in_list_table('1: testing')

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)
