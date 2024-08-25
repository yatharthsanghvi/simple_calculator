import tkinter as tk
from tkinter import font as tkfont

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Modern Calculator")
        self.master.geometry("500x600")  # Increased size
        self.master.resizable(False, False)

        self.create_gradient_background()

        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.create_widgets()

        # Bind keyboard events
        self.master.bind('<Key>', self.key_press)

    def create_gradient_background(self):
        gradient_frame = tk.Canvas(self.master, width=500, height=600)  # Match the window size
        gradient_frame.pack(fill="both", expand=True)  # Fill the window completely
        gradient_frame.create_rectangle(0, 0, 500, 600, fill="#1a1a2e", outline="")
        for i in range(600):
            color = self.interpolate("#1a1a2e", "#16213e", i/600)
            gradient_frame.create_line(0, i, 500, i, fill=color, width=2)

        self.content_frame = tk.Frame(self.master, bg="")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")

    def interpolate(self, color1, color2, t):
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:], 16)
        r = int(r1 * (1-t) + r2 * t)
        g = int(g1 * (1-t) + g2 * t)
        b = int(b1 * (1-t) + b2 * t)
        return f'#{r:02x}{g:02x}{b:02x}'

    def create_widgets(self):
        custom_font = tkfont.Font(family="Helvetica", size=18, weight="bold")

        result_entry = tk.Entry(self.content_frame, textvariable=self.result_var, font=("Helvetica", 32, "bold"), 
                                justify="right", bd=0, bg="#0f3460", fg="#e94560", insertbackground="#e94560")
        result_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew", ipady=15)

        buttons = [
            'C', '(', ')', 'AC',
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'sqr', 'sqrt', '%', '1/x'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            cmd = lambda x=button: self.click(x)
            btn = tk.Button(self.content_frame, text=button, command=cmd, font=custom_font,
                            bd=0, bg="#e94560", fg="#ffffff", activebackground="#c73e54", activeforeground="#ffffff")
            btn.grid(row=row_val, column=col_val, padx=5, pady=5, sticky="nsew", ipadx=10, ipady=10)
            btn.config(relief=tk.RAISED, overrelief=tk.SUNKEN, borderwidth=0, highlightthickness=0)
            
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        for i in range(7):
            self.content_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.content_frame.grid_columnconfigure(i, weight=1)

    def click(self, key):
        self.process_key(key)

    def key_press(self, event):
        key = event.char
        if key in '0123456789.+-*/%()':
            self.process_key(key)
        elif event.keysym == 'Return':
            self.process_key('=')
        elif event.keysym == 'BackSpace':
            current = self.result_var.get()
            self.result_var.set(current[:-1] if len(current) > 1 else '0')
        elif event.keysym == 'Escape':
            self.process_key('AC')

    def process_key(self, key):
        if key == '=':
            try:
                result = eval(self.result_var.get())
                self.result_var.set(result)
            except:
                self.result_var.set("Error")
        elif key in ['C', 'AC']:
            self.result_var.set("0")
        elif key == 'sqr':
            try:
                result = float(self.result_var.get()) ** 2
                self.result_var.set(result)
            except:
                self.result_var.set("Error")
        elif key == 'sqrt':
            try:
                result = float(self.result_var.get()) ** 0.5
                self.result_var.set(result)
            except:
                self.result_var.set("Error")
        elif key == '%':
            try:
                result = float(self.result_var.get()) / 100
                self.result_var.set(result)
            except:
                self.result_var.set("Error")
        elif key == '1/x':
            try:
                result = 1 / float(self.result_var.get())
                self.result_var.set(result)
            except:
                self.result_var.set("Error")
        else:
            current = self.result_var.get()
            if current == "0" or current == "Error":
                self.result_var.set(key)
            else:
                self.result_var.set(current + key)

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()