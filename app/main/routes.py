from flask import render_template, jsonify,request
from app.main import bp

@bp.route('/')
def index():
    ip="102"
    return render_template('index.html', ip=ip)

@bp.route('/run-python-function', methods=['POST'])
def run_python_function():
    # Get the value of the slider from the AJAX request
    slider_value = request.form.get('value')

    # Call your Python function here, passing the slider value as a parameter
    result = my_python_function(slider_value)
    return jsonify(result=result)

def my_python_function(slider):
    
    print("hello from web")
    print(slider)
    print("")