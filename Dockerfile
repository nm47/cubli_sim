FROM ros:rolling

ENV WS /root/dev
ENV ROS_PATH $WS/ros2_ws
ENV GAZEBO_PATH $WS/gazebo
ENV ROS_DISTRIBUTION rolling
ENV DEBIAN_FRONTEND noninteractive

# Install essentials
RUN \
	apt-get update \
	&& apt-get upgrade -y \
	&& apt-get install -y \
		curl \
		git \
		tmux \
		unzip \
		vim \
		wget \
	&& rm -rf /var/lib/apt/lists/*

# Setup gazebo
RUN \
        curl -sSL http://get.gazebosim.org | sh

# ROS env sourcing
RUN \
    echo 'source /root/cubli_ws/install/setup.bash' >> ~/.bashrc \
    echo 'source /opt/ros/rolling/setup.bash' >> ~/.bashrc \
    source ~/.bashrc
