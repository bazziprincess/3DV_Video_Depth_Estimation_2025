import zipfile
import os
from utils.Utils import download_url
from natsort import natsorted

test_sequences = ["2011_09_26_drive_0002",
                  "2011_09_26_drive_0005",
                  "2011_09_26_drive_0013",
                  "2011_09_26_drive_0020",
                  "2011_09_26_drive_0023",
                  "2011_09_26_drive_0036",
                  "2011_09_26_drive_0079",
                  "2011_09_26_drive_0095",
                  "2011_09_26_drive_0113",
                  "2011_09_28_drive_0037",
                  "2011_09_29_drive_0026",
                  "2011_09_30_drive_0016",
                  "2011_10_03_drive_0047"
                  ]
calib_files = ['2011_09_26_calib.zip', '2011_09_28_calib.zip', '2011_09_29_calib.zip', '2011_10_03_calib.zip']

save_dir = '../data/'
depth_annotated_dir = os.path.join(save_dir, 'data_depth_annotated.zip')

# Download KITTI Depth Prediction Dataset
base_url = 'https://s3.eu-central-1.amazonaws.com/avg-kitti/'
depth_annotated_url = base_url + "data_depth_annotated.zip"
download_url(depth_annotated_url, save_path=depth_annotated_dir, desc='Downloading KITTI Depth Prediction Dataset')

print(f"Unzipping {depth_annotated_dir}")
with zipfile.ZipFile(depth_annotated_dir, 'r') as zip_ref:
    zip_ref.extractall(depth_annotated_dir.replace('.zip', ''))

os.remove(depth_annotated_dir)

# Download calibration data for different dates
raw_kitti_dir = os.path.join(save_dir, 'raw_kitti')

for calib in calib_files:
    calib_url = base_url + 'raw_data/' + calib
    calib_save_path = os.path.join(raw_kitti_dir, calib)
    calib_extract_path = calib_save_path.replace('.zip', '')
    
    download_url(calib_url, save_path=calib_save_path, desc=f'Downloading {calib}')
    with zipfile.ZipFile(calib_save_path, 'r') as zip_ref:
        zip_ref.extractall(calib_extract_path)
    os.remove(calib_save_path)
    
    # 移动标定文件到 raw_kitti/<date>/
    date = calib.replace('_calib.zip', '')  # e.g. 2011_09_26
    source_dir = os.path.join(calib_extract_path, date)
    target_dir = os.path.join(raw_kitti_dir, date)
    os.makedirs(target_dir, exist_ok=True)
    
    for filename in ["calib_cam_to_cam.txt", "calib_imu_to_velo.txt", "calib_velo_to_cam.txt"]:
        src = os.path.join(source_dir, filename)
        dst = os.path.join(target_dir, filename)
        if os.path.exists(src):
            os.rename(src, dst)

# Download KITTI raw data sequences
sequences = {}
for split in ['train', 'val']:
    split_dir = os.path.join(save_dir, 'data_depth_annotated', split)
    sequences[split] = natsorted(os.listdir(split_dir))

all_sequences = sequences['train'] + sequences['val']
#for test
#all_sequences = [s + "_sync" for s in test_sequences]
total_sequence_num = len(all_sequences)
num = 1

for item in all_sequences:
    print(f'Download Sequence {item}: {num}/{total_sequence_num}')
    date = item.split('_drive_')[0]
    drive_name = item.replace('_sync', '')
    zip_name = f"{item}.zip"
    sequence_url = base_url + f"raw_data/{drive_name}/{zip_name}"

    zip_path = os.path.join(raw_kitti_dir, zip_name)
    download_url(sequence_url, save_path=zip_path, desc=f'Downloading {item}')

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(raw_kitti_dir) 

    os.remove(zip_path)
    num += 1

    print('Download KITTI Depth Done')