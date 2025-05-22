# 🛠 a4tunados-backend

Backend do projeto fullstack desenvolvido para o desafio técnico da empresa **a4tunados**.

Utiliza **Django** com **Django REST Framework** e **PostgreSQL** para fornecer APIs de autenticação, gerenciamento de usuários e vídeos privados.

---

## 🚀 Tecnologias

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [django-cors-headers](https://pypi.org/project/django-cors-headers/)
- [Pillow](https://pypi.org/project/Pillow/)
- [Docker](https://www.docker.com/) (opcional)

---

## ▶️ Como rodar o projeto

### 1. Clonando o repositório

```bash
git clone https://github.com/seu-usuario/a4tunados-backend.git
cd a4tunados-backend
```

### 2. Configurando variáveis de ambiente

Crie um arquivo `.env` na raiz do backend com o seguinte conteúdo (ajuste conforme necessário):

```env
DJANGO_SECRET_KEY=sua-chave-secreta
DEBUG=True
DB_NAME=a4tunados
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,api.majorssolutions.com.br
```

### 3. Rodando localmente (sem Docker)

```bash
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8081
```

> **Obs:** Certifique-se de ter um banco PostgreSQL rodando localmente.

### 4. Rodando com Docker

```bash
docker-compose up --build
```

- O backend estará disponível em `http://localhost:8000` (ou ajuste a porta no docker-compose).
- O banco de dados será criado automaticamente.

### 5. Rodando em produção (VPS)

- Configure o arquivo `.env` com as variáveis corretas de produção.
- Use o Docker ou configure um serviço WSGI (gunicorn/uwsgi) + nginx.
- Certifique-se de que a pasta `media/` está persistente e exposta via nginx.
- Configure o domínio e SSL (Let’s Encrypt).

### 6. Endpoints principais

- `/api/register/` – Cadastro de usuário
- `/api/token/` – Login (JWT)
- `/api/user/me/` – Dados do usuário autenticado
- `/api/videos/` – CRUD de vídeos
- `/api/playlists/` – CRUD de playlists

---

## 🛡️ Segurança

- Nunca exponha sua `SECRET_KEY` em produção.
- Sempre use HTTPS em produção.
- Configure corretamente o CORS e o CSRF.

---

## 📄 Licença

Desenvolvido para o desafio técnico da a4tunados.