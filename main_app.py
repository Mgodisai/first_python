import tkinter as tk
from model import Records
from view import View
from controller import Controller


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('python homework project - ue6li3')
        self.geometry('800x600')
        self.resizable(False, False)

        # create and place a view
        view = View(self)
        view.pack()

        # create a model
        model = Records()

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)

        # init data
        controller.load()


if __name__ == '__main__':
    app = App()
    app.mainloop()
