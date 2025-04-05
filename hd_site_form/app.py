from flask import Flask, render_template, request, redirect, url_for
from urllib.parse import quote_plus

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    birth_date = request.form['birth_date']
    birth_time = request.form['birth_time']
    birth_place = request.form['birth_place']

    # Формируем ссылку с параметрами (кодировка параметров через quote_plus)
    url = (
        "https://app.maiamechanics.com/#/free-chart?"
        f"name={quote_plus(name)}&"
        f"birth_date={quote_plus(birth_date)}&"
        f"birth_time={quote_plus(birth_time)}&"
        f"birth_place={quote_plus(birth_place)}"
    )

    return render_template('result.html', chart_url=url)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
