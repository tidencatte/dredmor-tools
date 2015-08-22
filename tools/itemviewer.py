from Tkinter import *
import Tix
from Tkconstants import *
import sys

sys.path.append("..")

from dredmordata import dredmordata

class ItemViewer(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=(N,E,W,S), columnspan=3,rowspan=3)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(1, weight=0)

        self.item_list = Listbox(self)
        self.item_list.grid(row=0, column=0, rowspan=3, sticky="ns")

        def next_item():
            self.item_pointer += 1
            self.update_display()

        def previous_item():
            self.item_pointer -= 1
            self.update_display()

        def update_display_from_list(event):
            print(event.widget.curselection())
            self.item_pointer = event.widget.curselection()[0]
            self.update_display()

        self.item_list.bind("<ButtonRelease>", update_display_from_list)

        self.prev_item = Button(self)
        self.prev_item["text"] = "<<<"
        self.prev_item["command"] = previous_item
        self.prev_item.grid(row=0,column=1,sticky="new")

        self.next_item = Button(self)
        self.next_item["text"] = ">>>"
        self.next_item["command"] = next_item
        self.next_item.grid(row=0, column=2,sticky="new")

        self.item_name_label = Label(self)
        self.item_name_label["anchor"] = "ne"
        self.item_name_label["text"] = "Item Name"
        self.item_name_label["justify"] = "left"
        self.item_name_label["background"] = "blue"
        self.item_name_label.grid(row=1,column=1)

        self.item_name_textvar = StringVar()
        self.item_name_text = Label(self)
        self.item_name_text["textvariable"] = self.item_name_textvar
        self.item_name_text["wraplength"] = 180
        self.item_name_text["justify"] = "left"
        self.item_name_text.grid(row=1,column=2)

        self.item_description_label = Label(self)
        self.item_description_label["text"] = "Item Description"
        self.item_description_label["anchor"] = "n"
        self.item_description_label.grid(row=2,column=1)

        self.item_description = StringVar()
        self.item_description_text = Label(self)
        self.item_description_text["textvariable"] = self.item_description
        self.item_description_text["wraplength"] = 180
        self.item_description_text["justify"] = "left"
        self.item_description_text.grid(row=2,column=2, sticky="s")

        self.attributes = StringVar()
        self.attributes_label = Label(self)
        self.attributes_label["text"] = "Attributes"
        self.attributes_text = Label()
        self.attributes_text["textvariable"] = self.attributes
        self.attributes_label.grid(row=3,column=1)
        self.attributes_text.grid(row=3,column=2)

        self.columnconfigure(0, weight=3)
        self.load_items()
        self.item_pointer = 0
        self.update_display()

    def load_items(self):
        self.items = [item for item in dredmordata.items()]
        for i in enumerate(self.items):
            self.item_list.insert(i[0],i[1]["name"])

    def update_display(self):
        self.item_list.selection_clear(0,len(self.items))
        self.item_list.activate(self.item_pointer)
        self.item_list.selection_set(self.item_pointer)
        self.item_description.set(self.items[self.item_pointer]["description"])
        self.item_name_textvar.set(self.items[self.item_pointer]["name"])
        self.attributes.set(self.items[self.item_pointer]["price"])
        self.item_list.see(self.item_pointer)


root = Tix.Tk()
app = ItemViewer(master=root)
# app.master.minsize(800, 480)
app.mainloop()
root.destroy()
