import re
import util


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.index = 0
        self.record_count = 0
        self.previous_search_string = ""
        self.search_counter = 0

    def load(self):
        try:
            self.model.read_json_data()
            self.update_message_label("Read success")
            self.record_count = self.model.get_records_length()
            self.populate_fields()
            # self.save()
        except FileNotFoundError as error:
            self.update_message_label("Error during reading: "+str(error))

    def save(self):
        try:
            self.model.save_json_data()
            self.update_message_label("Write success")
        except ValueError as error:
            self.update_message_label("Error during writing: "+str(error))

    def populate_fields(self):
        current_record = self.model.get_record(self.index)

        # identifier label
        self.view.identifier.config(text=current_record["identifier"])

        # confirmed_identifier entry
        self.view.conf_identifier.delete(0, 'end')
        self.view.conf_identifier.insert(0, current_record["confirmed_identifier"])

        # results label
        self.view.results.config(text=util.list_to_text(current_record["results"], self.model.delimiter))

        # confirmed_results entry
        self.view.conf_results.delete(0, 'end')
        self.view.conf_results.insert(0, util.list_to_text(current_record["confirmed_results"], self.model.delimiter))

        # identifier image canvas
        self.view.update()
        util.show_image(self.view.identifier_image, self.model.image_folder, current_record["identifier_image"])

        # results image canvas
        util.show_image(self.view.result_image, self.model.image_folder, current_record["result_image"])

        # record counter
        self.view.record_counter.config(text=str(self.index+1)+" / "+str(self.record_count))

    def forward(self):
        self.index = self.index+1 if self.index < self.record_count-1 else self.index
        self.populate_fields()
        self.clear_message_label()
        if self.index == self.record_count-1:
            self.update_message_label("Last record")

    def backward(self):
        self.index = self.index-1 if self.index > 0 else self.index
        self.populate_fields()
        self.clear_message_label()
        if self.index == 0:
            self.update_message_label("First record")

    def search_record(self):
        search_str = self.view.search_field.get()
        if search_str != self.previous_search_string:
            self.previous_search_string = search_str
            self.search_counter = 0

        found_dict = self.model.get_record_dict(search_str)
        list_size = len(found_dict)

        if list_size > 0:
            self.search_counter = self.search_counter+1 if self.search_counter < list_size else 1
            self.index = list(found_dict)[self.search_counter-1]
            self.populate_fields()

        self.update_message_label("Found "+str(list_size)+"/"+str(self.search_counter)+" records based on: "+search_str)

    def clear_message_label(self):
        self.view.message_label.config(text="")

    def update_message_label(self, message):
        self.view.message_label.config(text=message)

    def update(self, key, value):
        if key != "confirmed_identifier":
            if self.__validate_result(value):
                value = value.split(self.model.delimiter)
                for i in range(len(value)):
                    value[i] = int(value[i])
                    if not self.__validate_result_value_limit(value[i]):
                        self.update_message_label("Data is not valid")
                        return
            else:
                self.update_message_label("Data is not valid")
                return
        self.model.update_record_data(self.index, key, value)
        self.clear_message_label()

    def __validate_result(self, value):
        pattern = r"^((0|-?[1-9][0-9]*)"+self.model.delimiter+")+(0|-?[1-9][0-9]*)$"
        if re.match(pattern, value) is None:
            return False
        return True

    def __validate_result_value_limit(self, value):
        if self.model.res_min <= value <= self.model.res_max:
            return True
        else:
            return False
