import numpy as np
import pandas as pd
import sys
sys.path.append('../../experiments/')
import utils

filename = "../../data/pems_bay/pems-bay.h5"
loc_filename = "../../data/pems_bay/sensor_locations_bay.csv"

# h5 = h5py.File(filename,'r')

# print(list(h5['speed'].keys()))
# print(h5['speed']['block0_values'][0:-1].shape)
# print(h5['df'].values)

# h5.close()
# def get_train_test_locations(df_values):
#     all_locs = np.arange(df_values.shape[1])
#     train_locs = np.random.choice(all_locs, size=int(df_values.shape[1] * 0.8), replace=False)
#     test_locs = np.setdiff1d(all_locs, train_locs)  # All indices not in train_locs
#     return train_locs, test_locs

# def get_segmented_data(df, window_length):
#     df[df==0] = np.nan
#     n, num_cols = df.shape  # n rows, 325 columns

#     rows_per_segment = window_length

#     # Determine how many complete segments of 288 rows we need (ceiling division)
#     num_segments = int(np.ceil(n / rows_per_segment))

#     # Total rows required after padding
#     total_rows = num_segments * rows_per_segment

#     # Compute how many rows need to be padded
#     pad_rows = total_rows - n

#     # Pad the array with zeros along the row axis (axis 0)
#     padded_data = np.pad(df, pad_width=((0, pad_rows), (0, 0)), mode='constant', constant_values=0)

#     # Reshape into (-1, 288, 325)
#     return padded_data.reshape(num_segments, rows_per_segment, num_cols)
    # return df.reshape(-1, window_length, df.shape[1])

# def separate_train_test():
#     pass

# window_length = 12
df = pd.read_hdf(filename, 'speed')
# print(f"time0: {df.index[0]}, time last: {df.index[-1]}")

# if hasattr(df.index, 'freq') and isinstance(df.index.freq, (bytes, np.bytes_)):
#     df.index.freq = df.index.freq.decode('utf-8')
# print(pd.to_datetime(df.index, format='%m/%d/%Y %H:%M:%S', errors='coerce'))

date_strings = df.index.strftime('%m/%d/%Y %H:%M:%S')  # But this may fail if freq is bad; decode first.
new_index = pd.to_datetime(date_strings, format='%m/%d/%Y %H:%M:%S', errors='coerce')
df.index = new_index
print(new_index)
# print(df.index)
print(df.shape)
print(df.keys())
print(df.values.shape)

df_locs = pd.read_csv(loc_filename)
print(f"coords: {df_locs['longitude'].shape}")
coords_len = df_locs['longitude'].shape[0]
time_len = new_index.shape[0]

data = pd.DataFrame({
    'epoch': new_index
})
data = data.loc[data.index.repeat(coords_len)].reset_index(drop=True)
print(f"data: {data}")

dict_values = {
    'datetime': data['epoch'].values,
    'longitude': np.tile(df_locs['longitude'].values, time_len),
    'latitude': np.tile(df_locs['latitude'].values, time_len),
    'speed': df.values.reshape(-1)
}
new_df = pd.DataFrame(dict_values)
new_df.replace(0, np.nan, inplace=True)
new_df['epoch'] = utils.datetime_to_epoch(new_df['datetime'])
new_df.to_csv("data/pems_bay/clean_pemsbay.csv", index=False)
# 

# train_loc_indices, test_loc_indices = get_train_test_locations(df.values)

# train_locs = df_locs.iloc[train_loc_indices][['longitude', 'latitude']]
# test_locs = df_locs.iloc[test_loc_indices][['longitude', 'latitude']]

# total_locs = df_locs[['longitude', 'latitude']]

# total_data = get_segmented_data(df.values, window_length)
# print(f"total data: {total_data.shape}")

# test_start = int(total_data.shape[0] * 0.8)
# train_data = total_data[:test_start, :, train_loc_indices]
# test_data = total_data[test_start:, :, test_loc_indices]
# test_train_data = total_data[test_start:, :, train_loc_indices]

# print(f"train: {train_data.shape}, test: {test_data.shape}")

# folder = "./data/pems_bay"
# np.save(f"{folder}/test_nodes.npy", test_loc_indices)
# np.save(f"{folder}/X_train.npy", train_data)
# np.save(f"{folder}/X_test_test.npy", test_data)
# np.save(f"{folder}/X_test_train.npy", test_train_data)


# np.save(f"{folder}/X_total_locs.npy", total_locs)
# np.save(f"{folder}/X_train_locs.npy", train_locs)
# np.save(f"{folder}/X_test_locs.npy", test_locs)