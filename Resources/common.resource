*** Comments ***
# robotcode: ignore[PossibleCircularImport]


*** Settings ***
Documentation       Source of truth for declaring all the libraries, resource files and variable files

# Common variables used for test automation
# Builtin libraries of RF used in the repo
Library             Collections
Library             DateTime
Library             OperatingSystem
Library             Process
Library             String
Library             XML    use_lxml=True
Library             robot.utils
# Custom libraries used in the repo
Library             DataFiles/file_validation.py
Resource            DataFiles/data_validation.robot
