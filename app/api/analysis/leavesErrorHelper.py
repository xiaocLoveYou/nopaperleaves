import datetime
import json
import pandas as pd
import pymysql
from pandas import DataFrame, Series

from utils import *

data: DataFrame = pd.read_sql("select * from attendance", get_conn())

print(data)

