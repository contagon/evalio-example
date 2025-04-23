#include "evalio/pipeline.h"
#include "evalio/types.h"

#include <nanobind/nanobind.h>
#include <nanobind/stl/map.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/variant.h>

namespace nb = nanobind;

class MyCppPipeline : public evalio::Pipeline {
public:
  MyCppPipeline() : evalio::Pipeline() {}

  // custom params
  bool param1 = true;
  int param2 = 2;
  double param3 = 3.0;
  std::string param4 = "four";

  // sensor params
  int scanlines = 0;
  int columns = 0;
  double imu_gyro_std = 0;
  evalio::SE3 imu_T_lidar = evalio::SE3::identity();

  evalio::SE3 current_pose = evalio::SE3::identity();

  // Generally you may have a pipeline object that you simply wrap here
  // See the KissICP example for a more complex example
  // https://github.com/contagon/evalio/blob/master/cpp/evalio/pipelines/kiss_icp.h

  // ------------------------- Info ------------------------- //
  static std::string name() { return "MyCppPipeline"; }

  static std::string url() {
    return "https://github.com/contagon/evalio-example";
  }

  static std::map<std::string, evalio::Param> default_params() {
    return {
        {"param1", true},
        {"param2", 2},
        {"param3", 3.0},
        // Make sure to wrap strings in std::string
        // Otherwise pybind11 will parse as a char* and coerce it into a bool
        {"param4", std::string("four")},
    };
  }

  // ------------------------- Getters ------------------------- //
  // Returns the most recent pose estimate
  const evalio::SE3 pose() override { return current_pose; }

  // Returns the current submap of the environment
  const std::vector<evalio::Point> map() override { return {}; }

  // ------------------------- Setters ------------------------- //
  // Set the IMU parameters
  void set_imu_params(evalio::ImuParams params) override {
    imu_gyro_std = params.gyro;
  }

  // Set the LiDAR parameters
  void set_lidar_params(evalio::LidarParams params) override {
    scanlines = params.num_rows;
    columns = params.num_columns;
  }

  // Set the transformation from IMU to LiDAR
  void set_imu_T_lidar(evalio::SE3 T) override { imu_T_lidar = T; }

  // Set the custom parameters
  void set_params(std::map<std::string, evalio::Param> params) override {
    for (auto &[key, value] : params) {
      if (key == "param1") {
        param1 = std::get<bool>(value);
      } else if (key == "param2") {
        param2 = std::get<int>(value);
      } else if (key == "param3") {
        param3 = std::get<double>(value);
      } else if (key == "param4") {
        param4 = std::get<std::string>(value);
      } else {
        throw std::invalid_argument("Invalid parameter: " + key);
      }
    }
  }

  // ------------------------- Doers ------------------------- //
  // Initialize the pipeline
  void initialize() override {
    // Do some initialization here
    current_pose = evalio::SE3::identity();
  }

  // Add an IMU measurement
  void add_imu(evalio::ImuMeasurement mm) override {
    // Do something with the IMU measurement
  }

  // Add a LiDAR measurement
  std::vector<evalio::Point> add_lidar(evalio::LidarMeasurement mm) override {
    // Do something with the LiDAR measurement
    return {};
  }
};

NB_MODULE(_core, m) {
  m.doc() = "Custom evalio pipeline example";

  nb::module_ evalio = nb::module_::import_("evalio");

  // Only have to override the static methods here
  // All the others will be automatically inherited from the base class
  nb::class_<MyCppPipeline, evalio::Pipeline>(m, "MyCppPipeline")
      .def(nb::init<>())
      .def_static("name", &MyCppPipeline::name)
      .def_static("url", &MyCppPipeline::url)
      .def_static("default_params", &MyCppPipeline::default_params);
}
