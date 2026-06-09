*** Settings ***
Library    Collections
Library    OperatingSystem
Library    ../../../src/libraries/CSVDataValidator.py


*** Keywords ***
Load CSV Data File
    [Arguments]    ${file_path}
    [Documentation]    Load a CSV file for validation
    ${result}=    Load Csv File    ${file_path}
    Should Be True    ${result}    File could not be loaded: ${file_path}

Validate Required Columns Exist
    [Arguments]    @{columns}
    [Documentation]    Verify that required columns exist in the CSV
    ${result}=    Validate Required Columns    ${columns}
    Should Be True    ${result}    Required column validation failed

Validate Column Has Only Numeric Values
    [Arguments]    ${column_name}
    [Documentation]    Verify all values in a column are numeric
    ${result}=    Validate Column Data Type    ${column_name}    numeric
    Should Be True    ${result}    Column contains non-numeric values: ${column_name}

Validate Column Has Only String Values
    [Arguments]    ${column_name}
    [Documentation]    Verify all values in a column are strings
    ${result}=    Validate Column Data Type    ${column_name}    string
    Should Be True    ${result}    Column contains invalid string values: ${column_name}

Validate Column Values Are Unique
    [Arguments]    ${column_name}
    [Documentation]    Verify all values in a column are unique
    ${result}=    Validate Unique Values    ${column_name}
    Should Be True    ${result}    Column contains duplicate values: ${column_name}

Validate Column Values In Range
    [Arguments]    ${column_name}    ${min_value}    ${max_value}
    [Documentation]    Verify numeric values fall within a specified range
    ${result}=    Validate Value Range    ${column_name}    ${min_value}    ${max_value}
    Should Be True    ${result}    Column values outside range: ${column_name}

Validate Column Matches Pattern
    [Arguments]    ${column_name}    ${pattern}
    [Documentation]    Verify all values match a regex pattern
    ${result}=    Validate Pattern    ${column_name}    ${pattern}
    Should Be True    ${result}    Column values don't match pattern: ${column_name}

Get CSV Row Count
    [Documentation]    Get the number of rows in the loaded CSV
    ${count}=    Get Row Count
    [Return]    ${count}

Get CSV Column Names
    [Documentation]    Get the list of column names from the CSV
    ${columns}=    Get Column Names
    [Return]    ${columns}

Print Validation Errors
    [Documentation]    Print all validation errors to log
    ${errors}=    Get Errors
    Log Many    @{errors}

Print Validation Warnings
    [Documentation]    Print all validation warnings to log
    ${warnings}=    Get Warnings
    Log Many    @{warnings}

Validation Should Have No Errors
    [Documentation]    Assert that no validation errors exist
    ${errors}=    Get Errors
    Should Be Empty    ${errors}    Validation errors found: ${errors}

Validation Should Have No Warnings
    [Documentation]    Assert that no validation warnings exist
    ${warnings}=    Get Warnings
    Should Be Empty    ${warnings}    Validation warnings found: ${warnings}

Clear Validation Messages
    [Documentation]    Clear all stored error and warning messages
    Clear Messages
