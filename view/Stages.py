# Classe que manipula os estados da aplicação
class AplicationState:
    def __init__(self):
        self.current_stage = "inputs"

    def advance(self):
        if self.current_stage == "inputs":
            self.current_stage = "training"
        elif self.current_stage == "training":
            self.current_stage = "dashboards"

    def rewind(self):
        if self.current_stage == "dashboards":
            self.current_stage = "training"
        elif self.current_stage == "training":
            self.current_stage = "inputs"
