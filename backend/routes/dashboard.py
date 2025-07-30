from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Subject, Quiz, Score

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user.role == 'admin':
            stats = {
                'total_users': User.query.filter_by(role='user').count(),
                'total_subjects': Subject.query.count(),
                'total_quizzes': Quiz.query.count(),
                'total_attempts': Score.query.count(),
                'recent_attempts': [score.to_dict() for score in Score.query.order_by(Score.timestamp_of_attempt.desc()).limit(10)]
            }
        else:
            user_scores = Score.query.filter_by(user_id=current_user_id).all()
            stats = {
                'total_attempts': len(user_scores),
                'average_score': sum(score.percentage for score in user_scores) / len(user_scores) if user_scores else 0,
                'best_score': max(score.percentage for score in user_scores) if user_scores else 0,
                'recent_attempts': [score.to_dict() for score in user_scores[-10:]]
            }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500