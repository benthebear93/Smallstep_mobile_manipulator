#ifndef ssmm_robot_hardware__RRBOT_SYSTEM_POSITION_ONLY_HPP_
#define ssmm_robot_hardware__RRBOT_SYSTEM_POSITION_ONLY_HPP_

#include <memory>
#include <string>
#include <vector>

#include "hardware_interface/base_interface.hpp"
#include "hardware_interface/handle.hpp"
#include "hardware_interface/hardware_info.hpp"
#include "hardware_interface/system_interface.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"
#include "hardware_interface/types/hardware_interface_status_values.hpp"
#include "rclcpp/macros.hpp"
#include "ssmm_robot_hardware/visibility_control.h"

namespace ssmm_robot_hardware
{
class RRBotSystemPositionOnlyHardware
: public hardware_interface::BaseInterface<hardware_interface::SystemInterface>
{
public:
  RCLCPP_SHARED_PTR_DEFINITIONS(RRBotSystemPositionOnlyHardware);

  SSMM_ROBOT_HARDWARE_PUBLIC
  hardware_interface::return_type configure(const hardware_interface::HardwareInfo & info) override;

  SSMM_ROBOT_HARDWARE_PUBLIC
  std::vector<hardware_interface::StateInterface> export_state_interfaces() override;

  SSMM_ROBOT_HARDWARE_PUBLIC
  std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;

  SSMM_ROBOT_HARDWARE_PUBLIC
  hardware_interface::return_type start() override;

  SSMM_ROBOT_HARDWARE_PUBLIC
  hardware_interface::return_type stop() override;

  SSMM_ROBOT_HARDWARE_PUBLIC
  hardware_interface::return_type read() override;

  SSMM_ROBOT_HARDWARE_PUBLIC
  hardware_interface::return_type write() override;

private:
  // Parameters for the RRBot simulation
  double hw_start_sec_;
  double hw_stop_sec_;
  double hw_slowdown_;

  // Store the command for the simulated robot
  std::vector<double> hw_commands_;
  std::vector<double> hw_states_;
};

}  // namespace ssmm_robot_hardware

#endif  // ssmm_robot_hardware__RRBOT_SYSTEM_POSITION_ONLY_HPP_
