from enum import auto
from evalio.datasets import Dataset, DatasetIterator
from evalio.datasets.loaders import (
    LidarDensity,
    LidarFormatParams,
    LidarMajor,
    LidarPointStamp,
    LidarStamp,
    RosbagIter,
)
from evalio.types import Trajectory, SE3, ImuParams, LidarParams

import numpy as np


class MyRosbagDataset(Dataset):
    first_trajectory = auto()
    second_trajectory = auto()

    def data_iter(self) -> DatasetIterator:
        return RosbagIter(
            # self.folder is the location where the dataset is stored
            # It is a subdirectory under EVALIO_DATA
            path=self.folder / "temp.bag",
            imu_topic="/imu",
            lidar_topic="/lidar",
            lidar_params=self.lidar_params(),
            # These are optional - evalio will do it's best to guess row/column major and only_valid/all points
            # These are the defaults
            lidar_format=LidarFormatParams(
                major=LidarMajor.Row,
                point_stamp=LidarPointStamp.Guess,
                density=LidarDensity.Guess,
                stamp=LidarStamp.Start,
            ),
        )

    def ground_truth_raw(self) -> Trajectory:
        return Trajectory.from_tum(self.folder / "ground_truth.txt")
        # This is an alias for the following,
        return Trajectory.from_csv(
            self.folder / "ground_truth.txt",
            ["sec", "x", "y", "z", "qx", "qy", "qz", "qw"],
        )

    @staticmethod
    def url() -> str:
        return "https://github.com/contagon/evalio-example"

    def imu_T_lidar(self) -> SE3:
        return SE3.identity()

    def imu_T_gt(self) -> SE3:
        return SE3.identity()

    def imu_params(self) -> ImuParams:
        return ImuParams(
            gyro=0.01,
            accel=0.01,
            accel_bias=0.01,
            gyro_bias=0.01,
            bias_init=1e-8,
            integration=1e-8,
            gravity=np.array([0, 0, 9.81]),
        )

    def lidar_params(self) -> LidarParams:
        return LidarParams(
            num_rows=64,  # aka rings/channels/scanlines
            num_columns=1024,
            min_range=0.1,
            max_range=100.0,
        )

    def files(self) -> list[str]:
        # Lists what files should be in self.folder to check if dataset is downloaded
        return ["first_trajectory.bag", "second_trajectory.bag"]

    def download(self) -> None:
        # Implement an automatic downloader
        # This can be done using gdown
        # https://github.com/contagon/evalio/blob/master/python/evalio/datasets/multi_campus.py#L188-L263
        # Or directly using requests
        # https://github.com/contagon/evalio/blob/master/python/evalio/datasets/hilti_2022.py#L135-L147
        raise NotImplementedError("Download not implemented")
