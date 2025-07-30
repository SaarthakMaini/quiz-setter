from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import Question, Score, User
from database import db

score_bp = Blueprint('score', __name__)

@score_bp.route('/api/quizzes/<int:quiz_id>/submit', methods=['POST'])
@jwt_required()
def submit_quiz(quiz_id):
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        answers = data.get('answers', {})
        time_taken = data.get('time_taken', 0)
        
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        
        total_scored = 0
        total_possible = 0
        
        for question in questions:
            total_possible += question.points
            user_answer = answers.get(str(question.id))
            if user_answer and int(user_answer) == question.correct_option:
                total_scored += question.points
        
        percentage = (total_scored / total_possible * 100) if total_possible > 0 else 0
        
        score = Score(
            quiz_id=quiz_id,
            user_id=current_user_id,
            total_scored=total_scored,
            total_possible=total_possible,
            percentage=percentage,
            time_taken=time_taken
        )
        
        db.session.add(score)
        db.session.commit()
        
        return jsonify({
            'score': score.to_dict(),
            'message': 'Quiz submitted successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@score_bp.route('/api/users/<int:user_id>/scores', methods=['GET'])
@jwt_required()
def get_user_scores(user_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user.role != 'admin' and current_user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        scores = Score.query.filter_by(user_id=user_id).order_by(Score.timestamp_of_attempt.desc()).all()
        scores_data = [score.to_dict() for score in scores]
        
        return jsonify(scores_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500