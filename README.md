# Bycaptcha
A selenuim module to automaticly solve reCaptcha.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install bycaptcha.

```bash
pip3 install bycaptcha
```

## Usage

```python
import bycap
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('https://google.com/recaptcha/api2/demo')

bycap.checkForRecapcha(browser) # Return 1 if there is a captcha, and 0 if there is not.

bycap.resolveCaptcha(browser) # Return 0 if solve, 1 if is block and 2 if is already solve.
```

## Exemple

```python
import bycap
from time import sleep
from selenium import webdriver

browser = webdriver.Firefox()

browser.get('https://google.com/recaptcha/api2/demo')
    print('Searching for captcha...')
    if bycap.checkForRecapcha(browser) == 1:
        print('Captcha found ! Trying to solve...')
        sleep(1)
        captcha = 1
        while captcha != 0:
            captcha = bycap.resolveCaptcha(browser)
            if captcha == 1:
                print('Captcha is block!')
            elif captcha == 0:
                print('Captcha is solve!')

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.