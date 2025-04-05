from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    birthdate = request.form['birthdate']
    birthtime = request.form['birthtime']
    birthcity = request.form['birthcity']

    # Это просто пример — ты пока можешь ничего не отправлять
    return render_template("result.html", name=name, birthdate=birthdate, birthtime=birthtime, birthcity=birthcity)

if __name__ == "__main__":
    app.run()
