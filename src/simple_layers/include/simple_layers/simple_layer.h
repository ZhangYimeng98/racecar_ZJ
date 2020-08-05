#ifndef SIMPLE_LAYER_H_
#define SIMPLE_LAYER_H_
#include <ros/ros.h>
#include <costmap_2d/layer.h>
#include <costmap_2d/layered_costmap.h>
#include <costmap_2d/GenericPluginConfig.h>
#include <dynamic_reconfigure/server.h>
#include <std_msgs/Float64.h>
namespace simple_layer_namespace
{
 
class SimpleLayer : public costmap_2d::Layer
{
public:
  SimpleLayer();
 
  virtual void onInitialize();
  virtual void updateBounds(double origin_x, double origin_y, double origin_yaw, double* min_x, double* min_y, double* max_x,
                             double* max_y);
  virtual void updateCosts(costmap_2d::Costmap2D& master_grid, int min_i, int min_j, int max_i, int max_j);
 
private:
  void reconfigureCB(costmap_2d::GenericPluginConfig &config, uint32_t level);
  //void map_x_cb(const std_msgs::Float64& mx);
  //void map_y_cb(const std_msgs::Float64& my);
  double mark_x_, mark_y_,map__x,map__y;
  dynamic_reconfigure::Server<costmap_2d::GenericPluginConfig> *dsrv_;
};
}
#endif
