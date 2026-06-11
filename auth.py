import hashlib
from db import get_connection


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(nombre: str, correo: str, password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, contraseña) VALUES (?, ?, ?)",
            (nombre, correo, hash_password(password)),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def login_user(correo: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre FROM usuarios WHERE correo = ? AND contraseña = ?",
        (correo, hash_password(password)),
    )
    user = cursor.fetchone()
    conn.close()
    return user  # None si no encuentra
