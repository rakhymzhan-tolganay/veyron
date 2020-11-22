class User(object):
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        self.data = data
        self.is_authenticated = True

    def __str__(self):
        return str(self.data)
