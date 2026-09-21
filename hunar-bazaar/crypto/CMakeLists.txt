cmake_minimum_required(VERSION 3.16)
project(qr_crypto CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(qr_crypto src/main.cpp src/aes128.cpp)
target_include_directories(qr_crypto PRIVATE include)

if (NOT MSVC)
    target_compile_options(qr_crypto PRIVATE -O2 -Wall -Wextra)
endif()
