from __future__ import division
import zipfile as zf
import shutil
import sqlite3
import os
import random
from django.core.files import File
import re
from fpdf import FPDF
import itertools
import datetime

from operator import itemgetter
from .models import Question, QuestionDone, Class, Attendance
from django.forms import modelformset_factory
from django.db.models import Avg, F, Count

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

            last_id = get_last_qid()
            rename_questions(last_id)

            for row in all_rows:

                last_id += 1
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


def createPDF(student, category, user):

    # get date of next saturday (unless today is Saturday)
    d = getNextWeek(student)

    questions = []

    pdf = FPDF()
    createFrontPage(pdf, student, d)

    all_questions = chooseQuestions(student, category)

    # return None

    # create pdf of questions
    for question in all_questions:
        image_url = os.path.join(BASE_DIR, 'home') + question.image.url
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
        # If superuser, create unlimited docs
        if user.is_superuser:
            doc = False
            while not doc:
                d = d + datetime.timedelta(7)
                filename = str(student.first_name) + '_' + student.last_name + ':' + str(d) + '.pdf'
                if not os.path.exists(os.path.join(output_folder, filename)):
                    pdf.output(name=os.path.join(output_folder, filename))
                    addQuestionsDone(questions=questions, student=student)
                    doc = True


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


def chooseQuestions(student, category):

    # category, group_weakness, student_weakness_1, student_weakness_2
    topics = []

    # category for topic taught today
    topic_class = category
    topics.append(topic_class)

    # category for the group's weakness
    topic_group_weakness = QuestionDone.objects.filter(student__classID=student.classID)
    topic_group_weakness = getWeaknesses(topic_group_weakness, topics)
    topics.append(topic_group_weakness)

    # category for sections of the student's weakness
    student_weaknesses = QuestionDone.objects.filter(student=student.id)
    topic_student_weakness = getWeaknesses(student_weaknesses, topics)
    topics.append(topic_student_weakness)
    topic_student_weakness_two = getWeaknesses(student_weaknesses, topics)
    topics.append(topic_student_weakness_two)

    topics = filter(None, topics)

    # Now to choose the questions based on the topics :)
    year_group = student.classID.year
    new_questions = Question.objects.exclude(questiondone__student=student)

    selected_questions = []

    new_questions = getCategoryQuestions(year_group, new_questions, selected_questions, topics[0])

    # set hw depending on if student is year 4 of 5
    if year_group == 4:
        if len(topics) > 2:
            new_questions = getGroupAndStudentQuestions(year_group, new_questions, selected_questions, topics[2], category)
        else:
            new_questions = getMixQuestions(student, new_questions, selected_questions, topics)
    else:
        if len(topics) == 4:
            new_questions = getGroupAndStudentQuestions(year_group, new_questions, selected_questions, topics[1], category)
            new_questions = getGroupAndStudentQuestions(year_group, new_questions, selected_questions, topics[2], category)
            new_questions = getGroupAndStudentQuestions(year_group, new_questions, selected_questions, topics[3], category)
        elif len(topics) == 3:
            new_questions = getGroupAndStudentQuestions(year_group, new_questions, selected_questions, topics[1], category)
            new_questions = getGroupAndStudentQuestions(year_group, new_questions, selected_questions, topics[2], category)
            new_questions = getMixQuestions(student, new_questions, selected_questions, topics)
        elif len(topics) == 2:
            new_questions = getGroupAndStudentQuestions(year_group, new_questions, selected_questions, topics[1], category)
            new_questions = getMixQuestions(student, new_questions, selected_questions, topics)
            new_questions = getMixQuestions(student, new_questions, selected_questions, topics)
        else:
            new_questions = getMixQuestions(student, new_questions, selected_questions, topics)
            new_questions = getMixQuestions(student, new_questions, selected_questions, topics)
            new_questions = getMixQuestions(student, new_questions, selected_questions, topics)

    # and an extra page of mixed questions!
    new_questions = getMixQuestions(student, new_questions, selected_questions, topics)

    # quick test to see if right topics

    actual_topics = [category, ]
    low_topics = QuestionDone.objects.filter(student=student).exclude(score=-1).values('question__category').annotate(
        average_score=Avg(F('score') / F('question__out_of'))).order_by('average_score')
    if low_topics.exists():
        low_score = min(low_topics, key=itemgetter('average_score'))['average_score']
        for i in low_topics:
            if i['average_score'] == low_score:
                actual_topics.append(i['question__category'])
    print (actual_topics)
    print (topics)
    print (len(selected_questions))

    return selected_questions


def getMixQuestions(student, new_questions, selected_questions, topics):
    current_year = student.classID.year
    topic = getRandomCategory(topics)
    topics.append(topic)
    new_difficulty = current_year

    # get questions done by student, on that topic in the last 30 days
    filter_questions = QuestionDone.objects.filter(student=student, question__category=topic,
                                                   date__range=[datetime.date.today() - datetime.timedelta(30), datetime.date.today()])
    # work out which is the most common difficulty of questions given
    frequent_difficulty = filter_questions.values('question__difficulty').annotate(d_c=Count('question__difficulty')).order_by('-d_c')
    if frequent_difficulty.exists():
        frequent_difficulty = int(frequent_difficulty.first()['question__difficulty'])
    else:
        frequent_difficulty = current_year

    # see what the students average is on that difficulty
    filter_questions = filter_questions.filter(question__difficulty=frequent_difficulty)
    difficulty_average = filter_questions.values('question__difficulty').annotate(
        average_score=Avg(F('score') / F('question__out_of')))

    # see if it's empty or not and
    if difficulty_average.exists():
        difficulty_average_score = difficulty_average[0]['average_score']
        # if average is greater than 0.85 and not already on highest difficulty
        if difficulty_average_score > 0.85 and frequent_difficulty != max(Question.DIFFICULTIES, key=itemgetter(1))[0]:
            frequent_difficulty += 1
        # if average is less than 0.4 and not already on lowest difficulty
        elif difficulty_average_score < 0.4 and frequent_difficulty != min(Question.DIFFICULTIES, key=itemgetter(1))[0]:
            frequent_difficulty -= 1
        # otherwise frequent_difficulty stays the same

    marks = 0
    max_marks = 20
    count = 0

    while marks < max_marks:

        return_value = selectRandomQuestion(difficulty=frequent_difficulty, new_questions=new_questions,
                                            selected_questions=selected_questions, marks=marks, topic=topic)
        marks = return_value['marks']
        new_questions = return_value['new_questions']
        count += 1
        # ensure you don't get infinite while loop
        if count > max_marks:
            break

    return new_questions


# get questions to the corresponding weakness
def getGroupAndStudentQuestions(year_group, new_questions, selected_questions, topic, selected_topic):
    # if the topic has been covered, choose standard questions, else choose easier questions
    if Question.CATEGORIES.index((topic, topic)) > Question.CATEGORIES.index((selected_topic, selected_topic)):
        year_group -= 1

    marks = 0
    max_marks = 20
    count = 0

    while marks < max_marks:
        # pick random question of the difficulty, remove from overall questions, add to selected questions
        return_value = selectRandomQuestion(difficulty=year_group, new_questions=new_questions,
                             selected_questions=selected_questions, marks=marks, topic=topic)
        marks = return_value['marks']
        new_questions = return_value['new_questions']
        count += 1
        # ensure you don't get infinite while loop
        if count > max_marks:
            break

    return new_questions


def getCategoryQuestions(year_group, new_questions, selected_questions, topic):
    # questions from chosen category, mixture of easy, medium and hard
    marks = 0
    if year_group == 4:
        max_marks = 20
    else:
        max_marks = 40

    count = 0
    # get enough marks worth
    while marks < max_marks:
        # fifth of the questions are easy
        if marks / max_marks < 0.2:
            # pick random question of easy difficulty, remove from overall questions, add to selected questions
            return_value = selectRandomQuestion(difficulty=year_group-1, new_questions=new_questions,
                                                selected_questions=selected_questions, marks=marks, topic=topic)
        elif 0.8 <= marks / max_marks <= 1:
            return_value = selectRandomQuestion(difficulty=year_group+1, new_questions=new_questions,
                                                selected_questions=selected_questions, marks=marks, topic=topic)
        else:
            return_value = selectRandomQuestion(difficulty=year_group, new_questions=new_questions,
                                                selected_questions=selected_questions, marks=marks, topic=topic)

        # if no question is found...
        if marks == return_value['marks']:
            return_value = selectRandomQuestion(difficulty=year_group, new_questions=new_questions,
                                                selected_questions=selected_questions, marks=marks, topic=topic)

        marks = return_value['marks']
        new_questions = return_value['new_questions']
        count += 1
        # ensure you don't get infinite while loop
        if count > max_marks:
            break

    print('total marks for category: ' + str(marks))
    print('topic : ' + str(topic))
    return new_questions


# pick random question of some difficulty, remove from overall questions, add to selected questions
def selectRandomQuestion(difficulty, new_questions, selected_questions, marks, topic):
    question = new_questions.filter(difficulty=difficulty, category=topic).order_by('?')
    if question.exists():
        question = question.first()
        selected_questions.append(question)
        selected_questions_ids = [q.id for q in selected_questions]
        # TODO fix this :/
        marks += question.out_of
        new_questions = new_questions.exclude(id__in=selected_questions_ids)
    return {'marks': marks, 'new_questions': new_questions}


# return weaknesses of the queryset of questions
def getWeaknesses(questions, topics):
    student_weaknesses = questions.filter(date__range=[datetime.date.today() - datetime.timedelta(30),
                                                                datetime.date.today()])
    student_weaknesses = student_weaknesses.exclude(score=-1)
    student_weaknesses = student_weaknesses.values('question__category').annotate(
        average_score=Avg(F('score') / F('question__out_of')))
    student_weaknesses = student_weaknesses.order_by('average_score')
    student_weaknesses = student_weaknesses.filter(average_score__lt=0.85)
    student_weaknesses = student_weaknesses.exclude(question__category__in=topics)

    if student_weaknesses.exists():
        rand = random.randrange(0, len(student_weaknesses))
        return student_weaknesses[rand]['question__category']


# return a random category which has not already been selected
def getRandomCategory(topics):
    topic = random.choice(Question.CATEGORIES)[0]
    while topic in topics:
        topic = random.choice(Question.CATEGORIES)[0]

    return topic


# mark these questions as '-1'
def addQuestionsDone(questions, student):
    for question in questions:
        questionDone = QuestionDone(student=student, question=question, score=-1)
        questionDone.save()


def createAttendanceForms(students):
    # see if attendance for last week has been created.
    try:
        student_dates = Attendance.objects.filter(date=getLastWeek(students[0]), student__classID=students[0].classID)
    # if not then create forms to fill in by the tutor
    except Attendance.DoesNotExist:
        new_forms = []
        for student in students:
            stud = Attendance(student=student, date=getLastWeek(student), has_attended=False)
            stud.save()

    attendanceFormSet = modelformset_factory(Attendance, fields=('has_attended', 'student', 'date',), extra=0)
    formset = attendanceFormSet(queryset=Attendance.objects.filter(student__classID=students[0].classID,
                                                                   date=getLastWeek(students[0])))
    return formset


# get date of last Saturday/Sunday (or today if today is Saturday/Sunday)
def getLastWeek(student):

    student_class = Class.objects.filter(student=student.id)
    if student_class[0].get_time_display()[:3] == 'Sun':
        day = 6
    elif student_class[0].get_time_display()[:3] == 'Sat':
        day = 5
    else:
        day = 5

    d = datetime.date.today()
    while d.weekday() != day:
        d -= datetime.timedelta(1)
    return d


# get date of next saturday/sunday (unless today is Saturday/Sunday)
def getNextWeek(student):

    student_class = Class.objects.filter(student=student.id)
    if student_class[0].get_time_display()[:3] == 'Sun':
        day = 6
    elif student_class[0].get_time_display()[:3] == 'Sat':
        day = 5
    else:
        day = 5

    d = datetime.date.today()
    while d.weekday() != day:
        d += datetime.timedelta(1)
    return d

