

class Error(Exception):
    pass


#Exception raise when user attempts to do a forbidden/unavailable action in the game
class IvalidActionError(Error):
    def __init__(self,message):
        self.message = message


if __name__ == "__main__":
    print("Check what file .py are you running...")

    