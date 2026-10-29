*** Settings ***
Documentation     Suite de Pruebas Automatizadas de Autenticación con Robot Framework y Python
Library           libraries/SauceKeywords.py

*** Variables ***
${VALID_USER}         standard_user
${LOCKED_USER}        locked_out_user
${VALID_PASSWORD}     secret_sauce
${LOCKED_MSG}         Epic sadface: Sorry, this user has been locked out.
${MISSING_USER_MSG}   Epic sadface: Username is required

*** Test Cases ***
Verificar Inicio De Sesion Exitoso Con Usuario Estandar
    [Documentation]    Valida que un usuario activo pueda autenticarse correctamente
    [Tags]             smoke    auth    robot
    ${status}=         Authenticate User Session    ${VALID_USER}    ${VALID_PASSWORD}
    Should Be Equal    ${status}    AUTHENTICATED

Verificar Bloqueo De Seguridad Para Usuario Locked Out
    [Documentation]    Valida que el usuario bloqueado reciba el banner de error esperado
    [Tags]             smoke    security    robot
    ${status}=         Authenticate User Session    ${LOCKED_USER}    ${VALID_PASSWORD}
    ${error}=          Get Last Error Banner
    Should Be Equal    ${status}    LOCKED
    Should Be Equal    ${error}     ${LOCKED_MSG}

Verificar Validacion De Campo Usuario Vacio
    [Documentation]    Valida el mensaje de error cuando se omite el nombre de usuario
    [Tags]             regression    bva    robot
    ${status}=         Authenticate User Session    ${EMPTY}    ${VALID_PASSWORD}
    ${error}=          Get Last Error Banner
    Should Be Equal    ${status}    ERROR
    Should Be Equal    ${error}     ${MISSING_USER_MSG}

