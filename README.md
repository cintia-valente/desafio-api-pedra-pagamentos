# API REST de Atendimentos
#### Este é um projeto de uma API REST implementada em Python com o framweork Flask. A aplicação visa fornecer funcionalidades para gerenciar atendimentos de clientes, como inserção, consulta e atualização de registros.

## Estrutura do Projeto
O projeto foi organizado utilizando Clean Architecture, que visa separar as responsabilidades em camadas distintas. O fluxo de dados entre essas camadas é bem definido, o que facilita a manutenção e expansão do sistema.

```plaintext
📦src
│
├── app
│   └── app.py
│
├── domain
│   ├── atendimento
│   │   ├── atendimento_entity.py
│   │   └── atendimento_repository_interface.py
│   ├── cliente
│   │   └── cliente_entity.py
│   └── ___seedwork
│       └── use_case_interface.py
│
├── infrastructure
│   ├── data
│   │   ├── atendimento_repository.py
│   │   ├── bd_desafio.csv
│   │   └── bd_erros_de_conversao_datas.csv
│   ├── db
│   │   ├── create_tables.py
│   │   ├── database.py
│   │   └── insert_data.py
│   ├── process
│   │   └── processing.py
│   └── scripts
│       ├── load_data.py
│       └── main.py
│
├── tests
│   ├── e2e
│   │   └── test_api.py
│   ├── unit
│   │   └── test_atendimento_repository.py
│
├── usecases
│   ├── atendimento
│   │   ├── dtos
│   │   │   ├── get_atendimentos_dtos
│   │   │   │   ├── get_atendimentos_by_cliente_input_dto.py
│   │   │   │   └── get_atendimentos_cliente_by_angel_input_dto.py
│   │   │   ├── post_atendimentos_dtos
│   │   │   │   └── put_atendimento_input_dto.py
│   │   │   ├── put_atendimentos_dtos
│   │   │   │   └── put_atendimento_input_dto.py
│   │   │   └── atendimento_output_dto.py
│   │   ├── get_atendimentos
│   │   │   ├── get_atendimentos_by_id_cliente_usecase.py
│   │   │   └── get_atendimentos_cliente_by_angel_usecase.py
│   │   ├── post_atendimento
│   │   │   └── post_atendimento_usecase.py
│   │   └── put_atendimento
│   │       └── put_atendimento_usecase.py
│   └── factories
│       ├── get_atendimentos_by_id_cliente_usecase_factory.py
│       ├── get_atendimentos_cliente_by_angel_usecase_factory.py
│       ├── post_atendimento_usecase_factory.py
│       └── put_atendimento_usecase_factory.py
├── utils
│   ├── auth.py
│   ├── format.py
│   └── test_helpers.py
│
├── requirements.txt
├── Dockerfile
└── docker-compose.yaml
```

## Principais Diretórios e Arquivos:

- **src/app**: Contém a aplicação principal, como os endpoints e configurações do servidor.

- **src/domain**: Define as entidades e as interfaces de repositórios.

- **src/infrastructure**: Implementações dos repositórios, banco de dados e lógica de persistência.

- **src/usecases**: Casos de uso, DTOs e lógica de negócio da aplicação.

- **src/tests**: Testes unitário e end-to-end.

- **src/factories**: Contém as fábricas para criação dos casos de uso, promovendo o padrão Factory Method.

- **src/scripts**: Scripts auxiliares como load_data.py para carregar dados no banco de dados e efetuar a carga do arquivo CSV.

## Padrões de projeto
### Clean Architecture
A Arquitetura Limpa foi escolhida para separar claramente as responsabilidades do sistema em diferentes camadas, o que ajuda a manter o código organizado, testável e de fácil manutenção. A estrutura de pastas foi projetada para refletir os princípios dessa arquitetura, com o objetivo de garantir a independência das camadas e facilitar futuras extensões.

**Domain**: Esta camada contém as regras de negócios principais e as entidades de dados. Ela é independente de qualquer framework, biblioteca ou tecnologia externa. Temos:

- **atendimento_entity.py**: Define a entidade Atendimento, que representa os dados e comportamentos relacionados aos atendimentos.
- **cliente_entity.py**: Define a entidade Cliente.
- **atendimento_repository_interface.py**: Define a interface para o repositório de atendimentos, permitindo a implementação de diferentes soluções de persistência (banco de dados, arquivos, etc.), sem que a camada de domínio dependa delas.
- **use_case_interface.py**: Define a interface para os casos de uso, que são implementados na camada de usecases.

**Use Cases**: Contém a lógica de aplicação, ou seja, as regras específicas de como os dados e as entidades são manipulados. Cada caso de uso é responsável por uma operação que pode ser realizada no sistema.
Arquivos como **get_atendimentos_by_id_cliente_usecase.py** e **get_atendimentos_cliente_by_angel_usecase.py** são responsáveis por buscar atendimentos com base em diferentes critérios.

**Interfaces**: A camada de interfaces define contratos que permitem a comunicação entre a camada de aplicação (use cases) e a camada de infraestrutura (repositórios, bancos de dados, etc.). A interface do repositório **atendimento_repository_interface.py** é definida aqui, enquanto a implementação do repositório é feita em **infrastructure/data/atendimento_repository.py**.

**Infrastructure**: A camada de infraestrutura contém as implementações específicas para conectar-se ao banco de dados, fazer requisições a APIs externas e manipular arquivos. Ela implementa as interfaces definidas na camada de domínio:

- **atendimento_repository.py**: Implementa a interface do repositório de atendimentos, utilizando um banco de dados ou outra solução de persistência.
- Arquivos como **create_tables.py**, **database.py**, **insert_data.py** e **load_data.py** lidam com a configuração do banco de dados, criação de tabelas e inserção de dados.

## SOLID
A aplicação segue os princípios SOLID de design de software para garantir que o código seja bem estruturado, de fácil manutenção e escalabilidade.

**Responsabilidade Única (SRP):**

Cada classe e módulo tem uma única responsabilidade, como por exemplo:
 - **atendimento_entity.py** é responsável apenas por definir a estrutura da entidade Atendimento, sem envolver-se em lógica de persistência ou em detalhes de como os dados são manipulados.
 - **get_atendimentos_by_id_cliente_usecase.py** é responsável apenas por buscar atendimentos com base no ID do cliente, sem se preocupar com a lógica de armazenamento dos dados.

**Aberto/Fechado (OCP):**

 - O sistema está projetado de forma que novas funcionalidades podem ser adicionadas sem alterar o código existente, desde que as interfaces sejam respeitadas.
 - A adição de novos casos de uso, como **get_atendimentos_cliente_by_angel_usecase.py**, pode ser feita sem modificar os casos de uso já existentes, apenas implementando novas classes que estendem a interface definida.

**Substituição de Liskov (LSP):**

- As classes podem ser substituídas por suas subclasses sem afetar o comportamento do sistema. Por exemplo, diferentes implementações de repositórios (como um que use um banco de dados SQL e outro que use um arquivo CSV) podem ser substituídas sem afetar os casos de uso que as utilizam.

**Segregação de Interfaces (ISP):**

As interfaces são específicas, o que permite que as classes implementem apenas os métodos que realmente necessitam. Por exemplo:
- **atendimento_repository_interface.py** define os métodos que um repositório de atendimentos deve implementar, sem forçar uma implementação de métodos que não sejam necessários para o repositório específico.

**Inversão de Dependência (DIP):**

O projeto segue o princípio da inversão de dependência ao depender de abstrações (interfaces) em vez de implementações concretas.
Por exemplo, na camada de **usecases**, os casos de uso dependem da interface **atendimento_repository_interface.py** para buscar ou salvar atendimentos, mas não dependem diretamente da implementação específica do repositório (seja ela baseada em banco de dados ou arquivos).

## Design Patterns
### Factory Method

O padrão Factory Method é utilizado para criar objetos de forma flexível e desacoplada. Ele permite que os casos de uso e repositórios sejam criados sem que o código de execução precise saber os detalhes de como esses objetos são instanciados.

As fábricas são encontradas na pasta **usecases/factories**. Elas são responsáveis por criar instâncias dos casos de uso, fornecendo as dependências necessárias (como repositórios ou serviços).
Por exemplo, **get_atendimentos_by_id_cliente_usecase_factory.py** cria uma instância do caso de uso **get_atendimentos_by_id_cliente_usecase**, injetando o repositório correto (como o repositório baseado em banco de dados ou em arquivo CSV).

Exemplo de uma factory de caso de uso:
```
class GetAtendimentosByIdClienteUseCaseFactory:
    @staticmethod
    def create() -> GetAtendimentosByIdClienteUseCase:
        conn = connect_to_database(os.getenv("DATABASE_URL"))
        atendimento_repository = AtendimentoRepository(conn)
        return GetAtendimentosByIdClienteUseCase(atendimento_repository)
```

## Tratamento de Erros e Geração de CSV
Durante o processo de carga de dados a partir de arquivos CSV, é utilizado o Pandas para automaticamente identificar e converter os dados para os tipos esperados, como datas. No entanto, algumas entradas podem estar em um formato não reconhecível ou mal estruturado, o que pode impedir a conversão correta desses dados.

Quando o Pandas não consegue realizar a conversão de forma automática, essas entradas são identificadas como erros. Para garantir que o processo de carga não seja interrompido e que essas falhas não resultem na perda de dados, as entradas que não foram formatadas corretamente pelo Pandas são isoladas e armazenadas em um arquivo de erro separado, denominado bd_erros_de_conversao_datas.csv. 

Esse arquivo contém todas as entradas que não puderam ser convertidas corretamente, permitindo que elas sejam analisadas, corrigidas e processadas em uma carga de dados futura.

Essa abordagem assegura que o processo de carga de dados continue de maneira eficiente, sem ser interrompido por problemas de formato, e que estas entradas possam ser revisadas e corrigidas posteriormente.

## Docker
A aplicação foi contida utilizando Docker, o que facilita a configuração e execução do ambiente de desenvolvimento. O **docker-compose.yml** permite que todos os containers possam ser inicializados em conjunto sejam iniciados de maneira rápida e simples.


### Como Rodar a Aplicação

Para rodar a aplicação, siga os passos abaixo:

- **Clone o repositório**:
 ```
git clone <url-do-repositorio>
```

- **Configure as variáveis de ambiente***: Crie um arquivo **.env** na raiz do projeto com as variáveis necessárias, como a URL do banco de dados. Exemplo:

```
DATABASE_URL=postgres://user:password@localhost:5432/dbname
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_DB=nome_postgres
DATABASE_URL=postgres://postgres:senha@db:5432/nome_postgres
TOKEN="10a8b85a24031160459bca0025587b318581df6e7eee466e208dfbfd912d8b39"
```
**Token válido**:
TOKEN="10a8b85a24031160459bca0025587b318581df6e7eee466e208dfbfd912d8b39"


**Inicie os containers Docker**:
```
docker-compose up --build
```
A API estará disponível no Swagger UI **http://localhost:5000/apidocs/**.

Após acessar o Swagger UI:
- **cadastre** um usuário na url **/usuarios/registrar** 
- na url **/login** informe o usuário e senha cadastrados, ao clicar
em execute, retornará um token, copie a parte de dentro das aspas.
- no topo da tela, do lado direito, terá um botão **"Authorize"**.
- ao clicar no botão, abrirá um modal, insira o **token** JWT:
 Bearer <seu_token sem aspas>

   **Exemplo**:

  Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9frvrv7873w4gbvfvfbvv34vu

- clique em **"Authorize"** para aplicar o token às requisições.

Agora, ao testar as rotas protegidas, o Swagger 
enviará automaticamente o token de autenticação nas requisições, e a resposta de acordo com o estado de autenticação .

Isso permitirá utilizar as rotas protegidas diretamente no 
Swagger com o token de autenticação JWT.

Exemplo de um Atendimento:
````
{
  "angel": "Green Angel",
  "data_de_atendimento": "2025-01-21T10:00:00",
  "data_limite": "2025-01-22T12:00:00",
  "id_cliente": 77226365,
  "polo": "base"
}
````
## Testes

Foram implementados testes unitários e end-to-end para garantir o bom funcionamento da aplicação. Ao rodar docker-compose up --build os testes começarão após a execução da API.
