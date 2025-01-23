import datetime

class PutAtendimentoInputDto:
    def __init__(self, id_atendimento: int,
                       id_cliente: int = None,
                       angel: str = None,
                       polo: str = None,
                       data_limite: datetime = None,
                       data_de_atendimento: datetime = None):
        self.id_atendimento = id_atendimento
        self.id_cliente = id_cliente
        self.angel = angel
        self.polo = polo
        self.data_limite = data_limite
        self.data_de_atendimento = data_de_atendimento
