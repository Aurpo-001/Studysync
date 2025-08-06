from flask import Blueprint, request, jsonify
from app import db
from app.models.note import Note

note_bp = Blueprint('notes', __name__, url_prefix='/api/notes')

@note_bp.route('', methods=['GET', 'POST'])
def handle_notes():
    if request.method == 'GET':
        try:
            print("GET /api/notes called")
            notes = Note.query.all()
            return jsonify([note.to_dict() for note in notes])
        except Exception as e:
            print(f"Error getting notes: {str(e)}")
            return jsonify({'error': str(e)}), 400
    
    elif request.method == 'POST':
        try:
            print("POST /api/notes called")
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            print(f"Received data: {data}")
            
            note = Note(
                title=data.get('title', ''),
                content=data.get('content', ''),
                subject=data.get('subject', '')
            )
            
            db.session.add(note)
            db.session.commit()
            
            print(f"Note created with ID: {note.id}")
            
            return jsonify(note.to_dict()), 201
        except Exception as e:
            print(f"Error creating note: {str(e)}")
            return jsonify({'error': str(e)}), 400