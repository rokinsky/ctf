#!/usr/bin/env bash

socat tcp4-listen:13370,fork,reuseaddr exec:python3\ -u\ srv_osx.py
