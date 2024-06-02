from flask import Flask, abort, request

APP_NAME = 'My Application'
APP_VERSION = '0.1.0'
ABOUT_MESSAGE = 'This is the about page of my application.'
SECRET_KEY = 'my-secret-key'

app = Flask(APP_NAME)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def head():
    return 'Hello world Oktay'


@app.route('/second')
def second():
    return 'This is second page'


@app.route('/third')
def third():
    return 'This is third page'


@app.route('/forth/<string:id>')
def forth(id):
    return f'Id of this page is {id}'


@app.route('/about')
def about():
    return ABOUT_MESSAGE


@app.route('/not-found')
def not_found():
    return 'This page was not found', 404


@app.route('/version')
def version():
    return APP_VERSION


@app.route('/health')
def health():
    return 'OK'


@app.errorhandler(404)
def page_not_found(error):
    return not_found()


if __name__ == '__main__':
    docstring = f'{APP_NAME} ({APP_VERSION})'
    print(docstring)
    print('Starting server on http://0.0.0.0/0:80')
    app.run(debug=True, host='0.0.0.0/0', port=80)
