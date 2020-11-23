
from flask import Flask, render_template, url_for, request, Response
from flask_sqlalchemy import SQLAlchemy
from queries import runQuery
import os
<<<<<<< HEAD
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
=======
import psycopg2

>>>>>>> 1ac190671aa1a2c335161372a1647ce23ff4d3fc

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = ''
# db = SQLAlchemy(app)

# def pass(database_name, user, password, port):


@app.route('/')
def index():
    return render_template('index.html', Props = Props)


@app.route('/filter', methods=["GET", "POST"])
def filter():
    if request.method == "POST":

        columns = request.form['columns']
        conditions = request.form['conditions']
        
        Props['rows'] = runQuery(columns, conditions, Props['conn'])[1:]
        Props['rowCount'] = len(Props['rows'])
        
        #TODO: RUN FILTER QUERY HERE ON PROPS
        #
        #Props['rows'] = newTuple

        return render_template("index.html", Props = Props)


@app.route('/table', methods=["GET", "POST"])
def table():
    if request.method == "POST":
        Props['displayType'] = "table"

        return render_template("index.html", Props = Props)

    return render_template("index.html", Props = Props)


@app.route('/graph', methods=["GET", "POST"])
def graph():
    if request.method == "POST":
        Props['displayType'] = "graph"

        return render_template("index.html", Props = Props)

    return render_template("index.html", Props = Props)

@app.route('/plot.png')
def plot_png():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(50)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])
    axis.set_title('random graph')
    axis.set_ylabel('integers')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")

@app.route('/plot2.png')
def plot_png2():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    axis.set_title('graph 2')
    axis.set_ylabel('numbers')
    axis.set_xlabel('time')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# Weird hack to get hot reloading working with browser-caching, can mostly ignore
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == "__main__":
    conn = psycopg2.connect(dbname="412db", user="postgres", password="barrow22")

    # Main data structure to pass around values between page reloads
    Props = {

        # SQL query content, tuple containing dictionaries representing the rows
        'rows' : ((), (),) ,
        'columns' : "",
        'conditions' : "",

        # len(rows), must be recalculated in .py file after a query
        'rowCount' : 0,

        'displayType' : "table",
        'conn' : conn,
    }

    
    # TODO: RUN SQL FIRST QUEREY HERE
    # Props['rows'] = SQLQUERY

    Props['rowCount'] = len(Props['rows'])

    app.run(debug=True)