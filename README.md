# Construir as imagens e iniciar os containers
docker-compose up --build

📦src
 ┣ 📂app
 ┃ ┣ 📂__pycache__
 ┃ ┃ ┣ 📜app.cpython-313.pyc
 ┃ ┃ ┗ 📜__init__.cpython-313.pyc
 ┃ ┣ 📜app.py
 ┃ ┗ 📜__init__.py
 ┣ 📂domain
 ┃ ┣ 📂atendimento
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┣ 📜atendimento_entity.cpython-313.pyc
 ┃ ┃ ┃ ┗ 📜atendimento_repository_interface.cpython-313.pyc
 ┃ ┃ ┣ 📜atendimento_entity.py
 ┃ ┃ ┗ 📜atendimento_repository_interface.py
 ┃ ┣ 📂cliente
 ┃ ┃ ┣ 📜cliente_entity.py
 ┃ ┃ ┗ 📜cliente_repository.py
 ┃ ┗ 📂___seedwork
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┗ 📜use_case_interface.cpython-313.pyc
 ┃ ┃ ┗ 📜use_case_interface.py
 ┣ 📂infrastructure
 ┃ ┣ 📂data
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┗ 📜atendimento_repository.cpython-313.pyc
 ┃ ┃ ┣ 📜atendimento_repository.py
 ┃ ┃ ┣ 📜bd_desafio.csv
 ┃ ┃ ┗ 📜bd_erros_de_conversao_datas.csv
 ┃ ┣ 📂db
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┣ 📜create_tables.cpython-313.pyc
 ┃ ┃ ┃ ┣ 📜database.cpython-313.pyc
 ┃ ┃ ┃ ┗ 📜insert_data.cpython-313.pyc
 ┃ ┃ ┣ 📜create_tables.py
 ┃ ┃ ┣ 📜database.py
 ┃ ┃ ┗ 📜insert_data.py
 ┃ ┣ 📂process
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┗ 📜processing.cpython-313.pyc
 ┃ ┃ ┗ 📜processing.py
 ┃ ┗ 📂scripts
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┗ 📜load_data.cpython-313.pyc
 ┃ ┃ ┣ 📜load_data.py
 ┃ ┃ ┗ 📜main.py
 ┣ 📂usecases
 ┃ ┣ 📂atendimento
 ┃ ┃ ┣ 📂dtos
 ┃ ┃ ┃ ┣ 📂get_atendimentos_dtos
 ┃ ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┃ ┣ 📜get_atendimentos_by_cliente_input_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┃ ┗ 📜get_atendimentos_cliente_by_angel_input_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┣ 📜get_atendimentos_by_cliente_input_dto.py
 ┃ ┃ ┃ ┃ ┗ 📜get_atendimentos_cliente_by_angel_input_dto.py
 ┃ ┃ ┃ ┣ 📂post_atendimentos_dtos
 ┃ ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┃ ┗ 📜post_atendimento_input_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┗ 📜post_atendimento_input_dto.py
 ┃ ┃ ┃ ┣ 📂put_atendimentos_dto
 ┃ ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┃ ┗ 📜put_atendimento_input_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┗ 📜put_atendimento_input_dto.py
 ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┣ 📜atendimento_output_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┣ 📜get_atendimentos_by_cliente_and_angel_input_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┣ 📜get_atendimentos_by_cliente_input_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┣ 📜get_atendimentos_by_id_cliente_input_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┣ 📜get_atendimentos_by_id_cliente_output_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┣ 📜get_atendimentos_cliente_by_angel_input_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┣ 📜get_atendimentos_input_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┗ 📜get_atendimentos_output_dto.cpython-313.pyc
 ┃ ┃ ┃ ┗ 📜atendimento_output_dto.py
 ┃ ┃ ┣ 📂get_atendimentos
 ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┣ 📜get_atendimentos_by_cliente_and_angel_usecase.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┣ 📜get_atendimentos_by_id_cliente_input_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┣ 📜get_atendimentos_by_id_cliente_output_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┣ 📜get_atendimentos_by_id_cliente_usecase.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┗ 📜get_atendimentos_cliente_by_angel_usecase.cpython-313.pyc
 ┃ ┃ ┃ ┣ 📜get_atendimentos_by_id_cliente_usecase.py
 ┃ ┃ ┃ ┗ 📜get_atendimentos_cliente_by_angel_usecase.py
 ┃ ┃ ┣ 📂post_atendimento
 ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┣ 📜post_atendimento_input_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┣ 📜post_atendimento_output_dto.cpython-313.pyc
 ┃ ┃ ┃ ┃ ┗ 📜post_atendimento_usecase.cpython-313.pyc
 ┃ ┃ ┃ ┗ 📜post_atendimento_usecase.py
 ┃ ┃ ┗ 📂put_atendimento
 ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┗ 📜put_atendimento_usecase.cpython-313.pyc
 ┃ ┃ ┃ ┗ 📜put_atendimento_usecase.py
 ┃ ┗ 📂factories
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┣ 📜get_atendimentos_by_cliente_and_angel_usecase_factory.cpython-313.pyc
 ┃ ┃ ┃ ┣ 📜get_atendimentos_by_id_cliente_usecase_factory.cpython-313.pyc
 ┃ ┃ ┃ ┣ 📜get_atendimentos_cliente_by_angel_usecase_factory.cpython-313.pyc
 ┃ ┃ ┃ ┣ 📜get_atendimentos_usecase_factory.cpython-313.pyc
 ┃ ┃ ┃ ┣ 📜post_atendimento_usecase_factory.cpython-313.pyc
 ┃ ┃ ┃ ┗ 📜put_atendimento_usecase_factory.cpython-313.pyc
 ┃ ┃ ┣ 📜get_atendimentos_by_id_cliente_usecase_factory.py
 ┃ ┃ ┣ 📜get_atendimentos_cliente_by_angel_usecase_factory.py
 ┃ ┃ ┣ 📜post_atendimento_usecase_factory.py
 ┃ ┃ ┗ 📜put_atendimento_usecase_factory.py
 ┣ 📂__pycache__
 ┃ ┗ 📜app.cpython-313.pyc
 ┗ 📜requirements.txt