import tifffile
import numpy as np
import matplotlib.pyplot as plt

# 1. Import CSV
image_num = 20
image_data = np.zeros((271, 172, image_num))
for i_img in range(1,image_num+1):
    print(i_img)
    if i_img < 10:
        i_img_str = "0" + str(i_img)
    else:
        i_img_str = str(i_img)
    print(i_img_str)
    image_data[:, :, i_img-1] = tifffile.imread('./image_data/HQ/frap' + i_img_str + '.tiff')

# 2. Show Image
# print(image_data.shape)
# for i_img in range(image_num):
#     fig, ax = plt.subplots()
#     ax.imshow(image_data[:,:,i_img], cmap="gray")
#     plt.show()

# 3. Noise Detection


# 4. Determine the ROI


# 5. Calculate the Brightness of each Image inside ROI


# 6. Plot the Fluorescence Recovery Curve


# 7. Calculate the Diffusion Coefficient


