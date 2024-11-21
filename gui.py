import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import PSOAlgorithm

class PSOGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Метод роя частиц")

        params_frame = tk.LabelFrame(self.root, text="Параметры", padx=10, pady=10)
        params_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(params_frame, text="Функция:").grid(row=0, column=0, sticky="w")
        self.function_entry = tk.Entry(params_frame, width=30)
        self.function_entry.grid(row=0, column=1)
        self.function_entry.insert(0, "8*x1**2 + 4*x1*x2 + 5*x2**2")
        self.function_entry.configure(state='readonly')

        tk.Label(params_frame, text="Коэфф. текущей скорости:").grid(row=1, column=0, sticky="w")
        self.w_entry = self._create_entry(params_frame, "0.5", row=1, column=1)

        tk.Label(params_frame, text="Коэфф. собственного лучшего значения:").grid(row=2, column=0, sticky="w")
        self.c1_entry = self._create_entry(params_frame, "1.5", row=2, column=1)

        tk.Label(params_frame, text="Коэфф. глобального лучшего значения:").grid(row=3, column=0, sticky="w")
        self.c2_entry = self._create_entry(params_frame, "1.5", row=3, column=1)

        tk.Label(params_frame, text="Количество частиц:").grid(row=4, column=0, sticky="w")
        self.num_particles_entry = self._create_entry(params_frame, "30", row=4, column=1)

        control_frame = tk.LabelFrame(self.root, text="Управление", padx=10, pady=10)
        control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        tk.Button(control_frame, text="Создать частицы", command=self.create_particles).grid(row=0, column=0, pady=5)
        tk.Label(control_frame, text="Количество итераций:").grid(row=1, column=0, sticky="w")
        self.max_iter_entry = self._create_entry(control_frame, "50", row=1, column=1)

        tk.Button(control_frame, text="Рассчитать", command=self.run_pso).grid(row=2, column=0, pady=5)

        self.iterations_label = tk.Label(control_frame, text="Количество выполненных итераций: 0")
        self.iterations_label.grid(row=3, column=0, columnspan=2, sticky="w")

        self.inertia_decrease_var = tk.BooleanVar()
        tk.Checkbutton(control_frame, text="Использовать модификацию инерции", variable=self.inertia_decrease_var).grid(row=4, column=0, columnspan=2)

        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        results_frame = tk.LabelFrame(self.root, text="Результаты", padx=10, pady=10)
        results_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.result_text = tk.Text(results_frame, height=5, width=60)
        self.result_text.pack()

    def _create_entry(self, parent, default_value, row, column):
        entry = tk.Entry(parent)
        entry.grid(row=row, column=column)
        entry.insert(0, default_value)
        return entry

    def create_particles(self):
        try:
            num_particles = int(self.num_particles_entry.get())
            max_iter = int(self.max_iter_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные значения!")
            return

        # Получаем значение флажка для изменения инерции
        inertia_decrease = self.inertia_decrease_var.get()

        # Создаем экземпляр алгоритма PSO с выбранным параметром
        self.algorithm = PSOAlgorithm(num_particles=num_particles, max_iter=max_iter, inertia_decrease=inertia_decrease)
        self.algorithm.initialize_swarm()
        self.update_plot()

    def run_pso(self):
        self.create_particles()
        self.animate_pso()

    def animate_pso(self):
        if not self.algorithm.is_finished():
            w = float(self.w_entry.get())
            c1 = float(self.c1_entry.get())
            c2 = float(self.c2_entry.get())
            self.algorithm.step(w, c1, c2)
            self.update_plot()
            self.root.after(50, self.animate_pso)
        else:
            positions, global_best_position, global_best_value, _ = self.algorithm.get_swarm_data()
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(
                tk.END,
                f"Лучшее решение:\nX[0] = {global_best_position[0]}\nX[1] = {global_best_position[1]}\n"
                f"Значение функции: {global_best_value}"
            )

    def update_plot(self):
        positions, global_best_position, _, current_iter = self.algorithm.get_swarm_data()
        self.ax.clear()
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.scatter(positions[:, 0], positions[:, 1], label="Частицы")
        if global_best_position is not None:
            self.ax.scatter(global_best_position[0], global_best_position[1], color='red', label="Лучшее решение")
        self.ax.legend()
        self.ax.set_title(f'Итерация {current_iter}/{self.max_iter_entry.get()}')
        self.iterations_label.config(text=f"Количество выполненных итераций: {current_iter}")
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = PSOGUI(root)
    root.mainloop()
