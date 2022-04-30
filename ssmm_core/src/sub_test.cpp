#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using std::placeholders::_1;
class Sub_test : public rclcpp::Node
{
    public:
        Sub_test()
        : Node("Hellohuman_subscriber")
        {
            auto qos_profile = rclcpp::QoS(rclcpp::KeepLast(10));
            sub_test_subscriber_ = this->create_subscription<std_msgs::msg::String>(
                "pub_test",
                qos_profile,
                std::bind(&Sub_test::subscribe_topic_message, this, _1));
        }
    private:
        void subscribe_topic_message(const std_msgs::msg::String::SharedPtr msg) const
        {
            RCLCPP_INFO(this->get_logger(), "Received message: '%s'", msg->data.c_str());
        }
        rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_test_subscriber_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<Sub_test>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}