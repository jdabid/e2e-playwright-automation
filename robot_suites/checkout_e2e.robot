*** Settings ***
Documentation     Flujo E2E de Checkout y Validación Financiera Decimal en Robot Framework
Library           libraries/SauceKeywords.py

*** Test Cases ***
Verificar Calculo Exacto De Subtotal E Impuestos En Checkout
    [Documentation]    Agrega dos productos al carrito y verifica precisión matemática con Decimal
    [Tags]             smoke    e2e    checkout    robot
    ${status}=         Authenticate User Session    standard_user    secret_sauce
    Should Be Equal    ${status}    AUTHENTICATED
    Add Item Price To Cart    29.99
    Add Item Price To Cart    9.99
    ${subtotal}=       Calculate Cart Subtotal
    Should Be Equal    ${subtotal}    39.98
    ${is_valid}=       Verify Order Total With Tax    ${subtotal}    3.20    43.18
    Should Be True     ${is_valid}

