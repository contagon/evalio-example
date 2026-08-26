from enum import auto
from evalio.datasets import Dataset, DatasetIterator
from evalio.datasets.loaders import (
    RawDataIter,
)
from evalio.types import (
    LidarMeasurement,
    Stamp,
    Trajectory,
    SE3,
    ImuParams,
    LidarParams,
    ImuMeasurement,
)

import numpy as np


class MyRawDataset(Dataset):
    first_trajectory = auto()
    second_trajectory = auto()

    def data_iter(self) -> DatasetIterator:
        # make some fake data
        imu_data = np.random.rand(100, 6)
        imu_stamps = (Stamp.from_sec(x / 100) for x in range(100))
        imu_iter = (
            ImuMeasurement(stamp, gyro, accel)
            for stamp, gyro, accel in zip(
                imu_stamps,
                imu_data[:, :3],
                imu_data[:, 3:],
                strict=True,
            )
        )

        def lidar_iter():
            for i in range(10):
                yield LidarMeasurement(Stamp.from_sec(i / 10))

        # RawDataIter takes two iterators and interleaves measurements by timestamp.
        # This keeps data loading lazy, so scans do not need to be loaded all at once.
        # See HeLiPR for an example
        # https://github.com/contagon/evalio/blob/master/python/evalio/datasets/helipr.py#L40-L68
        return RawDataIter(
            lidar_iter(),
            imu_iter,
            10,
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
        # Generated data requires no downloaded files.
        return []

    def download(self) -> None:
        # Implement an automatic downloader
        # This can be done using gdown
        # https://github.com/contagon/evalio/blob/master/python/evalio/datasets/multi_campus.py#L188-L263
        # Or directly using requests
        # https://github.com/contagon/evalio/blob/master/python/evalio/datasets/hilti_2022.py#L135-L147
        raise NotImplementedError("Download not implemented")
