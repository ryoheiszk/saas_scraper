import re
from time import sleep

from tqdm import tqdm

import common


def get_categories(driver):
    driver.get("https://boxil.jp/categories/")
    sleep(common.WAIT_TIME)

    _elems = driver.find_elements_by_xpath("//div[contains(@class, 'pagesCategories-content-childCategory')]")

    categories = []
    for e in tqdm(_elems):
        category_name = e.find_element_by_tag_name("span").text
        category_url = e.find_element_by_tag_name("a").get_attribute("href")

        categories.append({
            "name": category_name,
            "url": category_url
        })

    return categories

def scrape_by_categories(driver, categories: list, min_review_num: int = 1):
    """
    レビュー数がすべて設定値以上でも、1ページ目で処理は終了する。
    """
    tools = []
    for cat in tqdm(categories):
        driver.get(cat["url"])
        sleep(common.WAIT_TIME)

        _elem = driver.find_elements_by_xpath("//div[@class='service-block__main-content']")

        cat_tools_urls = []
        for e in _elem:
            review_num = _get_review_num(e)

            if review_num < min_review_num:
                break

            _elem_tool =e.find_element_by_class_name("service-block__main-content-title-text")
            tool_name = _elem_tool.text
            tool_url = _elem_tool.find_element_by_tag_name("a").get_attribute("href")
            tool_url = re.sub("\?.+", "", tool_url)

            cat_tools_urls.append({
                "name": tool_name,
                "url": tool_url,
                "review_num": review_num
            })

        tools.append({
            "category_name": cat["name"],
            "category_url": cat["url"],
            "tools": cat_tools_urls
        })

    return tools

def _get_review_num(elem) -> int:
    try:
        review_num_text = elem.find_elements_by_class_name("service-block__main-content-review-count-text")[0].text
        review_num = int(re.search(".+(?=件)", review_num_text).group())
    except Exception:
        # 1件以上あった場合のXPathが見つからなかった場合、0件とみなす。
        # TODO: 直接取得した方がきれい。
        review_num = 0
    finally:
        return review_num

def get_tool_info(tool_urls):
    # TODO: ツール詳細を取得する。
    return "ツール詳細を取得する処理が未実装です。"


if __name__ == "__main__":
    try:
        driver = common.get_driver()

        categories = get_categories(driver)
        common.write_json("_boxil_categories", categories)

        categories = common.load_json("_boxil_categories")
        tools_urls = scrape_by_categories(driver, categories)
        common.write_json("_boxil_tools_urls", tools_urls)

        tools_urls = common.load_json("_boxil_tools_urls")
        tools_info = get_tool_info(tools_urls)
        common.write_json("boxil_tools_info", tools_info)
        # common.write_csv("boxil_tools_info", tools_info)
    except Exception:
        raise Exception
    finally:
        driver.quit()
