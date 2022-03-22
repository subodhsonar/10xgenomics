import numpy as np
import pandas as pd

x = float(input("Enter volume of gel beads (ml):\n"))

max_rep = 5
i=3
flag=0
while(i<max_rep):
    for vol in range(0,50000,1):
        dil=1/(x/(x+vol))
        wash = np.power(dil,i)
        if(wash>1000):
            flag=1 
            break
    if(flag==1):
        break
    else:
        i=i+1        
            
print("Perform " + str(i) + " washes with " + str(vol) + "ml of packaging buffer for " + str(int(wash)) + "x dilution.")

y = float(input("How many ladder points would you like to package?\n"))

targets = []
for i in range(int(y)):
    target = float(input("Enter ladder point "+ str(i+1) + " \n"))
    targets.append(target)

cols = ["tube_mass","tube_gb_mass","gb_mass","vol_gb","target_vf","target_buffer_vol","target_buffer_mass","tube_gb_buffer_mass","buffer_mass","%_error","total_volume","gb_fraction"]

df = pd.DataFrame(columns=cols)
df["target_vf"] = targets

print(df)

def calc(a,b,c):
    buff_density = 1.023
    bead_density = 1.08
    gb_mass = b-a
    vol_gb = gb_mass/bead_density
    target_buffer_vol = vol_gb*((1-c)/c)
    target_buffer_mass = target_buffer_vol*buff_density
    return target_buffer_mass , gb_mass, vol_gb , target_buffer_vol

for i in range(int(y)):
    tube_mass = float(input("Enter tare weight of falcon tube for ladder point "+str(i+1)+":\n"))
    df.iat[i,0] = tube_mass
    tube_gb_mass = float(input("Enter weight of falcon tube + gel beads for ladder point "+str(i+1)+":\n"))
    df.iat[i,1] = tube_gb_mass
    a,b,c,d = calc(tube_mass,tube_gb_mass,df.iloc[i].target_vf) 
    df.iat[i,6] = a 
    df.iat[i,2] = b 
    df.iat[i,3] = c
    df.iat[i,5] = d
    print("\nAdd "+str(round(df["target_buffer_mass"][i],2))+"ml of packaging buffer to the tube.")
    
    tube_gb_buffer_mass = float(input("Enter weight of falcon tube + gel beads + buffer for ladder point "+str(i+1)+":\n"))
    df.iat[i,7] = tube_gb_buffer_mass
    buffer_mass= tube_gb_buffer_mass-tube_gb_mass
    df.iat[i,8]=buffer_mass
    error = 100*(np.abs((df["target_buffer_mass"][i]-buffer_mass)/df["target_buffer_mass"][i]))
    df.iat[i,9] = error
    df.iat[i,10] = c + buffer_mass/1.023
    df.iat[i,11] = c/df.iat[i,10]
    print("\nPercent error in adding buffer = "+ str(round(error,2)))
    print("Final volume fraction for ladder point "+str(i+1)+": "+str(round(df.iloc[i].gb_fraction,4)))

print(df)





