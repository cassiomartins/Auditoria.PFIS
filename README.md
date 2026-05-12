# Auditoria PFIS

Sistema web de apoio à fiscalização periódica de unidades (PFIS — Fiscalização de Unidades), desenvolvido com Django. A ferramenta digitaliza o processo de auditoria de campo: o fiscal visita uma unidade, percorre um checklist padronizado de 119 itens, registra o status de conformidade de cada ponto, anexa evidências fotográficas e, ao final, gera um relatório em PDF.

## O que é auditado

Cada auditoria cobre uma **unidade** (filial ou estabelecimento) e é conduzida por um **Fiscal PFIS**. O checklist é dividido em seções temáticas e abrange itens com diferentes periodicidades (diária, semanal, mensal, semestral e anual). Para cada item o fiscal registra:

- **Conforme** — requisito atendido
- **Não Conforme** — requisito não atendido, com campo de observação obrigatório
- **Não Aplicável** — item não se aplica àquela unidade
- **Pendente** — ainda não avaliado

Ao fim do preenchimento o sistema calcula automaticamente o **índice de conformidade** da unidade e só permite finalizar a auditoria quando todos os itens foram respondidos.

## Para que serve

- Substituir planilhas e formulários em papel na fiscalização periódica
- Garantir rastreabilidade: cada auditoria recebe um número único (`PFIS-YYYY-NNNN`)
- Centralizar evidências fotográficas junto às respostas, sem depender de sistema de arquivos externo
- Permitir que gestores acompanhem o andamento das auditorias em tempo real
- Gerar relatórios formais em PDF prontos para arquivamento ou envio

## Funcionalidades

- **Controle de acesso por perfil**: Gestor, Fiscal e Responsável de Unidade com permissões distintas
- **Checklist padronizado**: 119 itens organizados por seção e periodicidade
- **Registro de evidências**: upload de imagens armazenadas diretamente no banco de dados
- **Índice de conformidade**: calculado automaticamente por auditoria
- **Geração de PDF**: relatório completo com seções, respostas e evidências embutidas
- **Numeração automática**: documentos `PFIS-YYYY-NNNN`, protegida contra condições de corrida
- **Interface HTMX**: respostas salvas item a item sem recarregar a página
- **Dashboard por perfil**: indicadores e auditorias recentes filtrados pelo perfil do usuário

## Stack

- **Backend**: Django 5.1 + PostgreSQL 16
- **Frontend**: Tailwind CSS + HTMX
- **PDF**: xhtml2pdf
- **Deploy**: Docker + Whitenoise
- **Config**: django-environ (`.env`)

## Estrutura do projeto

```
apps/
  accounts/     # Autenticação, perfis e gerenciamento de usuários
  auditorias/   # Modelos, checklist, respostas e evidências
  relatorios/   # Geração de PDF
  core/         # Mixins e utilitários compartilhados
config/
  settings/
    base.py         # Configurações compartilhadas
    development.py  # Ambiente local
    production.py   # Ambiente de produção
templates/      # HTML por app
static/         # Arquivos estáticos
```

## Pré-requisitos

- Docker e Docker Compose, **ou**
- Python 3.11+ e PostgreSQL 16

## Instalação com Docker

```bash
git clone <url-do-repositorio>
cd Auditoria.PFIS

cp .env.example .env
# Edite .env conforme necessário

docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Acesse em [http://localhost:8000](http://localhost:8000).

## Instalação local (sem Docker)

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

pip install -r requirements.txt

cp .env.example .env
# Edite .env com as credenciais do PostgreSQL local

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Variáveis de ambiente (`.env`)

| Variável        | Descrição                                | Exemplo                                     |
|-----------------|------------------------------------------|---------------------------------------------|
| `SECRET_KEY`    | Chave secreta do Django                  | `django-insecure-...`                       |
| `DEBUG`         | Modo debug                               | `True`                                      |
| `ALLOWED_HOSTS` | Hosts permitidos (separados por vírgula) | `localhost,127.0.0.1`                       |
| `DATABASE_URL`  | URL de conexão com o banco               | `postgres://postgres:postgres@db:5432/pfis` |
| `STATIC_ROOT`   | Diretório de coleta de estáticos         | `/app/staticfiles`                          |
| `MEDIA_ROOT`    | Diretório de mídia                       | `/app/media`                                |

## Perfis de usuário

| Perfil                  | Permissões                                                        |
|-------------------------|-------------------------------------------------------------------|
| **Gestor**              | Acesso total: gerencia usuários e visualiza todas as auditorias   |
| **Fiscal**              | Cria e preenche suas próprias auditorias                          |
| **Responsável de Unidade** | Visualiza apenas as auditorias da sua unidade                  |

## Comandos úteis

```bash
# Carregar checklist inicial (119 itens)
python manage.py seed_checklist

# Coletar arquivos estáticos (produção)
python manage.py collectstatic --noinput
```

## Licença

MIT License — consulte o arquivo [LICENSE](LICENSE) para detalhes.
