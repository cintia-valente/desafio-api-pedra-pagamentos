from datetime import datetime
from unittest.mock import MagicMock
import pytest

from domain.atendimento.atendimento_entity import Atendimento
from domain.atendimento.atendimento_repository_interface import AtendimentoRepositoryInterface
from infrastructure.data.atendimento_repository import AtendimentoRepository
from usecases.atendimento.dtos.get_atendimentos_dto.get_atendimentos_by_cliente_input_dto import GetAtendimentosByClienteInputDto
from usecases.atendimento.dtos.post_atendimentos_dto.post_atendimento_input_dto import PostAtendimentoInputDto

@pytest.fixture
def mock_database_connection():
    conn_mock = MagicMock()

    cursor_mock = MagicMock()
    conn_mock.cursor.return_value = cursor_mock

    return conn_mock

@pytest.fixture
def mock_atendimento():
    mock_atendimento = MagicMock(spec=Atendimento)
    mock_atendimento.id_atendimento = 1
    mock_atendimento.id_cliente = 123
    mock_atendimento.angel = "A1"
    mock_atendimento.polo = "Polo1"
    mock_atendimento.data_limite = datetime(2025, 1, 25, 12, 0)
    mock_atendimento.data_de_atendimento = datetime(2025, 1, 26, 12, 0)
    
    return mock_atendimento


@pytest.fixture
def mock_cursor_data():
    columns = ["id_atendimento", "id_cliente", "angel", "polo", "data_limite", "data_de_atendimento"]
    result = [
        (1, 123, "Angel1", "Polo1", datetime(2025, 1, 25, 12, 0), datetime(2025, 1, 26, 12, 0)),
        (2, 123, "Angel2", "Polo2", datetime(2025, 2, 25, 12, 0), datetime(2025, 2, 26, 12, 0))
    ]
    
    return columns, result

@pytest.fixture
def mock_post_atendimento_input_dto(mock_atendimento):
    return PostAtendimentoInputDto(
        id_atendimento=mock_atendimento.id_atendimento,
        id_cliente=mock_atendimento.id_cliente,
        angel=mock_atendimento.angel,
        polo=mock_atendimento.polo,
        data_limite=mock_atendimento.data_limite,
        data_de_atendimento=mock_atendimento.data_de_atendimento
    )

@pytest.fixture
def atendimento_repository(mock_db_connection):
    return AtendimentoRepository(mock_db_connection)

@pytest.fixture
def mock_atendimento_repository_interface():
    return MagicMock(spec=AtendimentoRepositoryInterface)


@pytest.fixture
def mock_format_atendimento():
      return [
        Atendimento(1, 123, "Angel1", "Polo1", datetime(2025, 1, 25, 12, 0), datetime(2025, 1, 26, 12, 0)),
        Atendimento(2, 123, "Angel2", "Polo2", datetime(2025, 2, 25, 12, 0), datetime(2025, 2, 26, 12, 0))
    ]

@pytest.fixture
def mock_get_atendimentos_by_cliente_input_dto(mock_format_atendimento):
    return GetAtendimentosByClienteInputDto(
        id_cliente=123
    )
