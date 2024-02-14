from rich import print
from rich.console import Console
from rich.style import Style
from rich.prompt import Prompt

class ManagementConsole():

    console = Console()
    welcomeStyle = Style(color = "green", blink=True, bold=True, underline2=True)
    welcomeStyle2 = Style(color = "green", bold=True)
    closeStyle = Style(color = "red", blink=True, bold=True)
    # styles etc for console interface
    def __init__(self) -> None:
        self.currentChoice = 0
        pass


    def start(self):
        self.console.print("\n\n======== PROXY SERVER CONSOLE =========", style=self.welcomeStyle)
        self.console.print("\n The python proxy server is now running\n and all internet traffic will be passing\n through this proxy.\n to access the menu press ^C", style=self.welcomeStyle2)

    def end(self):
        self.console.print("\n\n======== PROXY SERVER SHUTDOWN =========", style=self.closeStyle)

    def getChoice(self):
        self.console.print("\n\nPlease select a choice from the list bellow:", style="green_yellow")
        self.console.print("1. Shutdown\n2. Block host\n3. Unblock host\n4. Show blocked list\n5. Show all connections that have been made", style="green_yellow")
        return Prompt.ask("Your choice")

    def ensure(self):
        return Prompt.ask("Are you sure you want to shut down the proxy?(Y/N) |")
    def block(self):
        return Prompt.ask("Please enter the host you want to block |")
    def unblock(self):
        return Prompt.ask("Please enter the host you want to unblock |")
    def printList(self, list):
        for host in list:
            self.console.print(host, style="magenta")
    def printClients(self, clients):
        self.console.print("List of servers and ports currently connected:\n")
        for server in clients:
            self.console.print(f"S: {server} || P: {clients[server]}\n", style="magenta")
    
    
    def printRequest(self, request):
        print(request)
        pass