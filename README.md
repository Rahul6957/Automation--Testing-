# Automation--Testing-
Automation testing using Playwright


*************************************************************************************************************************************************************************************************************************testing set up *************


mkdir TFLCoMentor-Automation
cd TFLCoMentor-Automation
python -m venv venv
venv\Scripts\activate
pip install pytest pytest-playwright
playwright install chromium
**** it create venv  it enverment foldet dont modiffy
pip freeze > requirements.txt ********************
run command =  pytest tests/test_authentication.py -v
##################### Test Case #########################
Test ID	Test Scenario
TC_AUTH_001	Verify website loading ✅

TC_AUTH_002 – Verify Sign In Option✅
check sign in button is vissible on home page 

TC_AUTH_003 – Verify Sign In Navigation✅
Objective: Sign In वर click केल्यावर Login Page open होतो का ते तपासणे.

TC_AUTH_04	Login with valid credentials✅

TC_AUTH_05	Login with invalid credentials

TC_AUTH_06	Login with empty fields
TC_AUTH_07	Verify Register page opens
TC_AUTH_08	Register with valid details
TC_AUTH_09	Register with existing email
TC_AUTH_010	Verify Logout
