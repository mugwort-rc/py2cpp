#! /usr/bin/env bash

script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
project_dir="$script_dir/.."

pyuic4 "$project_dir/ui/mainwindow.ui" -o "$project_dir/ui/mainwindow.py"
