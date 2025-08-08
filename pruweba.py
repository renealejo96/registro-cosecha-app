import pandas as pd
import glob
import numpy as np
import openpyxl
pathh= glob.glob(r"C:\Users\rvelez\OneDrive - Elite Flower\KELLY ZNH\PRACTICAR\2519\*.xlsx",)
dataframes=[]
for archivo in pathh:
    df=pd.read_excel(archivo,sheet_name="DATOS",index_col=None)
    dataframes.append(df)
df_final=pd.concat(dataframes,ignore_index=False)
df_final.to_excel(r"C:\Users\rvelez\Downloads\exporta\RESUMEN.xlsx",index_label=None)