from datetime import datetime 
from typing import List
import psycopg2
from domain.atendimento.atendimento_entity import Atendimento
from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface

class AtendimentoRepository(AtendimentoRepositoryInterface):

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def post_atendimento(self, atendimento: Atendimento) -> Atendimento:
        try:
            query = """
            INSERT INTO atendimentos (id_atendimento, id_cliente, angel, polo, data_limite, data_de_atendimento)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_atendimento;
            """
            self.cursor.execute(query, (
                atendimento.id_atendimento,
                atendimento.id_cliente,
                atendimento.angel,
                atendimento.polo,
                atendimento.data_limite,
                atendimento.data_de_atendimento
            ))

            row = self.cursor.fetchone() 
            self.conn.commit()

            if row:
                id_atendimento = row[0] 
                return Atendimento(
                    id_atendimento=id_atendimento,
                    id_cliente=atendimento.id_cliente,
                    angel=atendimento.angel,
                    polo=atendimento.polo,
                    data_limite=atendimento.data_limite,
                    data_de_atendimento=atendimento.data_de_atendimento
                )
            else:
                raise Exception("id_atendimento was not returned from the database")
        
        except psycopg2.DatabaseError as db_error:
            self.conn.rollback()
            raise Exception(f"Database error: {db_error}")

        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error inserting atendimento: {e}")
    
    def get_atendimentos_by_id_cliente(self, id_cliente: int) -> list[Atendimento]:
        query = "SELECT * FROM atendimentos WHERE id_cliente = %s"
        
        self.cursor.execute(query, (id_cliente,))

        columns = [desc[0] for desc in self.cursor.description]

        result = self.cursor.fetchall()

        atendimentos = [Atendimento(**dict(zip(columns, row))) for row in result]

        self.cursor.close()
        return atendimentos
    
    def get_atendimentos_cliente_by_angel(self, id_cliente: int, angel: str) -> list[Atendimento]:
        query = """
            SELECT * 
            FROM atendimentos 
            WHERE id_cliente = %s 
            AND angel = %s
        """
        
        self.cursor.execute(query, (id_cliente, angel))

        columns = [desc[0] for desc in self.cursor.description]

        result = self.cursor.fetchall()

        atendimentos = [Atendimento(**dict(zip(columns, row))) for row in result]

        self.cursor.close()

        return atendimentos
    
    def get_atendimento_by_id(self, id_atendimento: int) -> Atendimento:
        try:
            query = """
            SELECT id_atendimento, id_cliente, angel, polo, data_limite, data_de_atendimento
            FROM atendimentos
            WHERE id_atendimento = %s;
            """
            self.cursor.execute(query, (id_atendimento,))
            row = self.cursor.fetchone()

            if row:
                return Atendimento(
                    id_atendimento=row[0],
                    id_cliente=row[1],
                    angel=row[2],
                    polo=row[3],
                    data_limite=row[4],
                    data_de_atendimento=row[5]
                )
            else:
                raise Exception(f"Atendimento com id_atendimento {id_atendimento} não encontrado.")
        
        except psycopg2.DatabaseError as db_error:
            self.conn.rollback()
            raise Exception(f"Erro de banco de dados: {db_error}")
        
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Erro ao buscar atendimento: {e}")

    def put_atendimento(self, atendimento: Atendimento) -> Atendimento:
        try:
            if isinstance(atendimento.data_limite, str):
                atendimento.data_limite = datetime.strptime(atendimento.data_limite, '%Y-%m-%dT%H:%M:%S')
            
            if isinstance(atendimento.data_de_atendimento, str):
                atendimento.data_de_atendimento = datetime.strptime(atendimento.data_de_atendimento, '%Y-%m-%dT%H:%M:%S')

            query = """
            UPDATE atendimentos
            SET id_cliente = %s, angel = %s, polo = %s, data_limite = %s, data_de_atendimento = %s
            WHERE id_atendimento = %s
            RETURNING id_atendimento;
            """
            
            # Passar as variáveis como datetime para a consulta SQL
            self.cursor.execute(query, (
                atendimento.id_cliente,
                atendimento.angel,
                atendimento.polo,
                atendimento.data_limite,
                atendimento.data_de_atendimento,
                atendimento.id_atendimento,
            ))

            row = self.cursor.fetchone()
            self.conn.commit()

            if row:
                id_atendimento = row[0]
                return Atendimento(
                    id_atendimento=id_atendimento,
                    id_cliente=atendimento.id_cliente,
                    angel=atendimento.angel,
                    polo=atendimento.polo,
                    data_limite=atendimento.data_limite,
                    data_de_atendimento=atendimento.data_de_atendimento
                )
            else:
                raise Exception("No atendimento found with the provided id_atendimento")
        
        except psycopg2.DatabaseError as db_error:
            self.conn.rollback()
            raise Exception(f"Database error: {db_error}")

        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error updating atendimento: {e}")
