"""
Very Basic Hex Viewer using python 3.

Created by Jack Ackermann
"""

import tkinter as tk
from tkinter import Tk, ttk, Frame, FALSE, Text, filedialog, Button, \
                    messagebox, Scrollbar, StringVar, END

from lib.tohex import ToHex
from lib.popup import RightClickMenu


class HexViewer(Frame):
    '''
    HexViewer Class
    '''
    
    def centre_window(self):
        '''
        Create window size and center in middle of screen
        '''
        w = 685
        h = 600
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        centre_title = (' '*60)  # Use spaces to center Title
        title_text = 'Simple Hex Viewer  -  Coded in Python 3.5'
        self.root.title(centre_title + title_text)
        self.centre_window()
        self.grid(column=0, row=0, sticky='nsew',  padx=12,  pady=10)
        self.to_hex = ToHex()

        # Stores all found 'self.find_string' matches
        self.idx_list = []

        # Create Textbox to store hex data
        self.hex_textbox = Text(self, borderwidth=1, relief='sunken')
        self.hex_textbox.config(height=30, width=80)
        self.hex_textbox.grid(row=0, column=0, sticky="new")
        self.scrollbar = Scrollbar(self, command=self.hex_textbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.hex_textbox['yscrollcommand'] = self.scrollbar.set

        # create color tags
        self.hex_textbox.tag_configure("header", foreground="dark blue",
                                       background="lightsteelblue")
        self.hex_textbox.tag_configure("offset", foreground="dark red",
                                       background="lightsteelblue")
        self.hex_textbox.tag_configure("hex", background="lightgray")
        self.hex_textbox.tag_configure("ascii", background="gray")

        # Create Button Widgets
        self.file_btn = ttk.Button(self, text='File',command=self.open_file)
        self.file_btn.grid(column=0, row=1, sticky='W', pady=7)
        self.exit_btn = ttk.Button(self, text='Exit', command=self.on_exit)
        self.exit_btn.grid(column=0, row=1, sticky='E', pady=7)
        self.find_btn = ttk.Button(self, text='Find', command=self.find_text)
        self.find_btn.grid(column=0, row=2, sticky='E')
        self.next_btn = ttk.Button(self, text='->', command=self.find_next)
        self.next_btn.config(width=2, state='disabled')
        self.next_btn.grid(column=1, row=2, sticky='E')

        # Create Entry Widget
        self.find_string = StringVar()
        self.find_entry = ttk.Entry(self, width=90)
        self.find_entry.config(textvariable=self.find_string)
        self.find_entry.grid(column=0, row=2, sticky='W')
        #self.find_entry.bind("<Return>", lambda _: self.find_text)
        self.file_name_string = StringVar()
        self.file_name_entry = ttk.Entry(self, width=110, state='readonly')
        self.file_name_entry.config(textvariable=self.file_name_string)
        self.file_name_entry.grid(column=0, row=3, sticky='W',
                                  pady=15, columnspan=2)
        # Load the Right Click Menu
        self.create_right_click_menu()


    # Find Text Callback
    def find_text(self):
        '''
        Finds all occurrences of string entered in self.find_string.get()

        All matches are then highlighted and messagebox with total number
        of strings found is created. When new search begins, all previous tags
        are deleted.
        
        data = self.hex_textbox.search(self.find_string.get(), '1.0', "end")
        self.hex_textbox.see(data)
        '''
        self.hex_textbox.tag_remove('found', '1.0', END)  #  Delete any old tags
        self.hex_textbox.tag_remove('found_next', '1.0', END)  #  Delete any old tags
        # Grabs the text from the entry box
        search = self.find_string.get()
        counter = 0
        self.idx_list.clear()
        if search:
            idx = '1.0'
            while 1:
                idx = self.hex_textbox.search(search, idx,
                                              nocase=1, stopindex=END)
                if not idx: break
                counter += 1
                lastidx = '%s+%dc' % (idx, len(search))
                self.hex_textbox.tag_add('found', idx, lastidx)
                idx = lastidx
                self.idx_list.append(idx)
                #self.hex_textbox.see(idx)
            self.hex_textbox.tag_config('found', foreground='darkred',
                                        background='yellow')
            # If more than one result is found, enable find next button
            if counter > 1:
                self.next_btn.config(state='enabled')
            else:
                self.next_btn.config(state='disabled')
                
        self.hex_textbox.focus_set()
        # if no search string entered, don't create messagebox
        if self.find_string.get() != "":
            message = "{0} matches were found and highlighted".format(counter)
            messagebox.showinfo("Matches Found", message)
        else:
            self.next_btn.config(state='disabled')

    # Find Text Callback
    def find_next(self):
        '''
        Loops through all found matches, one at a time, if more than one match.

        This allows you to jump to the next item, without having to scroll to it.
        '''
        search = self.find_string.get()
        search_len = len(search)
        self.hex_textbox.tag_remove('found_next', '1.0', END)  #  Delete any old tags
        lst = iter(self.idx_list)  # Make the list iterable
        #first_item = self.hex_textbox.see(next(lst))  # asign the first item in list to first_item
        index = str(next(lst)).split('+')  # split tag location to get start index of tag location
        start_index = index[0]
        #  Calculate the end index by using length of search string
        end_index = float(start_index) + float('0.{0}'.format(search_len))
        # Add new tag to highlight first_item
        self.hex_textbox.tag_add('found_next', start_index, end_index)
        self.hex_textbox.tag_config('found_next', foreground='darkred', background='green')
        self.hex_textbox.see(start_index)
        self.idx_list = self.idx_list[1:] + self.idx_list[:1]
    
    # Load a file callback
    def open_file(self):
        '''
        Function to open the file. Once file is opened, the
        self.file_name_string is updated with the file name and path.

        This function also creates the tag layout in the hex_data widget.

        Finally the self.to_hex.convert_to_hex function is called to convert
        the data. This functions is in a seperate class in its own module.
        '''
        try:
            self.hex_textbox.delete('1.0', END)  # make sure text box is clear
            file_type = [("All Files","*.*")]
            title_text = "---- Please select the file to edit ----"
            file_name = filedialog.askopenfilename(filetypes=file_type,
                                                   title=title_text)
        except (FileNotFoundError) as e:
            messagebox.showerror("File Error", "File could not be opened")
        else:
            if file_name != '':
                # Update self.file_name_string stringvar with filename
                self.file_name_string.set(file_name)
                # Create header index for hex data and insert it as first line
                header_space = "########:  "
                header_data = "00-01-02-03-04-05-06-07-08-09-0A-0B-0C-0D-0E-0F\n"
                header_sep = ("--" * 28 + '--\n')
                heder_row = header_space + header_data
                self.hex_textbox.insert(tk.END, heder_row, "header")
                self.hex_textbox.insert(tk.END, header_sep, "header")

                # Call the convert_to_hex() function, data is saved as a dictionery
                # Data is returned as dictionery, sort dictionery before loop
                get_data = self.to_hex.convert_to_hex(file_name)
                for key, value in sorted(get_data.items()):
                    # After each loop, update textbox with the hex data
                    self.hex_textbox.insert(tk.END, key, "offset")
                    self.hex_textbox.insert(tk.END, ' ' + value[0] + '  ', "hex")
                    self.hex_textbox.insert(tk.END, ' ' + value[1] + '\n', "ascii")

    # Create Popup menu widget
    def create_right_click_menu(self):
        '''
        Creates and binds the right click popup menu
        '''
        # Instanciate the imported popup class
        self.popup = RightClickMenu(self.master, self.find_string)
        self.popup2 = RightClickMenu(self.master, self.hex_textbox)
        # Bind the popup menus and Enter Key to the appropriate widgets.
        self.find_entry.bind("<Button-3>", self.popup.entry_popup)
        self.hex_textbox.bind("<Button-3>", self.popup2.text_popup)


    # Exit the program. Linked to the Exit Button
    def on_exit(self):
        # Quits the program
        self.root.destroy()


def main():
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    # root.configure(background="black")
    HexViewer(root)
    root.mainloop()

if __name__ == '__main__':
    main()
