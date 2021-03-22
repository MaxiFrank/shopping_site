"""Customers at Hackbright."""


class Customer(object):
    """Ubermelon customer."""
    def __init__(self,first_name, last_name, user_name, password):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = password

    def __repr__(self):
        """Convenience method to show information about melon in console."""

        return "<Customer: {}, {}, {}, {}>".format(self.first_name, self.last_name, self.user_name, self.password)
    
def create_customer_list(filepath):
    customer_file = open(filepath, 'r')
    customer_dict = {}
    for line in customer_file:
        first_name, last_name, user_name, password = line.split("|")
        password = password.strip()
        customer_dict[user_name] = Customer(first_name, last_name, user_name, password)
    return customer_dict

def get_by_email(email):
    return customer_dict.get(email, None)

customer_dict = create_customer_list('customers.txt')


