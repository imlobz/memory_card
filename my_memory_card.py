from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QRadioButton, QPushButton, QLabel, QButtonGroup)
from random import shuffle, randint

class Question():
    def __init__(self, quest, right_answer, wrong1, wrong2, wrong3):
        self.quest = quest
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

question_list = []
question_list.append(Question('Государственный язык Бразилии', 'Португальский', 'Бразильский', 'Испанский', 'Итальянский'))
question_list.append(Question('Какого цвета нет на флаге России?', 'Зеленого', 'Красного', 'Белого', 'Синего'))
question_list.append(Question('Какая страна имеет самую большую территорию?', 'Россия', 'Бразилия', 'Португалия', 'США'))
question_list.append(Question('Национальная хижина якутов', 'Ураса', 'Юрта', 'Иглу', 'Хата'))
question_list.append(Question('Какой национальности не существует?', 'Энцы', 'Смурфы', 'Чулымциы', 'Алеуты'))

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Memory Card')

main_win.q_amount = 0
main_win.a_amount = 0

def show_result():
    buttons.hide()
    answer_group.show()
    answer.setText('Следующий вопрос')

def show_question():
    buttons.show()
    answer_group.hide()
    answer.setText('Ответить')
    buttons_group.setExclusive(False) # сняли ограничения, чтобы можно было сбросить выбор радиокнопки
    button1.setChecked(False)
    button2.setChecked(False)
    button3.setChecked(False)
    button4.setChecked(False)
    buttons_group.setExclusive(True) # вернули ограничения, теперь только одна радиокнопка может быть выбрана

def start_test():
    if answer.text() == 'Ответить':
        show_result()
    else:
        show_question()

def ask(q):
    shuffle(answers)
    answers[0].setText(q.right_answer)
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    question.setText(q.quest)
    correct.setText(q.right_answer)
    show_question()

def show_correct(res):
    result.setText(res)
    start_test()

def print_stats():
    return f'-Всего вопросов: {main_win.q_amount}\n-Правильных ответов: {main_win.a_amount}\nРейтинг: {main_win.a_amount / main_win.q_amount * 100}%'

def check_answer():
    main_win.q_amount += 1
    if answers[0].isChecked():
        show_correct('Правильно! <3')
        main_win.a_amount += 1
        print('\n\n\nСтатистика')
        print(print_stats())
    else:
        show_correct('Неверно! :(')
        print('\n\n\nСтатистика')
        print(print_stats())

def next_question():
    if len(main_win.was) == len(question_list):
        final_stats()
        return
    print('\n\n\nСтатистика')
    print('-Всего вопросов:', main_win.q_amount)
    print('-Правильных ответов:', main_win.a_amount)
    print('Рейтинг:', 'loading...')
    while True:
        main_win.cur_question = randint(0, len(question_list) - 1)
        if main_win.cur_question not in main_win.was:
            break
    main_win.was.append(main_win.cur_question)
    q = question_list[main_win.cur_question]
    ask(q)
    

def restart():
    main_win.q_amount = 0
    main_win.a_amount = 0
    main_win.was = []
    buttons.show()
    answer_group.hide()
    answer.setText('Ответить')
    next_question()
    

def click_OK():
    if answer.text() == 'Ответить':
        check_answer()
    elif answer.text() == 'Следующий вопрос':
        next_question()
    else:
        restart()
        

def final_stats():
    question.setText('Вы ответили на все вопросы!')
    result.setText('Статистика:')
    correct.setText(print_stats())
    answer.setText('Начать заново')




question = QLabel('Какой национальности не существует?')
answer =  QPushButton('Ответить')
buttons = QGroupBox('Варианты ответов')
button1 = QRadioButton('Энцы')
button2 = QRadioButton('Смурфы')
button3 = QRadioButton('Чулымцы')
button4 = QRadioButton('Алеуты')
buttons_group = QButtonGroup()
buttons_group.addButton(button1)
buttons_group.addButton(button2)
buttons_group.addButton(button3)
buttons_group.addButton(button4)
answers = [button1, button2, button3, button4]

answer_group = QGroupBox('Результат теста')
result = QLabel('Правильно/Неправильно')
correct = QLabel('Правильный ответ')
answer_group.hide()

layout_res = QVBoxLayout()
layout_res.addWidget(result, alignment = (Qt.AlignLeft | Qt.AlignTop), stretch = 2)
layout_res.addWidget(correct, alignment = Qt.AlignHCenter, stretch = 2)
answer_group.setLayout(layout_res)

layout1 = QHBoxLayout()
layout2 = QVBoxLayout()
layout3 = QVBoxLayout()

layout2.addWidget(button1)
layout2.addWidget(button2)
layout3.addWidget(button3)  
layout3.addWidget(button4)

layout1.addLayout(layout2)
layout1.addLayout(layout3)

buttons.setLayout(layout1)
line1 = QHBoxLayout()
line2 = QHBoxLayout()
line3 = QHBoxLayout()

line1.addWidget(question, alignment = (Qt.AlignHCenter | Qt.AlignVCenter))
line2.addWidget(buttons)
line2.addWidget(answer_group)
line3.addWidget(answer, stretch = 2)

layout_card = QVBoxLayout()
layout_card.addLayout(line1, stretch = 2)
layout_card.addLayout(line2, stretch = 8)
layout_card.addLayout(line3, stretch = 1)
layout_card.setSpacing(5)

main_win.was = []
main_win.cur_question = -1
answer.clicked.connect(click_OK)

main_win.setLayout(layout_card)
main_win.show()
app.exec_()