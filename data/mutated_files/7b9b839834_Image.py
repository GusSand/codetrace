from typing import TypeAlias
__typ1 : TypeAlias = "int"
__typ0 : TypeAlias = "float"
"""
Changing contrast with PIL

This algorithm is used in
https://noivce.pythonanywhere.com/ python web app.

python/black: True
flake8 : True
"""

from PIL import Image


def __tmp2(__tmp3: <FILL>, __tmp0: __typ0) -> Image:
    """
    Function to change contrast
    """
    factor = (259 * (__tmp0 + 255)) / (255 * (259 - __tmp0))

    def __tmp1(c: __typ1) -> __typ0:
        """
        Fundamental Transformation/Operation that'll be performed on
        every bit.
        """
        return 128 + factor * (c - 128)

    return __tmp3.point(__tmp1)


if __name__ == "__main__":
    # Load image
    with Image.open("image_data/lena.jpg") as __tmp3:
        # Change contrast to 170
        cont_img = __tmp2(__tmp3, 170)
        cont_img.save("image_data/lena_high_contrast.png", format="png")
