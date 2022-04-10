import json
from pathlib import Path
import util


class Records:
    file = "data/data.json"
    # file_out = "data/data_out.json"
    # file_out = "data/data_in.json"
    image_folder = "images"
    delimiter = ", "
    res_min = 0
    res_max = 20
    fields = ["identifier", "identifier_image", "results", "result_image", "confirmed_identifier", "confirmed_results"]

    def __init__(self):
        self.records = []

    def read_json_data(self):
        str_json = Path(self.file).read_text()
        list_json = json.loads(str_json)

        for item in list_json:
            id_filename = item["identifier_image"]
            res_filename = item["result_image"]
            if not util.is_image_exists(self.image_folder, id_filename):
                util.create_image(
                    self.image_folder, id_filename, item["identifier"])
            if not util.is_image_exists(self.image_folder, res_filename):
                util.create_image(
                    self.image_folder, res_filename, util.list_to_text(item["results"], self.delimiter))

            if "confirmed_identifier" not in item.keys():
                item["confirmed_identifier"] = item["identifier"]
            if "confirmed_results" not in item.keys():
                item["confirmed_results"] = item["results"]
            item = dict([(f, item.get(f)) for f in self.fields])
            self.records.append(item)

    def save_json_data(self):
        with open(self.file, "w") as final:
            json.dump(self.records, final, indent=4)

    def update_record_data(self, index, key, value):
        self.records[index][key] = value
        # self.save_json_data()

    def get_records_length(self):
        return len(self.records)

    def get_record(self, index):
        return self.records[index]

    def get_record_dict(self, search_str):
        record_list = {}
        for item in self.records:
            if search_str.lower() in item["identifier"].lower() or \
                    search_str.lower() in item["confirmed_identifier"].lower():
                record_list[self.records.index(item)] = item
        return record_list
