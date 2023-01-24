import time

class Utils:
    def generateRandomId():
        return f"uuid-{str(time.time()).split('.')[0]}"
