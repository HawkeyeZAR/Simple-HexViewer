"""
Creates a right click popup menu
"""

import tkinter as tk
from tkinter import Frame, Entry, END, INSERT


class RightClickMenu(Frame):
    """
    Creates two types of popup menus

    entry_popup  - Only works with Entry Widgets
    text_popup     - Only works with Textbox Widgets
    """
    def __init__(self, parent, text):
        Frame.__init__(self, parent)
        self.textbox_text = text
        self.entry_text = text
        self.create_widgets()

    def create_widgets(self):
        self.create_right_click_menu_entry()
        self.create_right_click_menu_text()

    def create_right_click_menu_entry(self):
        '''Create 3 buttons for the entry_popup menu'''
        self.right_click_menu_entry = tk.Menu(self, tearoff=0, relief='sunken')
        self.right_click_menu_entry.add_command(label="Copy",
                                                command=self.copy_entry)
        self.right_click_menu_entry.add_separator()
        self.right_click_menu_entry.add_command(label="Paste",
                                                command=self.paste_entry)
        # self.right_click_menu_entry.add_separator()
        # self.right_click_menu_entry.add_command(label="Clear",
        #                                        command=self.clear_entry)

    def create_right_click_menu_text(self):
        '''Create 3 buttons for the text_popup menu'''
        self.right_click_menu_text = tk.Menu(self, tearoff=0, relief='sunken')
        self.right_click_menu_text.add_command(label="Copy",
                                               command=self.copy_text)
        self.right_click_menu_text.add_separator()
        self.right_click_menu_text.add_command(label="Paste",
                                               command=self.paste_text)
        # self.right_click_menu_text.add_separator()
        # self.right_click_menu_text.add_command(label="Clear",
        #                                        command=self.clear_text)

    # Methods for the the right click popup menu's
    def entry_popup(self, event):
        """ Creates the popup menu for Entry widgets """
        self.right_click_menu_entry.post(event.x_root, event.y_root)

    def text_popup(self, event):
        """ Creates the popup menu for Textbox widgets """
        self.right_click_menu_text.post(event.x_root, event.y_root)

    # Methods used by the right click popup menu items
    def copy_entry(self, event=None):
        """ Copies all text from the Entry Widget to clipboard"""
        self.clipboard_clear()
        text = self.entry_text.get()
        self.clipboard_append(text)

    def paste_entry(self):
        """ Pastes text from cliboard """
        self.entry_text.set(self.clipboard_get())

    def clear_entry(self):
        """ Clears all contents in the Entry widget """
        self.entry_text.set('')

    def copy_text(self, event=None):
        """ Copies selected text from the Textbox Widget to clipboard"""
        self.clipboard_clear()
        if self.textbox_text.tag_ranges("sel"):
            text = self.textbox_text.get("sel.first", "sel.last")
            self.clipboard_append(text)

    def paste_text(self):
        """ Pastes text from cliboard """
        self.textbox_text.insert(INSERT, self.clipboard_get())

    def clear_text(self):
        """ Clears all contents in the Textbox widget """
        self.textbox_text.delete(1.0, END)
