from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
import celery

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/api/tasks/send_daily_reminders', methods=['POST'])
@jwt_required()
def trigger_send_daily_reminders():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        if celery:
            from celery_app import send_daily_reminders
            send_daily_reminders.delay()
            return jsonify({'message': 'Daily reminder task triggered'}), 200
        else:
            return jsonify({'error': 'Celery is not available'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/api/tasks/send_monthly_reports', methods=['POST'])
@jwt_required()
def trigger_send_monthly_reports():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        if celery:
            from celery_app import send_monthly_reports
            send_monthly_reports.delay()
            return jsonify({'message': 'Monthly report task triggered'}), 200
        else:
            return jsonify({'error': 'Celery is not available'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/api/tasks/export_user_quiz_data', methods=['POST'])
@jwt_required()
def trigger_export_user_quiz_data():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        user_id = data.get('user_id', int(current_user_id))
        
        if celery:
            from celery_app import export_user_quiz_data
            export_user_quiz_data.delay(user_id)
            return jsonify({'message': f'Quiz data export task triggered for user {user_id}'}), 200
        else:
            return jsonify({'error': 'Celery is not available'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/api/tasks/export_admin_quiz_data', methods=['POST'])
@jwt_required()
def trigger_export_admin_quiz_data():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        if celery:
            from celery_app import export_admin_quiz_data
            export_admin_quiz_data.delay()
            return jsonify({'message': 'Admin quiz data export task triggered'}), 200
        else:
            return jsonify({'error': 'Celery is not available'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/api/tasks/export_my_quiz_data', methods=['POST'])
@jwt_required()
def trigger_export_my_quiz_data():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if celery:
            from celery_app import export_user_quiz_data
            export_user_quiz_data.delay(int(current_user_id))
            return jsonify({'message': f'Quiz data export task triggered for {user.full_name}'}), 200
        else:
            return jsonify({'error': 'Celery is not available'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500