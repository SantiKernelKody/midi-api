# midi-api
fastAPI project for the dashboard.

├── app
│   ├── api
│   │   ├── v1
│   │   │   ├── endpoints
│   │   │   │   ├── auth.py
│   │   │   │   ├── player.py
│   │   │   │   ├── game.py
│   │   │   │   ├── dashboard.py
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   ├── core
│   │   ├── config.py
│   │   └── security.py
│   ├── crud
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── player.py
│   │   └── game.py
│   ├── db
│   │   ├── base.py
│   │   ├── base_class.py
│   │   ├── session.py
│   ├── models
│   │   ├── user.py
│   │   ├── player.py
│   │   ├── game.py
│   │   └── __init__.py
│   ├── schemas
│   │   ├── user.py
│   │   ├── player.py
│   │   ├── game.py
│   │   └── __init__.py
│   ├── main.py
│   └── __init__.py
└── alembic
    ├── versions
    └── env.py


security->session->base_class->models/user->schemas/user->crud/user->core/security.py->endpoints/auth->main.py