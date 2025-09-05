import numpy as np
import pandas as pd
import sys
sys.path.append('../../experiments/')
import utils

filename_datetime = "../../data/pems_bay/pems-bay-datetime.csv"
filename_speed = "../../data/pems_bay/pems-bay-speed.npy"
loc_filename = "../../data/pems_bay/sensor_locations_bay.csv"

df_date = pd.read_csv(filename_datetime)

# df = pd.read_hdf(filename, 'speed')
# print(f"time0: {df.index[0]}, time last: {df.index[-1]}")

date_strings = df_date['datetime'] #.strftime('%m/%d/%Y %H:%M:%S')  # But this may fail if freq is bad; decode first.
new_index = pd.to_datetime(date_strings, format='%m/%d/%Y %H:%M:%S', errors='coerce')

speed = np.load(filename_speed)
# df.index = new_index

# df_dict = {
#     "datetime": new_index
# }

# df_new = pd.DataFrame(df_dict)
# df_new.to_csv("../../data/pems_bay/pems-bay-datetime.csv", index=False)
# np.save("../../data/pems_bay/pems-bay-speed.npy", df.values)

# print(new_index)
# # print(df.index)
# print(df.shape)
# print(df.keys())
# print(df.values.shape)
# exit()
df_locs = pd.read_csv(loc_filename)
print(f"coords: {df_locs['longitude'].shape}")
coords_len = df_locs['longitude'].shape[0]
time_len = new_index.shape[0]

data = pd.DataFrame({
    'epoch': new_index
})
data = data.loc[data.index.repeat(coords_len)].reset_index(drop=True)
# print(f"data: {data}")

dict_values = {
    'datetime': data['epoch'].values,
    'longitude': np.tile(df_locs['longitude'].values, time_len),
    'latitude': np.tile(df_locs['latitude'].values, time_len),
    'speed': speed.reshape(-1)
}
new_df = pd.DataFrame(dict_values)
new_df.replace(0, np.nan, inplace=True)
new_df['epoch'] = utils.datetime_to_epoch(new_df['datetime'])


new_df.to_csv("../../data/pems_bay/clean_pemsbay.csv", index=False)
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