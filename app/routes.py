from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def validate_model_id(model, id):
    if not id.isnumeric():
        abort(make_response(f'Error: {id} is invalid', 400))
    
    entity = model.query.get(id)
    if not entity:
        abort(make_response(f'Not found: No {model.__name__} with id#{id} is found', 404))
    return entity

def validate_model_entry(model, request_body):
    for atr in model.get_attributes():
        if atr not in request_body:
            abort(make_response(f'Invalid Request. {model.__name__} {atr} missing', 400))
    return request_body

def create_response(entity):
    entity_dict = entity.to_dict()
    if not entity_dict['completed_at']:
        entity_dict['is_complete'] = False
        del entity_dict['completed_at']
    # else:
    #     task['completed_at'] = func.now() ??? return current datetime?
    return entity_dict

@tasks_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json()
    valid_request = validate_model_entry(Task, request_body)

    new_task = Task.from_dict(valid_request)
    
    db.session.add(new_task)
    db.session.commit()
    
    return {'task': create_response(new_task)}, 201

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    title_query = request.args.get('title')
    
    if title_query:
        tasks = Task.guery.filter(Task.title.ilike(title_query+'%'))
    else:
        tasks = Task.query.all()
    
    task_response = [create_response(task) for task in tasks]
    
    return jsonify(task_response), 200

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_task_by_id(task_id):
    pass

@tasks_bp.route('/<task_id>', methods=['PUT'])
def replace_task(task_id):
    pass

@tasks_bp.route('/<task_id>', methods=['PATCH'])
def update_task(task_id):
    pass

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    pass