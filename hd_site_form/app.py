from flask import Flask, render_template, request, redirect
from urllib.parse import urlencode

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    birthdate = request.form['birthdate']
    birthtime = request.form['birthtime']
    birthcity = request.form['birthcity']

    # Формируем ссылку на сервис бодиграфа
    query_params = urlencode({
        'name': name,
        'birthdate': birthdate,
        'birthtime': birthtime,
        'birthcity': birthcity
    })

    link = f"https://app.maiamechanics.com/#/free-chart?{query_params}"

    return render_template('result.html', name=name, birthdate=birthdate, birthtime=birthtime, birthcity=birthcity, link=link)

if __name__ == '__main__':
    app.run(debug=True)

