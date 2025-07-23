
class Venue(object):

    def __tmp1(

            __tmp0,
            sk_id,
            displayName,
            city:        <FILL>,
            state):

            __tmp0.sk_id = sk_id
            __tmp0.displayName = displayName
            __tmp0.city = city
            __tmp0.state = state

    def __tmp2(__tmp0):

            return "  \n" \
            "ID: {}   \n" \
            "Name: {} \n" \
            "City: {} \n" \
            "State: {}\n".format(

            str(__tmp0.sk_id),
            __tmp0.displayName,
            __tmp0.city,
            __tmp0.state)

