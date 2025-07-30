from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Chapter, User
from database import db
import json
from app import redis_available, redis_client

chapter_bp = Blueprint('chapter', __name__)

@chapter_bp.route('/api/subjects/<int:subject_id>/chapters', methods=['GET'])
@jwt_required()
def get_chapters(subject_id):
    try:
        if redis_available:
            cache_key = f'chapters_subject_{subject_id}'
            cached_data = redis_client.get(cache_key)
            
            if cached_data:
                return jsonify(json.loads(cached_data)), 200
        
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        chapters_data = [chapter.to_dict() for chapter in chapters]
        
        if redis_available:
            redis_client.setex(cache_key, 300, json.dumps(chapters_data))
        
        return jsonify(chapters_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chapter_bp.route('/api/chapters', methods=['POST'])
@jwt_required()
def create_chapter():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        if not data.get('name') or not data.get('subject_id'):
            return jsonify({'error': 'Chapter name and subject_id are required'}), 400
        
        chapter = Chapter(
            name=data['name'],
            description=data.get('description', ''),
            subject_id=data['subject_id']
        )
        
        db.session.add(chapter)
        db.session.commit()
        
        if redis_available:
            redis_client.delete(f'chapters_subject_{data["subject_id"]}')
        
        return jsonify(chapter.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chapter_bp.route('/api/chapters/<int:chapter_id>', methods=['PUT'])
@jwt_required()
def update_chapter(chapter_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return jsonify({'error': 'Chapter not found'}), 404
        
        data = request.get_json()
        
        if data.get('name'):
            chapter.name = data['name']
        if data.get('description') is not None:
            chapter.description = data['description']
        
        db.session.commit()
        
        if redis_available:
            redis_client.delete(f'chapters_subject_{chapter.subject_id}')
        
        return jsonify(chapter.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chapter_bp.route('/api/chapters/<int:chapter_id>', methods=['DELETE'])
@jwt_required()
def delete_chapter(chapter_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return jsonify({'error': 'Chapter not found'}), 404
        db.session.delete(chapter)
        db.session.commit()
        if redis_available:
            redis_client.delete(f'chapters_subject_{chapter.subject_id}')
        return jsonify({'message': 'Chapter deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500