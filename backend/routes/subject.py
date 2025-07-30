from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import redis_available, redis_client
from models import Subject
import json
from database import db
from models import User

subject_bp = Blueprint('subject', __name__)

@subject_bp.route('/api/subjects', methods=['GET'])
@jwt_required()
def get_subjects():
    try:
        if redis_available:
            cache_key = 'subjects_list'
            cached_data = redis_client.get(cache_key)
            
            if cached_data:
                return jsonify(json.loads(cached_data)), 200
        
        subjects = Subject.query.all()
        subjects_data = [subject.to_dict() for subject in subjects]
        
        if redis_available:
            redis_client.setex(cache_key, 300, json.dumps(subjects_data))
        
        return jsonify(subjects_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@subject_bp.route('/api/subjects', methods=['POST'])
@jwt_required()
def create_subject():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Subject name is required'}), 400
        
        subject = Subject(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(subject)
        db.session.commit()
        
        if redis_available:
            redis_client.delete('subjects_list')
        
        return jsonify(subject.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@subject_bp.route('/api/subjects/<int:subject_id>', methods=['PUT'])
@jwt_required()
def update_subject(subject_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        data = request.get_json()
        
        if not data.get('description'):
            return jsonify({'error': 'Description is required'}), 400
        
        subject.description = data['description']
        db.session.commit()
        
        if redis_available:
            redis_client.delete('subjects_list')
        
        return jsonify(subject.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@subject_bp.route('/api/subjects/<int:subject_id>', methods=['DELETE'])
@jwt_required()
def delete_subject(subject_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        db.session.delete(subject)
        db.session.commit()
        if redis_available:
            redis_client.delete('subjects_list')
        return jsonify({'message': 'Subject deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500