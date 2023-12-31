from tkinter import *
from tkinter import messagebox
from tkinter import font
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
    with pd.ExcelWriter('C:/Credit calculator/schedule.xlsx',
                        engine='xlsxwriter') as wb:  # создание и форматирование файла в excel
        df.to_excel(wb, sheet_name='List 1', index=False)
        sheet = wb.sheets['List 1']
        sheet.set_column(2, 4, 10)  # установить ширину столбцов C, D, E в 10
        sheet.set_column(5, 12)  # установить ширину столбца F в 12

        # Ниже выдаёт ошибку "XlsxWriter ha no attr 'add_format'". Искать решение дальше
        # format_cell = wb.book.add_format({'num_format': '# ##0.00'})  # задать формат ячеек как числовой
        # sheet.set_column('D:F', format_cell) # задать формат столбцов D, E, F как числовой

    os.startfile('C:/Credit calculator/schedule.xlsx')  # открытие файла с платежами в excel


# Создание окна программы
window = Tk()
window.title('Кредитный калькулятор')
window.geometry('400x300')

font1 = font.Font(family='Cricket', size=14, weight='normal')  # описание шрифта для надписей в окне

frame = Frame(window, padx=10, pady=10)
frame.pack(expand=True)

object_price_lb = Label(frame, text='Стоимость объекта', font=font1)
object_price_lb.grid(row=2, column=1, sticky=W)
object_price_tf = Entry(frame, width=10)
object_price_tf.grid(row=2, column=4, sticky=W)
rub_lb1 = Label(frame, text='руб.', font=font1)
rub_lb1.grid(row=2, column=5, sticky=W)

init_payment_lb = Label(frame, text='Первоначальный взнос', font=font1)
init_payment_lb.grid(row=3, column=1, sticky=W)
init_payment_tf = Entry(frame, width=10)
init_payment_tf.grid(row=3, column=4, sticky=W)
rub_lb2 = Label(frame, text='руб.', font=font1)
rub_lb2.grid(row=3, column=5, sticky=W)

term_lb = Label(frame, text='Срок', font=font1)
term_lb.grid(row=4, column=1, sticky=W)
term_tf = Entry(frame, width=4)
term_tf.grid(row=4, column=4, sticky=W)
term_lb2 = Label(frame, text='лет', font=font1)
term_lb2.grid(row=4, column=5, sticky=W)

percent_lb = Label(frame, text='Ставка', font=font1)
percent_lb.grid(row=5, column=1, sticky=W)
percent_tf = Entry(frame, width=4)
percent_tf.grid(row=5, column=4, sticky=W)
percent_lb2 = Label(frame, text='%', font=font1)
percent_lb2.grid(row=5, column=5, sticky=W)

calc_btn = Button(frame, text='Рассчитать график платежей')
calc_btn.bind('<Button-1>', calculate_credit)
calc_btn.grid(row=6, column=1, columnspan=2, pady=30)

window.mainloop()
