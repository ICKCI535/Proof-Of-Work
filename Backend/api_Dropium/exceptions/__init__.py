

class IdentityNotMatchException(Exception):
    def __init__(self, *args, **kwargs):
        if not args: args = ("Identity not match",)

        # Call super constructor
        super().__init__(*args, **kwargs)


    
class DataValidationException(Exception):
    def __init__(self, *args, **kwargs):

        # Call super constructor
        super().__init__(*args, **kwargs)
