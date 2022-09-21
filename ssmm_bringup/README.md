### Launch 

```
ros2 launch ssmm_bringup ssmm_robot.launch.py
```

### publish topic

```
 ros2 topic pub /forward_position_controller/commands std_msgs/msg/Float64MultiArray "data:
- 0.5
- 0.5
- 0.2
- 0.2
- 0.2
- 0
- 0 
- 0
- 0"
```