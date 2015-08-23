from Tkinter import *
import Tix
from Tkconstants import *
import sys

sys.path.append("..")

from dredmordata import dredmordata

class ItemViewer(Frame):
    def __init__(self, master=None, menu=None):
        Frame.__init__(self, master)
        self.grid(sticky=(N,E,W,S), columnspan=4,rowspan=2)
        self.columnconfigure(0, weight=0)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=3)
        self.columnconfigure(1, weight=3)

        self.item_list_container = Frame(self)
        self.item_list_container.columnconfigure(0, weight=3)
        self.item_list_container.rowconfigure(0, weight=3)

        self.item_list = Listbox(self.item_list_container)
        self.list_scrollbar = Scrollbar(self.item_list_container,orient=VERTICAL)
        self.item_list.config(yscrollcommand=self.list_scrollbar.set)
        self.list_scrollbar.config(command=self.item_list.yview)
        self.item_list.grid(row=0, column=0, sticky="nswe")
        self.list_scrollbar.grid(row=0, column=1, sticky="nswe")

        self.item_list_container.grid(column=0, row=0, rowspan=2, sticky="nswe")

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

        self.navigation = Frame(self)

        self.prev_item = Button(self.navigation)
        self.prev_item["text"] = "<<<"
        self.prev_item["command"] = previous_item
        self.prev_item.pack(fill=X, side="left", expand=1)

        self.next_item = Button(self.navigation)
        self.next_item["text"] = ">>>"
        self.next_item["command"] = next_item
        self.next_item.pack(fill=X, side="right", expand=1)
        self.navigation.grid(row=0,column=1,sticky="nwe")

        self.item_info = Frame(self)
        self.item_name_label = Label(self.item_info)
        self.item_name_label["anchor"] = "ne"
        self.item_name_label["text"] = "Item Name"
        self.item_name_label["justify"] = "left"
        self.item_name_label.grid(row=0,column=0, sticky=N+W)

        self.item_name_textvar = StringVar()
        self.item_name_text = Label(self.item_info)
        self.item_name_text["textvariable"] = self.item_name_textvar
        self.item_name_text["wraplength"] = 380
        self.item_name_text["justify"] = "left"
        self.item_name_text.grid(row=0,column=1, sticky=N+W)

        self.item_description_label = Label(self.item_info)
        self.item_description_label["text"] = "Item Description"
        self.item_description_label.grid(row=1,column=0, sticky=N)

        self.item_description = StringVar()
        self.item_description_text = Label(self.item_info)
        self.item_description_text["textvariable"] = self.item_description
        self.item_description_text["wraplength"] = 380
        self.item_description_text["justify"] = "left"
        self.item_description_text.grid(row=1,column=1,sticky=N)

        self.attributes = StringVar()
        self.attributes_label = Label(self.item_info)
        self.attributes_label["text"] = "Attributes"
        self.attributes_label["justify"] = "left"
        self.attributes_text = Label(self.item_info)
        self.attributes_text["textvariable"] = self.attributes
        self.attributes_label.grid(row=2,column=0)
        self.attributes_text.grid(row=2,column=1)

        self.item_info.grid(row=1,column=1,sticky="nwse")

        self.load_items()
        self.item_pointer = 0
        self.update_display()
    
    def create_menu(self, root):
        self.menu = Menu(root)
        self.file_menu = Menu(self.menu)
        self.file_menu.add_command(label="Exit", command=root.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        root.configure(menu=self.menu)

    def load_items(self):
        self.items = [item for item in dredmordata.items()]
        for i in enumerate(self.items):
            self.item_list.insert(i[0],i[1]["name"])
            if (i[1]["type"] == "food"):
                self.item_list.itemconfigure(i[0],background="#FFCEBD")
            if (i[1]["type"] == "potion"):
                self.item_list.itemconfigure(i[0],background="#BDEEFF")
            if (i[1]["type"] == "weapon"):
                self.item_list.itemconfigure(i[0], background="#EFBDFF")

    def update_display(self):
        self.item_list.selection_clear(0,len(self.items))
        self.item_list.activate(self.item_pointer)
        self.item_list.selection_set(self.item_pointer)
        self.item_description.set(self.items[self.item_pointer]["description"])
        self.item_name_textvar.set(self.items[self.item_pointer]["name"])
        self.attributes.set(self.items[self.item_pointer]["price"])
        self.item_list.see(self.item_pointer)


root = Tix.Tk()
root.columnconfigure(0, weight=3)
root.rowconfigure(0, weight=3)
app = ItemViewer(master=root)
app.create_menu(root)
app.mainloop()
root.destroy()
