
class __typ0(object):

    def __init__(

            self,
            sk_id,
            displayName,
            city:        str,
            state:       <FILL>):

            self.sk_id = sk_id
            self.displayName = displayName
            self.city = city
            self.state = state

    def __str__(self):

            return "  \n" \
            "ID: {}   \n" \
            "Name: {} \n" \
            "City: {} \n" \
            "State: {}\n".format(

            str(self.sk_id),
            self.displayName,
            self.city,
            self.state)

