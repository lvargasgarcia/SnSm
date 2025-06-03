#!/bin/bash

mkdir -p build
cd build

cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)

if [ $? -ne 0 ]; then
    echo "Build failed. Please check the output for errors."
    exit 1
fi

echo "Build completed successfully."

sudo make install

if [ $? -ne 0 ]; then
    echo "Installation failed. Please check the output for errors."
    exit 1
fi

echo "Installation completed successfully."