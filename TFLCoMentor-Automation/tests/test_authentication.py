# check sign in button is vissible on home page 
def test_signin_button_visible(page): 
    page.goto("http://localhost:8081/")
    signin = page.get_by_text("Sign In")
    assert signin.is_visible()



def test_signin_navigation(page):
    page.goto("http://localhost:8081/")
    page.get_by_text("Sign In").click()
    assert page.url == "http://localhost:8081/models/membership/Login"


import pytest

@pytest.mark.parametrize("role, dashboard", [
    ("Student", "DashboardStudent"),
    ("Mentor", "DashboardMentor"),
    ("SME", "DashboardSME"),
    ("Employer", "DashboardEmployer"),
    ("Alumni", "DashboardAlumni"),
])

def test_role_login(page, role, dashboard):

    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_label("Contact Number").fill("7972542628")

    page.get_by_role("combobox").click()
    page.get_by_role("option", name=role).click()

    page.get_by_label("Password").fill("12345")

    page.get_by_role("button", name="Login").click()

    page.wait_for_url("**/models/membership/dashboard")

    assert page.url.endswith("/models/membership/dashboard")


def test_invalid_login(page):
    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_label("Contact Number").fill("7972542628")
    page.get_by_role("combobox").click()
    page.get_by_role("option", name="Student").click()
    page.get_by_label("Password").fill("wrongpassword")

    def verify_dialog(dialog):
        assert dialog.message == "Invalid Credentials..!"
        dialog.accept()

    page.once("dialog", verify_dialog)

    page.get_by_role("button", name="Login").click()



def test_wrong_role_login(page):
    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_label("Contact Number").fill("9130240968")

    page.get_by_role("combobox").click()
    page.get_by_role("option", name="Mentor").click()

    page.get_by_label("Password").fill("12345")

    page.get_by_role("button", name="Login").click()

    page.wait_for_timeout(2000)

    assert page.url.endswith("/models/membership/Login")

def test_empty_role(page):
    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_label("Contact Number").fill("9130240968")
    page.get_by_label("Password").fill("12345")

    messages = []

    page.once("dialog", lambda dialog: (
        messages.append(dialog.message),
        dialog.accept()
    ))

    page.get_by_role("button", name="Login").click()

    assert messages == ["Please select a role"]



def test_empty_password(page):
    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_label("Contact Number").fill("9130240968")

    page.get_by_role("combobox").click()
    page.get_by_role("option", name="Student").click()

    print("Password value:",
          page.get_by_label("Password").input_value())

    print("Password required:",
          page.get_by_label("Password").get_attribute("required"))

    print("Password validity:",
          page.get_by_label("Password").evaluate(
              "(element) => element.validity.valid"
          ))

    page.get_by_role("button", name="Login").click()




def test_empty_contact_number(page):
    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_role("combobox").click()
    page.get_by_role("option", name="Student").click()
    page.get_by_label("Password").fill("12345")

    contact = page.get_by_label("Contact Number")

    print("Contact value:", contact.input_value())
    print("Required:", contact.get_attribute("required"))
    print("Validity:", contact.evaluate(
        "(element) => element.validity.valid"
    ))

    page.get_by_role("button", name="Login").click()




def test_register_navigation(page):
    page.goto("http://localhost:8081/models/membership/Login")

    register = page.get_by_text("Register Now", exact=True)

    print("Tag name:", register.evaluate("(element) => element.tagName"))
    print("HTML:", register.evaluate("(element) => element.outerHTML"))

    
import time
def test_register_valid_details(page):
    page.goto("http://localhost:8081/models/membership/Register")

    unique_id = str(time.time_ns())[-8:]

    page.get_by_label("First Name").fill("Rahul")
    page.get_by_label("Last Name").fill("Gaike")
    page.get_by_label("Email").fill(f"rahul{unique_id}@example.com")
    page.get_by_label("Contact").fill(f"98765{unique_id[-5:]}")

    page.get_by_role("button", name="Register").click()

    page.get_by_text("Registration successful").wait_for(
        state="visible",
        timeout=10000
    )

    page.wait_for_url("**/models/membership/Login", timeout=10000)

    assert page.url.endswith("/Login")


def test_register_existing_email(page):
    page.goto("http://localhost:8081/models/membership/Register")

    page.get_by_label("First Name").fill("Rahul")
    page.get_by_label("Last Name").fill("Gayke")
    page.get_by_label("Email").fill("rahulgayke1704@gmail.com")
    page.get_by_label("Contact").fill("9130240968")

    page.get_by_role("button", name="Register").click()

    page.get_by_text("Email already exists").wait_for(
        state="visible",
        timeout=10000
    )

def test_sme_login(page):

    with page.expect_response(
        lambda response: (
            "/roles/getAllRoles" in response.url and response.ok
        )
    ) as roles_response_info:
        page.goto("http://localhost:8081/models/membership/Login")

    roles_data = roles_response_info.value.json()["data"]
    sme_role = next(
        role for role in roles_data
        if role["role_name"].strip().lower() == "sme"
    )

    page.get_by_label("Contact Number").fill("7972542628")

    page.get_by_role("combobox").click()
    page.get_by_role("option", name="SME").click()

    page.get_by_label("Password").fill("12345")

    page.get_by_role("button", name="Login").click()
    page.wait_for_url("**/models/membership/dashboard")

    assert page.url.endswith("/models/membership/dashboard")

    current_user = page.evaluate(
        "() => JSON.parse(sessionStorage.getItem('current') || '{}')"
    )
    assert current_user["role_id"] == sme_role["role_id"]


def test_sme_dashboard_tests_created_visible(page):
    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_label("Contact Number").fill("7972542628")

    page.get_by_role("combobox").click()
    page.get_by_role("option", name="SME").click()

    page.get_by_label("Password").fill("12345")
    page.get_by_role("button", name="Login").click()

    page.wait_for_url("**/models/membership/dashboard")

    tests_created_option = page.get_by_text("Tests Created", exact=True)
    assert tests_created_option.is_visible()

def test_sme_tests_created_opens_assessments_page(page):
    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_label("Contact Number").fill("7972542628")

    page.get_by_role("combobox").click()
    page.get_by_role("option", name="SME").click()

    page.get_by_label("Password").fill("12345")
    page.get_by_role("button", name="Login").click()

    page.wait_for_url("**/models/membership/dashboard")

    tests_created_card = page.get_by_text("Tests Created", exact=True)
    assert tests_created_card.is_visible()

    tests_created_card.click()

    page.wait_for_url("**/models/created-assessments")

    assert page.url == "http://localhost:8081/models/created-assessments"


def test_create_test_button_visible(page):
    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_label("Contact Number").fill("7972542628")

    page.get_by_role("combobox").click()
    page.get_by_role("option", name="SME").click()

    page.get_by_label("Password").fill("12345")
    page.get_by_role("button", name="Login").click()

    page.wait_for_url("**/models/membership/dashboard")

    page.get_by_text("Tests Created", exact=True).click()
    page.wait_for_url("**/models/created-assessments")

    create_test_button = page.get_by_role("button", name="Create Test")
    assert create_test_button.is_visible()



def test_create_test_button_visible(page):
    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_label("Contact Number").fill("7972542628")

    page.get_by_role("combobox").click()
    page.get_by_role("option", name="SME").click()

    page.get_by_label("Password").fill("12345")
    page.get_by_role("button", name="Login").click()

    page.wait_for_url("**/models/membership/dashboard")

    page.get_by_text("Tests Created", exact=True).click()
    page.wait_for_url("**/models/created-assessments")

    create_test_button = page.get_by_role("button", name="Create Test")
    assert create_test_button.is_visible()


def test_create_test_opens_create_test_page(page):
    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_label("Contact Number").fill("7972542628")

    page.get_by_role("combobox").click()
    page.get_by_role("option", name="SME").click()
    page.get_by_label("Password").fill("12345")
    page.get_by_role("button", name="Login").click()
    page.wait_for_url("**/models/membership/dashboard")
    page.get_by_text("Tests Created", exact=True).click()
    page.wait_for_url("**/models/created-assessments")
    create_test_button = page.get_by_role("button", name="Create Test")
    assert create_test_button.is_visible()
    create_test_button.click()
    page.wait_for_url("**/models/create-test")
    assert page.url == "http://localhost:8081/models/create-test"



def test_create_test_opens_question_setup(page):
    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_label("Contact Number").fill("7972542628")
    page.get_by_role("combobox").click()
    page.get_by_role("option", name="SME").click()
    page.get_by_label("Password").fill("12345")
    page.get_by_role("button", name="Login").click()

    page.wait_for_url("**/models/membership/dashboard")

    page.get_by_text("Tests Created", exact=True).click()
    page.wait_for_url("**/models/created-assessments")

    page.get_by_role("button", name="Create Test").click()
    page.wait_for_url("**/models/create-test")

    page.get_by_placeholder("Enter test name").fill("Automation Test")
    page.locator("select[name='difficultyLevel']").select_option("BEGINNER")
    page.get_by_placeholder("Enter description").fill(
        "Test created for automation verification."
    )
    page.get_by_placeholder("Enter duration").fill("55")

    page.get_by_role("button", name="Create New Test").click()

    page.wait_for_url("**/models/question-options")

    assert page.url == "http://localhost:8081/models/question-options"
    question_setup = page.get_by_text("Question Setup", exact=True)
    question_setup.wait_for(state="visible", timeout=10000)
    assert question_setup.is_visible()
    assert page.get_by_text("Test: Automation Test").is_visible()


def test_add_question(page):
    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_label("Contact Number").fill("7972542628")
    page.get_by_role("combobox").click()
    page.get_by_role("option", name="SME").click()
    page.get_by_label("Password").fill("12345")
    page.get_by_role("button", name="Login").click()

    page.wait_for_url("**/models/membership/dashboard")

    page.get_by_text("Tests Created", exact=True).click()
    page.wait_for_url("**/models/created-assessments")

    page.get_by_role("button", name="Create Test").click()
    page.wait_for_url("**/models/create-test")

    page.get_by_placeholder("Enter test name").fill("Automation Test")
    page.locator("select[name='difficultyLevel']").select_option("BEGINNER")
    page.get_by_placeholder("Enter description").fill(
        "Test created for question automation."
    )
    page.get_by_placeholder("Enter duration").fill("55")

    page.get_by_role("button", name="Create New Test").click()
    page.wait_for_url("**/models/question-options")

    page.get_by_text("Question Setup", exact=True).wait_for(
        state="visible",
        timeout=10000,
    )

    question_type = page.get_by_role("combobox").nth(0)
    question_type.click()
    page.get_by_role("option", name="MCQ").click()

    skill_level = page.get_by_role("combobox").nth(1)
    skill_level.click()
    page.get_by_role("option", name="Beginner").click()

    status = page.get_by_role("combobox").nth(2)
    status.click()
    page.get_by_role("option", name="Approved").click()
    page.get_by_role("button", name="Add Questions").click()

    page.get_by_placeholder("Enter Question").fill(
        "Which platform runs Java applications?"
    )
    page.get_by_placeholder("Framework").fill("Spring")
    page.get_by_placeholder("Concept").fill("Java Virtual Machine")
    page.get_by_placeholder("Option A").fill("JVM")
    page.get_by_placeholder("Option B").fill("JDK")
    page.get_by_placeholder("Option C").fill("JRE")
    page.get_by_placeholder("Option D").fill("Javadoc")

    page.locator("select").last.select_option(label="Option A")



    with page.expect_event("dialog") as dialog_info:
        page.get_by_role("button", name="Submit").click()

    dialog = dialog_info.value
    assert dialog.message == "Question Saved Successfully ✅"
    dialog.accept()


def test_create_test_with_selected_questions(page):
    page.goto("http://localhost:8081/models/membership/Login")

    page.get_by_label("Contact Number").fill("7972542628")
    page.get_by_role("combobox").click()
    page.get_by_role("option", name="SME").click()
    page.get_by_label("Password").fill("12345")
    page.get_by_role("button", name="Login").click()

    page.wait_for_url("**/models/membership/dashboard")

    page.get_by_text("Tests Created", exact=True).click()
    page.wait_for_url("**/models/created-assessments")

    page.get_by_role("button", name="Create Test").click()
    page.wait_for_url("**/models/create-test")


    page.get_by_placeholder("Enter test name").fill("Automation Test")
    page.locator("select[name='difficultyLevel']").select_option("BEGINNER")
    page.get_by_placeholder("Enter description").fill(
        "Test created for question selection automation."
    )
    page.get_by_placeholder("Enter duration").fill("55")

    page.get_by_role("button", name="Create New Test").click()
    page.wait_for_url("**/models/question-options")

    page.get_by_text("Question Setup", exact=True).wait_for(
        state="visible",
        timeout=10000,
    )


    question_type = page.get_by_role("combobox").nth(0)
    question_type.click()
    page.get_by_role("option", name="MCQ").click()

    skill_level = page.get_by_role("combobox").nth(1)
    skill_level.click()
    page.get_by_role("option", name="Beginner").click()

    status = page.get_by_role("combobox").nth(2)
    status.click()
    page.get_by_role("option", name="Approved").click()

    page.get_by_role("button", name="Select Questions").click()
    page.get_by_text("Question ID:", exact=False).first.wait_for(
        state="visible",
        timeout=10000,
    )
    checkboxes = page.locator("input[type='checkbox']")
    assert checkboxes.count() > 0

    for index in range(checkboxes.count()):
        checkboxes.nth(index).check()

  
    with page.expect_event("dialog") as dialog_info:
        page.get_by_role("button", name="Create Test").click()

    dialog = dialog_info.value
    assert "test" in dialog.message.lower()
    assert "creat" in dialog.message.lower()
    dialog.accept()