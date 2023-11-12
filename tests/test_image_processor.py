import unittest
from image_processor import ImageProcessor
from tkinter import Event

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()

    def test_randomize_subdirectory_names(self):
        # Assuming you have a directory with subdirectories for this test
        directory = "./data/rips"
        new_names = self.processor.randomize_subdirectory_names(directory)
        self.assertIsInstance(new_names, list)

    def test_get_character_from_keypress(self):
        event = Event()
        event.char = 'a'
        result = self.processor.get_character_from_keypress(event)
        self.assertEqual(result, 'a')

        event.char = '1'
        result = self.processor.get_character_from_keypress(event)
        self.assertEqual(result, 'UNKNOWN')

    def test_extract_string2(self):
        input_string = "string1_string2-123"
        result = self.processor.extract_string2(input_string)
        self.assertEqual(result, 'string2')

        input_string = "string1"
        result = self.processor.extract_string2(input_string)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()