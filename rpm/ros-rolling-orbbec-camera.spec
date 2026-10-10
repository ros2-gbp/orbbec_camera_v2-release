%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

%global __cmake_in_source_build 1

Name:           ros-rolling-orbbec-camera
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
Requires:       ros-rolling-ament-index-cpp
Requires:       ros-rolling-ament-index-python
Requires:       ros-rolling-ament-lint-auto
Requires:       ros-rolling-ament-lint-common
Requires:       ros-rolling-backward-ros
Requires:       ros-rolling-builtin-interfaces
Requires:       ros-rolling-camera-info-manager
Requires:       ros-rolling-cv-bridge
Requires:       ros-rolling-diagnostic-msgs
Requires:       ros-rolling-diagnostic-updater
Requires:       ros-rolling-geometry-msgs
Requires:       ros-rolling-image-publisher
Requires:       ros-rolling-image-transport
Requires:       ros-rolling-launch
Requires:       ros-rolling-launch-ros
Requires:       ros-rolling-message-filters
Requires:       ros-rolling-orbbec-camera-msgs >= 2.10.6
Requires:       ros-rolling-rcl-interfaces
Requires:       ros-rolling-rclcpp
Requires:       ros-rolling-rclcpp-action
Requires:       ros-rolling-rclcpp-components
Requires:       ros-rolling-rclpy
Requires:       ros-rolling-rmw
Requires:       ros-rolling-sensor-msgs
Requires:       ros-rolling-statistics-msgs
Requires:       ros-rolling-std-msgs
Requires:       ros-rolling-std-srvs
Requires:       ros-rolling-tf2
Requires:       ros-rolling-tf2-msgs
Requires:       ros-rolling-tf2-ros
Requires:       ros-rolling-tf2-sensor-msgs
Requires:       yaml-cpp-devel
Requires:       ros-rolling-ros-workspace
BuildRequires:  eigen3-devel
BuildRequires:  gflags-devel
BuildRequires:  glog-devel
BuildRequires:  json-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  opencv-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  ros-rolling-ament-cmake
BuildRequires:  ros-rolling-ament-index-cpp
BuildRequires:  ros-rolling-ament-lint-auto
BuildRequires:  ros-rolling-ament-lint-common
BuildRequires:  ros-rolling-backward-ros
BuildRequires:  ros-rolling-builtin-interfaces
BuildRequires:  ros-rolling-camera-info-manager
BuildRequires:  ros-rolling-cv-bridge
BuildRequires:  ros-rolling-diagnostic-msgs
BuildRequires:  ros-rolling-diagnostic-updater
BuildRequires:  ros-rolling-geometry-msgs
BuildRequires:  ros-rolling-image-publisher
BuildRequires:  ros-rolling-image-transport
BuildRequires:  ros-rolling-message-filters
BuildRequires:  ros-rolling-orbbec-camera-msgs >= 2.10.6
BuildRequires:  ros-rolling-rcl-interfaces
BuildRequires:  ros-rolling-rclcpp
BuildRequires:  ros-rolling-rclcpp-action
BuildRequires:  ros-rolling-rclcpp-components
BuildRequires:  ros-rolling-rmw
BuildRequires:  ros-rolling-sensor-msgs
BuildRequires:  ros-rolling-statistics-msgs
BuildRequires:  ros-rolling-std-msgs
BuildRequires:  ros-rolling-std-srvs
BuildRequires:  ros-rolling-tf2
BuildRequires:  ros-rolling-tf2-msgs
BuildRequires:  ros-rolling-tf2-ros
BuildRequires:  ros-rolling-tf2-sensor-msgs
BuildRequires:  yaml-cpp-devel
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-rolling-ament-cmake-gtest
%endif

%description
Orbbec Camera package

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
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
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/rolling

%changelog
* Sat Oct 10 2026 yalian <yalian@orbbec.com> - 2.10.6-1
- Autogenerated by Bloom

