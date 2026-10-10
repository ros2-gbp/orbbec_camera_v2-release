%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/lyrical/.*$
%global __requires_exclude_from ^/opt/ros/lyrical/.*$

%global __cmake_in_source_build 1

Name:           ros-lyrical-orbbec-camera
Version:        2.10.6
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS orbbec_camera package

License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       eigen3-devel
Requires:       gflags-devel
Requires:       glog-devel
Requires:       json-devel
Requires:       mesa-libGL-devel
Requires:       mesa-libGLU-devel
Requires:       opencv-devel
Requires:       openssl-devel
Requires:       python%{python3_pkgversion}-psutil
Requires:       python%{python3_pkgversion}-yaml
Requires:       python3-tabulate
Requires:       ros-lyrical-ament-index-cpp
Requires:       ros-lyrical-ament-index-python
Requires:       ros-lyrical-ament-lint-auto
Requires:       ros-lyrical-ament-lint-common
Requires:       ros-lyrical-backward-ros
Requires:       ros-lyrical-builtin-interfaces
Requires:       ros-lyrical-camera-info-manager
Requires:       ros-lyrical-cv-bridge
Requires:       ros-lyrical-diagnostic-msgs
Requires:       ros-lyrical-diagnostic-updater
Requires:       ros-lyrical-geometry-msgs
Requires:       ros-lyrical-image-publisher
Requires:       ros-lyrical-image-transport
Requires:       ros-lyrical-launch
Requires:       ros-lyrical-launch-ros
Requires:       ros-lyrical-message-filters
Requires:       ros-lyrical-orbbec-camera-msgs >= 2.10.6
Requires:       ros-lyrical-rcl-interfaces
Requires:       ros-lyrical-rclcpp
Requires:       ros-lyrical-rclcpp-action
Requires:       ros-lyrical-rclcpp-components
Requires:       ros-lyrical-rclpy
Requires:       ros-lyrical-rmw
Requires:       ros-lyrical-sensor-msgs
Requires:       ros-lyrical-statistics-msgs
Requires:       ros-lyrical-std-msgs
Requires:       ros-lyrical-std-srvs
Requires:       ros-lyrical-tf2
Requires:       ros-lyrical-tf2-msgs
Requires:       ros-lyrical-tf2-ros
Requires:       ros-lyrical-tf2-sensor-msgs
Requires:       yaml-cpp-devel
Requires:       ros-lyrical-ros-workspace
BuildRequires:  eigen3-devel
BuildRequires:  gflags-devel
BuildRequires:  glog-devel
BuildRequires:  json-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  opencv-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  ros-lyrical-ament-cmake
BuildRequires:  ros-lyrical-ament-index-cpp
BuildRequires:  ros-lyrical-ament-lint-auto
BuildRequires:  ros-lyrical-ament-lint-common
BuildRequires:  ros-lyrical-backward-ros
BuildRequires:  ros-lyrical-builtin-interfaces
BuildRequires:  ros-lyrical-camera-info-manager
BuildRequires:  ros-lyrical-cv-bridge
BuildRequires:  ros-lyrical-diagnostic-msgs
BuildRequires:  ros-lyrical-diagnostic-updater
BuildRequires:  ros-lyrical-geometry-msgs
BuildRequires:  ros-lyrical-image-publisher
BuildRequires:  ros-lyrical-image-transport
BuildRequires:  ros-lyrical-message-filters
BuildRequires:  ros-lyrical-orbbec-camera-msgs >= 2.10.6
BuildRequires:  ros-lyrical-rcl-interfaces
BuildRequires:  ros-lyrical-rclcpp
BuildRequires:  ros-lyrical-rclcpp-action
BuildRequires:  ros-lyrical-rclcpp-components
BuildRequires:  ros-lyrical-rmw
BuildRequires:  ros-lyrical-sensor-msgs
BuildRequires:  ros-lyrical-statistics-msgs
BuildRequires:  ros-lyrical-std-msgs
BuildRequires:  ros-lyrical-std-srvs
BuildRequires:  ros-lyrical-tf2
BuildRequires:  ros-lyrical-tf2-msgs
BuildRequires:  ros-lyrical-tf2-ros
BuildRequires:  ros-lyrical-tf2-sensor-msgs
BuildRequires:  yaml-cpp-devel
BuildRequires:  ros-lyrical-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-lyrical-ament-cmake-gtest
%endif

%description
Orbbec Camera package

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/lyrical/setup.sh" ]; then . "/opt/ros/lyrical/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/lyrical" \
    -DAMENT_PREFIX_PATH="/opt/ros/lyrical" \
    -DCMAKE_PREFIX_PATH="/opt/ros/lyrical" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/lyrical/setup.sh" ]; then . "/opt/ros/lyrical/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/lyrical/setup.sh" ]; then . "/opt/ros/lyrical/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/lyrical

%changelog
* Sat Oct 10 2026 yalian <yalian@orbbec.com> - 2.10.6-1
- Autogenerated by Bloom

