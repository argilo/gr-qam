INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_QAM qam)

FIND_PATH(
    QAM_INCLUDE_DIRS
    NAMES qam/api.h
    HINTS $ENV{QAM_DIR}/include
        ${PC_QAM_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    QAM_LIBRARIES
    NAMES gnuradio-qam
    HINTS $ENV{QAM_DIR}/lib
        ${PC_QAM_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(QAM DEFAULT_MSG QAM_LIBRARIES QAM_INCLUDE_DIRS)
MARK_AS_ADVANCED(QAM_LIBRARIES QAM_INCLUDE_DIRS)

