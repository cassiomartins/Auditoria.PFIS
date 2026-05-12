# Auditoria PFIS

Sistema web de gestão e fiscalização periódica de unidades, desenvolvido com Django. Permite que fiscais registrem auditorias com checklist padronizado, anexem evidências e gerem relatórios em PDF.

## Funcionalidades

- **Controle de acesso por perfil**: Gestor, Fiscal e Unidade com permissões distintas
- **Checklist padronizado**: 119 itens organizados por seção e periodicidade
- **Registro de evidências**: upload de imagens diretamente em cada item do checklist
- **Índice de conformidade**: cálculo automático de conformes, não conformes e não aplicáveis
- **Geração de PDF**: relatório completo da auditoria com seções, respostas e evidências
- **Numeração automática**: documentos no formato `PFIS-YYYY-NNNN`, protegido contra race conditions
- **Dashboard por perfil**: visão consolidada com auditorias recentes e indicadores

## Stack

- **Backend**: Django 5.1 + PostgreSQL 16
- **Frontend**: Tailwind CSS (via CDN)
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
# Clone o repositório
git clone <url-do-repositorio>
cd Auditoria.PFIS

# Copie e configure o .env
cp .env.example .env

# Suba os serviços
docker compose up -d

# Execute as migrações e crie o superusuário
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

| Variável        | Descrição                                 | Exemplo                                      |
|-----------------|-------------------------------------------|----------------------------------------------|
| `SECRET_KEY`    | Chave secreta do Django                   | `django-insecure-...`                        |
| `DEBUG`         | Modo debug                                | `True`                                       |
| `ALLOWED_HOSTS` | Hosts permitidos (separados por vírgula)  | `localhost,127.0.0.1`                        |
| `DATABASE_URL`  | URL de conexão com o banco                | `postgres://postgres:postgres@db:5432/pfis`  |
| `STATIC_ROOT`   | Diretório de coleta de estáticos          | `/app/staticfiles`                           |
| `MEDIA_ROOT`    | Diretório de mídia                        | `/app/media`                                 |

## Perfis de usuário

| Perfil      | Permissões                                                       |
|-------------|------------------------------------------------------------------|
| **Gestor**  | Acesso total: cria/edita usuários, visualiza todas as auditorias |
| **Fiscal**  | Cria e edita suas próprias auditorias                            |
| **Unidade** | Visualiza apenas as auditorias da sua unidade                    |

## Comandos úteis

```bash
# Carregar checklist inicial (119 itens)
python manage.py seed_checklist

# Coletar arquivos estáticos (produção)
python manage.py collectstatic --noinput
```

## Licença

Uso interno. Todos os direitos reservados.
