import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- LOGIKA METODE NUMERIK ---
def f(func_str, t):
    """Mengevaluasi fungsi kecepatan v(t). Mengubah variabel 't' dalam string."""
    try:
        # Mengizinkan fungsi matematika umum
        allowed_names = {k: v for k, v in np.__dict__.items() if not k.startswith("__")}
        # Kita mapping agar user bisa pakai huruf 'x' atau 't'
        # Tapi secara logika internal kita pakai t
        context = {"__builtins__": {}, "t": t, "x": t} 
        return eval(func_str, context, allowed_names)
    except Exception as e:
        return None

def metode_trapezoid(func_str, a, b, n):
    h = (b - a) / n
    t = np.linspace(a, b, n+1)
    v = f(func_str, t)
    if v is None: return None
    result = (h/2) * (v[0] + 2 * np.sum(v[1:-1]) + v[-1])
    return result

def metode_simpson(func_str, a, b, n):
    if n % 2 != 0: n += 1 
    h = (b - a) / n
    t = np.linspace(a, b, n+1)
    v = f(func_str, t)
    if v is None: return None
    result = (h/3) * (v[0] + 4 * np.sum(v[1:-1:2]) + 2 * np.sum(v[2:-2:2]) + v[-1])
    return result, n

# --- GUI ---
def hitung_dan_plot():
    try:
        func_str = entry_fungsi.get()
        a = float(entry_a.get()) # Waktu awal
        b = float(entry_b.get()) # Waktu akhir
        n = int(entry_n.get())

        hasil_trap = metode_trapezoid(func_str, a, b, n)
        hasil_simp, n_used = metode_simpson(func_str, a, b, n)

        if hasil_trap is None:
            messagebox.showerror("Error", "Sintaks fungsi salah. Contoh: 3*t**2 + 5")
            return

        # Update Label Hasil
        lbl_hasil_trap.config(text=f"Jarak (Trapezoid): {hasil_trap:.4f} meter")
        lbl_hasil_simp.config(text=f"Jarak (Simpson 1/3, n={n_used}): {hasil_simp:.4f} meter")

        # Plotting
        ax.clear()
        
        # Plot Kurva Kecepatan
        t_plot = np.linspace(a, b, 200)
        v_plot = f(func_str, t_plot)
        ax.plot(t_plot, v_plot, 'b-', linewidth=2, label=f'v(t) = {func_str}')
        
        # Visualisasi Area (Jarak)
        t_area = np.linspace(a, b, n+1)
        v_area = f(func_str, t_area)
        ax.fill_between(t_area, v_area, color='orange', alpha=0.3, label='Jarak Tempuh')
        ax.scatter(t_area, v_area, color='red', s=15, zorder=5) 

        ax.set_title("Grafik Kecepatan vs Waktu")
        ax.set_xlabel("Waktu (detik)")
        ax.set_ylabel("Kecepatan (m/s)")
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        canvas.draw()

    except ValueError:
        messagebox.showerror("Error", "Pastikan input angka valid!")

# Setup Window Utama
root = tk.Tk()
root.title("Estimasi Jarak Tempuh - Integrasi Numerik")
root.geometry("950x650")

frame_input = ttk.Frame(root, padding="15")
frame_input.pack(side=tk.LEFT, fill=tk.Y)

# Input Widgets
ttk.Label(frame_input, text="JUDUL TUGAS:\nEstimasi Jarak Tempuh Objek", font=("Arial", 12, "bold")).pack(pady=(0,20))

ttk.Label(frame_input, text="Fungsi Kecepatan v(t):\n(Contoh: 3*t**2 + 2*t)", font=("Arial", 10)).pack(pady=5, anchor='w')
entry_fungsi = ttk.Entry(frame_input, width=30, font=("Consolas", 10))
entry_fungsi.insert(0, "3*t**2 + 2*t") # Contoh fungsi v(t)
entry_fungsi.pack(pady=5)

ttk.Label(frame_input, text="Waktu Awal (detik):").pack(pady=5, anchor='w')
entry_a = ttk.Entry(frame_input)
entry_a.insert(0, "0")
entry_a.pack(pady=5)

ttk.Label(frame_input, text="Waktu Akhir (detik):").pack(pady=5, anchor='w')
entry_b = ttk.Entry(frame_input)
entry_b.insert(0, "10")
entry_b.pack(pady=5)

ttk.Label(frame_input, text="Jumlah Segmen (n):").pack(pady=5, anchor='w')
entry_n = ttk.Entry(frame_input)
entry_n.insert(0, "20")
entry_n.pack(pady=5)

btn_hitung = ttk.Button(frame_input, text="HITUNG JARAK", command=hitung_dan_plot)
btn_hitung.pack(pady=20, fill=tk.X)

# Output Text
lbl_hasil_trap = ttk.Label(frame_input, text="Jarak (Trapezoid): -", font=("Arial", 10, "bold"), foreground="blue")
lbl_hasil_trap.pack(pady=10, anchor='w')

lbl_hasil_simp = ttk.Label(frame_input, text="Jarak (Simpson 1/3): -", font=("Arial", 10, "bold"), foreground="green")
lbl_hasil_simp.pack(pady=5, anchor='w')

# Info Kaki
ttk.Label(frame_input, text="*User bisa pakai variabel 't' atau 'x'", font=("Arial", 8, "italic")).pack(side=tk.BOTTOM, pady=10)

# Frame Grafik
frame_plot = ttk.Frame(root)
frame_plot.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root.mainloop()