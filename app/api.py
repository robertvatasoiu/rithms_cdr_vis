import random
import datetime
import csv
import pandas as pd
import random
import datetime
import os
import numpy as np
import uuid


def cdr_view(latitude1, latitude2, longitude1, longitude2):
    print(os.getcwd())
    ro = pd.read_csv("utils/Romania.csv")
    ro.columns = [
        "radio",
        "mcc",
        "net",
        "area",
        "cell",
        "unit",
        "lon",
        "lat",
        "range",
        "samples",
        "changeable",
        "created",
        "updated",
        "averageSignal",
    ]
    date_sintetice = pd.read_csv("utils/date_sintetice_noi_v1.csv")

    df = ro[
        (ro["lat"] >= latitude1)
        & (ro["lat"] <= latitude2 + 0.045)
        & (ro["lon"] >= longitude1)
        & (ro["lon"] <= longitude2 + 0.064)
    ]
    lon = list(df["lon"].values)
    lat = list(df["lat"].values)
    cell_ids_cdr = list(df["cell"].values)

    cell_dict = {}
    for index, row in df.iterrows():
        cell_dict[row["cell"]] = (row["lon"], row["lat"])

    def generate_phone_number():
        # Generate a random 10-digit phone number starting with "+4073"
        phone_number = "+4073" + "".join(random.choice("0123456789") for _ in range(6))
        return phone_number

    def generate_imei_number():
        # Generate a random 15-digit IMEI number
        imei = "".join(random.choice("0123456789") for _ in range(15))
        return imei

    # Define list of possible cell IDs
    cell_ids = cell_ids_cdr

    # Define list of possible GPS coordinates for location field
    longitudine = lon
    latitudine = lat

    # Define list to hold CDRs
    cdrs = []
    caller_callee_pairs = []

    # Generate and store a pool of caller-callee pairs
    for i in range(100):  # You can adjust the number of pairs as needed
        caller_id = generate_phone_number()
        callee_id = generate_phone_number()
        caller_callee_pairs.append((caller_id, callee_id))

    # Generate 2000 random CDRs
    for i in range(2000):
        # Generate random values for CDR fields
        caller_imei = generate_imei_number()
        callee_id, callee_imei = generate_phone_number(), generate_imei_number()

        caller_id = date_sintetice["apelant"][i]

        call_start_time = date_sintetice["datetime"][i]
        call_end_time = date_sintetice["ora sfarsit"][i]
        call_duration = date_sintetice["secunde"][i]
        call_type = random.choice(["inbound", "outbound"])
        call_result = random.choice(["answered"])

        # This needs to be changed.
        cell_id = random.choice(cell_ids)
        caller_imsi = "".join(random.choice("0123456789") for i in range(15))
        callee_imsi = "".join(random.choice("0123456789") for i in range(15))
        longitudine_cdr = cell_dict[cell_id][0]
        latitudine_cdr = cell_dict[cell_id][1]

        # Generate a unique identifier using uuid
        unique_id = str(uuid.uuid4())

        # Create a dictionary to hold the CDR fields
        cdr = {
            "unique_id": unique_id,
            "caller_id": caller_id,
            "caller_imei": caller_imei,
            "callee_id": callee_id,
            "callee_imei": callee_imei,
            "call_start_time": call_start_time,
            "call_end_time": call_end_time,
            "call_duration": call_duration,
            "call_type": call_type,
            "call_result": call_result,
            "cell_id": cell_id,
            "caller_imsi": caller_imsi,
            "callee_imsi": callee_imsi,
            # "direction": "incoming" if call_type == "inbound" else "outgoing",
            "service_type": "voice",
            "longitudine": longitudine_cdr,
            "latitudine": latitudine_cdr,
        }

        # Add the CDR to the list of CDRs
        cdrs.append(cdr)
        for cdr in cdrs:
            for key, value in cdr.items():
                if isinstance(value, np.int64):
                    cdr[key] = int(value)

    return pd.DataFrame(cdrs)
