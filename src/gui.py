from tkinter import *

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
            ranker_list_box.pack()
            #
            self.list_boxes[ranker] = ranker_list_box

    def search_query(self):
        query = self.search_entry.get()
        results, correlation = main.search_query(query, rankers)
        for result in results:
            result_list = results[result]
            list_box = self.list_boxes[result]
            list_box.delete(0, list_box.size() - 1)
            list_box.insert(0, *['%d - %s' % (index, doc) for index, (doc, similarity) in enumerate(result_list)])


Gui(rankers).mainloop()
