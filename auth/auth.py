"""
Authentication layer: sign up, log in, and per-user data isolation.

Passwords are hashed with bcrypt before storage; plaintext passwords are
never written to disk or logged.
"""

import re
import sqlite3
from dataclasses import dataclass
from typing import Optional

import bcrypt

from database.db import get_connection

USERNAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,32}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class User:
    id: int
    username: str
    email: str


class AuthError(Exception):
    """Raised for validation or credential errors surfaced to the UI."""


def _validate_signup_fields(username: str, email: str, password: str) -> None:
    if not USERNAME_RE.match(username):
        raise AuthError(
            "Username must be 3-32 characters: letters, numbers, underscores only."
        )
    if not EMAIL_RE.match(email):
        raise AuthError("Please enter a valid email address.")
    if len(password) < 8:
        raise AuthError("Password must be at least 8 characters long.")


def sign_up(username: str, email: str, password: str) -> User:
    username = username.strip()
    email = email.strip().lower()
    _validate_signup_fields(username, email, password)

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    conn = get_connection()
    try:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash),
            )
            conn.commit()
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                raise AuthError("That username is already taken.")
            if "email" in str(e):
                raise AuthError("That email is already registered.")
            raise AuthError("Could not create account.")

        return User(id=cur.lastrowid, username=username, email=email)
    finally:
        conn.close()


def log_in(username_or_email: str, password: str) -> User:
    identifier = username_or_email.strip().lower()

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, email, password_hash FROM users "
            "WHERE lower(username) = ? OR lower(email) = ?",
            (identifier, identifier),
        )
        row = cur.fetchone()
    finally:
        conn.close()

    if row is None:
        raise AuthError("Invalid username/email or password.")

    if not bcrypt.checkpw(password.encode("utf-8"), row["password_hash"]):
        raise AuthError("Invalid username/email or password.")

    return User(id=row["id"], username=row["username"], email=row["email"])


def get_user_by_id(user_id: int) -> Optional[User]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
    finally:
        conn.close()

    if row is None:
        return None
    return User(id=row["id"], username=row["username"], email=row["email"])
