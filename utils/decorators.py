class IconicDecorator(object):
    def __init__(self):
        self.PASS = "[ ✔ ]"
        self.FAIL = "[ ✘ ]"
        self.WARN = "[ ! ]"
        self.HEAD = "[ # ]"
        self.CMDL = "[ → ]"
        self.STDS = "     "


class StatusDecorator(object):
    def __init__(self):
        self.PASS = "[ SUCCESS ]"
        self.FAIL = "[ FAILURE ]"
        self.WARN = "[ WARNING ]"
        self.HEAD = "[ SECTION ]"
        self.CMDL = "[ COMMAND ]"
        self.STDS = "           "


class MessageDecorator(object):
    def __init__(self, attr):
        ICON = IconicDecorator()
        STAT = StatusDecorator()
        if attr == "icon":
            self.PASS = ICON.PASS
            self.FAIL = ICON.FAIL
            self.WARN = ICON.WARN
            self.HEAD = ICON.HEAD
            self.CMDL = ICON.CMDL
            self.STDS = ICON.STDS
        elif attr == "stat":
            self.PASS = STAT.PASS
            self.FAIL = STAT.FAIL
            self.WARN = STAT.WARN
            self.HEAD = STAT.HEAD
            self.CMDL = STAT.CMDL
            self.STDS = STAT.STDS

    def SuccessMessage(self, RequestMessage):
        print(self.PASS + " " + RequestMessage)

    def FailureMessage(self, RequestMessage):
        print(self.FAIL + " " + RequestMessage)

    def WarningMessage(self, RequestMessage):
        print(self.WARN + " " + RequestMessage)

    def SectionMessage(self, RequestMessage):
        print(self.HEAD + " " + RequestMessage)

    def CommandMessage(self, RequestMessage):
        return self.CMDL + " " + RequestMessage

    def GeneralMessage(self, RequestMessage):
        print(self.STDS + " " + RequestMessage)
