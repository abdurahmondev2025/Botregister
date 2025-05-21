import pandas as pd
import numpy as np
from pandas import Series

# x = pd.DataFrame({'A': list(range(1,11) )})
# y = pd.Series([1.4, 4.5,np.nan,3.5,6])
# dates = pd.date_range('20250512',periods=7)
# print(x)
# print(y)
# print(dates)
dates = pd.date_range('20250505',periods=7)
df = pd.DataFrame(np.random.randn(7,3), index=dates,columns=list('ABC'))
df2 = pd.DataFrame({
    "A": 1.0,
    "B": pd.Timestamp("20250505"),
    "C": pd.Series(list(range(1,5)), index=list(range(4)),dtype="float32"),
})
print(df2)
print(df)
