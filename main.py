import tifffile
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

# 0. Set Parameter
img_num = 20
img_height = 271
img_width = 172
kernel_size = 3
out_path = "./image_data/output/"
if not os.path.exists(out_path):
    os.mkdir(out_path)

# 1. Import tiff
raw_img = np.zeros((img_height, img_width, img_num))
print(raw_img.shape)
for i_img in range(1,img_num+1):
    if i_img < 10:
        i_img_str = "0" + str(i_img)
    else:
        i_img_str = str(i_img)
    raw_img[:, :, i_img-1] = tifffile.imread('./image_data/HQ/frap' + i_img_str + '.tiff')

# 2. Show Image
def show_image(img, file_name):
    plt.figure()
    plt.subplot(2,1,1)
    plt.imshow(img, cmap="gray")
    plt.subplot(2,1,2)
    plt.hist(img.flatten(), bins=np.arange(256 + 1))
    plt.ylim([0,38000])
    # plt.show()
    plt.savefig(out_path + file_name)

# show_image(raw_img[:,:, 0], "raw_img.png")

# 3. Noise Removal
## median filter function
def median_filter(img, kernel_size):
    d = int((kernel_size-1)/2)
    h, w = img.shape[0], img.shape[1]

    out = img.copy()

    for y in range(d, h - d):
        for x in range(d, w - d):
            out[y][x] = np.median(img[y-d:y+d+1, x-d:x+d+1])
    return out

## execute filter function
filt_img_pkl_path = "./image_data/filt_img.pickle" 
if not os.path.exists(filt_img_pkl_path):
    filt_img = np.zeros((img_height, img_width, img_num))
    for i_img in range(img_num):
        print("Filtering img_" + str(i_img))
        filt_img[:,:, i_img] = median_filter(raw_img[:,:, i_img], kernel_size)
    with open(filt_img_pkl_path, 'wb') as out_file:
        pickle.dump(filt_img, out_file)
else:
    with open(filt_img_pkl_path, "rb") as img:
        filt_img = pickle.load(img)

## show filtered image
print(filt_img.shape)
# show_image(filt_img[:,:, 0], "filt_img.png")

# 4. Determine the ROI
## sum the amount of changes in each pixel
diff_img_pkl_path = "./image_data/diff_img.pickle" 
diff_img = np.zeros((img_height, img_width, img_num - 1))
if not os.path.exists(diff_img_pkl_path):
    for i_img in range(img_num - 1):
        print("Diff img_" + str(i_img))
        for i_height in range(img_height):
            for i_width in range(img_width):
                diff_img[i_height, i_width, i_img] += np.abs(filt_img[i_height, i_width, i_img + 1] - filt_img[i_height, i_width, i_img])
        show_image(diff_img[:,:, i_img], "diff_img_" + str(i_img))
    with open(diff_img_pkl_path, 'wb') as out_file:
        pickle.dump(diff_img, out_file)
else:
    with open(diff_img_pkl_path, "rb") as img:
        diff_img = pickle.load(img) 

max_val = 255
threshold = 128
bin_img = (diff_img[:,:, 1] > threshold) * max_val
bin_bool = (diff_img[:,:, 1] > threshold) 
show_image(bin_img, "bin_img")

# 5. Calculate the Brightness of each Image inside ROI
bright_curve = np.zeros((img_num,1))
for i_img in range(img_num):
    for i_height in range(img_height):
        for i_width in range(img_width):
            if bin_bool[i_height,i_width] == True:
                bright_curve[i_img, 0] = filt_img[i_height, i_width, i_img]

# 6. Plot the Fluorescence Recovery Curve
fig, ax = plt.subplots()
ax.plot(bright_curve)
plt.savefig(out_path + "curve.png")
plt.show()

# 7. Calculate the Diffusion Coefficient
bleach_radius = 1.0       # m
diffusion_time = 1.0      # sec
diffusion_coefficient = bleach_radius ** 2 / (4 * diffusion_time)
print("D = " + str(diffusion_coefficient))

