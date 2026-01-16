# Desafio Técnico — Desenvolvedor Backend Python Pleno

## Contexto

O setor de Recursos Humanos de uma empresa de tecnologia em rápido crescimento recebe centenas de currículos semanalmente para diversas vagas. Atualmente, a triagem inicial é feita manualmente, onde os recrutadores precisam:

- Abrir cada currículo individualmente
- Extrair informações relevantes (skills, experiência, formação)
- Classificar o candidato por senioridade
- Comparar candidatos entre si para priorizar entrevistas

Esse processo consome **horas de trabalho repetitivo** e está sujeito a inconsistências na avaliação.

Seu desafio é construir uma **API que automatize a extração, análise e ranking** de currículos, processando múltiplos documentos em paralelo e gerando um relatório consolidado que auxilie o time de RH na tomada de decisão.

---

## O Desafio

Desenvolver uma API REST que receba múltiplos currículos em PDF, processe-os **paralelamente** e retorne uma análise consolidada com ranking dos candidatos.

### Entrada da API

| # | Documento |
|---|-----------|
| 1 | **Currículos em PDF** |
| 2 | **Descrição da vaga** |

> A API deve suportar o upload de **2 a 10 currículos** em uma única requisição.

### Análise esperada

A API deve ser capaz de:

1. **Extrair dados estruturados** de cada currículo:
   - Nome completo
   - E-mail e telefone
   - Formação acadêmica
   - Anos de experiência
   - Habilidades técnicas (skills)
   - Último cargo ocupado
   - Empresas anteriores

2. **Classificar cada candidato** por senioridade estimada:
   - `JUNIOR` (0-2 anos de experiência)
   - `PLENO` (2-5 anos de experiência)
   - `SENIOR` (5+ anos de experiência)

3. **Gerar um ranking** dos candidatos com base em critérios como:
   - Match com a descrição da vaga
   - Anos de experiência
   - Experiências relevante

4. **Produzir um relatório consolidado** contendo:
   - Resumo de cada candidato
   - Ranking ordenado por pontuação
   - Pontos fortes e fracos de cada candidato
   - Recomendação de quais candidatos priorizar para entrevista

---

## Requisitos Técnicos

### Stack obrigatória
- **Python 3.10+**
- **FastAPI** — Framework para construção da API
- **Celery** — Processamento assíncrono de tarefas
- **RabbitMQ** — Message broker para filas de tarefas
- **Integração com LLM via OpenRouter**

### Requisitos de código
- Código organizado e legível
- Tipagem com Type Hints
- Tratamento adequado de erros (PDF corrompido, timeout de LLM, etc.)
- README com instruções de execução

### Diferenciais
- Testes unitários
- Containerização com Docker e Docker Compose
- Logs estruturados
- Retry automático em caso de falha
- Monitoramento das tasks

---

## Entregáveis

1. **Repositório Git** (GitHub, GitLab ou similar) contendo:
   - Código fonte da aplicação
   - README.md com instruções de instalação e execução
   - Arquivo de dependências (requirements.txt ou pyproject.toml)

---

## Critérios de Avaliação

| Critério | O que avaliamos |
|----------|-----------------|
| **Processamento paralelo** | Uso correto do Celery com RabbitMQ, orquestração de tasks, agregação de resultados |
| **Integração com LLM** | Qualidade dos prompts, estruturação das respostas, parsing robusto |
| **Lógica de ranking** | Capacidade de comparar candidatos, aplicar critérios de pontuação |
| **Design da API** | Endpoints bem definidos, contratos claros, responses adequados |
| **Qualidade de código** | Organização, legibilidade, boas práticas, tipagem |
| **Resiliência** | Tratamento de erros, retries, timeouts |
| **Documentação** | Clareza do README, explicação das decisões arquiteturais |
| **Extras** | Testes, Docker, logs, monitoramento |

---

## Recursos Fornecidos

### Chave de API
Será fornecida uma chave da **OpenRouter** para acesso aos modelos de LLM. Você pode escolher o modelo que preferir dentre os disponíveis.

Documentação OpenRouter: https://openrouter.ai/docs

### Documentos de exemplo
Disponibilizamos 5 currículos fictícios em PDF para desenvolvimento.

---

## Prazo

**4 dias corridos** a partir do recebimento deste desafio.

---

## Dúvidas

Caso tenha dúvidas sobre o desafio, entre em contato. Responderemos o mais breve possível.

---

## Observações finais

- Não existe uma única solução correta. Queremos entender como você pensa e resolve problemas.
- Valorizamos código funcional e bem organizado mais do que features extras incompletas.
- O uso correto de processamento assíncrono é um dos principais pontos de avaliação.

**Boa sorte!** 🚀
