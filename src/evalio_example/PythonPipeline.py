from typing import Mapping
from evalio.pipelines import Pipeline
from evalio.types import (
    SE3,
    Point,
    ImuParams,
    LidarParams,
    ImuMeasurement,
    LidarMeasurement,
)


class MyPythonPipeline(Pipeline):
    def __init__(self):
        super().__init__()

        self.param_one = True
        self.param_two = 2
        self.param_three = 3.0
        self.param_four = "four"

        self.scanlines = 0
        self.columns = 0
        self.imu_gyro_std = 0.0
        self.imu_T_lidar = SE3.identity()

        self.current_pose = SE3.identity()

        # Generally you may have a pipeline object that you simply wrap here
        # See the KissICP example for a more complex example (in C++)
        # https://github.com/contagon/evalio/blob/master/cpp/evalio/pipelines/kiss_icp.h

    # ------------------------- Info ------------------------- #
    @staticmethod
    def name():
        return "MyPythonPipeline"

    @staticmethod
    def url() -> str:
        return "https://github.com/contagon/evalio-example"

    @staticmethod
    def default_params() -> dict[str, bool | int | float | str]:
        return {
            "param1": True,
            "param2": 2,
            "param3": 3.0,
            "param4": "four",
        }

    # ------------------------- Getters ------------------------- #
    def pose(self) -> SE3:
        return self.current_pose

    def map(self) -> list[Point]:
        return []

    # ------------------------- Setters ------------------------- #
    def set_imu_params(self, params: ImuParams) -> None:
        self.imu_gyro_std = params.gyro

    def set_lidar_params(self, params: LidarParams) -> None:
        self.scanlines = params.num_rows
        self.columns = params.num_columns

    def set_imu_T_lidar(self, T: SE3) -> None:
        self.imu_T_lidar = T

    def set_params(self, params: Mapping[str, bool | int | float | str]) -> None:
        for key, value in params.items():
            match key:
                case "param1":
                    self.param_one = value
                case "param2":
                    self.param_two = value
                case "param3":
                    self.param_three = value
                case "param4":
                    self.param_four = value

    # ------------------------- Doers ------------------------- #
    def initialize(self) -> None:
        self.current_pose = SE3.identity()

    def add_imu(self, mm: ImuMeasurement) -> None:
        pass

    def add_lidar(self, mm: LidarMeasurement) -> list[Point]:
        return []
