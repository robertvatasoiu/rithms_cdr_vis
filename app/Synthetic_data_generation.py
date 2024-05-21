# -*- coding: utf-8 -*-
"""Generate DATA_RITHMS.ipynb

Automatically generated by Colab.

"""

from google.colab import drive

drive.mount("/content/drive")

import pandas as pd

column_names = ["data", "ora", "grp", "trunk", "durata", "format"]
cdr = pd.read_csv(
    "/content/drive/MyDrive/RITHMS/FTFILE - 05.03.2024.csv", names=column_names
)

cdr.head()

cdr.info()

cdr.format.value_counts()

cdr["format"] = cdr["format"].astype(str)

cdr = cdr.convert_dtypes()

cdr["format"] = cdr["format"].str.lstrip("0")

cdr.head()

cdr.format.value_counts()

cdr[cdr["format"] == 212322165]

cdr["format"] = cdr["format"].apply(str)

cdr.info()

cdr.format[0]

cdr["format"].str.strip()

cdr.format[0]

cdr["format"].str.replace(" ", "")

cdr.format

cdr.format[0][0:9]

cdr["format"] = cdr["format"].apply(lambda x: x[:9])

cdr.format.value_counts()

cdr.to_csv("/content/drive/MyDrive/RITHMS/cdr_prelucrat.csv")

"""# Cel prelucrat"""

df = pd.read_csv("/content/drive/MyDrive/RITHMS/cdr_prelucrat.csv")

df = df.drop(columns=["Unnamed: 0", "grp", "trunk"])

df["durata"] = pd.to_timedelta(df["durata"])

df["minute"] = df["durata"].dt.total_seconds() / 60

df.drop(columns=["durata"], inplace=True)

df["ora"] = pd.to_datetime(df["ora"])

df["ora_apel"] = df["ora"].dt.hour
df["minut_apel"] = df["ora"].dt.minute
df["secunda_apel"] = df["ora"].dt.second

df.drop(columns=["ora"], inplace=True)

df.format.value_counts()

df["format"].replace(212322165, "a", inplace=True)
df["format"].replace(212042528, "b", inplace=True)
df["format"].replace(212406415, "c", inplace=True)
df["format"].replace(213506351, "d", inplace=True)
df["format"].replace(744108318, "e", inplace=True)
df["format"].replace(723547444, "f", inplace=True)
df["format"].replace(75801145, "g", inplace=True)
df["format"].replace(758011131, "h", inplace=True)

df.format.value_counts()

df.rename(columns={"format": "apelant"}, inplace=True)

df.to_csv("/content/drive/MyDrive/RITHMS/cdr_prelucrat_final.csv", index=False)

df.rename(
    columns={
        "data": "date",
        "apelant": "caller",
        "minute": "minutes",
        "ora_apel": "call_hour",
        "minut_apel": "call_minute",
        "secunda_apel": "second_call",
    },
    inplace=True,
)

df.head()

"""# Data generation"""


from sdv.metadata import SingleTableMetadata

metadata = SingleTableMetadata()
metadata.detect_from_dataframe(df)
python_dict = metadata.to_dict()
python_dict

metadata.validate()

from sdv.lite import SingleTablePreset

synthesizer = SingleTablePreset(metadata, name="FAST_ML")
synthesizer.fit(df)

synthetic_data = synthesizer.sample(num_rows=2000)

synthetic_data.head()

print("Max call hour:", max(synthetic_data["call_hour"]))
print("Min call hour:", min(synthetic_data["call_hour"]))
print("Max call minute:", max(synthetic_data["call_minute"]))
print("Min call minute:", min(synthetic_data["call_minute"]))
print("Max call second:", max(synthetic_data["second_call"]))
print("Min call second:", min(synthetic_data["second_call"]))

max(synthetic_data.minutes)

synthetic_data.caller.value_counts()

synthetic_data.to_csv(
    "/content/drive/MyDrive/RITHMS/date_sintetice_noi.csv", index=False
)

from sdv.single_table import GaussianCopulaSynthesizer

synthesizer2 = GaussianCopulaSynthesizer(metadata)
synthesizer2.fit(df)
synthetic_data2 = synthesizer.sample(num_rows=2000)

from sdv.single_table import CTGANSynthesizer

synthesizer3 = CTGANSynthesizer(metadata)
synthesizer3.fit(df)

synthetic_data3 = synthesizer.sample(num_rows=1000)

"""## Verification"""

from sdv.evaluation.single_table import run_diagnostic, evaluate_quality
from sdv.evaluation.single_table import get_column_plot

# 1. perform basic validity checks
diagnostic = run_diagnostic(df, synthetic_data, metadata)

# 2. measure the statistical similarity
quality_report = evaluate_quality(df, synthetic_data, metadata)

# 3. plot the data
fig = get_column_plot(
    real_data=df,
    synthetic_data=synthetic_data,
    metadata=metadata,
    column_name="minutes",
)

fig.show()

from sdv.evaluation.single_table import run_diagnostic, evaluate_quality
from sdv.evaluation.single_table import get_column_plot

# 1. perform basic validity checks
diagnostic = run_diagnostic(df, synthetic_data, metadata)

# 2. measure the statistical similarity
quality_report = evaluate_quality(df, synthetic_data, metadata)

# 3. plot the data
fig = get_column_plot(
    real_data=df, synthetic_data=synthetic_data, metadata=metadata, column_name="caller"
)

fig.show()

"""## CDR processing"""

df = pd.read_csv("/content/drive/MyDrive/RITHMS/date_sintetice_noi.csv")

df.head()

df["datetime"] = (
    pd.to_datetime(df["data"], format="%d.%m.%y")
    + pd.to_timedelta(df["ora_apel"], unit="h")
    + pd.to_timedelta(df["minut_apel"], unit="m")
    + pd.to_timedelta(df["secunda_apel"], unit="s")
)

df.head()

df["secunde"] = (df["minute"] * 60).round().astype(int)

df["ora sfarsit"] = df["datetime"] + pd.to_timedelta(df["secunde"], unit="s")

df.to_csv("/content/drive/MyDrive/RITHMS/date_sintetice_noi_v1.csv", index=False)
