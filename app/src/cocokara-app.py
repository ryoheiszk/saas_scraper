import itertools
import time

from tqdm import tqdm

import common


def scrape_tool_urls(driver, page_cnt):
    URL = "https://ittools.smrj.go.jp/app/index.php?page={}&sort=intro_number"
    PAGE_CNT = page_cnt

    print("scrape_app_urls")

    page_tool_urls_lists = []
    for i in tqdm(range(PAGE_CNT)):
        driver.get(URL.format(i+1))
        time.sleep(common.WAIT_TIME)

        _elems = driver.find_elements_by_xpath("//li[contains(@class, 'app_lists_item col3_item')]/a")
        page_tool_urls = [e.get_attribute("href") for e in _elems]
        page_tool_urls_lists.append(page_tool_urls)

    tool_urls = list(itertools.chain.from_iterable(page_tool_urls_lists))

    return tool_urls


def scrape_tools_info(driver, tool_urls):
    print("scrape_tool_info")

    tools_info = []
    for tool_url in tqdm(tool_urls):
        driver.get(tool_url)
        time.sleep(common.WAIT_TIME)

        tool_info = {}

        # 情報源
        tool_info["引用元"] = tool_url

        # 製品情報
        _elems = driver.find_elements_by_xpath("//div[contains(@class, 'products_table')]/dl")
        for e in _elems:
            key = e.find_element_by_tag_name("dt").text
            value = e.find_element_by_tag_name("dd").text

            if key:
                tool_info[key] = value

        # 製品概要
        about = driver.find_element_by_xpath("//div[contains(@class, 'app_info')]//p").text
        tool_info["概要"] = about

        # 製品URL
        official_url = driver.find_elements_by_xpath("//div[contains(@class, 'app_info_btn')]/a")[0].get_attribute("href")
        tool_info["公式サイト"] = official_url

        # タグ
        _elems = driver.find_elements_by_xpath("/html/body/main/div[2]/div/div[2]/ul/li")
        tags = [e.text for e in _elems]
        tool_info["タグ"] = tags

        tools_info.append(tool_info)

    return tools_info

def get_tags(basename: str) -> list:
    common.load_json(basename)

    tags = [inf["タグ"] for inf in tool_info]

    # 平坦化・重複削除
    tags = list(set(itertools.chain.from_iterable(tags)))

    return tags


if __name__ == "__main__":
    PAGE_CNT = 23

    try:
        driver = common.get_driver()

        tool_urls = scrape_tool_urls(driver, PAGE_CNT)
        common.write_json("cocokara-app_urls", tool_urls)

        tool_urls = common.load_json("cocokara-app_urls")
        tool_info = scrape_tools_info(driver, tool_urls)
        common.write_json("cocokara-app_info", tool_info)
        common.write_csv("cocokara-app_info", tool_info)

        tool_info = common.load_json("cocokara-app_info")
        tags = get_tags(tool_info)
        common.write_json(tags)
        common.write_csv("tags", tags)

    except Exception:
        raise Exception
    finally:
        driver.quit()
