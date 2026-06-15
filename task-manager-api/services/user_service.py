import secrets
import re

from sqlalchemy import func

from config.settings import MIN_PASSWORD_LENGTH, VALID_ROLES
from database import db
from middlewares.error_handler import AppError
from models.task import Task
from models.user import User
from services.task_service import get_tasks_for_user


def list_users():
    rows = (
        db.session.query(User, func.count(Task.id).label('task_count'))
        .outerjoin(Task, Task.user_id == User.id)
        .group_by(User.id)
        .all()
    )
    result = []
    for user, task_count in rows:
        data = user.to_dict()
        data['task_count'] = task_count
        result.append(data)
    return result


def get_user(user_id):
    user = find_user(user_id)
    data = user.to_dict()
    data['tasks'] = [task.to_dict() for task in Task.query.filter_by(user_id=user_id).all()]
    return data


def create_user(data):
    payload = validate_user_payload(data, create=True)
    user = User()
    user.name = payload['name']
    user.email = payload['email']
    user.set_password(payload['password'])
    user.role = payload['role']
    db.session.add(user)
    db.session.commit()
    return user.to_dict()


def update_user(user_id, data):
    user = find_user(user_id)
    payload = validate_user_payload(data, create=False, current_user_id=user_id)
    for field in ['name', 'email', 'role', 'active']:
        if field in payload:
            setattr(user, field, payload[field])
    if 'password' in payload:
        user.set_password(payload['password'])
    db.session.commit()
    return user.to_dict()


def delete_user(user_id):
    user = find_user(user_id)
    Task.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()


def get_user_tasks(user_id):
    return get_tasks_for_user(user_id)


def login(data):
    if not data:
        raise AppError('Dados inválidos', 400)
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        raise AppError('Email e senha são obrigatórios', 400)
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        raise AppError('Credenciais inválidas', 401)
    if not user.active:
        raise AppError('Usuário inativo', 403)
    return {
        'message': 'Login realizado com sucesso',
        'user': user.to_dict(),
        'token': secrets.token_urlsafe(24),
    }


def find_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        raise AppError('Usuário não encontrado', 404)
    return user


def validate_user_payload(data, create, current_user_id=None):
    if not data:
        raise AppError('Dados inválidos', 400)
    payload = {}

    if create or 'name' in data:
        if not data.get('name'):
            raise AppError('Nome é obrigatório', 400)
        payload['name'] = data['name']

    if create or 'email' in data:
        email = data.get('email')
        if not email:
            raise AppError('Email é obrigatório', 400)
        if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', email):
            raise AppError('Email inválido', 400)
        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != current_user_id:
            raise AppError('Email já cadastrado', 409)
        payload['email'] = email

    if create or 'password' in data:
        password = data.get('password')
        if not password:
            raise AppError('Senha é obrigatória', 400)
        if len(password) < MIN_PASSWORD_LENGTH:
            raise AppError('Senha deve ter no mínimo 4 caracteres', 400)
        payload['password'] = password

    role = data.get('role', 'user' if create else None)
    if role is not None:
        if role not in VALID_ROLES:
            raise AppError('Role inválido', 400)
        payload['role'] = role

    if 'active' in data:
        payload['active'] = data['active']

    return payload
