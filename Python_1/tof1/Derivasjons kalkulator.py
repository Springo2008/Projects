import sympy as sp
import tkinter as tk
from tkinter import messagebox

def calculate_derivative(func_str, a, delta_x):
    x = sp.symbols('x')
    func = sp.sympify(func_str)
    f = sp.lambdify(x, func, 'numpy')
    
    derivative = (f(a + delta_x) - f(a)) / delta_x
    return derivative

def on_calculate():
    func_str = entry_func.get()
    try:
        a = float(entry_point.get())
        delta_x = float(entry_delta_x.get())
        derivative = calculate_derivative(func_str, a, delta_x)
        result_label.config(text=f"f'(x) er: {derivative:.2f} når x={a}")
    except ValueError:
        messagebox.showerror("Input Error", "Vennligst skriv inn gyldige tall for punktet x og delta_x.")

# GUI
root = tk.Tk()
root.title("Derivat Kalkulator")

tk.Label(root, text="Skriv inn funksjonen f(x):").grid(row=0, column=0, padx=10, pady=10)
entry_func = tk.Entry(root)
entry_func.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Skriv inn punktet x:").grid(row=1, column=0, padx=10, pady=10)
entry_point = tk.Entry(root)
entry_point.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Skriv inn delta_x:").grid(row=2, column=0, padx=10, pady=10)
entry_delta_x = tk.Entry(root)
entry_delta_x.grid(row=2, column=1, padx=10, pady=10)


calculate_button = tk.Button(root, text="Beregn Derivat", command=on_calculate)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)


result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2, pady=10)



root.mainloop()