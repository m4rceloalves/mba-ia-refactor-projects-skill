from config.settings import DEFAULT_COLOR
from database import db
from middlewares.error_handler import AppError
from models.category import Category
from models.task import Task


def list_categories():
    categories = Category.query.all()
    return [serialize_category(category) for category in categories]


def create_category(data):
    if not data or not data.get('name'):
        raise AppError('Nome é obrigatório', 400)
    category = Category()
    category.name = data['name']
    category.description = data.get('description', '')
    category.color = data.get('color', DEFAULT_COLOR)
    db.session.add(category)
    db.session.commit()
    return category.to_dict()


def update_category(cat_id, data):
    if not data:
        raise AppError('Dados inválidos', 400)
    category = find_category(cat_id)
    for field in ['name', 'description', 'color']:
        if field in data:
            setattr(category, field, data[field])
    db.session.commit()
    return category.to_dict()


def delete_category(cat_id):
    category = find_category(cat_id)
    Task.query.filter_by(category_id=cat_id).update({'category_id': None})
    db.session.delete(category)
    db.session.commit()


def find_category(cat_id):
    category = db.session.get(Category, cat_id)
    if not category:
        raise AppError('Categoria não encontrada', 404)
    return category


def serialize_category(category):
    data = category.to_dict()
    data['task_count'] = Task.query.filter_by(category_id=category.id).count()
    return data
