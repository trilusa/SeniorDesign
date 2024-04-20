import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def print_df(d,name="DATAFRAME"):
    print(f"\n********** {name} ***********\n"); print(d); d.info(); print("\n")

az=100
df_hrtf = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/HRTF_df.pkl")
df_hrtf = df_hrtf.query('az == @az')


print_df(df_hrtf)