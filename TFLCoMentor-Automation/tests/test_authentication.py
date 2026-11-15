# check sign in button is vissible on home page 
def test_signin_button(page): 
    page.goto("http://localhost:8081/")
    signin = page.get_by_text("Sign In")
    assert signin.is_visible()


#  check sign in button is working or not
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