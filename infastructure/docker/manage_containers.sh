#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 {start|stop|restart|remove}"
  exit 1
fi

ACTION=$1
container_ids=$(sudo docker ps -q -a)

if [ -z "$container_ids" ]; then
  echo "No running containers found."
  exit 1
fi

for container_id in $container_ids; do
  echo "******************************************"
  echo "$ACTION Container: $container_id"

  case $ACTION in
    start)
      pid=$(sudo docker inspect --format '{{ .State.Pid }}' $container_id)
      sudo kill -9 "$pid"
      sudo docker start "$container_id"
      echo "Container $container_id started successfully."
      ;;
    stop)
      pid=$(sudo docker inspect --format '{{ .State.Pid }}' $container_id)
      sudo kill -9 "$pid"
      sudo docker stop "$container_id"
      echo "Container $container_id stopped successfully."
      ;;
    restart)
      pid=$(sudo docker inspect --format '{{ .State.Pid }}' $container_id)
      sudo kill -9 "$pid"
      sudo docker restart "$container_id"
      echo "Container $container_id restarted successfully."
      ;;
    remove)
      pid=$(sudo docker inspect --format '{{ .State.Pid }}' $container_id)
      sudo kill -9 "$pid"
      sudo docker container rm -f "$container_id"
      echo "Container $container_id removed successfully."
      ;;
    *)
      echo "Invalid action: $ACTION"
      echo "Usage: $0 {start|stop|restart}"
      exit 1
      ;;
  esac

  echo "******************************************"
done
