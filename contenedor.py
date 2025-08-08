import pandas as pd
import glob
import numpy as np
import os
import openpyxl
pathh= glob.glob(r"C:\Users\rvelez\Downloads\cosas\*.xls",)
dataframes=[]
for archivo in pathh:
    df=pd.read_excel(archivo,sheet_name="Lista",index_col=None)
    nombre = os.path.splitext(os.path.basename(archivo))[0]
    df["CONTENEDOR"] = nombre
    dataframes.append(df)
df_final=pd.concat(dataframes,ignore_index=False)
df_final.to_excel(r"C:\Users\rvelez\Downloads\exporta\RESUMEN1.xlsx",index_label=None)