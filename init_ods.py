import json
import pyexcel_ods3 as ods

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

data = {"Hoja1": [config["columns"]] + config["initial_data"]}
ods.save_data("registros.ods", data)
