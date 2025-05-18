import os

# Chemin vers le fichier de log	
LOGFILE = "{}/suspicious_domains.log".format(os.path.dirname(os.path.abspath(__file__)))

class Logger:
    def __init__(self, print_logs: bool = False):
        self.print_logs = print_logs

    def alert(self, message: str):
        # Ouverture mode ajout
        with open(LOGFILE, "a") as f:
            f.write(message + "\n")

        if self.print_logs:
            print(message)
