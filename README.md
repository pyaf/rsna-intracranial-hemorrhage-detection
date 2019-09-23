# RSNA Intracranial hemorrhage detection


## Approach

1. use global windowing params, save int16 npy files (dcm.pixel_array only, 500KB), do windowing on the fly. NOPE. npy files will take a 400GB of space.






## Revelations:

1. We can use meta data, but not as input to the models.
2. Use .apply on columns, much faster than when applied on whole dataframe



## Questions:

1. How are we gonna target this competition?
2. Raw images have -2k to 4k HU values, clip the intensities? what range? see [this](https://www.kaggle.com/samusram/eda-windowing-allowed-per-rules)
2.
