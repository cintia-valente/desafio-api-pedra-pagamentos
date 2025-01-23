class GetAtendimentosClienteByAngelInputDto:
    def __init__(self, id_cliente: int, angel: str):
        self.id_cliente = id_cliente,
        self.angel = angel