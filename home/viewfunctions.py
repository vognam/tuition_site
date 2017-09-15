import zipfile as zf
import shutil
import sqlite3
import os
from django.core.files import File
import re
from fpdf import FPDF
import itertools, datetime

from .models import Question, QuestionDone, Student
from django.contrib.staticfiles.templatetags.staticfiles import static
from .forms import InputScoreForm


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# handle the uploaded file
# unzip file, get all questions from DB, save them as models
def handle_file(file):
    try:
        # extract zip into a folder
        if os.path.isdir('./extraction'):
            shutil.rmtree('./extraction')
        input_zip = zf.ZipFile(file, 'r')
        input_zip.extractall('./extraction')

        # see if the database exists and connect to it
        if os.path.isfile('./extraction/Categoriser-master/data.db'):
            db = sqlite3.connect('./extraction/Categoriser-master/data.db')
            cursor = db.cursor()
            cursor.execute('SELECT * FROM questions')
            all_rows = cursor.fetchall()

            for row in all_rows:
                print(row)

            last_id = get_last_qid()
            rename_questions(last_id)

            for row in all_rows:

                last_id += 1
                print('./extraction/Categoriser-master{}'.format(row[7][1:]))
                print(os.path.basename(row[7]))
                question = Question(category=row[1], difficulty=row[2], out_of=row[3],
                                    answer=row[6])
                question.save()
                question.image.save(
                    'QID{}.jpg'.format(last_id),
                    File(open('./extraction/Categoriser-master/questions/QID{}.jpg'.format(last_id), str('rb')))
                )
            db.close()
            return 'Uploaded success!'
    except Exception as e:
        return 'Upload failed: ' + str(e)


# Get the last question id
def get_last_qid():
    print('getting last id')
    all_questions = Question.objects.all()
    if len(all_questions) == 0:
        return 0
    else:
        path = os.path.basename(str(all_questions[len(all_questions)-1].image))
        print('got last id {}'.format(path))
        return int(path[3:-4])


# Rename the question jpgs in the uploaded file
def rename_questions(last_id):
    print('renaming files - last_id = ' + str(last_id))
    folder = './extraction/Categoriser-master/questions'

    # natural sort and reverse order the list of questions
    lst = os.listdir(folder)
    lst = natural_sort(lst)
    lst.reverse()

    for filename in lst:
        if filename.endswith('.jpg'):
            # print('first file doing')
            # last_id += 1
            question_id = int(filename[3:-4])
            print('file is {}/{}'.format(folder, filename))
            os.rename('{}/{}'.format(folder, filename), '{}/QID{}.jpg'.format(folder, question_id + last_id))


# sort numerically
def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def createPDF(student):

    # get date of next saturday (unless today is Saturday)
    d = datetime.date.today()
    while d.weekday() != 5:
        d += datetime.timedelta(1)

    questions = []

    pdf = FPDF()
    createFrontPage(pdf, student, d)

    all_questions = chooseQuestions(student)

    # create pdf of questions
    for question in itertools.islice(all_questions, 0, 10):
        image_url = os.path.join(BASE_DIR, 'home') + question.image.url
        print(image_url)
        pdf.image(name=image_url, w=195)
        questions.append(question)

    # create folder to store the homeworks in
    output_folder = os.path.join(BASE_DIR, 'home', 'media', 'homework',
                                 str(student.classID.time), str(student.id),)
    try:
        os.makedirs(output_folder)
    except:
        pass

    # if homework has been made, then return an error, otherwise create homework
    filename = str(student.first_name) + '_' + student.last_name + ':' + str(d) + '.pdf'

    if not os.path.exists(os.path.join(output_folder, filename)):
        pdf.output(name=os.path.join(output_folder, filename))
        addQuestionsDone(questions=questions, student=student)
    else:
        # TODO return some kind of message
        print('already exists')
        pass


def createFrontPage(pdf, student, date):
    pdf.add_page()
    # set font
    pdf.set_font('Arial', 'B', 30)
    pdf.set_y(pdf.get_y() + 60)
    # add logo
    pdf.image(x=65, name=os.path.join(BASE_DIR, 'home', 'static', 'home', 'images', 'logo.png'), w=80)
    pdf.set_y(pdf.get_y() + 10)
    pdf.cell(w=0, h=0, txt=str(student.first_name) + ' ' + str(student.last_name),
             border=0, ln=1, align='C')
    pdf.set_y(pdf.get_y() + 15)
    pdf.cell(w=0, h=0, txt=str(date), border=0, align='C')
    pdf.add_page()


def chooseQuestions(student):
    not_done_questions = Question.objects.exclude(questiondone__student=student)

    return not_done_questions


# mark these questions as '-1'
def addQuestionsDone(questions, student):
    for question in questions:
        questionDone = QuestionDone(student=student, question=question, score=-1)
        questionDone.save()
