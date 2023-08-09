docker run -it \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    --privileged \
    -e DISPLAY=$DISPLAY \
    -v /usr/lib/nvidia-384:/usr/lib/nvidia-384 \
    -v /usr/lib32/nvidia-384:/usr/lib32/nvidia-384 \
    -v ./cubli_description:/root/cubli_ws/src/cubli_description \
    -v ./cubli_gazebo:/root/cubli_ws/src/cubli_gazebo \
    --device /dev/dri \
    --name cubli_sim \
    -w /root/cubli_ws \
    cubli_sim
