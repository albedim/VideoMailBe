class GException(Exception):
    message = "An error occured while performing this action. {error}"
    code = 500

    def __init__(self, err=None):
        self.message = self.message.replace("{error}", str(err))