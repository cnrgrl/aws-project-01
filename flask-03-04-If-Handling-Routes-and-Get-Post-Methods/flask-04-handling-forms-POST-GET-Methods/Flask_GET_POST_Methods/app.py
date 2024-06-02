# Import Flask modules
from flask import Flask, render_template, request, flash
# Import int validator from wtforms
from wtforms.validators import InputRequired, NumberRange, IntValidators
# Import Form class from flask forms
from flask_wtf import FlaskForm
# Import integer field from wtforms
from wtforms import IntegerField

# Create an object named app
app = Flask(__name__)
# Set a secret key for the app
app.config['SECRET_KEY'] = 'mysecretkey'

# Create a form named `CalculationForm` which inherits from FlaskForm
class CalculationForm(FlaskForm):
    # Add two integer fields named `number1` and `number2`
    number1 = IntegerField('Number 1', validators=[InputRequired(), NumberRange(min=1, max=10000)])
    number2 = IntegerField('Number 2', validators=[InputRequired(), NumberRange(min=1, max=10000)])

# create a function named "lcm" which calculates a least common multiple values of two numbers. 
def lcm(num1, num2):
    common_multiplications = [] 
    for i in range(max(num1, num2), num1*num2+1):
        if i%num1==0 and i%num2==0:
           common_multiplications.append(i) 
    return min(common_multiplications)

# Create a function named `index` which uses template file named `index.html` 
# send an empty form as template variable to the app.py and assign route of no path ('/') 
@app.route("/", methods=["GET", "POST"])
def index():
    # Create a form object named `form`
    form = CalculationForm()
    # If the form is submitted and valid
    if form.validate_on_submit():
        # Flash a success message
        flash('Form submitted successfully!', 'success')
        # Redirect to the calculation route
        return calculate(form.number1.data, form.number2.data)
    # Render the `index.html` template with the form object
    return render_template("index.html", form=form)

# calculate sum of them using "lcm" function, then sent the result to the 
# "result.hmtl" file and assign route of path ('/calc'). 
# When the user comes directly "/calc" path, "Since this is a GET request, LCM has not been calculated" string returns to them with "result.html" file
@app.route("/calc", methods=["GET", "POST"])
def calculate(result1=None, result2=None):
    if request.method == "POST":
        # Create a form object named `form`
        form = CalculationForm()
        # If the form is submitted and valid
        if form.validate_on_submit():
            # Get the two numbers from the form
            result1 = form.number1.data
            result2 = form.number2.data
            # Calculate the LCM
            lcm_value = lcm(result1, result2)
            # Render the `result.html` template with the two numbers and the LCM value
            return render_template("result.html", result1=result1, result2=result2, lcm=lcm_value, developer_name='Caner')
    else:
        # If the request method is GET, check if the two numbers are provided
        if result1 is not None and result2 is not None:
            # Calculate the LCM
            lcm_value = lcm(result1, result2)
            # Render the `result.html` template with the two numbers and the LCM value
            return render_template("result.html", result1=result1, result2=result2, lcm=lcm_value, developer_name='Caner')
        else:
            # If the two numbers are not provided, render the `result.html` template with a message
            return render_template("result.html", developer_name='Caner', message='Since this is a GET request, LCM has not been calculated')

# Add a statement to run the Flask application which can be debugged.
if __name__== "__main__":
    # app.run(debug=True)
     app.run(host='0.0.0.0', port=80)
