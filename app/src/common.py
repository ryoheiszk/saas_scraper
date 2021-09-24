import json
import os

import pandas
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


WAIT_TIME = 0.5


def get_driver():
    driver = webdriver.Remote(
        command_executor=os.environ["SELENIUM_URL"],
        desired_capabilities=DesiredCapabilities.FIREFOX.copy()
    )
    driver.implicitly_wait(10)

    return driver

def load_json(basename: str) -> str:
    print(f"load {basename}.json")

    with open(f"/app/exported/{basename}.json", "r") as f:
        s = json.load(f)

    return s

def write_json(basename: str, content: str) -> None:
    print(f"write {basename}.json")

    with open(f"/app/exported/{basename}.json", "w") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

def write_csv(basename: str, content: str) -> None:
    print(f"write {basename}.csv")

    df = pandas.DataFrame.from_dict(content)
    df.to_csv(f"/app/exported/{basename}.csv", encoding="utf-8-sig", index=False)
