import os
from domain.atendimento.atendimento_entity import Atendimento
from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface
import psycopg2
from psycopg2.extras import RealDictCursor

class AtendimentoRepository(AtendimentoRepositoryInterface):

    def __init__(self):
        self.dsn = os.getenv('DATABASE_URL')
        if not self.dsn:
            raise ValueError("DATABASE_URL environment variable not set")
        
        self.connection = psycopg2.connect(self.dsn)
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def post_atendimento(self, atendimento: Atendimento):
        self.session.commit()
        self.session.refresh(atendimento)

        return atendimento