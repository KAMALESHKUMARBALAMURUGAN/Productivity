from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

tasks = {
    "Urgent & Important(DO FIRST)": [],
    "Not Urgent & Important(SCHEDULE)": [],
    "Urgent & Not Important(DELEGATE)": [],
    "Not Urgent & Not Important(DON'T DO)": []
}

@app.route('/')
def index():
    current_date = datetime.now().strftime("%A, %d %B %Y")
    return render_template('index.html', current_date=current_date)

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    task = data.get('task')
    category = data.get('category')
    if task and category in tasks:
        tasks[category].append(task)
        return jsonify({'success': True, 'tasks': tasks})
    return jsonify({'success': False, 'error': 'Invalid data'})

@app.route('/remove_task', methods=['POST'])
def remove_task():
    data = request.json
    task = data.get('task')
    category = data.get('category')
    if task and category in tasks and task in tasks[category]:
        tasks[category].remove(task)
        return jsonify({'success': True, 'tasks': tasks})
    return jsonify({'success': False, 'error': 'Invalid data'})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(debug=True)