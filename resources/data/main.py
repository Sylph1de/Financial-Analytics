import pandas as pd

from resources.utils import get_sheet

sheet = get_sheet()
records = sheet.get_all_records()
df = pd.DataFrame(records)
