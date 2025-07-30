from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Question
from app import redis_available, redis_client
import json
from database import db

question_bp = Blueprint('question', __name__)

@question_bp.route('/api/quizzes/<int:quiz_id>/questions', methods=['GET'])
@jwt_required()
def get_questions(quiz_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if redis_available:
            cache_key = f'questions_quiz_{quiz_id}'
            cached_data = redis_client.get(cache_key)
            
            if cached_data:
                questions_data = json.loads(cached_data)
            else:
                questions = Question.query.filter_by(quiz_id=quiz_id).all()
                questions_data = [question.to_dict() for question in questions]
                
                redis_client.setex(cache_key, 600, json.dumps(questions_data))
        else:
            questions = Question.query.filter_by(quiz_id=quiz_id).all()
            questions_data = [question.to_dict() for question in questions]
        
        if user.role != 'admin':
            for question in questions_data:
                question.pop('correct_option', None)
        
        return jsonify(questions_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@question_bp.route('/api/questions', methods=['POST'])
@jwt_required()
def create_question():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        required_fields = ['quiz_id', 'question_statement', 'option1', 'option2', 'correct_option']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        question = Question(
            quiz_id=data['quiz_id'],
            question_statement=data['question_statement'],
            option1=data['option1'],
            option2=data['option2'],
            option3=data.get('option3'),
            option4=data.get('option4'),
            correct_option=data['correct_option'],
            points=data.get('points', 1)
        )
        
        db.session.add(question)
        db.session.commit()
        
        if redis_available:
            redis_client.delete(f'questions_quiz_{data["quiz_id"]}')
        
        return jsonify(question.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@question_bp.route('/api/questions/<int:question_id>', methods=['PUT'])
@jwt_required()
def update_question(question_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if data.get('question_statement'):
            question.question_statement = data['question_statement']
        if data.get('option1'):
            question.option1 = data['option1']
        if data.get('option2'):
            question.option2 = data['option2']
        if data.get('option3') is not None:
            question.option3 = data['option3']
        if data.get('option4') is not None:
            question.option4 = data['option4']
        if data.get('correct_option') is not None:
            question.correct_option = data['correct_option']
        if data.get('points') is not None:
            question.points = data['points']
        
        db.session.commit()
        
        # Clear cache for the quiz this question belongs to
        if redis_available:
            redis_client.delete(f'questions_quiz_{question.quiz_id}')
        
        return jsonify(question.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@question_bp.route('/api/questions/<int:question_id>', methods=['DELETE'])
@jwt_required()
def delete_question(question_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        db.session.delete(question)
        db.session.commit()
        if redis_available:
            redis_client.delete(f'questions_quiz_{question.quiz_id}')
        return jsonify({'message': 'Question deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500