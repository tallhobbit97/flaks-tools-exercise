from flask import Flask, request, flash, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)

app.debug = True

app.config['SECRET_KEY'] = 'lollipop'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
curr_question = 0

@app.route('/')
def root_page():
    """Shows the user the title and instructions for the survey."""
    return render_template('survey.html', title=satisfaction_survey.title, survey_name=satisfaction_survey.title, instructions=satisfaction_survey.instructions)

@app.route('/start-survey', methods=['POST'])
def handle_start():
    '''Initializes the responses list within the session and redirects to the first question'''
    global repsonses
    session['responses'] = responses
    return redirect('question/0')

@app.route('/question/<num>')
def question_page(num):
    """Checks to make sure which question the user is on.
    Shows the user the question and records their answer.
    Redirects to thank-you-page when survey is complete."""
    if not int(num) == curr_question:
        flash('You are trying to access an invalid question. Please only answer the questions in order.')
        return redirect(f'/question/{curr_question}')
    else:
        if int(num) < len(satisfaction_survey.questions):
            try:
                return render_template('question.html', title=satisfaction_survey.title, survey_name=satisfaction_survey.title, question=satisfaction_survey.questions[int(num)].question, choices=satisfaction_survey.questions[int(num)].choices)
            except Exception as e:
                return str(e)
        else:
            return redirect('/thank-you-page')

@app.route('/answer', methods=['POST'])
def receive_answer():
    """Handling the storage of answers to questions."""
    answer = request.form['choice']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    global curr_question
    curr_question += 1
    return redirect(f'/question/{curr_question}')

@app.route('/thank-you-page')
def thank_you_page():
    """Shows user a thank you at completion of survey."""
    return render_template('thankyou.html', title=satisfaction_survey.title, survey_name='Thanks!')
