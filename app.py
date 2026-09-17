from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        name = request.form.get('name')
        prediction = f"Hello {name}! Based on your planetary positions, strong career growth in cloud computing is expected."
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
