import datetime
from typing import Optional

class Atendimento:

    id_atendimento: int
    id_cliente: int
    angel: str
    polo: str
    data_limite: datetime
    data_de_atendimento: datetime
    
    def __init__(self,  id_atendimento: int,
                        id_cliente: int,
                        angel: str,
                        polo: str,
                        data_limite: datetime,
                        data_de_atendimento: datetime):
        self.id_atendimento = id_atendimento
        self.id_cliente = id_cliente
        self.angel = angel
        self.polo = polo
        self.data_limite = data_limite
        self.data_de_atendimento = data_de_atendimento

    def __str__(self):
        return (f"Atendimento(id_atendimento={self.id_atendimento}, "
                f"id_cliente={self.id_cliente}, angel={self.angel}, "
                f"polo={self.polo}, data_limite={self.data_limite}, "
                f"data_de_atendimento={self.data_de_atendimento})")

    def __repr__(self):
        return self.__str__()