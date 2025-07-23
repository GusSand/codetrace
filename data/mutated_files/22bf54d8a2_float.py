from typing import TypeAlias
__typ0 : TypeAlias = "Image"
"""
Changing contrast with PIL

This algorithm is used in
https://noivce.pythonanywhere.com/ python web app.

python/black: True
flake8 : True
"""

from PIL import Image


def change_contrast(__tmp2, level: <FILL>) :
    """
    Function to change contrast
    """
    factor = (259 * (level + 255)) / (255 * (259 - level))

    def __tmp0(__tmp1: int) :
        """
        Fundamental Transformation/Operation that'll be performed on
        every bit.
        """
        return 128 + factor * (__tmp1 - 128)

    return __tmp2.point(__tmp0)


if __name__ == "__main__":
    # Load image
    with __typ0.open("image_data/lena.jpg") as __tmp2:
        # Change contrast to 170
        cont_img = change_contrast(__tmp2, 170)
        cont_img.save("image_data/lena_high_contrast.png", format="png")
