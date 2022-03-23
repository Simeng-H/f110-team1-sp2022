#!/bin/bash -i

# Note: You must use a network profile (you can add this in network settings) with your desired configuration, 
# provided that it is called f1tenth

CASE=$1

PROFILE=f1tenth # Name of your f1tenth network config profile

if [ "${CASE}" = "enable" ]; then
  export ROS_MASTER_URI=http://192.168.1.1:11311
  export ROS_IP=192.168.1.105
  nmcli c up ${PROFILE}
elif [ "${CASE}" = "disable" ]; then
  unset ROS_MASTER_URI
  unset ROS_IP
  nmcli c down ${PROFILE}
else
  echo "Usage: source network.sh [enable/disable] INS";
  echo "Note: This script only works if you've configured a network profile called f1tenth in Ubuntu settings."
fi