from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'secret'

leaders = []


@app.route('/')
def index():
    random_number = random.randint(1, 100)
    session['ran_num'] = random_number
    session['tracker'] = 0
    print(session['ran_num'])
    return render_template('index.html', ran_num=random_number)


@app.route('/guess')
def guess():
    valid_number = False
    guess_number = int(request.args['guess'])
    correct = False
    if 1 <= guess_number <= 100:
        valid_number = True
        session['tracker'] += 1
        if guess_number == session['ran_num']:
            correct = True
        elif guess_number > session['ran_num']:
            correct = False
            print('Too high!')
        elif guess_number < session['ran_num']:
            correct = False
            print('Too low!')
    return render_template('guess.html', guess_num=guess_number, correct=correct, valid_number=valid_number)


@app.route('/leaderboard', methods=['POST'])
def leaderboard():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    attempts = int(session['tracker'])

    global leaders
    leaders.append({'first_name': first_name,
                   'last_name': last_name, 'attempts': attempts})
    sorted_leaders = sorted(leaders, key=lambda x: x['attempts'])
    return render_template('leaderboard.html', leaders=sorted_leaders)


if __name__ == '__main__':
    app.run(debug=True)
