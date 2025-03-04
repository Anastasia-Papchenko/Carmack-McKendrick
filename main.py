import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

def model(S0, I0, beta, gamma, days):
    N = S0 + I0  # Общее количество людей
    S = np.zeros(days)
    I = np.zeros(days)
    R = np.zeros(days)
    
    S[0] = S0
    I[0] = I0
    R[0] = 0

    for t in range(1, days):
        new_infected = beta * S[t-1] * I[t-1] / N  # Новые зараженные
        new_recovered = gamma * I[t-1]              # Новые выздоровевшие
        
        S[t] = S[t-1] - new_infected
        I[t] = I[t-1] + new_infected - new_recovered
        R[t] = R[t-1] + new_recovered

        # Убедимся, что значения неотрицательные
        if S[t] < 0: S[t] = 0
        if I[t] < 0: I[t] = 0
        if R[t] < 0: R[t] = 0
        
        # Сохранение замкнутости S + I + R = N
        R[t] = N - (S[t] + I[t])

    return S, I, R

def plot():
    S0 = float(entry_S.get())
    I0 = float(entry_I.get())
    beta = float(entry_beta.get())
    gamma = float(entry_gamma.get())
    days = int(entry_days.get())

    S, I, R = model(S0, I0, beta, gamma, days)

    ax.plot(S, label='(S) Здоровые', alpha=0.5)  # Добавление прозрачности
    ax.plot(I, label='(I) Зараженные', alpha=0.5)
    ax.plot(R, label='(R) Выздоровевшие', alpha=0.5)
    
    # График фазовой плоскости I(S)

    ax.set_title('Модель эпидемии Кармака-МакКендрика', fontsize='16')
    ax.set_xlabel('Дни', fontsize='16')
    ax.set_ylabel('Количество людей', fontsize='16')
    ax.legend()
    # ax.grid()
    
    
    ax_phase.plot(S, I, label='I(S)', alpha=0.5)
    
    ax_phase.set_title('Фазовая плоскость I(S)', fontsize='16')
    ax_phase.set_xlabel('Здоровые (S)', fontsize='16')
    ax_phase.set_ylabel('Зараженные (I)', fontsize='16')
    ax_phase.legend()
    # ax_phase.grid()
    

    canvas.draw()

def clear_plots():
    ax.clear()
    ax_phase.clear()
    ax.set_title('Модель эпидемии Кармака-МакКендрика', fontsize='16')
    ax_phase.set_title('Фазовая плоскость I(S)', fontsize='16')
    canvas.draw()


root = tk.Tk()
root.title("Модель эпидемии Кармака-МакКендрика")

# Создаем главный фрейм, который будет содержать все элементы
main_frame = ttk.Frame(root)
main_frame.pack(padx=10, pady=10)

# Создаем фрейм для полей ввода
input_frame = ttk.Frame(main_frame)
input_frame.pack(side=tk.LEFT, padx=10)

# Создаем фрейм для графиков
plot_frame = ttk.Frame(main_frame)
plot_frame.pack(side=tk.RIGHT)
font = ('Arial', 16)
font_entry = tkFont.Font(size=16)

ttk.Label(input_frame, text="Начальное число здоровых (S_0):", font=font).grid(column=0, row=0)
entry_S = ttk.Entry(input_frame, font=font_entry)
entry_S.grid(column=1, row=0)
entry_S.insert(0, "990")

ttk.Label(input_frame, text="Начальное число зараженных (I_0):", font=font).grid(column=0, row=1)
entry_I = ttk.Entry(input_frame, font=font_entry)
entry_I.grid(column=1, row=1)
entry_I.insert(0, "10")

ttk.Label(input_frame, text="Начальное число выздоровевших (R_0):", font=font).grid(column=0, row=2)
entry_R = ttk.Entry(input_frame, font=font_entry)
entry_R.grid(column=1, row=2)
entry_R.insert(0, "0")

ttk.Label(input_frame, text="Коэффициент передачи (\u03B2):", font=font).grid(column=0, row=3)
entry_beta = ttk.Entry(input_frame, font=font_entry)
entry_beta.grid(column=1, row=3)
entry_beta.insert(0, "0.3")

ttk.Label(input_frame, text="Коэффициент выздоровления (\u03B3):", font=font).grid(column=0, row=4)
entry_gamma = ttk.Entry(input_frame, font=font_entry)
entry_gamma.grid(column=1, row=4)
entry_gamma.insert(0, "0.1")

ttk.Label(input_frame, text="Количество дней:", font=font).grid(column=0, row=5)
entry_days = ttk.Entry(input_frame, font=font_entry)
entry_days.grid(column=1, row=5)
entry_days.insert(0, "160")

# Создаем область для графика
fig, (ax, ax_phase) = plt.subplots(2, 1, figsize=(15, 12))
plt.subplots_adjust(hspace=0.35)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(padx=10, pady=10)

style = ttk.Style()
font = tkFont.Font(family="Arial", size=16)
style.configure("TButton", font=font)


button_plot = ttk.Button(input_frame, text="Построить график", command=plot, width=20, style="TButton")
button_plot.grid(column=0, row=6, columnspan=2)

button_clear = ttk.Button(input_frame, text="Очистить графики", command=clear_plots, width=20, style="TButton")
button_clear.grid(column=0, row=7, columnspan=2)

root.mainloop()
