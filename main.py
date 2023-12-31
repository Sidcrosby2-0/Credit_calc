from tkinter import *
from tkinter import messagebox
import pandas as pd
import os


def calculate_credit(percent):
    object_price = float(object_price_tf.get())
    init_payment = float(init_payment_tf.get())
    credit_sum = object_price - init_payment
    percent = float(percent_tf.get())
    term = int(term_tf.get())
    month_pct = percent / 12 / 100
    total_pct = (1 + month_pct) ** (term * 12)
    payment = round(credit_sum * month_pct * total_pct / (total_pct - 1), 2)
    messagebox.showinfo('РЕЗУЛЬТАТ', f'Ежемесячный платёж составляет {payment} руб.')
    month_pay = term * 12  # количество месяцев

    owe_pay_lst = []
    pct_pay_lst = []
    credit_sum_lst = []
    month_pay_lst = []
    payment_lst = []

    for i in range(1, month_pay + 1):
        month_pay_lst.append(i)
        payment_lst.append(payment)
        pct_pay = round(month_pct * credit_sum, 2)  # платёж по процентам
        pct_pay_lst.append(pct_pay)
        owe_pay = round(payment - pct_pay, )  # платёж по основному долгу
        owe_pay_lst.append(owe_pay)
        credit_sum = round(credit_sum - owe_pay, 2)
        if credit_sum < 0:
            credit_sum = 0
        credit_sum_lst.append(credit_sum)  # остаток долга

    dict = {'месяц': month_pay_lst, 'сумма платежа': payment_lst, 'платёж по основному долгу': owe_pay_lst,
            'платёж по процентам': pct_pay_lst, 'остаток долга': credit_sum_lst}

    df = pd.DataFrame(dict)  # создание датафрейма из словаря

    if not os.path.exists('C:/Credit calculator'):  # создаём папку, если её ещё не существует
        os.makedirs('C:/Credit calculator')
    df.to_excel('C:/Credit calculator/schedule.xlsx', sheet_name='List 1')  # запись файла с графиком платежей в excel
    os.startfile('C:/Credit calculator/schedule.xlsx')  # открытие файла с платежами в excel


window = Tk()
window.title('Кредитный калькулятор')
window.geometry('400x300')

frame = Frame(window, padx=10, pady=10)
frame.pack(expand=True)

object_price_lb = Label(frame, text='Стоимость объекта')
object_price_lb.grid(row=2, column=1)
object_price_tf = Entry(frame, width=10)
object_price_tf.grid(row=2, column=4)
rub_lb1 = Label(frame, text='руб.')
rub_lb1.grid(row=2, column=5)

init_payment_lb = Label(frame, text='Первоначальный взнос')
init_payment_lb.grid(row=3, column=1)
init_payment_tf = Entry(frame, width=10)
init_payment_tf.grid(row=3, column=4)
rub_lb2 = Label(frame, text='руб.')
rub_lb2.grid(row=3, column=5)

term_lb = Label(frame, text='Срок')
term_lb.grid(row=4, column=1)
term_tf = Entry(frame, width=4)
term_tf.grid(row=4, column=4)
term_lb2 = Label(frame, text='лет')
term_lb2.grid(row=4, column=5)

percent_lb = Label(frame, text='Ставка')
percent_lb.grid(row=5, column=1)
percent_tf = Entry(frame, width=4)
percent_tf.grid(row=5, column=4)
percent_lb2 = Label(frame, text='%')
percent_lb2.grid(row=5, column=5)

calc_btn = Button(frame, text='Рассчитать график\n платежей')
calc_btn.bind('<Button-1>', calculate_credit)
calc_btn.grid(row=7, column=3)

window.mainloop()
