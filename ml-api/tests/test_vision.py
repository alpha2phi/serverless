import unittest
from PIL import Image


class TestVision(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_vision(self):
        Image.open("./test_images/uploaded.png")
