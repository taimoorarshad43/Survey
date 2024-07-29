from flask import Flask, render_template, redirect, jsonify, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responsekey = 'RESPONSES'
answers = []
count = 0

@app.route('/')
def home():
    return render_template('home.html',survey_title = satisfaction_survey.title, survey_instructions = satisfaction_survey.instructions)

@app.route('/session', methods = ['POST'])
def add_to_session():
    session[responsekey] = []
    return redirect('/question/0')

@app.route('/question/<int:question>')
def questions(question):

    if question != count: # In case the user wants to bypass the question order
        tgt= satisfaction_survey.questions[count]
        tgt_question = tgt.question
        q_responses = tgt.choices
        flash("Please answer the questions in order!")
        return redirect(f'/question/{count}')

    tgt= satisfaction_survey.questions[question]
    tgt_question = tgt.question
    q_responses = tgt.choices

    return render_template('question.html', question = tgt_question, question_no = question, choices = q_responses)

@app.route('/answer', methods = ["POST"])
def answer():
    # answers.append(request.form["responses"])
    session[responsekey].append(request.form["responses"])
    # responses = session[responsekey]
    # responses.append(request.form["responses"])
    # session[responsekey] = responses
    global count
    count += 1

    if count >= len(satisfaction_survey.questions):
        count = 0 # resetting the counter if we go beyond the original set of questions.
        return redirect('/thankyou')

    return redirect(f'/question/{count}')

@app.route('/thankyou')
def thankyou():
    print(session[responsekey])
    return "Thank You!"