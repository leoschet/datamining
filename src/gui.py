from tkinter import *
import webbrowser

import main

# getting default rankers (takes some time)
rankers = main.get_default_rankers()


class Gui(Tk):
    def __init__(self, rankers):
        super().__init__()
        self.search_frame = Frame(self)
        self.search_frame.pack(side=TOP)
        self.search_entry = Entry(self.search_frame)
        self.search_entry.pack(side=LEFT)
        self.search_button = Button(self.search_frame, text='search', command=self.search_query)
        self.search_button.pack(side=LEFT)
        #
        self.get_all_var = IntVar()
        self.get_all_option = Checkbutton(self.search_frame, text='get all', variable=self.get_all_var)
        self.get_all_option.pack(side=LEFT)
        #
        self.search_result_frame = Frame(self)
        self.search_result_frame.pack(side=TOP)
        #
        self.list_boxes = {}
        for ranker in rankers:
            ranker_frame = Frame(self.search_result_frame)
            ranker_frame.pack(side=LEFT)
            Label(ranker_frame, text=ranker).pack(side=TOP)
            #
            ranker_list_box_scroll = Scrollbar(ranker_frame)
            ranker_list_box_scroll.pack(side=LEFT)
            #
            ranker_list_box = Listbox(ranker_list_box_scroll)
            ranker_list_box.bind('<Double-Button-1>', self.on_click_document)

            ranker_list_box.pack()
            #
            self.list_boxes[ranker] = ranker_list_box

    def search_query(self):
        query = self.search_entry.get()
        results, correlation = main.search_query(query, rankers, True if self.get_all_var.get() == 1 else False)
        for result in results:
            result_list = results[result]
            list_box = self.list_boxes[result]
            list_box.delete(0, list_box.size() - 1)
            list_box.insert(0, *['%d - %s' % (index, doc) for index, (doc, similarity) in enumerate(result_list)])

    def on_click_document(self, event):
        list_box = event.widget
        selection=list_box.curselection()
        value = list_box.get(selection[0])
        link = 'https://docs.unity3d.com/Manual/%s' % value.split(' - ')[1].strip('\n').strip(' ')
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(link)

Gui(rankers).mainloop()
