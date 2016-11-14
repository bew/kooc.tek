class KError(Exception):
    """Error class for all Kooc exceptions"""

class KUnsupportedFeature(KError):
    """You tried to use an unsupported feature"""

    def __init__(self, what):
        KError.__init__(self, 'You tried to use an unsupported feature: ' + what)

