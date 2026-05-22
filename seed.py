from app.core.database import SessionLocal
from app.models.user import User
from app.models.module import Module
from app.core.security import hash_senha

db = SessionLocal()

# =========================
# CRIAR ADMIN
# =========================

admin_exists = db.query(User).filter(
    User.email == "admin@erp.com"
).first()

if not admin_exists:

    admin = User(
        nome="Administrador",
        email="admin@erp.com",
        senha_hash=hash_senha("12345"),
        role="admin",
        is_active=True
    )

    db.add(admin)

    print("✅ Admin criado")


# =========================
# CRIAR USER PADRÃO
# =========================

user_exists = db.query(User).filter(
    User.email == "user@erp.com"
).first()

if not user_exists:

    user = User(
        nome="Usuário",
        email="user@erp.com",
        senha_hash=hash_senha("12345"),
        role="user",
        is_active=True
    )

    db.add(user)

    print("✅ Usuário padrão criado")


# =========================
# CRIAR MÓDULOS
# =========================

modules = [
    {
        "nome": "financeiro",
        "url": "http://127.0.0.1",
        "porta": 8001
    },
    {
        "nome": "rh",
        "url": "http://127.0.0.1",
        "porta": 8002
    },
    {
        "nome": "estoque",
        "url": "http://127.0.0.1",
        "porta": 8003
    },
    {
        "nome": "compras",
        "url": "http://127.0.0.1",
        "porta": 8004
    }
]

for item in modules:

    exists = db.query(Module).filter(
        Module.nome == item["nome"]
    ).first()

    if not exists:

        module = Module(
            nome=item["nome"],
            url=item["url"],
            porta=item["porta"]
        )

        db.add(module)

        print(f"✅ Módulo {item['nome']} criado")


db.commit()

print("\n🚀 Seed executada com sucesso!")