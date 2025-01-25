import pytest
from domain.atendimento.atendimento_entity import Atendimento
from unittest.mock import MagicMock
from psycopg2 import DatabaseError

from infrastructure.data.atendimento_repository import AtendimentoRepository

def test_post_atendimento_success(mock_atendimento):
    params = (
        mock_atendimento.id_atendimento,
        mock_atendimento.id_cliente,
        mock_atendimento.angel,
        mock_atendimento.polo,
        mock_atendimento.data_limite,
        mock_atendimento.data_de_atendimento,
    )

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = [1]  

    atendimento_repository = AtendimentoRepository(mock_conn)

    post_return = atendimento_repository.post_atendimento(mock_atendimento)

    except_query = """
                INSERT INTO atendimentos (id_atendimento, id_cliente, angel, polo, data_limite, data_de_atendimento)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_atendimento;
                """
    
    mock_cursor.execute.assert_called_once_with(except_query, params)
    assert isinstance(post_return, Atendimento)

def test_post_atendimento_id_not_returned(mock_atendimento, mock_database_connection):
    mock_cursor = MagicMock()
    mock_database_connection.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    atendimento_repository = AtendimentoRepository(mock_database_connection)
    
    with pytest.raises(Exception) as exc_info:
        atendimento_repository.post_atendimento(mock_atendimento)
    
    assert "id_atendimento was not returned from the database" in str(exc_info.value)

def test_post_atendimento_database_error(mock_atendimento, mock_database_connection):
    mock_cursor = MagicMock()
    mock_database_connection.cursor.return_value = mock_cursor
    
    mock_cursor.execute.side_effect = DatabaseError("Database error")
    
    atendimento_repository = AtendimentoRepository(mock_database_connection)
    
    with pytest.raises(Exception) as exc_info:
        atendimento_repository.post_atendimento(mock_atendimento)

    assert "Database error" in str(exc_info.value)

def test_get_atendimentos_by_id_cliente_success(mock_cursor_data):
    columns, result = mock_cursor_data
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = result
    mock_cursor.description = [(col,) for col in columns]

    atendimento_repository = AtendimentoRepository(mock_conn)

    id_cliente = 123
    get_by_id_cliente_return = atendimento_repository.get_atendimentos_by_id_cliente(id_cliente)

    mock_cursor.execute.assert_called_once_with("SELECT * FROM atendimentos WHERE id_cliente = %s", (id_cliente,))
    assert get_by_id_cliente_return[0].id_atendimento == 1
    assert get_by_id_cliente_return[1].id_atendimento == 2  
    assert len(get_by_id_cliente_return) == 2 

def test_get_atendimentos_by_id_cliente_database_error():    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.execute.side_effect = DatabaseError("Simulated database error")
    
    atendimento_repository = AtendimentoRepository(mock_conn)

    id_cliente = 123

    with pytest.raises(Exception) as exc_info:
        atendimento_repository.get_atendimentos_by_id_cliente(id_cliente)

    assert "An error occurred while retrieving atendimentos" in str(exc_info.value)

def test_get_atendimentos_by_id_cliente_unexpected_error():    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.execute.side_effect = Exception("Simulated unexpected error")
    
    atendimento_repository = AtendimentoRepository(mock_conn)
    
    id_cliente = 123

    with pytest.raises(Exception) as exc_info:
        atendimento_repository.get_atendimentos_by_id_cliente(id_cliente)

    assert "An unexpected error occurred while retrieving atendimentos" in str(exc_info.value)

def test_get_atendimentos_cliente_by_angel_sucess(mock_cursor_data):
    columns, result = mock_cursor_data
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = result
    mock_cursor.description = [(col,) for col in columns]

    atendimento_repository = AtendimentoRepository(mock_conn)

    id_cliente = 123
    angel = "Angel1"
    get_by_id_cliente_return = atendimento_repository.get_atendimentos_cliente_by_angel(id_cliente, angel)

    except_query = """
                SELECT * 
                FROM atendimentos 
                WHERE id_cliente = %s 
                AND angel = %s
            """

    mock_cursor.execute.assert_called_once_with(except_query, (id_cliente, angel))
    assert get_by_id_cliente_return[0].id_atendimento == 1
    assert get_by_id_cliente_return[1].id_atendimento == 2
    assert len(get_by_id_cliente_return) == 2 

def test_get_atendimentos_by_id_cliente_database_error():    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.execute.side_effect = DatabaseError("Simulated database error")
    
    atendimento_repository = AtendimentoRepository(mock_conn)

    id_cliente = 123
    angel = "Angel1"
    
    with pytest.raises(Exception) as exc_info:
        atendimento_repository.get_atendimentos_cliente_by_angel(id_cliente, angel)

    assert "An error occurred while retrieving atendimentos by angel" in str(exc_info.value)

def test_get_atendimentos_by_id_cliente_unexpected_error():    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.execute.side_effect = Exception("Simulated unexpected error")
    
    atendimento_repository = AtendimentoRepository(mock_conn)

    id_cliente = 123
    angel = "Angel1"

    with pytest.raises(Exception) as exc_info:
        atendimento_repository.get_atendimentos_cliente_by_angel(id_cliente, angel)

    assert "An unexpected error occurred while retrieving atendimentos by angel" in str(exc_info.value)

def test_get_atendimento_by_id_success(mock_cursor_data):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    _, result = mock_cursor_data
    mock_cursor.fetchone.return_value = result[0]

    atendimento_repository = AtendimentoRepository(mock_conn)

    id_atendimento = 1
    atendimento = atendimento_repository.get_atendimento_by_id(id_atendimento)

    except_query = """
                SELECT id_atendimento, id_cliente, angel, polo, data_limite, data_de_atendimento
                FROM atendimentos
                WHERE id_atendimento = %s;
            """
    
    mock_cursor.execute.assert_called_once_with(except_query, (id_atendimento,))
    assert isinstance(atendimento, Atendimento)
    assert atendimento.id_atendimento == result[0][0]
    assert atendimento.id_cliente == result[0][1]
    assert atendimento.angel == result[0][2]
    assert atendimento.polo == result[0][3]
    assert atendimento.data_limite == result[0][4]
    assert atendimento.data_de_atendimento == result[0][5]

def test_get_atendimento_by_id_not_found():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    atendimento_repository = AtendimentoRepository(mock_conn)
    id_atendimento = 1

    with pytest.raises(Exception) as exc_info:
        atendimento_repository.get_atendimento_by_id(id_atendimento)

    assert "Erro while fetching atendimento: Atendimento with id_atendimento 1 not found" in str(exc_info.value)

def test_get_atendimento_by_id_database_error():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = DatabaseError("Database error")

    atendimento_repository = AtendimentoRepository(mock_conn)
    id_atendimento = 1
    
    with pytest.raises(Exception) as exc_info:
        atendimento_repository.get_atendimento_by_id(id_atendimento)

    assert "Database error" in str(exc_info.value)

def test_get_atendimento_by_id_unexpected_error():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = Exception("Simulated unexpected error")

    atendimento_repository = AtendimentoRepository(mock_conn)
    id_atendimento = 1

    with pytest.raises(Exception) as exc_info:
        atendimento_repository.get_atendimento_by_id(id_atendimento)

    assert "Erro while fetching atendimento" in str(exc_info.value)
  
def test_put_atendimento_success(mock_atendimento):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (mock_atendimento.id_atendimento,)

    atendimento_repository = AtendimentoRepository(mock_conn)

    updated_atendimento = atendimento_repository.put_atendimento(mock_atendimento)

    query = """
                UPDATE atendimentos
                SET id_cliente = %s, angel = %s, polo = %s, data_limite = %s, data_de_atendimento = %s
                WHERE id_atendimento = %s
                RETURNING id_atendimento;
            """
    mock_cursor.execute.assert_called_once_with(query, (
        mock_atendimento.id_cliente,
        mock_atendimento.angel,
        mock_atendimento.polo,
        mock_atendimento.data_limite,
        mock_atendimento.data_de_atendimento,
        mock_atendimento.id_atendimento,
    ))
    
    assert updated_atendimento.id_atendimento == mock_atendimento.id_atendimento
    assert updated_atendimento.id_cliente == mock_atendimento.id_cliente
    assert updated_atendimento.angel == mock_atendimento.angel
    assert updated_atendimento.polo == mock_atendimento.polo
    assert updated_atendimento.data_limite == mock_atendimento.data_limite
    assert updated_atendimento.data_de_atendimento == mock_atendimento.data_de_atendimento

def test_put_atendimento_not_found(mock_atendimento):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    atendimento_repository = AtendimentoRepository(mock_conn)

    with pytest.raises(Exception) as exc_info:
        atendimento_repository.put_atendimento(mock_atendimento)

    assert "No atendimento found with the provided id_atendimento" in str(exc_info.value)

def test_put_atendimento_database_error(mock_atendimento):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = DatabaseError("Database error")

    atendimento_repository = AtendimentoRepository(mock_conn)

    with pytest.raises(Exception) as exc_info:
        atendimento_repository.put_atendimento(mock_atendimento)

    assert "Database error" in str(exc_info.value)

def test_put_atendimento_generic_error(mock_atendimento):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = Exception("Unexpected error")

    atendimento_repository = AtendimentoRepository(mock_conn)

    with pytest.raises(Exception) as exc_info:
        atendimento_repository.put_atendimento(mock_atendimento)

    assert "Error updating atendimento: Unexpected error" in str(exc_info.value)
