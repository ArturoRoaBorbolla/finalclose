import sys
import os
from  openperiod import openp

mon = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
yeartwo=sys.argv[1]
year = f"20{yeartwo}"
for i in range(0,12):
    m = mon[i]
    period=f"{m}-{yeartwo}" 
    openp(period)
    period=f"{m}-{year}" 
    openp(period)
    if len(str(i))==1:
        m=f"0{i}"
    period=f"{m}-{yeartwo}" 
    openp(period)
    period=f"{m}-{year}" 
    openp(period)