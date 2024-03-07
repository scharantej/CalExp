
# Import necessary libraries
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)

# Set up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calculator.db'
db = SQLAlchemy(app)

# Define the model for calculation records
class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(255))
    result = db.Column(db.Float)

# Create the database tables
db.create_all()

# Main route
@app.route('/')
def index():
    return render_template('index.html')

# Calculate route
@app.route('/calculate', methods=['POST'])
def calculate():
    # Get the input values
    expression = request.form['expression']

    # Perform calculation
    try:
        result = eval(expression)
    except Exception as e:
        result = 'Invalid expression'

    # Store the calculation record
    calculation = Calculation(expression=expression, result=result)
    db.session.add(calculation)
    db.session.commit()

    # Return the result
    return render_template('index.html', result=result)

# Export route
@app.route('/export')
def export():
    # Get the file name and export format
    file_name = request.args.get('file_name')
    export_format = request.args.get('export_format')

    # Generate the export file
    if export_format == 'csv':
        data = 'Expression,Result\n'
        for calculation in Calculation.query.all():
            data += f'{calculation.expression},{calculation.result}\n'
        return send_file(data, as_attachment=True, attachment_filename=file_name + '.csv')
    elif export_format == 'json':
        data = []
        for calculation in Calculation.query.all():
            data.append({'expression': calculation.expression, 'result': calculation.result})
        return send_file(json.dumps(data), as_attachment=True, attachment_filename=file_name + '.json')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
