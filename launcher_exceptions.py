# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#     W T D E     L A U N C H E R + +     E X C E P T I O N S
#
#       All custom exceptions thrown by the GHWT: DE Launcher++.
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
""" All custom exceptions thrown by the WTDE Launcher++. """
# Non-matching number of inputs and widgets in the aspyr_key_encode() function.
class AspyrLenMismatchError(Exception):
    """ Raised by `aspyr_key_encode()` when the number of inputs and widgets do not match. """
    def __init__(self, message, *args):
        """ Raised by `aspyr_key_encode()` when the number of inputs and widgets do not match. """
        self.message = message
        super(AspyrLenMismatchError, self).__init__(message, *args)