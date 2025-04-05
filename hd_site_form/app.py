from flask import Flask, render_template, request

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
    city = request.form['city']  # 🛠 исправлено
    return render_template('result.html', name=name, birth_date=birth_date, birth_time=birth_time, city=city)

if __name__ == '__main__':
    app.run(debug=True)

