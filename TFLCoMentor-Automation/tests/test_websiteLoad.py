def test_website_load(page):

    # Open TFLCoMentor website
    response = page.goto("http://localhost:8081")

    # Verify website response
    assert response.status == 200

    # Verify page body is visible
    assert page.locator("body").is_visible()

    print("TFLCoMentor website loaded successfully!")