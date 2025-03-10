from flask import Blueprint, request, jsonify
from flask_socketio import emit
from models import db, CodeBlock
from sqlalchemy.exc import IntegrityError

# Create Blueprint for API routes
api = Blueprint('api', __name__)

# Reference to rooms (will be imported from server.py)
rooms = None

def set_rooms_reference(rooms_dict):
    global rooms
    rooms = rooms_dict

# Get list of code blocks for the lobby page
@api.route('/api/codeblocks', methods=['GET'])
def get_codeblocks():
    codeblocks = CodeBlock.query.all()
    data = []
    for cb in codeblocks:
        data.append({
            'id': cb.id,
            'name': cb.name
        })
    return jsonify(data)

# Get a specific code block (the solution is kept on the server)
@api.route('/api/codeblocks/<int:codeblock_id>', methods=['GET'])
def get_codeblock(codeblock_id):
    cb = CodeBlock.query.get_or_404(codeblock_id)
    return jsonify({
        'id': cb.id,
        'name': cb.name,
        'template': cb.template,
        'explanation': cb.explanation
    })

# Get all code blocks with full details for admin interface
@api.route('/api/codeblocks/admin', methods=['GET'])
def get_all_codeblocks_admin():
    codeblocks = CodeBlock.query.all()
    data = []
    for cb in codeblocks:
        data.append({
            'id': cb.id,
            'name': cb.name,
            'template': cb.template,
            'solution': cb.solution,
            'explanation': cb.explanation
        })
    return jsonify(data)

# Update an existing code block
@api.route('/api/codeblocks/<int:codeblock_id>', methods=['PUT'])
def update_codeblock(codeblock_id):
    codeblock = CodeBlock.query.get_or_404(codeblock_id)
    data = request.json
    
    if 'name' in data:
        codeblock.name = data['name']
    if 'template' in data:
        codeblock.template = data['template']
    if 'solution' in data:
        codeblock.solution = data['solution']
    if 'explanation' in data:
        codeblock.explanation = data['explanation']
    
    try:
        db.session.commit()
        
        # If this codeblock is currently in use in a room, update the template
        for room_id, state in rooms.items():
            if int(room_id) == codeblock_id:
                state['code'] = codeblock.template
                emit('update_code', {'code': codeblock.template}, room=room_id)
        
        return jsonify({
            'id': codeblock.id,
            'name': codeblock.name,
            'template': codeblock.template,
            'solution': codeblock.solution,
            'explanation': codeblock.explanation
        })
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while updating the code block'}), 500

# Create a new code block
@api.route('/api/codeblocks', methods=['POST'])
def create_codeblock():
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'template', 'solution', 'explanation']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    new_codeblock = CodeBlock(
        name=data['name'],
        template=data['template'],
        solution=data['solution'],
        explanation=data['explanation']
    )
    
    try:
        db.session.add(new_codeblock)
        db.session.commit()
        
        return jsonify({
            'id': new_codeblock.id,
            'name': new_codeblock.name,
            'template': new_codeblock.template,
            'solution': new_codeblock.solution,
            'explanation': new_codeblock.explanation,
            'message': 'Code block created successfully'
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while saving the code block'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

# Delete a code block
@api.route('/api/codeblocks/<int:codeblock_id>', methods=['DELETE'])
def delete_codeblock(codeblock_id):
    codeblock = CodeBlock.query.get_or_404(codeblock_id)

    try:
        # Check if the codeblock is currently in use in any room
        if str(codeblock_id) in rooms:
            # Notify clients in this room to return to lobby
            emit('redirect_to_lobby', {
                'message': 'This code block has been deleted. Returning to lobby.'
            }, room=str(codeblock_id))
            # Remove the room
            del rooms[str(codeblock_id)]
        
        db.session.delete(codeblock)
        db.session.commit()
        
        return jsonify({'message': 'Code block deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred while deleting the code block: {str(e)}'}), 500