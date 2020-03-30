from unittest import skip
from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Mark goes to the home page and accidently tries to submit an empty list item

        # He submits and the page refreshes saying there cannot be an empty item

        # He tries again with some text and it works

        # He then writes another blank message and gets the similar warning 

        # He can then correct it by writing some text
        self.fail("Write me")
        
