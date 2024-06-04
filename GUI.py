from tkinter import *
from tkinter import filedialog
import im

class MyWindow:
    def __init__(self):
        self.root = Tk()
        self.file_path = None
        self.text_input_window = None
        self.shape_input_window = None

        background_color = "#263238"
        button_color = "#FF5722"
        hover_color = "#FF7043"
        text_color = "#FFFFFF"

        self.lbl_title = Label(self.root, text="Image Design", font=("Helvetica", 20, "bold"), bg=background_color, fg=text_color)
        self.btn_open = Button(self.root, text="Choose Image", command=self.open_image, bg=button_color, fg=text_color, font=("Helvetica", 12, "bold"), height=2, bd=0)
        self.btn_cut = Button(self.root, text="Cut Image", command=self.cut_image, height=2, bg=button_color, fg=text_color, font=("Helvetica", 12, "bold"), bd=0)
        self.btn_add_text = Button(self.root, text="Add Text", command=self.add_text, bg=button_color, fg=text_color, font=("Helvetica", 12, "bold"), height=2, bd=0)
        self.btn_draw_shape = Button(self.root, text="Draw Shape", command=self.draw_shape, bg=button_color, fg=text_color, font=("Helvetica", 12, "bold"), height=2, bd=0)
        self.btn_effects = Button(self.root, text="Effects", command=self.apply_effects, bg=button_color, fg=text_color, font=("Helvetica", 12, "bold"), height=2, bd=0)
        self.btn_save = Button(self.root, text="Save Image", command=self.save_image, bg=button_color, fg=text_color, font=("Helvetica", 12, "bold"), height=2, bd=0)
        self.btn_exit = Button(self.root, text="Exit", command=self.exit_program, bg=button_color, fg=text_color, font=("Helvetica", 12, "bold"), height=2, bd=0)

        self.positions()

        self.root.title("Image Processing")
        self.root.geometry("450x500")  # Adjusted to fit the new button
        self.root.config(bg=background_color)
        self.image_processor = None
        self.root.mainloop()

    def positions(self):
        self.lbl_title.grid(row=0, column=0, columnspan=2, pady=(20, 10))
        self.btn_open.grid(row=1, column=0, pady=10, padx=(70, 10), sticky="ew")
        self.btn_cut.grid(row=1, column=1, pady=10, padx=(10, 70), sticky="ew")
        self.btn_add_text.grid(row=2, column=0, pady=10, padx=(70, 10), sticky="ew")
        self.btn_draw_shape.grid(row=2, column=1, pady=10, padx=(10, 70), sticky="ew")
        self.btn_effects.grid(row=3, column=0, columnspan=2, pady=10, padx=70, sticky="ew")  # New Effects button
        self.btn_save.grid(row=4, column=0, columnspan=2, pady=10, padx=70, sticky="ew")
        self.btn_exit.grid(row=5, column=0, columnspan=2, pady=10, padx=70, sticky="ew")

        for i in range(6):  # Updated range to include new row
            self.root.rowconfigure(i, weight=1)
        for i in range(2):
            self.root.columnconfigure(i, weight=1)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path = file_path
            self.image_processor = im.MyImage("image", file_path)

    def open_text_input_window(self):
        self.text_input_window = Toplevel(self.root)
        self.text_input_window.title("Add Text")
        self.text_input_window.geometry("300x150")
        self.text_input_window.configure(bg="#263238")

        label = Label(self.text_input_window, text="Enter Text:", fg="white", bg="#263238", font=("Helvetica", 12, "bold"))
        label.pack(pady=(20, 5))

        self.text_entry = Entry(self.text_input_window, font=("Helvetica", 12))
        self.text_entry.pack(pady=5)

        confirm_button = Button(self.text_input_window, text="Add", command=self.confirm_text_input, bg="#FF5722", fg="white", font=("Helvetica", 12, "bold"))
        confirm_button.pack(pady=10, padx=20, ipadx=10, ipady=3)

    def confirm_text_input(self):
        text = self.text_entry.get()
        self.image_processor.add_text(text)
        self.text_input_window.destroy()

    def cut_image(self):
        if self.image_processor:
            self.image_processor.set_action("cut")

    def add_text(self):
        if self.file_path:
            self.open_text_input_window()

    def open_shape_input_window(self):
        self.shape_input_window = Toplevel(self.root)
        self.shape_input_window.title("Choose Shape")
        self.shape_input_window.geometry("300x300")
        self.shape_input_window.configure(bg="#263238")

        label = Label(self.shape_input_window, text="Select Shape:", fg="white", bg="#263238",
                      font=("Helvetica", 12, "bold"))
        label.pack(pady=(20, 5))

        shapes = ["Triangle", "Rectangle", "Circle"]
        self.shape_listbox = Listbox(self.shape_input_window, font=("Helvetica", 12), selectbackground="#FF5722",
                                     selectforeground="white", bg="#37474F", fg="white", bd=0, highlightthickness=0)
        for shape in shapes:
            self.shape_listbox.insert(END, "Draw " + shape)  # Adjusted here
        self.shape_listbox.pack(pady=5)

        confirm_button = Button(self.shape_input_window, text="Confirm", command=self.confirm_shape_selection,
                                bg="#FF5722", fg="white", font=("Helvetica", 12, "bold"))
        confirm_button.pack(pady=10, padx=20, ipadx=10, ipady=3)

    def confirm_shape_selection(self):
        selection = self.shape_listbox.curselection()
        if selection:
            shape = self.shape_listbox.get(selection[0])
            if shape == "Draw Triangle":
                self.image_processor.set_action("draw_triangle")
            elif shape == "Draw Rectangle":
                self.image_processor.set_action("draw_rectangle")
            elif shape == "Draw Circle":
                self.image_processor.set_action("draw_circle")
            self.shape_input_window.destroy()

    def draw_shape(self):
        if self.file_path:
            self.open_shape_input_window()

    def open_effects_window(self):
        self.effects_window = Toplevel(self.root)
        self.effects_window.title("Apply Effects")
        self.effects_window.geometry("300x300")
        self.effects_window.configure(bg="#263238")

        label = Label(self.effects_window, text="Select Effect:", fg="white", bg="#263238", font=("Helvetica", 12, "bold"))
        label.pack(pady=(20, 5))

        effects = ["Blur", "Contour", "Detail", "Sharpen"]
        self.effects_listbox = Listbox(self.effects_window, font=("Helvetica", 12), selectbackground="#FF5722",
                                       selectforeground="white", bg="#37474F", fg="white", bd=0, highlightthickness=0)
        for effect in effects:
            self.effects_listbox.insert(END, effect)
        self.effects_listbox.pack(pady=5)

        confirm_button = Button(self.effects_window, text="Apply", command=self.confirm_effect_selection,
                                bg="#FF5722", fg="white", font=("Helvetica", 12, "bold"))
        confirm_button.pack(pady=10, padx=20, ipadx=10, ipady=3)

    def confirm_effect_selection(self):
        selection = self.effects_listbox.curselection()
        if selection:
            effect = self.effects_listbox.get(selection[0])
            self.image_processor.apply_effect(effect)
            self.effects_window.destroy()

    def apply_effects(self):
        if self.file_path:
            self.open_effects_window()

    def save_image(self):
        self.image_processor.save_image()

    def exit_program(self):
        self.root.quit()

if __name__ == "__main__":
    window = MyWindow()
