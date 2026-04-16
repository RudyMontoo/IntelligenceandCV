import tkinter as tk

root = tk.Tk()
root.title("Tkinter Demo")
root.geometry("300x200")

label = tk.Label(root, text="Hello, Tkinter!")
label2 = tk.Label(root, text="My name is Rudra!")
label.pack()
label2.pack()

def add():
    a=10
    b=20
    print(a+b)
button=tk.Button(root, text="Click Me", command=add)
button.pack()
root.mainloop()