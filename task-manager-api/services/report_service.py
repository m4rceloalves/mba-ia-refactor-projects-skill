from datetime import timedelta

from database import db
from middlewares.error_handler import AppError
from models.category import Category
from models.task import Task
from models.user import User
from utils.time_utils import utc_now


def summary_report():
    total_tasks = Task.query.count()
    seven_days_ago = utc_now() - timedelta(days=7)
    status_counts = {
        status: Task.query.filter_by(status=status).count()
        for status in ['pending', 'in_progress', 'done', 'cancelled']
    }
    priority_counts = {
        priority: Task.query.filter_by(priority=priority).count()
        for priority in range(1, 6)
    }
    overdue_tasks = Task.query.filter(
        Task.due_date < utc_now(),
        Task.status.notin_(['done', 'cancelled']),
    ).all()
    users = User.query.all()
    return {
        'generated_at': str(utc_now()),
        'overview': {
            'total_tasks': total_tasks,
            'total_users': User.query.count(),
            'total_categories': Category.query.count(),
        },
        'tasks_by_status': status_counts,
        'tasks_by_priority': {
            'critical': priority_counts[1],
            'high': priority_counts[2],
            'medium': priority_counts[3],
            'low': priority_counts[4],
            'minimal': priority_counts[5],
        },
        'overdue': {
            'count': len(overdue_tasks),
            'tasks': [
                {
                    'id': task.id,
                    'title': task.title,
                    'due_date': str(task.due_date),
                    'days_overdue': (utc_now() - task.due_date).days,
                }
                for task in overdue_tasks
            ],
        },
        'recent_activity': {
            'tasks_created_last_7_days': Task.query.filter(Task.created_at >= seven_days_ago).count(),
            'tasks_completed_last_7_days': Task.query.filter(Task.status == 'done', Task.updated_at >= seven_days_ago).count(),
        },
        'user_productivity': [user_productivity(user) for user in users],
    }


def user_report(user_id):
    user = db.session.get(User, user_id)
    if not user:
        raise AppError('Usuário não encontrado', 404)
    tasks = Task.query.filter_by(user_id=user_id).all()
    counts = {
        status: sum(1 for task in tasks if task.status == status)
        for status in ['done', 'pending', 'in_progress', 'cancelled']
    }
    overdue = sum(1 for task in tasks if task.is_overdue())
    high_priority = sum(1 for task in tasks if task.priority <= 2)
    total = len(tasks)
    return {
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        },
        'statistics': {
            'total_tasks': total,
            'done': counts['done'],
            'pending': counts['pending'],
            'in_progress': counts['in_progress'],
            'cancelled': counts['cancelled'],
            'overdue': overdue,
            'high_priority': high_priority,
            'completion_rate': round((counts['done'] / total) * 100, 2) if total > 0 else 0,
        },
    }


def user_productivity(user):
    tasks = Task.query.filter_by(user_id=user.id).all()
    total = len(tasks)
    completed = sum(1 for task in tasks if task.status == 'done')
    return {
        'user_id': user.id,
        'user_name': user.name,
        'total_tasks': total,
        'completed_tasks': completed,
        'completion_rate': round((completed / total) * 100, 2) if total > 0 else 0,
    }
