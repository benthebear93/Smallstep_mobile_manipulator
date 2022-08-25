#ifndef SSMM_ROBOT_HARDWARE__VISIBILITY_CONTROL_H_
#define SSMM_ROBOT_HARDWARE__VISIBILITY_CONTROL_H_

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
#ifdef __GNUC__
#define SSMM_ROBOT_HARDWARE_EXPORT __attribute__((dllexport))
#define SSMM_ROBOT_HARDWARE_IMPORT __attribute__((dllimport))
#else
#define SSMM_ROBOT_HARDWARE_EXPORT __declspec(dllexport)
#define SSMM_ROBOT_HARDWARE_IMPORT __declspec(dllimport)
#endif
#ifdef SSMM_ROBOT_HARDWARE_BUILDING_DLL
#define SSMM_ROBOT_HARDWARE_PUBLIC SSMM_ROBOT_HARDWARE_EXPORT
#else
#define SSMM_ROBOT_HARDWARE_PUBLIC SSMM_ROBOT_HARDWARE_IMPORT
#endif
#define SSMM_ROBOT_HARDWARE_PUBLIC_TYPE SSMM_ROBOT_HARDWARE_PUBLIC
#define SSMM_ROBOT_HARDWARE_LOCAL
#else
#define SSMM_ROBOT_HARDWARE_EXPORT __attribute__((visibility("default")))
#define SSMM_ROBOT_HARDWARE_IMPORT
#if __GNUC__ >= 4
#define SSMM_ROBOT_HARDWARE_PUBLIC __attribute__((visibility("default")))
#define SSMM_ROBOT_HARDWARE_LOCAL __attribute__((visibility("hidden")))
#else
#define SSMM_ROBOT_HARDWARE_PUBLIC
#define SSMM_ROBOT_HARDWARE_LOCAL
#endif
#define SSMM_ROBOT_HARDWARE_PUBLIC_TYPE
#endif

#endif  // SSMM_ROBOT_HARDWARE__VISIBILITY_CONTROL_H_