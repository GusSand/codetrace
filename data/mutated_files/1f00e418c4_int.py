import math
import logging

import azure.functions as func


def __tmp0(req: func.HttpRequest) :
    logging.info("Python HTTP trigger function processed a request.")

    __tmp1 = req.params.get("number")
    try:
        __tmp1 = int(__tmp1)
    except TypeError:
        return func.HttpResponse(
            "Please pass an integer corresponding to the key `number` on the query string.",
            status_code=400,
        )

    response = "is prime" if is_prime(__tmp1) else "is composite"
    return func.HttpResponse(f"{__tmp1} {response}.")


def is_prime(__tmp1: <FILL>) :
    """Tests primeness of number, returns true if prime."""
    min_divisor = 2
    max_divisor = math.ceil(math.sqrt(__tmp1))
    for divisor in range(min_divisor, max_divisor + 1):
        if __tmp1 % divisor == 0:
            return False
    return True
