import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Import CSV
image_num = 20

for i_img in range(1,image_num+1):
    print(i_img)
    if i_img < 10:
        i_img_str = "0" + str(i_img)
    else:
        i_img_str = str(i_img)
    print(i_img_str)
    df = pd.read_csv('./image_data/HQ/frap' + i_img_str + '.csv')

# 2. Show Image
# plt.imshow(df)
print(df)
# 3. Noise Detection

print(image_num)

# 4. Determine the ROI


# 5. Calculate the Brightness of each Image inside ROI


# 6. Plot the Fluorescence Recovery Curve


# 7. Calculate the Diffusion Coefficient


