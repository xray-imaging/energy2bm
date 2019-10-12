import numpy as np

npixel_x = 2560
npixel_y = 2160
pixel_size_x = 6.5
pixel_size_y = 6.5
lens_magnifications = np.array([1, 2, 5, 7.5, 10])

pixel_size_x = pixel_size_x/lens_magnifications
pixel_size_y  = pixel_size_y/lens_magnifications
field_of_view_x = npixel_x*pixel_size_x
field_of_view_y = npixel_y*pixel_size_y


print("Mag      Pixel size              Field of view")
for k in range(len(lens_magnifications)):
   print("%.1fx\t %.2fum x %.2fum\t %.2fmm x %.2fmm" % (lens_magnifications[k],pixel_size_x[k],pixel_size_y[k],field_of_view_x[k]/1000,field_of_view_y[k]/1000))

