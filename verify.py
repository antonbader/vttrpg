from playwright.sync_api import sync_playwright

def test_paint_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Mock some campaigns and a scene to get into GM View directly,
        # but since we lack db setup in the script, we can just start the app
        # and create one from the UI.
        page.goto("http://127.0.0.1:5000/")

        # Create campaign
        page.fill("input[name='name']", "Test Campaign")
        page.click("button:has-text('Kampagne erstellen')")

        # Open Adventures
        page.click("h4:has-text('Abenteuer')")

        # Create adventure
        page.fill("input[placeholder='Neues Abenteuer...']", "Test Adv")
        page.click("button:has-text('+ Abenteuer')")

        # Open Scenes
        page.click("strong:has-text('Test Adv')")

        # Create scene
        page.fill("input[placeholder='Neue Szene...']", "Test Scene")
        page.click("button:has-text('+ Szene')")

        # Go to GM View
        page.click("a:has-text('GM-Ansicht')")

        # Wait for page load
        page.wait_for_selector("#btn-paint-brush")

        # Open the Paint details (it should be open by default, but let's check)
        paint_details = page.locator("details:has-text('Paint')")
        paint_details_open = paint_details.evaluate("el => el.open")

        # Take a screenshot to verify UI elements are there
        page.screenshot(path="/home/jules/verification/paint_ui.png")

        browser.close()

if __name__ == "__main__":
    test_paint_ui()
