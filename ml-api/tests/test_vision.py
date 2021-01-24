import unittest
from PIL import Image
from ..mllib import vision


class TestVision(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_vision(self):
        input_image = Image.open("./test_images/human.jpg")
        output_image = vision.get_segments(input_image)
        output_image.save("./test_images/output.png")
