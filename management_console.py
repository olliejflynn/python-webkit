

class ManagementConsole():


    # styles etc for console interface
    def __init__(self) -> None:
        self.currentChoice = 0
        pass


    def start(self):
        print("\n\n ======= PROXY SERVER CONSOLE ========")

    def end(self):
        print("\n\n ======= PROXY SERVER SHUTDOWN ========")

    def getChoice(self):
        print("\n\nPlease select a choice from the list bellow:")
        print("1. Shutdown\n2. Block host\n3. Unblock host\n4. Show blocked list")
        return input("Your choice")

    def ensure(self):
        return input("Are you sure you want to shut down the proxy?(Y/N) |")
    def block(self):
        return input("Please enter the host you want to block | default", default="")
    def unblock(self):
        return input("Please enter the host you want to unblock | default", default="")
    def printList(self, list):
        for host in list:
            print(host)
    