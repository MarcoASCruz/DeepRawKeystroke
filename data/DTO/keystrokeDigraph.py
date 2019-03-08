class KeystrokeDigraph:
    def __init__(self,
                 firstKeyCode = None,
                 firstUpTime = None,
                 secondKeyCode = None,
                 secondDownTime=None,
                 secondUpTime = None):
        self.firstKeyCode = firstKeyCode;
        self.firstDownTime = 0;
        self.firstUpTime = int(firstUpTime);
        self.secondKeyCode = int(secondKeyCode);
        self.secondDownTime = int(secondDownTime);
        self.secondUpTime = int(secondUpTime);