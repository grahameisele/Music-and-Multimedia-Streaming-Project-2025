from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('project_template.html')

def start_server():
    app.run("0.0.0.0", port=80)