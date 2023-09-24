#!/usr/bin/python3
"""
A script that starts a Flask web application.
"""

from flask import Flask, render_template,abort

app = Flask("__name__")


@app.route('/', strict_slashes=False)
def hello():
    """Returns a string"""
    return ("Hello HBNB!")


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Returns a string"""
    return ("HBNB")


@app.route('/c/<text>', strict_slashes=False)
def ctext(text):
    """display C followed by the value of the text variable.
        replace underscore _ symbols with a space
    """
    return "C {}".format(text.replace("_", " "))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def pytext(text='is cool'):
    """display Python followed by the value of the text variable.
        replace underscore _ symbols with a space
        The default value of text is “is cool”
    """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """display “n is a number” only if n is an integer
    """
    if isinstance(n, int):
        return f'{n} is a number'
    else:
        return f'{n} is not a number'

@app.route('/number_template/<n>', strict_slashes=False)
def number_rendered(n=None):
    """display a html page only if n is a number"""
    if isinstance(n, int):
        return render_template('5-number.html', n=n)
    else:
        abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
