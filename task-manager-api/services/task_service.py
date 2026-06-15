from sqlalchemy.orm import joinedload

from config.settings import DEFAULT_PRIORITY, MAX_TITLE_LENGTH, MIN_TITLE_LENGTH, VALID_STATUSES
from database import db
from middlewares.error_handler import AppError
from models.category import Category
from models.task import Task
from models.user import User
from utils.helpers import parse_date
from utils.time_utils import utc_now


def list_tasks():
    tasks = Task.query.options(joinedload(Task.user), joinedload(Task.category)).all()
    return [serialize_task(task, include_names=True) for task in tasks]


def get_task(task_id):
    task = find_task(task_id)
    return serialize_task(task, include_overdue=True)


def create_task(data):
    payload = validate_task_payload(data, require_title=True)
    task = Task(**payload)
    db.session.add(task)
    db.session.commit()
    return task.to_dict()


def update_task(task_id, data):
    task = find_task(task_id)
    payload = validate_task_payload(data, require_title=False)
    for key, value in payload.items():
        setattr(task, key, value)
    task.updated_at = utc_now()
    db.session.commit()
    return task.to_dict()


def delete_task(task_id):
    task = find_task(task_id)
    db.session.delete(task)
    db.session.commit()


def search_tasks(args):
    query = Task.query
    text = args.get('q', '')
    status = args.get('status', '')
    priority = args.get('priority', '')
    user_id = args.get('user_id', '')

    if text:
        query = query.filter(db.or_(Task.title.like(f'%{text}%'), Task.description.like(f'%{text}%')))
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == int(priority))
    if user_id:
        query = query.filter(Task.user_id == int(user_id))
    return [task.to_dict() for task in query.all()]


def task_stats():
    total = Task.query.count()
    counts = {
        status: Task.query.filter_by(status=status).count()
        for status in VALID_STATUSES
    }
    overdue_count = Task.query.filter(
        Task.due_date < utc_now(),
        Task.status.notin_(['done', 'cancelled']),
    ).count()
    return {
        'total': total,
        'pending': counts['pending'],
        'in_progress': counts['in_progress'],
        'done': counts['done'],
        'cancelled': counts['cancelled'],
        'overdue': overdue_count,
        'completion_rate': round((counts['done'] / total) * 100, 2) if total > 0 else 0,
    }


def get_tasks_for_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        raise AppError('Usuário não encontrado', 404)
    return [serialize_task(task, include_overdue=True) for task in Task.query.filter_by(user_id=user_id).all()]


def find_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        raise AppError('Task não encontrada', 404)
    return task


def validate_task_payload(data, require_title):
    if not data:
        raise AppError('Dados inválidos', 400)
    payload = {}

    if require_title or 'title' in data:
        title = data.get('title')
        if not title:
            raise AppError('Título é obrigatório', 400)
        if len(title) < MIN_TITLE_LENGTH:
            raise AppError('Título muito curto', 400)
        if len(title) > MAX_TITLE_LENGTH:
            raise AppError('Título muito longo', 400)
        payload['title'] = title.strip()

    if 'description' in data:
        payload['description'] = data.get('description', '')

    status = data.get('status')
    if status is not None:
        if status not in VALID_STATUSES:
            raise AppError('Status inválido', 400)
        payload['status'] = status
    elif require_title:
        payload['status'] = 'pending'

    priority = data.get('priority')
    if priority is not None:
        if priority < 1 or priority > 5:
            raise AppError('Prioridade deve ser entre 1 e 5', 400)
        payload['priority'] = priority
    elif require_title:
        payload['priority'] = DEFAULT_PRIORITY

    if 'user_id' in data:
        user_id = data.get('user_id')
        if user_id and not db.session.get(User, user_id):
            raise AppError('Usuário não encontrado', 404)
        payload['user_id'] = user_id

    if 'category_id' in data:
        category_id = data.get('category_id')
        if category_id and not db.session.get(Category, category_id):
            raise AppError('Categoria não encontrada', 404)
        payload['category_id'] = category_id

    if 'due_date' in data:
        payload['due_date'] = parse_date(data['due_date']) if data['due_date'] else None
        if data['due_date'] and payload['due_date'] is None:
            raise AppError('Formato de data inválido. Use YYYY-MM-DD', 400)

    if 'tags' in data:
        tags = data.get('tags')
        payload['tags'] = ','.join(tags) if isinstance(tags, list) else tags

    return payload


def serialize_task(task, include_names=False, include_overdue=False):
    data = task.to_dict()
    if include_overdue:
        data['overdue'] = task.is_overdue()
    if include_names:
        data['overdue'] = task.is_overdue()
        data['user_name'] = task.user.name if task.user else None
        data['category_name'] = task.category.name if task.category else None
    return data
