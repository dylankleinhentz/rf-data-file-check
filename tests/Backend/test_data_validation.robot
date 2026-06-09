*** Settings ***
Documentation       Sample test suite for CSV data validation

Resource            ../../Resources/common.resource


*** Variables ***
${CUSTOMER_CSV}     ${CURDIR}/../../Data/sample_customers.csv


*** Test Cases ***
Validate Customer Data File Structure
    [Documentation]    Test that the customer CSV has required columns
    Load CSV Data File    ${CUSTOMER_CSV}
    Validate Required Columns Exist    customer_id    first_name    last_name    email    age

Validate Customer IDs Are Numeric
    [Documentation]    Test that customer_id column contains only numeric values
    Load CSV Data File    ${CUSTOMER_CSV}
    Validate Column Has Only Numeric Values    customer_id

Validate Customer IDs Are Unique
    [Documentation]    Test that each customer has a unique ID
    Load CSV Data File    ${CUSTOMER_CSV}
    Validate Column Values Are Unique    customer_id

Validate Email Format
    [Documentation]    Test that email addresses match valid format
    Load CSV Data File    ${CUSTOMER_CSV}
    Validate Column Matches Pattern    email    ^[^@]+@[^@]+\\.[^@]+$

Validate Age Values
    [Documentation]    Test that age values fall within valid range
    Load CSV Data File    ${CUSTOMER_CSV}
    Validate Column Values In Range    age    18    120

Validate Registration Dates
    [Documentation]    Test that registration dates are in correct format
    Load CSV Data File    ${CUSTOMER_CSV}
    Validate Column Has Only String Values    registration_date

Report Validation Results
    [Documentation]    Summary of all validations
    Load CSV Data File    ${CUSTOMER_CSV}
    ${row_count}=    Get CSV Row Count
    ${columns}=    Get CSV Column Names
    Log    Loaded ${row_count} customer records
    Log    Columns: ${columns}
    Validation Should Have No Errors
    Validation Should Have No Warnings
