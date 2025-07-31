from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Quiz, User
from app import redis_available, redis_client
import json
from datetime import datetime
from database import db

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/api/quizzes', methods=['GET'])
@jwt_required()
def get_quizzes():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if redis_available:
            cache_key = 'all_quizzes' if user.role == 'admin' else 'active_quizzes'
            cached_data = redis_client.get(cache_key)
            
            if cached_data:
                return jsonify(json.loads(cached_data)), 200
        
        if user.role == 'admin':
            quizzes = Quiz.query.all()
        else:
            quizzes = Quiz.query.filter_by(is_active=True).all()
        
        quizzes_data = [quiz.to_dict() for quiz in quizzes]

        if redis_available:
            redis_client.setex(cache_key, 180, json.dumps(quizzes_data))
        
        return jsonify(quizzes_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/api/quizzes', methods=['POST'])
@jwt_required()
def create_quiz():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        required_fields = ['title', 'chapter_id', 'date_of_quiz', 'time_duration']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        quiz = Quiz(
            title=data['title'],
            chapter_id=data['chapter_id'],
            date_of_quiz=datetime.fromisoformat(data['date_of_quiz']),
            time_duration=data['time_duration'],
            remarks=data.get('remarks', ''),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(quiz)
        db.session.commit()
        
        if redis_available:
            redis_client.delete('all_quizzes')
            redis_client.delete('active_quizzes')
        
        return jsonify(quiz.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/api/quizzes/<int:quiz_id>', methods=['DELETE'])
@jwt_required()
def delete_quiz(quiz_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        db.session.delete(quiz)
        db.session.commit()
        if redis_available:
            redis_client.delete('all_quizzes')
            redis_client.delete('active_quizzes')
        return jsonify({'message': 'Quiz deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@quiz_bp.route('/api/quizzes/<int:quiz_id>', methods=['PUT'])
@jwt_required()
def update_quiz(quiz_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        data = request.get_json()
        
        quiz.title = data.get('title', quiz.title)
        quiz.chapter_id = data.get('chapter_id', quiz.chapter_id)
        quiz.date_of_quiz = datetime.fromisoformat(data.get('date_of_quiz', quiz.date_of_quiz.isoformat()))
        quiz.time_duration = data.get('time_duration', quiz.time_duration)
        quiz.remarks = data.get('remarks', quiz.remarks)
        quiz.is_active = data.get('is_active', quiz.is_active)
        
        db.session.commit()
        
        if redis_available:
            redis_client.delete('all_quizzes')
            redis_client.delete('active_quizzes')
        
        return jsonify({'message': 'Quiz updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/api/quizzes/<int:quiz_id>', methods=['PATCH'])
@jwt_required()
def patch_quiz(quiz_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        data = request.get_json()
        
        if 'is_active' in data:
            quiz.is_active = data['is_active']
        
        db.session.commit()
        
        if redis_available:
            redis_client.delete('all_quizzes')
            redis_client.delete('active_quizzes')
        
        return jsonify({'message': 'Quiz status updated successfully', 'is_active': quiz.is_active}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500