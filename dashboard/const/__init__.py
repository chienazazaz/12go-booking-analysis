import pandas as pd
import os

DATA = pd.read_parquet(os.path.join(os.getcwd().replace("dashboard",""),  "post_clean.parquet"))

COLOR_CODES= {
    "blue":"#3691e1",
    "orange":"#e66b3b",
    "green":"#00aa97",
    "red":"#ef605c",
    "white":"#ffffff",
}