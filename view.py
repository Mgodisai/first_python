import tkinter as tk
from tkinter import ttk, messagebox


class View(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.controller = None

        # setup the grid layout manager
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=2)

        # define widgets
        self.record_counter = None
        self.identifier = None
        self.conf_identifier = None
        self.results = None
        self.conf_results = None
        self.message_label = None
        self.search_field = None
        self.identifier_image = None
        self.result_image = None
        self.__create_widgets()

    def set_controller(self, controller):
        self.controller = controller

    # event handlers
    def forward(self, event=None):
        self.controller.forward()

    def backward(self, event=None):
        self.controller.backward()

    def search_record(self, event=None):
        self.controller.search_record()

    def entry_changed(self, event):
        self.controller.update(event.widget.extra, event.widget.get())

    def on_closing(self):
        confirm = messagebox.askyesnocancel("Save before quit", "Do you want to save before quit?")
        if confirm:
            self.controller.save()
        elif confirm is None:
            return
        self.container.destroy()

    def __create_widgets(self):

        # Record Counter
        self.record_counter = tk.Label(self, width=30, anchor="w", fg="blue")
        self.record_counter.grid(column=0, row=0, sticky=tk.W)

        # Identifier
        ttk.Label(self, text='Identifier: ').grid(column=0, row=1, sticky=tk.W)
        self.identifier = ttk.Label(self, width=30)
        self.identifier.grid(column=1, row=1, sticky=tk.W)

        # Confirmed identifier
        ttk.Label(self, text='Confirmed identifier:').grid(column=0, row=2, sticky=tk.W)
        self.conf_identifier = ttk.Entry(self, width=30)
        self.conf_identifier.extra = "confirmed_identifier"
        self.conf_identifier.grid(column=1, row=2, sticky=tk.W)
        self.conf_identifier.bind("<KeyRelease>", self.entry_changed)

        # Identifier image
        self.identifier_image = tk.Canvas(self, width=100, height=80, bg="red")
        self.identifier_image.grid(column=2, rowspan=2, row=1, sticky=tk.W)

        # Result
        ttk.Label(self, text='Results: ').grid(column=0, row=3, sticky=tk.W)
        self.results = ttk.Label(self, width=30)
        self.results.grid(column=1, row=3, sticky=tk.W)

        # Confirmed results
        ttk.Label(self, text='Confirmed results:').grid(column=0, row=4, sticky=tk.W)
        self.conf_results = ttk.Entry(self, width=30)
        self.conf_results.extra = "confirmed_results"
        self.conf_results.grid(column=1, columnspan=3, row=4, sticky=tk.W)
        self.conf_results.bind("<KeyRelease>", self.entry_changed)

        # Results images
        self.result_image = tk.Canvas(self, width=500, height=160, bg="green")
        self.result_image.grid(column=0, columnspan=3, row=5, sticky=tk.EW)

        # Control widgets
        # Search field
        ttk.Label(self, text='Identifier:').grid(column=0, row=6, sticky=tk.E)
        self.search_field = ttk.Entry(self, width=30)
        self.search_field.grid(column=1, row=6, sticky=tk.N)
        self.search_field.bind("<Return>", self.search_record)

        ttk.Button(self, text='Show previous', command=self.backward).grid(column=0, row=7, sticky=tk.N)
        ttk.Button(self, text='Search', command=self.search_record).grid(column=1, row=7, sticky=tk.N)
        ttk.Button(self, text='Show next', command=self.forward).grid(column=2, row=7, sticky=tk.N)

        # Message label
        self.message_label = ttk.Label(self, text="default message")
        self.message_label.grid(column=0, columnspan=3, row=8, sticky=tk.N)

        # arrow events
        self.container.bind("<Left>", self.backward)
        self.container.bind("<Right>", self.forward)

        # closing protocol
        self.container.protocol("WM_DELETE_WINDOW", self.on_closing)

        for widget in self.winfo_children():
            widget.grid(padx=10, pady=12)
