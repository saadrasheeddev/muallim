from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests
import geocoder

app = Flask(__name__, static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/bar', methods=['GET', 'POST'])
def bar():
    button = request.form.get('button')
    if button == "Proceed":
        return redirect(url_for('start_umrah'))

    return render_template('bar_test.html')

@app.route('/submit', methods=['POST'])
def submit():
    choice = request.form['choice']
    if choice == 'hajj':
        return redirect(url_for('hajj'))
    elif choice == 'umrah':
        return redirect(url_for('umrah'))

@app.route('/hajj')
def hajj():
    return render_template('hajj.html')

@app.route('/qibla', methods=['GET', 'POST'])
def get_qibla_direction():
    return render_template('qibla.html')


@app.route('/umrah', methods=['GET', 'POST'])
def umrah():
    if request.method == "POST":
        return redirect(url_for('passport'))
    else:    
        return render_template('umrah.html')

@app.route('/passport', methods=['GET', 'POST'])
def passport():
    if request.method == "POST":
        return redirect(url_for('bar'))
    return render_template('passport.html')

@app.route('/start_umrah', methods=['GET', 'POST'])
def start_umrah():
    if request.method == "POST":
        return redirect(url_for('tawaf_steps'))
    return render_template('start_umrah.html')

@app.route('/tawaf_steps')
def tawaf_steps():
    return render_template('tawaf_steps.html')

@app.route('/intend_tawaf', methods=['GET', 'POST'])
def intend_tawaf():
    if request.method == 'POST':
        location = request.form.get('location')
        if location:
            counter = 1
            circle_time = 300 if location == 'mataf' else 600
            return render_template('tawaf.html', location=location, counter=counter, circle_time=circle_time)

    if request.args.get('reset') == 'true':
        counter = 1
        return render_template('intend_tawaf.html')

    return render_template('intend_tawaf.html')

@app.route('/reset', methods=['GET'])
def reset():
    return render_template('reset.html')



@app.route('/tawaf', methods=['POST'])
def tawaf():
    counter = int(request.form.get('counter'))
    circle_time = int(request.form.get('circle_time'))
    location = request.form.get('location')
    button = request.form.get('button')

    if counter > 7:
            return render_template('tawaf.html', location=location, counter=counter, circle_time=circle_time, complete=True)

    if button == 'Salah Break':
        return render_template('tawaf.html', location=location, counter=counter, circle_time=circle_time, pause=True)
    elif button == f'Done with {counter} circle':
        counter += 1
        if counter > 7:
            return render_template('tawaf.html', location=location, counter=counter, circle_time=circle_time, complete=True)
        else:
            return render_template('tawaf.html', location=location, counter=counter, circle_time=circle_time)
    elif button == f'Resume Timer':
        return render_template('tawaf.html', location=location, counter=counter, circle_time=circle_time)
    else:
        counter += 1
        return render_template('tawaf.html', location=location, counter=counter, circle_time=circle_time)

# import openai
# openai.api_key = ''

# @app.route('/get_response', methods=['POST'])
# def get_response():
#     request_data = request.get_json()
#     user_message = request_data['message']

#     response = openai.Completion.create(
#         engine='text-davinci-003',
#         prompt=user_message,
#         max_tokens=50,
#         n=1,
#         stop=None,
#     )

#     print(response.choices[0].text.strip())

#     return jsonify({'response': response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(debug=True)