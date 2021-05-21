#!/usr/bin/env python3
# -*- config: utf-8 -*-

# Вариант 13. Использовать словарь, содержащий следующие ключи: фамилия, имя; номер телефона;
# дата рождения. Написать программу, выполняющую следующие
# действия: ввод с клавиатуры данных в список, состоящий из словарей заданной структуры;
# записи должны быть упорядочены по трем первым цифрам номера телефона; вывод на
# экран информации о человеке, чья фамилия введена с клавиатуры; если такого нет, выдать
# на дисплей соответствующее сообщение.

# Выполнить индивидуальное задание 2 лабораторной работы 13, добавив возможность работы с
# исключениями и логгирование.

# Изучить возможности модуля logging. Добавить для предыдущего задания вывод в файлы лога
# даты и времени выполнения пользовательской команды с точностью до миллисекунды.


from tkinter import *
from tkinter import messagebox as mb
import modul

def add_window():
    def add():
        surname = en1.get()
        name = en2.get()
        number = en3.get()
        date = en4.get()

        peoples.add(surname, name, number, date)

    add_w = Toplevel()
    add_w.title('Добавить')
    add_w.resizable(False, False)
    add_w.geometry('400x200')
    en1 = Entry(add_w)
    en2 = Entry(add_w)
    en3 = Entry(add_w)
    en4 = Entry(add_w)
    lb1 = Label(add_w, text="Фамилия")
    lb2 = Label(add_w, text="Имя")
    lb3 = Label(add_w, text="Номер телефона")
    lb4 = Label(add_w, text="Дата рождения")
    bt1 = Button(add_w, text="Добавить", command=add)

    lb1.grid(row=0, column=0)
    lb2.grid(row=1, column=0)
    lb3.grid(row=2, column=0)
    lb4.grid(row=3, column=0)
    en1.grid(row=0, column=1)
    en2.grid(row=1, column=1)
    en3.grid(row=2, column=1)
    en4.grid(row=3, column=1)
    bt1.grid(row=4, column=0, columnspan=2)


def load_window():
    def load_f():
        peoples.load(en4.get())
        load_w.destroy()

    load_w = Toplevel()
    load_w.title('Сохранение')
    load_w.resizable(False, False)
    load_w.geometry('225x100')
    lb5 = Label(load_w, text="Введите название файла")
    en5 = Entry(load_w)
    bt3 = Button(load_w, text="Загрузить", command=load_f)
    lb5.pack(padx=2, pady=2)
    en5.pack(padx=2, pady=2)
    bt3.pack(padx=2, pady=2)

def save_window():
    def save_f():
        peoples.save(en5.get())
        save_w.destroy()

    save_w = Toplevel()
    save_w.title('Сохранение')
    save_w.resizable(False, False)
    save_w.geometry('225x100')
    lb5 = Label(save_w, text="Введите название файла")
    en5 = Entry(save_w)
    bt3 = Button(save_w, text="Сохранить", command=save_f)
    lb5.pack(padx=2, pady=2)
    en5.pack(padx=2, pady=2)
    bt3.pack(padx=2, pady=2)


def help_window():
    help_w = Toplevel()
    help_w.title('Помощь')
    help_w.resizable(False, False)
    help_w['bg'] = 'white'
    img = PhotoImage(file='1.png')
    bt2 = Button(
        help_w,
        image=img,
        bg='white',
        borderwidth=0,
        activebackground='white',
        command=lambda: help_w.destroy()
    )
    bt2.image = img
    bt2.pack()


def select_window():
    def choice():
        try:
            choice_en = int(en5.get())
            res = peoples.select(choice_en)
            if res:
                for idx, people in enumerate(res, 1):
                    text.delete(0.0, END)
                    text.insert(0.0, '{:>4}: {}'.format(idx, people.surname))
            else:
                text.delete(0.0, END)
                text.insert(0.0, 'Нет людей с такой фамилией')
        except(ValueError, TypeError):
            mb.showinfo("Выбор фамилии",
                        "Введите фамилию!")

    sel_w = Toplevel()
    sel_w.title('Выбрать')
    sel_w.resizable(False, False)
    sel_w.geometry('225x100')
    lb5 = Label(sel_w, text="Введите фамилию")
    en5 = Entry(sel_w)
    bt3 = Button(sel_w, text="Подтвердить", command=choice)
    lb5.pack(padx=2, pady=2)
    en5.pack(padx=2, pady=2)
    bt3.pack(padx=2, pady=2)


def show():
    text.delete(0.0, END)
    text.insert(0.0, peoples)


if __name__ == '__main__':
    peoples = modul.Peoples()


    root = Tk()
    root.geometry('800x450')
    root.title('Главное окно')
    root.resizable(False, False)

    main_menu = Menu(root)
    root.config(menu=main_menu)

    file_menu = Menu(main_menu, tearoff=0)
    file_menu.add_command(label="Открыть", command=load_window)
    file_menu.add_command(label="Добавить", command=add_window)
    file_menu.add_command(label="Сохранить", command=save_window)

    main_menu.add_cascade(label="Файл", menu=file_menu)
    main_menu.add_command(label="Показать", command=show)
    main_menu.add_command(label="Выбрать", command=select_window)
    main_menu.add_command(label="Помощь", command=help_window)
    main_menu.add_command(label="Выход", command=lambda: root.destroy())

    text = Text(bg='white', width=97, height=100)
    text.pack(side=LEFT)
    scroll = Scrollbar(command=text.yview)
    scroll.pack(side=LEFT, fill=Y)
    text.config(yscrollcommand=scroll.set)

    root.mainloop()