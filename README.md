# Resume Analyzer API

API assíncrona para análise e ranking de currículos utilizando Python (FastAPI), Celery, RabbitMQ e LLMs (OpenRouter).

## 🚀 Funcionalidades

- **Upload de múltiplos currículos (PDF)**: Processamento paralelo.
- **Extração de Texto**: Suporte robusto a diferentes formatos de PDF via `pdfminer.six`.
- **Análise com IA**: Extração estruturada de dados (Skills, Experiência, Senioridade) e pontuação de match com a vaga.
- **Ranking Automático**: Classificação dos candidatos baseada em critérios objetivos.
- **Relatório Consolidado**: Geração de recomendação final de contratação.
- **Arquitetura Escalável**: Separação entre API e Workers Assíncronos.

## 🛠️ Stack Tecnológica

- **Python 3.11**
- **FastAPI**: API REST
- **Celery**: Fila de tarefas distribuídas
- **RabbitMQ**: Message Broker
- **Redis**: Backend de resultados e cache
- **OpenRouter (LLM)**: Inteligência Artificial para análise
- **Docker & Docker Compose**: Orquestração de containers

## 📦 Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados.
- Uma chave de API da OpenRouter (já configurada no `.env` para teste).

### Passos

1. **Clone o repositório** (se estiver em um):
   ```bash
   git clone <repo-url>
   cd Automatiz
   ```

2. **Verifique o arquivo `.env`**:
   Certifique-se de que o arquivo `.env` existe na raiz com sua chave `OPENROUTER_API_KEY`.

3. **Suba a aplicação**:
   ```bash
   docker-compose up --build
   ```
   *Aguarde alguns instantes para que todos os serviços (RabbitMQ, Web, Worker) iniciem.*

4. **Acesse a Documentação (Swagger UI)**:
   Abra seu navegador em: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Como Testar

1. No Swagger UI, vá para o endpoint `POST /api/v1/analyze`.
2. Clique em **Try it out**.
3. Em **files**, selecione múltiplos arquivos PDF (ex: os currículos da pasta `Docs`).
4. Em **job_description**, cole a descrição da vaga desejada.
5. Execute. A API retornará um `task_id`.
6. Copie o `task_id` e use no endpoint `GET /api/v1/result/{task_id}` para acompanhar o status (`PROCESSING` -> `COMPLETED`) e ver o relatório final.

## 📂 Estrutura do Projeto

```
/
├── app/
│   ├── api/            # Endpoints da API
│   ├── core/           # Configurações (Env, Celery)
│   ├── models/         # Schemas Pydantic
│   ├── services/       # Lógica (PDF, LLM, Ranking)
│   └── tasks/          # Tarefas do Celery
├── tests/              # Testes unitários
├── docker-compose.yml  # Orquestração
├── Dockerfile          # Imagem Python
└── requirements.txt    # Dependências
```

## 📝 Decisões Arquiteturais

- **Processamento Assíncrono**: O upload de arquivos é rápido, delegando a análise pesada (PDF + LLM) para workers em background. Isso evita timeout na requisição HTTP.
- **Chord do Celery**: Utilizamos o padrão `chord` para paralelizar a análise de N currículos e, somente após o término de todos, executar a tarefa de consolidação/ranking.
- **File Handling**: Arquivos são salvos temporariamente no disco (volume compartilhado) para evitar passar grandes binários pelo Message Broker, aumentando a performance.
  - *Nota Arquitetural*: Em um ambiente de produção distribuído, recomenda-se o uso de um **Object Storage** (AWS S3, MinIO) para o compartilhamento de arquivos entre API e Workers.
- **Resiliência**: Fallback na extração de PDF e tratamento de erros na comunicação com a LLM para garantir que um arquivo corrompido não falhe todo o lote.
