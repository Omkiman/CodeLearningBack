from flask import request
from flask_socketio import join_room, emit
from models import CodeBlock

# Reference to socketio and rooms (will be imported from server.py)
socketio = None
rooms = None

def init_socket_handlers(socketio_instance, rooms_dict):
    """Initialize Socket.IO handlers with references to the SocketIO instance and rooms dictionary"""
    global socketio, rooms
    socketio = socketio_instance
    rooms = rooms_dict
    
    # Register event handlers
    socketio.on_event('connect', handle_connect)
    socketio.on_event('join_room', handle_join)
    socketio.on_event('code_change', handle_code_change)
    socketio.on_event('disconnect', handle_disconnect)

def handle_connect():
    """Handle client connection - send list of active rooms to the client"""
    active_rooms = []
    for room_id in rooms:
        cb = CodeBlock.query.get(room_id)
        if cb:
            active_rooms.append({
                'id': room_id,
                'name': cb.name,
                'student_count': len(rooms[room_id]['students'])
            })
    emit('active_rooms', active_rooms)

def handle_join(data):
    """Handle client joining a room"""
    room_id = data.get('room_id')
    if room_id is None:
        return
    join_room(room_id)
    # Load code block details from the database.
    cb = CodeBlock.query.get(room_id)
    if cb is None:
        return
    # If the room does not exist, first connection becomes mentor.
    if room_id not in rooms:
        rooms[room_id] = {'mentor': request.sid, 'code': cb.template, 'students': set()}
        role = 'mentor'
    else:
        role = 'student'
        rooms[room_id]['students'].add(request.sid)
    # Send role, current code, and student count back to the client.
    emit('role_assignment', {
        'role': role,
        'code': rooms[room_id]['code'],
        'student_count': len(rooms[room_id]['students'])
    })
    # Update student count for everyone in the room.
    emit('update_student_count', {
        'student_count': len(rooms[room_id]['students'])
    }, room=room_id)
    
    # After updating room state, broadcast active rooms to all clients
    active_rooms = []
    for rid in rooms:
        cb = CodeBlock.query.get(rid)
        if cb:
            active_rooms.append({
                'id': rid,
                'name': cb.name,
                'student_count': len(rooms[rid]['students'])
            })
    emit('active_rooms', active_rooms, broadcast=True)

def handle_code_change(data):
    """Handle code change events from clients"""
    room_id = data.get('room_id')
    new_code = data.get('code')
    if room_id not in rooms:
        return
    # Prevent mentor from making code changes (mentor is read-only)
    if request.sid == rooms[room_id].get('mentor'):
        return
    # Update the room's code state.
    rooms[room_id]['code'] = new_code
    # Broadcast updated code to all users in the room.
    emit('update_code', {'code': new_code}, room=room_id)
    # Check if the new code matches the solution.
    cb = CodeBlock.query.get(room_id)
    if cb and new_code.strip() == cb.solution.strip():
        emit('solution_found', {}, room=room_id)
    if cb and new_code.strip() != cb.solution.strip():
        emit('solution_incorrect', {}, room=room_id)

def handle_disconnect():
    """Handle client disconnection"""
    # When a user disconnects, check if they are in any room.
    for room_id, state in list(rooms.items()):
        if request.sid == state.get('mentor'):
            # If mentor disconnects, inform all students and reset the room.
            emit('redirect_to_lobby', {'message': 'Mentor left. Returning to lobby.'}, room=room_id)
            del rooms[room_id]
            break
        elif request.sid in state['students']:
            state['students'].remove(request.sid)
            # Update student count for remaining clients.
            emit('update_student_count', {
                'student_count': len(state['students'])
            }, room=room_id)
            break
    
    # After updating room state, broadcast active rooms to all clients
    active_rooms = []
    for rid in rooms:
        cb = CodeBlock.query.get(rid)
        if cb:
            active_rooms.append({
                'id': rid,
                'name': cb.name,
                'student_count': len(rooms[rid]['students'])
            })
    emit('active_rooms', active_rooms, broadcast=True)