from flask import Flask, render_template, TemplateNotFound

app = Flask(__name__)

@app.route('/')
def head() -> str:
    """Renders the index.html template with the given values."""
    return render_template('index.html', number1=35, number2=36)

@app.route('/sum')
def sum() -> str:
    """Renders the body.html template with the sum of the two numbers."""
    number1 = 35
    number2 = 36
    sum_value = number1 + number2
    return render_template('body.html', value1=number1, value2=number2, sum=sum_value)

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    except TemplateNotFound:
        print("One of the templates is missing. Please check the template files.")
