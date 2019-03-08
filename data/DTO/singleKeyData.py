class SingleKeyData:
    def __init__(self, keyCode = None, initialTime = None, upTime = None):
        self.keyCode = keyCode;
        self.initialTime = initialTime;
        self.downTime = 0;
        self.upTime = upTime;
