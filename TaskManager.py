from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from marshmallow import Schema, fields, ValidationError
from flasgger import Swagger
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tasks.db?check_same_thread=False&timeout=30'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER'] = {
    "definitions": {
        "Task": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "example": "Новая задача"},
                "description": {"type": "string", "example": "Описание задачи"},
                "status": {"type": "string", "example": "в процессе"},
                "due_date": {"type": "string", "example": "2024-11-09"}
            }
        }
    }
}
db = SQLAlchemy(app)
swagger = Swagger(app)
CORS(app)

class Task(db.Model):
    __tablename__ = "Tasks"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    status = db.Column(db.String, default="в процессе")
    due_date = db.Column(db.Date, default=date.today)

class Taskschema(Schema):
    title = fields.String(required=True, validate=lambda s: len(s) <= 100)
    description = fields.String(validate=lambda s: len(s) <= 500)
    status = fields.String(validate=lambda s: s in ["в процессе", "выполнено", "отложено"], dump_default="в процессе")
    due_date = fields.Date()
    
task_schema = Taskschema()
Tasks_schema = Taskschema(many=True)

@app.route("/Tasks", methods=["POST"])
def create_task():
    """
    Создать задачу
    ---
    tags:
      - Tasks
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/Task'
    responses:
      201:
        description: Задача создана
      400:
        description: Ошибка проверки
      500:
        description: Ошибка базы данных
    """
    if not request.json:
        return jsonify({"error": "Отсутствует тело запроса"}), 400
    try:
        data = task_schema.load(request.json)
        new_task = Task(**data)
        db.session.add(new_task)
        db.session.commit()
        return jsonify(task_schema.dump(new_task)), 201
    except ValidationError as err:
        return jsonify({"error": "Ошибка валидации", "details": err.messages}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Ошибка базы данных", "details": str(e)}), 500

@app.route("/Tasks", methods=["GET"])
def get_Tasks():
    """
    Получить список задач
    ---
    tags:
      - Tasks
    parameters:
      - name: status
        in: query
        type: string
        required: false
      - name: due_date
        in: query
        type: string
        required: false
      - name: page
        in: query
        type: integer
        required: false
        default: 1
      - name: size
        in: query
        type: integer
        required: false
        default: 10
    responses:
      200:
        description: Список задач
      400:
        description: Недопустимый формат даты
      500:
        description: Ошибка базы данных | Внутренняя ошибка сервера
    """
    try:
        status = request.args.get("status")
        due_date = request.args.get("due_date")
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 10))

        query = Task.query

        if status:
            query = query.filter_by(status=status)
        if due_date:
            try:
                due_date_obj = date.fromisoformat(due_date)
                query = query.filter(Task.due_date <= due_date_obj)
            except ValueError:
                return jsonify({"error": "Недопустимый формат даты"}), 400

        tasks = query.paginate(page=page, per_page=size, error_out=False)
        return jsonify(Tasks_schema.dump(tasks.items))
    except SQLAlchemyError as e:
        return jsonify({"error": "Ошибка базы данных", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Внутренняя ошибка сервера", "details": str(e)}), 500

@app.route("/Tasks/<int:id>", methods=["GET"])
def get_task(id):
    """
    Получить задачу по id
    ---
    tags:
      - Tasks
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Задача по id
      404:
        description: Задача не найдена
      500:
        description: Ошибка базы данных
    """
    try:
        task = Task.query.get(id)
        if not task:
            return jsonify({"error": "Задача не найдена"}), 404
        return jsonify(task_schema.dump(task))
    except SQLAlchemyError as e:
        return jsonify({"error": "Ошибка базы данных", "details": str(e)}), 500

@app.route("/Tasks/<int:id>", methods=["PUT"])
def update_task(id):
    """
    Обновить задачу
    ---
    tags:
      - Tasks
    parameters:
      - name: id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/Task'
    responses:
      200:
        description: Задача обновлена
      400:
        description: Ошибка проверки
      404:
        description: Задача не найдена
      500:
        description: Ошибка базы данных
    """
    if not request.json:
        return jsonify({"error": "Отсутствует тело запроса"}), 400
    try:
        task = Task.query.get(id)
        if not task:
            return jsonify({"error": "Задача не найдена"}), 404
        data = task_schema.load(request.json, partial=True)
        for key, value in data.items():
            setattr(task, key, value)
        db.session.commit()
        return jsonify(task_schema.dump(task)), 200
    except ValidationError as err:
        return jsonify({"error": "Ошибка валидации", "details": err.messages}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Ошибка базы данных", "details": str(e)}), 500

@app.route("/Tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    """
    Удалить задачу
    ---
    tags:
      - Tasks
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Задача удалена
      404:
        description: Задача не найдена
      500:
        description: Ошибка базы данных
    """
    try:
        task = Task.query.get(id)
        if not task:
            return jsonify({"error": "Задача не найдена"}), 404
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Задача удалена"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Ошибка базы данных", "details": str(e)}), 500

def populate_test_data():
    db.session.query(Task).delete()
    Tasks = [
        Task(title="Задача 1", description="Описание задачи 1", status="в процессе", due_date=date(2024, 12, 31)),
        Task(title="Задача 2", description="Описание задачи 2", status="выполнено", due_date=date(2024, 10, 15)),
        Task(title="Задача 3", description="Описание задачи 3", status="отложено", due_date=date(2024, 11, 25)),
    ]
    db.session.bulk_save_objects(Tasks)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        populate_test_data()
        app.run(debug=True)
