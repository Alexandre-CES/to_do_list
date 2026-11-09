# Lista de tarefas

Aplicação web de lista de tarefas feita com Flask. Usuários podem criar uma conta, entrar, registrar tarefas com prioridade e datas, e trocar solicitações de amizade para visualizar as tarefas de amigos.

> Esta documentação descreve o código-fonte atual. O repositório contém um banco SQLite em `instance/tasks.db`, mas o código não contém migrações nem uma rotina que crie o esquema automaticamente. Por isso, a execução em uma instalação nova depende de um banco com as tabelas esperadas; esse preparo não pode ser confirmado pelo código disponível.

## Funcionalidades implementadas

- Cadastro, login e logout de usuários.
- Alteração de nome de exibição e senha.
- Cadastro e listagem de tarefas próprias com prioridade (0 a 3), descrição, início e término.
- Coloração visual de prioridades 1, 2 e 3 e cálculo no navegador do tempo até o término.
- Solicitações de amizade por ID, aceitação ou rejeição, listagem de amigos e visualização das tarefas de um amigo.
- Proteção de páginas por sessão com o decorator `login_required`.

O código não oferece edição ou exclusão de tarefas. A coluna “Tempo restante” existe na interface; o JavaScript tenta calculá-la a partir do horário de início e término.

## Tecnologias

- Python e Flask 3, com templates Jinja.
- Flask-SQLAlchemy e SQLAlchemy para persistência relacional.
- SQLite, configurado em `configs/config.py` como `sqlite:///tasks.db` (no Flask-SQLAlchemy, o caminho relativo fica associado à pasta `instance`).
- Flask-Session com armazenamento de sessão em arquivos temporários.
- Werkzeug para hash e verificação de senhas.
- HTML, CSS e JavaScript no navegador. Os ícones Bootstrap Icons são carregados de um CDN externo.

As versões declaradas estão em `requirements.txt`. A lista também inclui `requests`, mas não foi encontrado uso dessa biblioteca no código da aplicação.

## Estrutura do projeto

```text
.
├── app.py                    # Cria e configura a aplicação, registra rotas e blueprints
├── extensions.py             # Instância compartilhada de SQLAlchemy
├── configs/
│   └── config.py              # Configuração de sessão e URI do banco
├── blueprints/
│   ├── account/account.py     # Cadastro, login e configurações da conta
│   ├── tasks/tasks.py         # Criação de tarefas
│   └── friends/friends.py    # Solicitações, amizades e tarefas de amigos
├── models/
│   ├── User.py               # Modelo de usuário
│   ├── Task.py               # Modelo de tarefa
│   ├── Friend.py             # Relação de amizade
│   └── Request.py            # Solicitação de amizade pendente
├── helpers/helpers.py        # Decorator de autenticação e página de erro
├── templates/                # Páginas Jinja renderizadas pelo Flask
├── static/
│   ├── css/style.css         # Estilos
│   ├── scripts/dom.js        # Comportamentos de interface e temporizador
│   └── images/               # Ícones e imagem de erro
├── instance/                  # Banco SQLite local presente neste repositório
├── requirements.txt          # Dependências Python fixadas por versão
└── README.md
```

## Como a aplicação funciona

### Inicialização e roteamento

`app.py` cria `Flask(__name__)`, carrega a classe `Config`, conecta a extensão `db` à aplicação e inicializa `Session`. Em seguida importa e registra os blueprints `account`, `friends` e `tasks`. Blueprints agrupam rotas por assunto; seus endpoints são prefixados pelo nome do blueprint, como `account.login` e `tasks.add_task`. A rota principal `/` fica diretamente em `app.py`.

Ao executar `python app.py`, o bloco final chama `app.run(debug=True)`. Isso inicia o servidor de desenvolvimento do Flask com depuração habilitada; não é uma configuração apropriada para publicar o serviço em produção.

### Sessão e autenticação

O login em `blueprints/account/account.py` procura o usuário pelo identificador textual `user`, verifica a senha com `check_password_hash` e coloca o ID numérico em `session['user_id']`. `login_required`, em `helpers/helpers.py`, verifica esse valor antes de permitir acesso às rotas decoradas; sem login, redireciona para `account.login`. O logout limpa a sessão.

A configuração define `SESSION_TYPE = 'filesystem'`, `SESSION_PERMANENT = False` e cria um diretório temporário para arquivos de sessão. Não há variável de ambiente nem `SECRET_KEY` declarada no código de configuração; o comportamento completo de assinatura/persistência deve ser revisto antes de qualquer implantação.

### Modelos e armazenamento

`extensions.py` cria uma instância única de `SQLAlchemy`, importada pelos modelos e pelas rotas. Os modelos declaram as tabelas:

- `User` (`users`): ID, identificador de login, nome de exibição e hash da senha.
- `Task` (`tasks`): dono, prioridade, título, descrição e horários.
- `Friend` (`friends`): uma linha direcionada de usuário para amigo. A amizade recíproca é representada por duas linhas.
- `Request` (`requests`): solicitante e destinatário de uma solicitação pendente.

As rotas fazem consultas com `Model.query.filter_by(...).first()` ou `.all()`, e persistem alterações com `db.session.add`, `delete` e `commit`. Embora existam chaves estrangeiras declaradas, não há relacionamentos ORM (`relationship`) nem regras de cascata configuradas. Também não há `db.create_all()` ou migração no código: declarar modelos não cria tabelas por si só.

### Fluxos principais

1. **Cadastro e conta:** `/register` valida campos e tamanhos, gera hash da senha e grava o usuário. `/login` inicia a sessão; as rotas de configurações verificam a senha atual antes de alterar dados.
2. **Tarefas:** `/add_task` recebe o formulário, converte datas com `datetime.strptime`, associa a tarefa ao ID da sessão e grava no banco. `/` consulta as tarefas do usuário atual e formata os horários para exibição.
3. **Amigos:** `/add_friend` recebe um ID. Se já existe uma solicitação no sentido inverso, o código a remove e cria os dois registros de amizade; caso contrário, grava uma solicitação. As rotas de aceitar/rejeitar recebem o ID do solicitante pela URL. A listagem e a consulta de tarefas verificam a relação antes de mostrar tarefas de outra pessoa.
4. **Interface:** os templates em `templates/` herdam de `layout.html`. O Flask/Jinja insere valores e gera URLs com `url_for`. `static/scripts/dom.js` altera a aparência da prioridade e atualiza o tempo restante no cliente, sem comunicação assíncrona com o servidor.

## Instalação e execução

### Pré-requisitos

- Python compatível com as versões das dependências listadas em `requirements.txt`.
- Um banco SQLite que contenha as tabelas e colunas descritas pelos modelos.

O projeto não documenta nem implementa um comando de criação/migração do esquema. O arquivo `instance/tasks.db` está presente no repositório, mas não é possível garantir que ele seja adequado a uma instalação limpa ou que deva ser distribuído com dados existentes.

### Passos

1. Clone o repositório e entre na pasta:

   ```bash
   git clone https://github.com/Alexandre-CES/to_do_list.git
   cd to_do_list
   ```

2. Crie e ative um ambiente virtual (opcional, recomendado) e instale as dependências:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   # Linux/macOS: source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Antes de iniciar, confirme que `instance/tasks.db` contém as quatro tabelas (`users`, `tasks`, `friends`, `requests`) com as colunas definidas em `models/`. Não há procedimento de inicialização do banco confirmado no código.

4. Inicie o servidor de desenvolvimento:

   ```bash
   python app.py
   ```

O código não define variáveis de ambiente obrigatórias. A URI SQLite está fixa em `configs/config.py`; alterar sua localização exige alterar essa configuração. A aplicação imprime o endereço do servidor no terminal ao iniciar, mas uma inicialização funcional não foi testada para esta documentação.

## Exemplos de uso

- Acesse `/register`, crie uma conta e depois entre em `/login`.
- Na página inicial, veja suas tarefas; use “Adicionar tarefa” para registrar prioridade, título, descrição e horários.
- Em “Adicionar amigo”, informe o ID exibido na página da outra conta. A pessoa pode aceitar ou rejeitar o pedido.
- Em “Amigos”, abra a visualização de tarefas de uma amizade aceita.
- Em configurações, altere o nome de exibição ou a senha informando a senha atual.

## Limitações e pontos de atenção

- O esquema do banco não é criado pelo aplicativo e não há migrações incluídas.
- O servidor é iniciado com `debug=True`; use servidor apropriado e configuração segura antes de disponibilizar em rede.
- Formulários de alteração de estado usam GET em ações como aceitar/rejeitar solicitação e logout, e não há proteção CSRF visível.
- A rota de aceitar/rejeitar não trata solicitação inexistente antes de tentar excluí-la. A rota de visualização de tarefas também pode falhar se um registro de amizade apontar para usuário ausente.
- Em `add_task`, a verificação de tamanho chama `apology(...)` sem retornar a resposta; o fluxo continua e pode gravar os dados. Datas inválidas também não são tratadas. O cálculo de duração do JavaScript usa anos iniciados por `20`, e tarefas sem término aparecem sem tempo calculável.
- A consulta de amigos executa uma consulta de usuário para cada amizade, em vez de trazer os dados em uma consulta relacionada.
- A interface referencia Bootstrap Icons por CDN, então esses ícones dependem de acesso externo.
- `TEMPLATES_AUTO_RELOAD` em `configs/config.py` tem vírgula final e, portanto, recebe uma tupla em vez de um booleano.
- Não foram encontrados testes automatizados no conjunto de arquivos analisado.

Esta análise foi estática: os comandos e fluxos não foram executados nem testados.
