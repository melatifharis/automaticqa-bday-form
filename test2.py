from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


FORM_URL = (
	"https://docs.google.com/forms/d/"
	"1jfGLwpduIv7CuNIpKGxRytyhuz3X0xWFryQI5Q5ckpc/"
)
OVERNIGHT_ANSWER = "Yes"

test_users = [
    {
        "name": "Liam Davis",
        "IG/twt account": "liam@test.com",
        "phone number": "847291"
    },
    {
        "name": "Sophia Martinez",
        "IG/twt account": "sophia@test.com",
        "phone number": "555839"
    },
    {
        "name": "Oliver Taylor",
        "IG/twt account": "oliver@test.com",
        "phone number": "432109"
    }
]

FIELD_XPATHS = {
	"name": "//*[@role='listitem'][.//*[@role='heading'][contains(normalize-space(.), 'Name')]]//textarea",
	"IG/twt account": "//*[@role='listitem'][.//*[@role='heading'][contains(normalize-space(.), 'IG/twt account')]]//textarea",
	"phone number": "//*[@role='listitem'][.//*[@role='heading'][contains(normalize-space(.), 'Phone number')]]//textarea",
}


def main():
	users = test_users[:3]
	if len(users) != 3:
		raise ValueError("Add exactly three users before running this script.")

	for index, user in enumerate(users, start=1):
		missing_fields = [field for field in FIELD_XPATHS if not user.get(field)]
		if missing_fields:
			raise ValueError(
				f"User {index} is missing: {', '.join(missing_fields)}"
			)

	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
	wait = WebDriverWait(driver, 20)

	try:
		for index, user in enumerate(users, start=1):
			driver.get(FORM_URL)

			for field, xpath in FIELD_XPATHS.items():
				textbox = wait.until(
					EC.visibility_of_element_located((By.XPATH, xpath))
				)
				driver.execute_script(
					"arguments[0].scrollIntoView({block: 'center'});",
					textbox,
				)
				textbox.click()
				textbox.send_keys(user[field])

			overnight_xpath = (
				"//*[@role='listitem'][.//*[@role='heading']"
				"[contains(normalize-space(.), 'Nginep engga')]]"
				f"//*[@role='radio' and @aria-label='{OVERNIGHT_ANSWER}']"
			)
			wait.until(
				EC.element_to_be_clickable((By.XPATH, overnight_xpath))
			).click()

			send_xpath = "//*[@role='button'][.//*[normalize-space(.)='Kirim']]"
			send_button = wait.until(
				EC.element_to_be_clickable((By.XPATH, send_xpath))
			)
			send_button.click()
			wait.until(EC.staleness_of(send_button))
			print(f"Submitted response {index} of 3 for {user['name']}.")
	finally:
		driver.quit()


if __name__ == "__main__":
	main()
