from typing import TypeAlias
__typ0 : TypeAlias = "float"
"""
Changing contrast with PIL

This algorithm is used in
https://noivce.pythonanywhere.com/ python web app.

python/black: True
flake8 : True
"""

from PIL import Image


def change_contrast(img, level) -> Image:
    """
    Function to change contrast
    """
    factor = (259 * (level + 255)) / (255 * (259 - level))

    def contrast(__tmp0: <FILL>) :
        """
        Fundamental Transformation/Operation that'll be performed on
        every bit.
        """
        return 128 + factor * (__tmp0 - 128)

    return img.point(contrast)


if __name__ == "__main__":
    # Load image
    with Image.open("image_data/lena.jpg") as img:
        # Change contrast to 170
        cont_img = change_contrast(img, 170)
        cont_img.save("image_data/lena_high_contrast.png", format="png")
