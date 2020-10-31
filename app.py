from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

# debug = DebugToolbarExtension(app)

current_survey = surveys.get("satisfaction")

@app.route('/')
def show_title():
    return render_template('index.html', survey_title = current_survey.title, survey_instructions = current_survey.instructions)

@app.route('/startsurvey', methods=['POST'])
def start_survey():
    session["responses"] = []
    return redirect('/questions/0')

@app.route('/questions/<question_num>')
def show_question(question_num):
    responses = session["responses"]
    
    try:
        question_num = int(question_num)
    except ValueError:
        flash("Not a valid question number")
        return redirect(f'/questions/{len(responses)}')

    if question_num != len(responses):
        flash("Wrong question number")
        return redirect(f'/questions/{len(responses)}')
    elif question_num > len(current_survey.questions):
        flash("You've already taken the survey")
        return redirect('/end')
    else:
        current_question = current_survey.questions[question_num] 
        return render_template('question.html', survey_question = current_question.question, question = current_question.choices)

@app.route('/answer', methods=['POST'])
def store_answer():
    responses = session["responses"]
    responses.append(request.form["answer"])
    session["responses"] = responses
    if len(responses) < len(current_survey.questions):
        return redirect(f'/questions/{len(responses)}')
    else:
        return redirect('/end')

@app.route('/end')
def end_survey():
    return render_template('end.html', survey_title = current_survey.title)
    