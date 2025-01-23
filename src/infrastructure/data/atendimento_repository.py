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