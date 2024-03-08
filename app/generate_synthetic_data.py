from ydata_synthetic.synthesizers.regular import RegularSynthesizer
from ydata_synthetic.synthesizers import ModelParameters, TrainParameters
import pandas as pd

df_cdrs = pd.read_csv(
    "utils/sms-call-internet-mi-2013-11-01.csv",
    parse_dates=["datetime"],
)
df_cdrs = df_cdrs.fillna(0)
df_cdrs["sms"] = df_cdrs["smsin"] + df_cdrs["smsout"]
df_cdrs["calls"] = df_cdrs["callin"] + df_cdrs["callout"]

df = df_cdrs[["smsin", "smsout", "callin", "callout", "internet", "sms", "calls"]].iloc[
    :1000
]

data = df
num_cols = ["smsin", "smsout", "callin", "callout", "internet", "sms", "calls"]
cat_cols = []


synth = RegularSynthesizer(modelname="fast")
synth.fit(data=data, num_cols=num_cols, cat_cols=cat_cols)


synth_data = synth.sample(1000)
