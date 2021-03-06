import tkinter.filedialog
import csv
import os
# from tkscrolledframe import ScrolledFrame
# from tkscrolledframe import *


class InputTable:
    """class responsible for generating the input table
    for both force and bolt data
    
    it includes all the secondary functions for table like add
    submit or remove"""
    def __init__(self, bolt, force, dname):
        self.table_type = None
        self.bolt_info = bolt
        self.force_info = force
        self.path = dname

        self.force_moment_entry = None
        self.force_moment_entry_label = None
        self.force_moment = ''
        self.force_moment_label = 'M'

    def choose_width(self, idx, width):
        """returns desired width for an entry box
        the ones containing name should be wider"""

        if idx == 0: return width[1]
        else: return width[0]

    def construct_table(self, table_type):
        """
        function which constructs input tables for either force or geometry data
        it has inner function which provide functionality 
        """
        nroot = tkinter.Tk()
        nroot.title('input table')
        entrys_id = []
        entry_width = [12, 15]

        if table_type == 'bolt':
            width, height = 860, 250
            self.table_type = table_type
            info = self.bolt_info
        else:
            width, height = 600, 250
            self.table_type = table_type
            info = self.force_info

        entrys = list(info.keys())
        samplekey = list(info.keys())[0]
        entrys_id = [['' for _ in range(len(entrys))]
                     for _ in range(len(info[samplekey]))]

        err_lab = tkinter.Label(nroot, text='', fg='red')
        err_lab.grid(row=5,
                     column=0,
                     columnspan=3,
                     sticky='n' + 's' + 'e' + 'w')
        err_lab.grid_remove()
        num_rows = 1 if not info[samplekey] else len(info[samplekey])

        # Create a ScrolledFrame widget and buttons
        # scrll_frm = ScrolledFrame(nroot, width=width, height=height)
        # scrll_frm.grid(row=0, column=0, columnspan=3)

        # Bind the arrow keys and scroll wheel
        # scrll_frm.bind_arrow_keys(nroot)
        # scrll_frm.bind_scroll_wheel(nroot)

        # Create a frame within the ScrolledFrame
        # inner_frame = scrll_frm.display_widget(tkinter.Frame)

        inner_frame = tkinter.Frame(nroot, width=width, height=height)
        inner_frame.grid(row=0, column=0, columnspan=3)

        def add_row():
            nonlocal num_rows

            err_lab.grid_forget()
            entrys_id.append(['' for _ in range(len(entrys))])

            for column in range(len(entrys)):
                entrys_id[num_rows][column] = tkinter.Entry(
                    inner_frame,
                    width=self.choose_width(column, entry_width),
                    borderwidth=2,
                    relief="groove",
                    justify="center")
                entrys_id[num_rows][column].grid(row=num_rows + 1,
                                                 column=column,
                                                 padx=0,
                                                 pady=0)
            num_rows += 1

        def remove_row():
            nonlocal num_rows

            err_lab.grid_forget()
            if num_rows > 1:
                for column in range(len(entrys)):
                    entrys_id[num_rows - 1][column].grid_remove()
                entrys_id.pop()
                num_rows -= 1

        def submit_data():
            nonlocal num_rows

            err_lab.grid_remove()
            ypos = entrys.index('y-pos[mm]')
            xpos = entrys.index('x-pos[mm]')

            try:
                for column in range(len(entrys)):
                    info[entrys[column]] = []
                    for row in range(num_rows):
                        value = entrys_id[row][column].get()

                        # save name as string others as float
                        if column != 0: info[entrys[column]].append(float(value))
                        else: info[entrys[column]].append(value)
        
                if table_type == 'bolt':
                    self.bolt_info = info.copy()
                else:
                    self.force_moment = float(self.force_moment_entry.get())
                    self.force_moment_label = self.force_moment_entry_label.get()
                    self.force_info = info.copy()
                return 'ok'
            except:
                err_lab.grid(row=3, column=0, sticky='n' + 's' + 'e' + 'w')
                err_lab.config(text='all entrys must be filled a with valid value')

        def select_entry(event):
            id = nroot.focus_get()
            for i in range(len(entrys_id)):
                if id in entrys_id[i]:
                    idx = entrys_id[i].index(id)
                    if idx + 1 == len(
                            entrys):  # if forcus is on last entry in column
                        if i != len(
                                entrys_id) - 1:  # if focus is NOT in last row
                            entrys_id[i + 1][0].focus()
                            if entrys_id[i + 1][0].get() == '':
                                entrys_id[i + 1][0].insert(
                                    0, info[entrys[0]][i])
                        else:
                            if submit_data(
                            ) == 'ok':  # if all entrys are filled
                                add_row()
                                entrys_id[i + 1][0].focus()
                                entrys_id[i + 1][0].delete(0, 'end')
                                entrys_id[i + 1][0].insert(
                                    0, info[entrys[0]][i])
                    else:
                        entrys_id[i][idx + 1].focus()
                        if i != 0 and 2 < idx + 1:
                            if entrys_id[i][idx + 1].get() == '':
                                entrys_id[i][idx + 1].delete(0, 'end')
                                entrys_id[i][idx + 1].insert(
                                    0, info[entrys[idx + 1]][i - 1])
                    break

        # generate initial table
        for row in range(num_rows):
            for column in range(len(entrys)):
                if row == 0:
                    tkinter.Label(inner_frame,
                                  text=entrys[column],
                                  relief="flat",
                                  justify="center").grid(row=row,
                                                         column=column,
                                                         padx=0,
                                                         pady=0)

                if not info[samplekey]:
                    add_row()

                if info[samplekey] and row < num_rows:
                    entrys_id[row][column] = tkinter.Entry(
                        inner_frame,
                        width=self.choose_width(column, entry_width),
                        borderwidth=2,
                        relief="groove",
                        justify="center")
                    entrys_id[row][column].grid(row=row + 1,
                                                column=column,
                                                padx=0,
                                                pady=0)
                    # inserting default values
                    entrys_id[row][column].insert(0, info[entrys[column]][row])

        # display image of axis orientation
        if table_type == 'force':
            img = tkinter.PhotoImage(master=nroot,
                                     file=os.path.join(
                                         self.path,
                                         r'images/angle_orientation.png'))
            img = img.subsample(3, 3)
            img_lab = tkinter.Label(nroot, image=img)
            img_lab.grid(row=0, column=3, columnspan=2, sticky='N')

            tkinter.Label(nroot, text='force moment[N*mm]').grid(row=1,
                                                                 column=3)
            self.force_moment_entry = tkinter.Entry(nroot,
                                                    width=15,
                                                    justify='center')
            self.force_moment_entry.grid(row=1, column=4, sticky='W')
            self.force_moment_entry.insert(0, self.force_moment)

            tkinter.Label(nroot, text='moment name').grid(row=2, column=3)
            self.force_moment_entry_label = tkinter.Entry(nroot,
                                                          width=15,
                                                          justify='center')
            self.force_moment_entry_label.grid(row=2, column=4, sticky='W')
            self.force_moment_entry_label.insert(0, self.force_moment_label)
        else:
            img = tkinter.PhotoImage(master=nroot,
                                     file=os.path.join(
                                         self.path,
                                         r'images/axis_orientation.png'))
            img = img.subsample(4, 4)
            img_lab = tkinter.Label(nroot, image=img)
            img_lab.grid(row=0, column=3, rowspan=1)

        tkinter.Button(nroot, text='add row', command=lambda: add_row()).grid(
            row=1, column=0, rowspan=2, sticky='n' + 's' + 'e' + 'w')
        tkinter.Button(nroot, text='delete row',
                       command=lambda: remove_row()).grid(row=1,
                                                          column=1,
                                                          rowspan=2,
                                                          sticky='n' + 's' +
                                                          'e' + 'w')
        tkinter.Button(nroot, text='submit data',
                       command=submit_data).grid(row=1,
                                                 column=2,
                                                 rowspan=2,
                                                 sticky='n' + 's' + 'e' + 'w')
        nroot.bind('<Tab>', select_entry)
        nroot.mainloop()

    def load_data(self, inpt_type, err_lab):
        test_data = tkinter.filedialog.askopenfilename()
        err_lab.config(text='')
        if inpt_type == 'bolt': data = self.bolt_info
        else: data = self.force_info

        # remove old data from the dictionary
        for x in list(data.keys()):
            data[x].clear()

        #     if len(line) != len(list(data.keys())):
        #         # in case there are more arrtibutes in the input we need
        #         self.err_lab.config(text='invalid input data look at documentation')
        #         break
        try:
            keys = list(data.keys())
            with open(test_data, mode='r') as inp:
                reader = csv.reader(inp)
                for idx, row in enumerate(reader):

                    # get force moment as the last value of the first row and 
                    # chceck the number of columns
                    if idx == 0:
                        if inpt_type == 'force':
                            self.force_moment = float(row[-1])
                            if len(row)-1 != len(keys):
                                err_lab.config(text='invalid number of columns in the input')
                        if len(row) != len(keys) and inpt_type == 'bolt':
                            err_lab.config(text='invalid number of columns in the input')

                    # get the remaining values
                    for i in range(len(keys)):
                        if i > 0: data[keys[i]].append(float(row[i]))
                        else: data[keys[i]].append(row[i])
        except:
            err_lab.config(text='invalid number of columns in the input')


class Interface:
    """ this class creates interface where the user can input data"""
    def __init__(self, root, bg, font, err_lab, table):
        self.bg = bg
        self.font = font
        self.relief = 'groove'
        self.err_lab = err_lab

        self.table = table

        self.object1 = {}
        self.object2 = {}

        self.construct_labelframes()
        self.construct_object1_UI()
        self.construct_object2_UI()

    def construct_labelframes(self):
        self.inputs = tkinter.LabelFrame(text='inputs',
                                         relief='solid',
                                         bg=self.bg)
        self.inputs.grid(row=0,
                         column=0,
                         rowspan=2,
                         sticky='n' + 'e' + 'w',
                         ipady=5,
                         ipadx=5,
                         padx=5)

        self.tab = tkinter.LabelFrame(self.inputs,
                                      text='input_tables',
                                      relief='groove',
                                      bg=self.bg)
        self.tab.grid(row=0, column=0, sticky='e' + 'w')

        self.obj1 = tkinter.LabelFrame(self.inputs,
                                       text='connection material 1',
                                       relief='groove',
                                       bg=self.bg)
        self.obj1.grid(row=1, column=0, sticky='n' + 'e' + 'w' + 's')

        self.obj2 = tkinter.LabelFrame(self.inputs,
                                       text='connection material 2',
                                       relief='groove',
                                       bg=self.bg)
        self.obj2.grid(row=2, column=0, sticky='n' + 'e' + 'w' + 's')

        self.buttons = tkinter.LabelFrame(text='buttons',
                                          relief='solid',
                                          bg=self.bg)
        self.buttons.grid(row=2,
                          column=0,
                          sticky='n' + 'e' + 'w' + 's',
                          padx=5,
                          pady=5)

        tkinter.Button(self.tab,
                       text='edit geometry data',
                       command=lambda: self.table.construct_table('bolt'),
                       font=self.font[1],
                       bg=self.bg,
                       relief=self.relief).pack(fill='x')

        tkinter.Button(self.tab,
                       text='edit load data',
                       command=lambda: self.table.construct_table('force'),
                       font=self.font[1],
                       bg=self.bg,
                       relief=self.relief).pack(fill='x')

    # MATERIAL INFORMATION -------------------------------------------
    def construct_object1_UI(self):
        entry_id = ['name', 'Fbry[MPa]']
        for index, id in enumerate(entry_id):
            tkinter.Label(self.obj1, text=id, font=self.font[1],
                          bg=self.bg).grid(row=index, column=0, padx=55)
            self.object1[id] = tkinter.Entry(self.obj1,
                                             justify='center',
                                             font=self.font[1],
                                             relief=self.relief,
                                             width=20)
            self.object1[id].grid(row=index, column=1, sticky='e')
            # insert default values
            if id == 'name': self.object1[id].insert(0, 'Material 1')
            else: self.object1[id].insert(0, '1')

    def construct_object2_UI(self):
        entry_id = ['name', 'Fbry[MPa]']
        for index, id in enumerate(entry_id):
            tkinter.Label(self.obj2, text=id, font=self.font[1],
                          bg=self.bg).grid(row=index, column=0, padx=55)
            self.object2[id] = tkinter.Entry(self.obj2,
                                             justify='center',
                                             font=self.font[1],
                                             relief=self.relief,
                                             width=20)
            self.object2[id].grid(row=index, column=1, sticky='e')
            # insert default values
            if id == 'name': self.object2[id].insert(0, 'Material 2')
            else: self.object2[id].insert(0, '1')
