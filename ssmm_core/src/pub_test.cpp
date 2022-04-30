#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class Pub_test : public rclcpp::Node
{
    public:
    Pub_test()
    : Node("pub_test"), count_(0)
    {
        auto qos_profile = rclcpp::QoS(rclcpp::KeepLast(0));
        pub_test_publisher_ = this->create_publisher<std_msgs::msg::String>("pub_test", qos_profile);
        timer_ = this-> create_wall_timer(1s, std::bind(&Pub_test::pub_test_msg, this));
    }
    private:
    void pub_test_msg()
    {
        auto msg = std_msgs::msg::String();
        msg.data = "pub test :" + std::to_string(count_++);
        RCLCPP_INFO(this->get_logger(), "Published msg : '%s' ", msg.data.c_str());
        pub_test_publisher_->publish(msg);
    }
    rclcpp::TimerBase::SharedPtr timer_;
    
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr pub_test_publisher_;
    size_t count_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<Pub_test>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}