import pandas as pd 
import numpy as np 
import os
import csv 
from datetime import datetime


def csv_convert_parent(filename, parent_filename, tab_name): 
    df = pd.read_csv(filename)
    df = df.dropna()
    data = df.to_numpy()
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(parent_filename, 'a', newline = '') as f:
        write_csv = csv.writer(f)
        write_csv.writerow(f"Tab: {tab_name} - Date: {current_date}")
        write_csv.writerows(data)
    f.close()
