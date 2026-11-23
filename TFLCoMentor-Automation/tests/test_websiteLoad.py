def test_website_load(page):


    response = page.goto("http://localhost:8081")


    assert response.status == 200

    assert page.locator("body").is_visible()

    print("TFLCoMentor website loaded successfully!")