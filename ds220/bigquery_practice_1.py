import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/home/karen/key.json'

import bq_helper
from bq_helper import BigQueryHelper

patents = bq_helper.BigQueryHelper(active_project='patents-public-data',
                                   dataset_name='patents')

bq_assist = BigQueryHelper(active_project='patents-public-data',
                           dataset_name='patents')
df = bq_assist.head(table_name=bq_assist.list_tables()[0])

print(df.columns)

# number of publications by country
query1 = """
SELECT COUNT(*) AS cnt, country_code
FROM (
  SELECT ANY_VALUE(country_code) AS country_code
  FROM `patents-public-data.patents.publications` AS pubs
  GROUP BY application_number
)
GROUP BY country_code
ORDER BY cnt DESC
        """
#bq_assistant.estimate_query_size(query1)

applications = patents.query_to_pandas_safe(query1, max_gb_scanned=3)
print(applications.head())