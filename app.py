from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eisenhower.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la base de datos
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    quadrant = db.Column(db.String(50), nullable=False)  # Urgente-Importante, etc.

# Crear la base de datos
with app.app_context():
    db.create_all()

# Ruta principal: Mostrar la matriz de Eisenhower
@app.route('/')
def index():
    tasks = Task.query.all()
    # Organizar las tareas por cuadrantes
    matrix = {'Urgente-Importante': [], 'No Urgente-Importante': [],
              'Urgente-No Importante': [], 'No Urgente-No Importante': []}
    for task in tasks:
        matrix[task.quadrant].append(task)
    return render_template('index.html', matrix=matrix)

# Ruta para agregar una nueva tarea
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form.get('description', '')
    quadrant = request.form['quadrant']
    new_task = Task(title=title, description=description, quadrant=quadrant)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

# Ruta para eliminar una tarea
@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Ruta para actualizar una tarea (descripción y cuadrante)
@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    task = Task.query.get_or_404(id)
    task.description = request.form['description']
    task.quadrant = request.form['quadrant']
    db.session.commit()
    return redirect(url_for('index'))

# Ruta para inicializar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
