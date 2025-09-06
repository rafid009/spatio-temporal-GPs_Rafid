import numpy as np
import pandas as pd
import sys
sys.path.append('../../experiments/')
import utils
# np.set_printoptions(threshold=np.inf)

filename_datetime = "../../data/metr-lay/metr-la-datetime.csv"
filename_speed = "../../data/metr-la/metr-la-speed.npy"
loc_filename = "../../data/metr-la/sensor_locations_la.csv"

# filename = '../../data/metr-la/metr-la.h5'


# df = pd.read_hdf(filename, 'df')
# print(f"time0: {df.index[0]}, time last: {df.index[-1]}")

# date_strings = df.index.strftime('%m/%d/%Y %H:%M:%S')  # But this may fail if freq is bad; decode first.
# new_index = pd.to_datetime(date_strings, format='%m/%d/%Y %H:%M:%S', errors='coerce')


# df.index = new_index

# df_dict = {
#     "datetime": new_index
# }

# df_new = pd.DataFrame(df_dict)
# df_new.to_csv("../../data/metr-la/metr-la-datetime.csv", index=False)
# np.save("../../data/metr-la/metr-la-speed.npy", df.values)
# exit()
# print(new_index)
# # print(df.index)
# print(df.shape)
# print(df.keys())
# print(df.values.shape)
# exit()
df_date = pd.read_csv(filename_datetime)
speed = np.load(filename_speed)
df_locs = pd.read_csv(loc_filename)
print(f"coords: {df_locs['longitude'].shape}")
coords_len = df_locs['longitude'].shape[0]


data = pd.DataFrame({
    'epoch': pd.to_datetime(df_date['datetime'])
})
print(f"data epoch before: {data['epoch']}")
data = data.loc[data.index.repeat(coords_len)].reset_index(drop=True)

time_len = df_date['datetime'].shape[0]
print(f"time len: {time_len}, coords len: {coords_len}")
data_epoch = data['epoch'].values[:int(len(data['epoch'].values)/200)]
print(f"data epoch: {data_epoch.shape}")
data_speed = speed.reshape(-1)[:int(len(speed.reshape(-1))/200)]
print(f"data speed: {data_speed.shape}")
data_longitude = np.tile(df_locs['longitude'].values, time_len)
data_longitude = data_longitude[:len(data_longitude)//200]
print(f"data longitude: {data_longitude.shape}")
data_latitude = np.tile(df_locs['latitude'].values, time_len)
data_latitude = data_latitude[:len(data_latitude)//200]
print(f"data latitude: {data_latitude.shape}")
dict_values = {
    'datetime': data_epoch,
    'longitude': data_longitude,
    'latitude': data_latitude,
    'speed': data_speed
}
print(dict_values['datetime'])
new_df = pd.DataFrame(dict_values)
new_df.replace(0, np.nan, inplace=True)
new_df['epoch'] = utils.datetime_to_epoch(new_df['datetime'])


new_df.to_csv("../../data/metr-la/clean_metrla.csv", index=False)
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