# Refatoração Arquitetural Automatizada

## Análise Manual

### Projeto 1 — `code-smells-project`

- **CRITICAL — SQL arbitrário:** `app.py:59-78` executava comandos recebidos em `/admin/query`, permitindo leitura ou alteração completa do banco.
- **CRITICAL — SQL Injection:** `models.py:28`, `models.py:47-49`, `models.py:109-110` e `models.py:289-299` concatenavam entrada do usuário em SQL.
- **CRITICAL — Segredo hardcoded:** `app.py:7-8` expunha `SECRET_KEY` e debug no código.
- **HIGH — God module:** `models.py:1-314` misturava produtos, usuários, pedidos, busca, relatórios e persistência.
- **MEDIUM — N+1 queries:** `models.py:171-233` fazia consultas em loops para montar pedidos.
- **MEDIUM — Validação duplicada:** `controllers.py:24-96` repetia validações de produto em criação e atualização, aumentando risco de regras divergentes.
- **LOW — Magic values:** categorias, status e regras de desconto estavam espalhados em `controllers.py` e `models.py`.
- **LOW — Import não usado:** `models.py:2` importava `sqlite3` sem uso, sinalizando código morto e reduzindo legibilidade.

### Projeto 2 — `ecommerce-api-legacy`

- **CRITICAL — Credenciais hardcoded:** `src/utils.js:1-6` continha usuário, senha, SMTP e chave de gateway.
- **CRITICAL — Hash inseguro:** `src/utils.js:17-22` usava base64 truncado como “hash” de senha.
- **CRITICAL — Dados sensíveis em log:** `src/AppManager.js:43-46` registrava cartão e chave de pagamento.
- **HIGH — God Class:** `src/AppManager.js:4-138` concentrava banco, rotas, checkout, relatório e exclusão.
- **MEDIUM — N+1/callback cascade:** `src/AppManager.js:89-127` fazia consultas aninhadas para relatório financeiro.
- **MEDIUM — Error handling descentralizado:** `src/AppManager.js:37-77` e `src/AppManager.js:83-128` tratavam erros inline e ignoravam falhas em alguns callbacks.
- **LOW — Nomes ruins:** `usr`, `eml`, `pwd`, `c_id` e `cc` reduziam clareza do contrato.
- **LOW — Export morto:** `src/utils.js:10` e `src/utils.js:25` exportavam `totalRevenue` sem uso real.

### Projeto 3 — `task-manager-api`

- **CRITICAL — Segredos hardcoded:** `app.py:11-13` e `services/notification_service.py:7-10` expunham chave Flask e SMTP.
- **CRITICAL — MD5 para senha:** `models/user.py:27-32` usava hashing fraco e rápido.
- **CRITICAL — Senha no serializer:** `models/user.py:16-25` retornava `password` em respostas.
- **HIGH — Regras em rotas:** `routes/task_routes.py` e `routes/user_routes.py` misturavam HTTP, validação, regra e persistência.
- **MEDIUM — API deprecated:** múltiplos `Query.get()` usavam API legada do SQLAlchemy 2.x.
- **MEDIUM — N+1 queries:** `routes/task_routes.py:14-59` e `routes/report_routes.py:53-68` faziam consultas extras por item/usuário.
- **LOW — Imports mortos:** imports não usados indicavam código obsoleto em `app.py`, rotas e helpers.
- **LOW — Magic values duplicados:** `routes/task_routes.py:110-113`, `routes/user_routes.py:64` e `utils/helpers.py:110-116` repetiam status, roles e limites.

## Construção da Skill

A skill `refactor-arch` foi criada em `code-smells-project/.claude/skills/refactor-arch/` e copiada para `ecommerce-api-legacy/` e `task-manager-api/`.

O `SKILL.md` define três fases:

1. **Análise:** detectar linguagem, framework, domínio, banco, entry point, arquivos e riscos arquiteturais.
2. **Auditoria:** cruzar código com catálogo de anti-patterns, gerar relatório com severidade e linhas exatas, e pausar para confirmação.
3. **Refatoração:** reorganizar para MVC, preservar endpoints e validar boot + respostas HTTP.

Arquivos de referência:

- `project-analysis.md`: heurísticas para stack, domínio, arquitetura e riscos.
- `anti-pattern-catalog.md`: 12 anti-patterns com severidades, incluindo APIs deprecated.
- `report-template.md`: template obrigatório para relatórios.
- `mvc-guidelines.md`: responsabilidades de `config/`, `models/`, `views/routes`, `controllers`, `services` e `middlewares`.
- `refactoring-playbook.md`: 10 transformações antes/depois, como SQL parametrizado, hashing seguro, config por ambiente e troca de APIs legadas.

A skill é agnóstica de tecnologia porque usa sinais estruturais (`requirements.txt`, `package.json`, imports Flask/Express, rotas, SQL/ORM e entry points), não nomes fixos dos projetos.

Desafios resolvidos:

- O CLI `claude` não estava disponível; a execução foi conduzida com OpenAI Codex, ferramenta permitida pelo enunciado.
- O sandbox exigiu permissão de rede para instalar dependências e permissão elevada para abrir portas locais.
- O validador da skill precisava de `PyYAML`; a dependência foi instalada em virtualenv temporário e as três cópias passaram em `quick_validate.py`.

## Resultados

### Resumo dos Relatórios

| Projeto | CRITICAL | HIGH | MEDIUM | LOW | Relatório |
|---|---:|---:|---:|---:|---|
| `code-smells-project` | 4 | 3 | 3 | 2 | `reports/audit-project-1.md` |
| `ecommerce-api-legacy` | 3 | 4 | 3 | 2 | `reports/audit-project-2.md` |
| `task-manager-api` | 3 | 3 | 4 | 2 | `reports/audit-project-3.md` |

### Antes e Depois

- `code-smells-project`: de `app.py`, `controllers.py`, `models.py` e `database.py` para `config/`, `controllers/`, `models/`, `services/`, `views/` e `middlewares/`.
- `ecommerce-api-legacy`: de `AppManager.js` monolítico para `config/`, `database/`, `models/`, `services/`, `controllers/`, `views/` e `middlewares/`.
- `task-manager-api`: manteve `routes/` como camada HTTP fina e moveu regras para `controllers/` e `services/`.

### Checklist de Validação

#### `code-smells-project`

- [x] Linguagem, framework e domínio detectados.
- [x] Relatório com linhas exatas e findings ordenados.
- [x] Estrutura MVC criada.
- [x] Configuração sensível extraída.
- [x] SQL parametrizado e `/admin/query` desabilitado.
- [x] Aplicação iniciou em `PORT=5101`.
- [x] Endpoints validados: `/health`, `/produtos`, `/produtos/busca`, `/login`, `/pedidos`, `/relatorios/vendas`, `/admin/query`.

Log:

```text
GET /health -> 200
GET /produtos -> 200
POST /login -> 200
POST /pedidos -> 201
POST /admin/query -> 403
```

#### `ecommerce-api-legacy`

- [x] Linguagem, framework e domínio detectados.
- [x] Relatório com linhas exatas e findings ordenados.
- [x] Estrutura MVC criada.
- [x] Credenciais movidas para config por ambiente.
- [x] Hash de senha trocado por `crypto.pbkdf2Sync`.
- [x] Aplicação iniciou em `PORT=3102`.
- [x] Endpoints validados: `/api/checkout`, `/api/admin/financial-report`, `DELETE /api/users/1`.

Log:

```text
POST /api/checkout cartão 4... -> 200
POST /api/checkout cartão 5... -> 400
GET /api/admin/financial-report -> 200
DELETE /api/users/1 -> 200
```

#### `task-manager-api`

- [x] Linguagem, framework e domínio detectados.
- [x] Relatório com linhas exatas e findings ordenados.
- [x] Estrutura MVC criada.
- [x] `Query.get()` substituído por `db.session.get()`.
- [x] Senha removida dos serializers e MD5 substituído por Werkzeug.
- [x] Aplicação iniciou em `PORT=5103` após `python seed.py`.
- [x] Endpoints validados: `/health`, `/tasks`, `/tasks/search`, `/tasks/stats`, `/users`, `/login`, `/reports/summary`, `/categories`.

Log:

```text
python seed.py -> Seed concluído com sucesso
GET /health -> 200
GET /tasks/stats -> 200
POST /login -> 200 sem campo password na resposta
```

## Como Executar

### Pré-requisitos

- Python 3 com `pip`.
- Node.js e npm.
- Claude Code, Gemini CLI ou OpenAI Codex configurado.
- Para Claude Code, a skill está disponível em `.claude/skills/refactor-arch/` dentro de cada projeto.

### Executar a Skill

```bash
cd code-smells-project
claude "/refactor-arch"

cd ../ecommerce-api-legacy
claude "/refactor-arch"

cd ../task-manager-api
claude "/refactor-arch"
```

### Rodar e Validar os Projetos

```bash
cd code-smells-project
pip install -r requirements.txt
python app.py
curl http://localhost:5000/health
curl http://localhost:5000/produtos
```

```bash
cd ecommerce-api-legacy
npm install
npm start
curl http://localhost:3000/api/admin/financial-report
```

```bash
cd task-manager-api
pip install -r requirements.txt
python seed.py
python app.py
curl http://localhost:5000/health
curl http://localhost:5000/tasks/stats
```
