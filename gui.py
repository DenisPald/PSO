import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import PSOAlgorithm

class PSOGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Метод Роя Частиц")

        tk.Label(self.root, text="Размер роя").grid(row=0, column=0)
        self.num_particles_entry = self._create_entry(default_value="30", row=0, column=1)

        tk.Label(self.root, text="Коэффициент текущей скорости:").grid(row=1, column=0)
        self.w_entry = self._create_entry(default_value="0.5", row=1, column=1)

        tk.Label(self.root, text="Коэффициент локального ускорения").grid(row=2, column=0)
        self.c1_entry = self._create_entry(default_value="1.5", row=2, column=1)

        tk.Label(self.root, text="Коэффициент глобального ускорения").grid(row=3, column=0)
        self.c2_entry = self._create_entry(default_value="1.5", row=3, column=1)

        tk.Label(self.root, text="Количество итераций:").grid(row=4, column=0)
        self.max_iter_entry = self._create_entry(default_value="50", row=4, column=1)

        # Добавляем флажок для включения/выключения модификации инерции
        self.inertia_decrease_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Использовать модификацию инерции", variable=self.inertia_decrease_var).grid(row=5, column=0, columnspan=2)

        tk.Button(self.root, text="Рассчитать", command=self.run_pso).grid(row=6, column=0, columnspan=2)

        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(row=7, column=0)

        tk.Label(self.root, text="Результаты:").grid(row=8, column=0, columnspan=2)
        self.result_text = tk.Text(self.root, height=5, width=40)
        self.result_text.grid(row=9, column=0, columnspan=2)

    def _create_entry(self, default_value, row, column):
        entry = tk.Entry(self.root)
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

        inertia_decrease = self.inertia_decrease_var.get()

        self.algorithm = PSOAlgorithm(
            num_particles=num_particles, 
            max_iter=max_iter, 
            inertia_decrease=inertia_decrease
        )
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
                f"Лучшее положение:\nx1={global_best_position[0]}\nx2={global_best_position[1]}\nЛучшее значение: {global_best_value}\n"
            )

    def update_plot(self):
        positions, global_best_position, _, current_iter = self.algorithm.get_swarm_data()
        self.ax.clear()
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.scatter(positions[:, 0], positions[:, 1])
        if global_best_position is not None:
            self.ax.scatter(global_best_position[0], global_best_position[1], color='red')
        self.ax.set_title(f'Итерация {current_iter}/{self.max_iter_entry.get()}')
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = PSOGUI(root)
    root.mainloop()
