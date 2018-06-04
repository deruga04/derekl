class async_server:
    def __init__(self, account, done_fun, long=1):
        self.name, self.host = tuple(string.split(account, '@'))
        self.done_fun = done_fun