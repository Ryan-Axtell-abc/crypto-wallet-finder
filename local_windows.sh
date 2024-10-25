#!/usr/bin/bash

# Remove the build directory
rm -rf _build/

# Configure Meson for Windows installation
meson --prefix /mingw64 _build && cd _build

# Compile the project
meson compile

# Install the project
meson install