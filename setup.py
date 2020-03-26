# coding: utf-8

from cx_Freeze import setup, Executable

name="d01_"
name_postfix="tool"

executables = [Executable(name+'.py')]

setup(name=name+name_postfix,
      version='0.0.1',
      description='KSD tool app',
      executables=executables)