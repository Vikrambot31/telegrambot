from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    birth_date = request.form['birth_date']
    birth_time = request.form['birth_time']
    birth_place = request.form['birth_place']
    # Можно сохранять или обрабатывать дальше
    return render_template('result.html', name=name, birth_date=birth_date, birth_time=birth_time, birth_place=birth_place)

if __name__ == '__main__':
    app.run()

