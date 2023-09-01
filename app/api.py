import random
import datetime
import csv
import pandas as pd
import random
import datetime
import os
import numpy as np


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

    caller_ids = {
        "+40734657481": "123456789012345",
        "+40734657491": "234567890123456",
        "+40734657381": "345678901234567",
        "+40734653481": "456789012345678",
    }

    # Define list of possible callee IDs and corresponding IMEIs
    callee_ids = {
        "+40734653381": "567890123456789",
        "+40732657481": "678901234567890",
        "+40734653481": "789012345678901",
        "+40734657421": "890123456789012",
    }

    # Define list of possible cell IDs
    cell_ids = cell_ids_cdr

    # Define list of possible GPS coordinates for location field
    longitudine = lon
    latitudine = lat

    # Define list to hold CDRs
    cdrs = []

    # Generate 100 random CDRs
    for i in range(100):
        # Generate random values for CDR fields
        caller_id, caller_imei = random.choice(list(caller_ids.items()))
        callee_id, callee_imei = random.choice(list(callee_ids.items()))
        call_start_time = datetime.datetime.now() - datetime.timedelta(
            minutes=random.randint(1, 60)
        )
        call_end_time = call_start_time + datetime.timedelta(
            minutes=random.randint(1, 10)
        )
        call_duration = (call_end_time - call_start_time).total_seconds()
        call_type = random.choice(["inbound", "outbound"])
        call_result = random.choice(["answered", "busy", "no answer", "failed"])

        # This needs to be changed.
        cell_id = random.choice(cell_ids)
        imsi = "".join(random.choice("0123456789") for i in range(15))
        longitudine_cdr = cell_dict[cell_id][0]
        latitudine_cdr = cell_dict[cell_id][1]
        qos_metrics = {
            "jitter": random.uniform(0.1, 1),
            "packet_loss": random.uniform(0, 5),
            "latency": random.uniform(10, 100),
        }

        # Create a dictionary to hold the CDR fields
        cdr = {
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
            "imei": callee_imei,
            "imsi": imsi,
            "direction": "incoming" if call_type == "inbound" else "outgoing",
            "longitudine": longitudine_cdr,
            "latitudine": latitudine_cdr,
            "service_type": "voice",
            "billing_info": "Unknown",
            "jitter": qos_metrics["jitter"],
            "packet_loss": qos_metrics["packet_loss"],
            "latency": qos_metrics["latency"],
        }

        # Add the CDR to the list of CDRs
        cdrs.append(cdr)
        for cdr in cdrs:
            for key, value in cdr.items():
                if isinstance(value, np.int64):
                    cdr[key] = int(value)
    # return JsonResponse({"cdrs": cdrs})
    return pd.DataFrame(cdrs)
