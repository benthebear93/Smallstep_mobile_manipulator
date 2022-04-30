# Set minimum required version of cmake, project name and compile options
cmake_minimum_required(VERSION 3.5)
project(ssmm_core)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# Build
add_executable(pub_test src/pub_test.cpp)
ament_target_dependencies(pub_test rclcpp std_msgs)

add_executable(sub_test src/sub_test.cpp)
ament_target_dependencies(sub_test rclcpp std_msgs)

# Install
install(TARGETS
  pub_test
  sub_test
  DESTINATION lib/${PROJECT_NAME})

# Test
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

# Macro for ament package
ament_package()