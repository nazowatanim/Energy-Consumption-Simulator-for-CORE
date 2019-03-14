
#import psutil
#import subprocess
#p=subprocess.call(['ps', '-aux'])
import os
import pandas as pd
#print (p.USER)
output_lines2=[s.split() for s in os.popen("pidstat -dl").read().splitlines()]
df_disc=pd.DataFrame(output_lines2)
df3=(df_disc.iloc[3:,3])        #take read_to_disc parameter column only
df4=(df_disc.iloc[3:,4]) 
print(df3)
print(df4)