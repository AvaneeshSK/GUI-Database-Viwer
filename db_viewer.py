# Database GUI Tkinter 
    # Practise


import tkinter as tk
import customtkinter as ctk
import os

import sqlite3
import sqlite_utils

from tkinter import messagebox

ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('blue')


# functions 
def view_dbs():
    contents = os.listdir(os.getcwd())
    dbs = []
    for each in contents:
        if '.db' in each:
            dbs.append(each)
    if len(dbs) != 0:
        view_dbs_btn.configure(state='disabled')
        root2 = ctk.CTk()
        root2.title('Existing Databases')
        height=20
        contents_box = ctk.CTkTextbox(root2, fg_color='black', height=height, width=400, font=('Comic Sans MS', 20))
        contents_box.pack(fill='both', expand=True)
        for each in dbs:
            contents_box.insert(tk.END, each + '\n' )
            contents_box.configure(height=height)
            height += 45
        content = contents_box.get('1.0', tk.END)
        content = content.strip()
        contents_box.delete('1.0', tk.END)
        contents_box.insert(tk.END, content)
        root2.protocol('WM_DELETE_WINDOW', lambda:onclose(root2, view_dbs_btn))
        root2.mainloop()
    else:
        messagebox.showinfo('No Databased Found')

def onclose(win, btn):
    win.destroy()
    btn.configure(state='normal')


def view_tables(result, btn):
    btn.configure(state='disabled')
    if len(result) == 0:
        messagebox.showinfo('Empty')
    else:
        height=20
        root3 = ctk.CTk()
        root3.title('Existing Tables')
        tables_textbox = ctk.CTkTextbox(root3, font=('Comic Sans MS', 20), height=height, width=400, fg_color='black')
        tables_textbox.pack(fill='both', expand=True)
        for each in result:
            tables_textbox.insert(tk.END, text=f'{each}\n')
            tables_textbox.configure(height=height)
            height += 55
        content = tables_textbox.get('1.0', tk.END).strip()
        tables_textbox.delete(1.0, tk.END)
        tables_textbox.insert(tk.END, content)
        root3.protocol('WM_DELETE_WINDOW', lambda:onclose(root3, btn))
        root3.mainloop()


def show_values(btn, box, cur, result):
    if box.get('1.0', tk.END).strip() in result:
        btn.configure(state='disabled')
        root4 = ctk.CTk()
        height=20
        show_vals_textbox = ctk.CTkTextbox(root4, fg_color='black', font=('Comic Sans MS', 20), height=height, width=400)
        show_vals_textbox.pack(fill='both', expand=True)
        table = box.get('1.0', tk.END).strip()
        root4.title(table)
        result = cur.execute(f'SELECT * FROM {table}').fetchall()
        get_tab_cols = cur.execute(f'PRAGMA table_info({table})').fetchall()
        show_vals_textbox.insert(tk.END, 'Table Columns:\n')
        show_vals_textbox.insert(tk.END,f'{get_tab_cols}\n\n')
        show_vals_textbox.insert(tk.END, 'Table Values:\n')
        for row in result:
            show_vals_textbox.insert(tk.END, f'{row }\n')
            show_vals_textbox.configure(height=height)
            height += 35
        content = show_vals_textbox.get('1.0', tk.END).strip()
        show_vals_textbox.delete('1.0', tk.END)
        show_vals_textbox.insert(tk.END, content)
        root4.protocol('WM_DELETE_WINDOW', lambda:onclose(root4, btn))
        box.delete('1.0', tk.END)
        root4.mainloop()
    else:
        messagebox.showerror('', 'Table Not Present')


def connect():
    contents = os.listdir(os.getcwd())
    x = dbs_textbox.get('1.0', tk.END).strip().lower()
    if '.db' not in x:
        x += '.db'
    if x in contents:
        # connect db
        messagebox.showinfo('', 'Connected Successfully')
        dbs_textbox.delete('1.0', tk.END)
        con = sqlite3.connect(x)
        cur = con.cursor()
        label = ctk.CTkLabel(root, text='connected')
        label.place(x=235, y=250)
        # show tables
        result = sqlite_utils.Database(x).table_names()
        show_tables_btn = ctk.CTkButton(root, text='View Tables', font=('Comic Sans MS', 20), height=70, width=200, command=lambda:view_tables(result, show_tables_btn))
        show_tables_btn.place(x=168, y=285)

        # enter table name
        values_label = ctk.CTkLabel(root, text='Table Name', font=('Comic Sans MS', 20))
        values_label.place(x=102, y=380)
        table_textbox = ctk.CTkTextbox(root, font=('Comic Sans MS', 20), height=1)
        table_textbox.place(x=250, y=370)

        # show values btn
        values_btn = ctk.CTkButton(root, text='Show Values', font=('Comic Sans MS', 20), height=70, width=200, command=lambda:show_values(values_btn, table_textbox, cur, result))
        values_btn.place(x=170, y=430)
        
        # query box
        query_box = ctk.CTkTextbox(root, font=('Comic Sans MS', 20), width=450)
        query_box.place(x=35, y=520)

        # query button
        exec_btn = ctk.CTkButton(root, font=('Comic Sans MS', 20), width=200, height=70, text='Execute', command=lambda:execute(query_box, cur, exec_btn))
        exec_btn.place(x=170, y=740)

    else:
        messagebox.showerror('', 'Not Found')

def execute(box, cur, btn):
    try:
        btn.configure(state='disabled')
        content = box.get('1.0', tk.END).strip()
        result = cur.execute(content).fetchall()
        root5 = ctk.CTk()
        textbox = ctk.CTkTextbox(root5, width=400, height=200, fg_color='black', font=('Comic Sans MS', 20))
        textbox.insert(tk.END, result)
        textbox.pack(fill='both', expand=True)
        root5.protocol('WM_DELETE_WINDOW', lambda:onclose(root5, btn))
        root5.mainloop()
    except Exception as e:
        messagebox.showerror('', e)
        btn.configure(state='normal')
# design
root = ctk.CTk()

root.title('Database Viewer')
root.geometry('520x830')


view_dbs_btn = ctk.CTkButton(root, text='View Databases', font=('Comic Sans MS', 20), command=lambda:view_dbs(), height=70, width=200)
view_dbs_btn.update()
view_dbs_btn.place(relx=0.33, rely=0.03)

dbs_label = ctk.CTkLabel(root, text='Database Name', font=('Comic Sans MS', 20))
dbs_label.place(x=60, y=125)

dbs_textbox = ctk.CTkTextbox(root, font=('Comic Sans MS', 20), height=1)
dbs_textbox.place(x=250, y=115)

db_connect_btn = ctk.CTkButton(root, font=('Comic Sans MS', 20), text='Connect', height=70, command=lambda:connect(), width=200)
db_connect_btn.place(x=172, y=175)

root.mainloop()
