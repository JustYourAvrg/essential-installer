import customtkinter as ctk


class Message:
    def showmsg(title: str, message: str):
        msg_root = ctk.CTk()
        msg_root.title(title)
        msg_root.geometry("200x200")
        msg_root.resizable(0, 0)

        msg_root.grid_rowconfigure(0, weight=1)
        msg_root.grid_columnconfigure(0, weight=1)
        msg_root.grid_propagate(0)

        msg = ctk.CTkLabel(msg_root, text=message, wraplength=180)
        msg.grid(row=0, column=0)

        msg_root.mainloop()


    def askyesno(title: str, message: str):
        res = None

        yn = ctk.CTk()
        yn.title(title)
        yn.geometry("200x200")
        yn.resizable(0, 0)

        yn.grid_rowconfigure((0, 1), weight=1)
        yn.grid_columnconfigure((0, 1), weight=1)
        yn.grid_propagate(0)

        msg = ctk.CTkLabel(yn, text=message, wraplength=180)
        msg.grid(row=0, column=0, sticky='nsew', columnspan=2)

        def yes_action():
            nonlocal res
            yn.quit()
            yn.destroy()
            res = True

        def no_action():
            nonlocal res
            yn.quit()
            yn.destroy()
            res = False

        yes_btn = ctk.CTkButton(yn, text="YES", fg_color="#66FF66", text_color="#000000", font=ctk.CTkFont(weight='bold'), width=40, command=yes_action)
        yes_btn.grid(row=1, column=0)

        no_btn = ctk.CTkButton(yn, text="NO", fg_color="#FF6666", text_color="#000000", font=ctk.CTkFont(weight='bold'), width=40, command=no_action)
        no_btn.grid(row=1, column=1)

        yn.mainloop()
        return res


    def askinput(title: str, message: str):
        res = None

        input_frame = ctk.CTk()
        input_frame.title(title)
        input_frame.geometry("200x200")

        input_frame.grid_rowconfigure(0, weight=1)
        input_frame.grid_rowconfigure(1, weight=2)
        input_frame.grid_columnconfigure(0, weight=1)

        msg = ctk.CTkLabel(input_frame, text=message, wraplength=180)
        msg.grid(row=0, column=0)

        def set_return_value(event):
            nonlocal res
            res = user_input.get()
            input_frame.quit()
            input_frame.destroy()

        user_input = ctk.CTkEntry(input_frame)
        user_input.grid(row=1, column=0, padx=10, pady=10)
        user_input.bind("<Return>", command=set_return_value)

        input_frame.mainloop()
        return res
