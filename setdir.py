#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
#
import os.path


def _set_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
