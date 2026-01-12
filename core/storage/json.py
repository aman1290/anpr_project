import json
import os
from datetime import datetime

class JSONStorage:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.cumulative_file = os.path.join(output_dir, "LicensePlateData.json")

    def save(self, license_plates, start_time, end_time):
        interval_data = {
            "Start Time": start_time.isoformat(),
            "End Time": end_time.isoformat(),
            "License Plate": list(license_plates)
        }

        filename = f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        path = os.path.join(self.output_dir, filename)

        with open(path, "w") as f:
            json.dump(interval_data, f, indent=2)

        if os.path.exists(self.cumulative_file):
            with open(self.cumulative_file, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(interval_data)

        with open(self.cumulative_file, "w") as f:
            json.dump(data, f, indent=2)
