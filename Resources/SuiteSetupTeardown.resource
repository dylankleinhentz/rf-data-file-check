*** Settings ***
Documentation       Contains all variables/actions/keywords for starting/ending a suite

# Common variables used for test automation
Library             DatabaseLibrary


*** Variables ***
${PROJECT_DIR}      ${CURDIR}/../


*** Keywords ***
Setup Suite
    [Documentation]    contains all keywords which should be executed at the start of a suite
    IF    not $ENV    Fatal Error    No ENV variable was given
    ${env_vars} =    EnvVariables.Get Variables
    IF    "TST" in "${ENV}"    VAR    ${db_port} =    5432
    IF    "gcp" in "${ENV}"
        VAR    ${db_port} =    ${env_vars}[local_db_port]
        Open IAP Tunnel    ${env_vars}[project]    ${env_vars}[vm]    ${db_port}    ${env_vars}[local_sftp_port]
    END
    VAR    ${mats_db_connect_string} =
    ...    user=${env_vars}[postgre_db_username] password=${env_vars}[postgre_db_password]
    ...    host=${env_vars}[postgre_db_host] dbname=${env_vars}[postgre_db_name] port=${db_port} connect_timeout=10
    Connect To Database Using Custom Connection String    psycopg    db_connect_string=${mats_db_connect_string}

Teardown Suite
    [Documentation]    contains all keywords which should be executed at the end of a suite
    DatabaseLibrary.Disconnect From Database

Remove Specific Tags
    [Documentation]    Remove specific test tags from RF output files so these test tags are not added to JIRA test case
    Remove Tags    robot:*    PMB:*
