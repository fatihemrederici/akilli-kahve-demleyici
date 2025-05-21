import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from fuzzy_logic import simulate

def calculate():
    try:
        inputs = {
            "coffee_type": coffee_type_cb.current(),
            "intensity": int(intensity_slider.get()),
            "room_temp": int(room_temp_slider.get()),
            "water_temp": int(water_temp_slider.get()),
            "coffee_amount": int(coffee_amount_slider.get())
        }

        brew_time, flow_rate = simulate(inputs)

        result_label.config(
            text=f"Demleme Süresi: {brew_time:.2f} sn\nAkış Hızı: {flow_rate:.2f} ml/s",
            fg="white", background="red"
        )
    except Exception as e:
        messagebox.showerror("Hata", str(e))

app = tk.Tk()
app.title("Akıllı Kahve Demleme Uygulaması")
app.geometry("400x450")

# Pencere saydamlığı %90
app.attributes('-alpha', 0.9)

# Arkaplan resmi yükleme
image = Image.open("coffee.jpg")
image = image.resize((400, 450), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image)

background_label = tk.Label(app, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Widget'lar - Arka plan şeffaf olmadığından bg'yi ayarlamadım
tk.Label(app, text="Kahve Türü:", fg="green").pack()
coffee_type_cb = ttk.Combobox(app, values=["Espresso", "Filtre Kahve", "Türk Kahvesi"])
coffee_type_cb.current(0)
coffee_type_cb.pack(pady=5)

tk.Label(app, text="Yoğunluk (0-10):", fg="green").pack()
intensity_slider = tk.Scale(app, from_=0, to=10, orient=tk.HORIZONTAL, fg="red")
intensity_slider.set(5)
intensity_slider.pack(pady=5)

tk.Label(app, text="Oda Sıcaklığı (°C):", fg="green").pack()
room_temp_slider = tk.Scale(app, from_=10, to=35, orient=tk.HORIZONTAL, fg="red")
room_temp_slider.set(22)
room_temp_slider.pack(pady=5)

tk.Label(app, text="Su Sıcaklığı (°C):", fg="green").pack()
water_temp_slider = tk.Scale(app, from_=60, to=100, orient=tk.HORIZONTAL, fg="red")
water_temp_slider.set(85)
water_temp_slider.pack(pady=5)

tk.Label(app, text="Kahve Miktarı (g):", fg="green").pack()
coffee_amount_slider = tk.Scale(app, from_=5, to=30, orient=tk.HORIZONTAL, fg="red")
coffee_amount_slider.set(15)
coffee_amount_slider.pack(pady=5)

tk.Button(app, text="Demlemeyi Hesapla", command=calculate, fg="red").pack(pady=10)

result_label = tk.Label(app, font=("Arial", 12), fg="blue")
result_label.pack(pady=10)

app.mainloop()
