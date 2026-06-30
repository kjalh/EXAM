import time
import urllib.request
import re
import requests
import pandas as pd
import os

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException


def yes24_crawl(max_page):
    search_list = []
    title_list = []
    name_list = []
    price_list = []
    com_list = []
    date_list = []
    image_list = []

    folder_path = r"imgaes\yes24"

    url = "https://www.yes24.com/Main/default.aspx"

    driver = webdriver.Chrome()
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    driver.get(url)
    ban = True
    need_input = True

    while ban:
        if need_input:
            keyword = input("검색어 입력: ")
            need_input = False

        try:
            search_box = wait.until(
                EC.presence_of_element_located((By.ID, "query"))
            )

            search_box.clear()
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.ENTER)

            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                    
                time.sleep(2)
                need_input = True
                continue 
                    
            except TimeoutException:
                pass
            ban = False
        
        except Exception as e:
            continue
    # ----------------------------------------------------- 검색

    for page in range(1, max_page + 1): 
            
            if page == max_page + 1:                      
                print(f"크롤링 끝")
                break
            

            print(f"{page}번 페이지 크롤링")

            req = driver.page_source

            soup = BeautifulSoup(req, "html.parser")
            
            ALL_books = soup.find("ul", id = "yesSchList").find_all("li")

            for row in ALL_books:
                if not row.select_one(".gd_name"): 
                    continue
                
                title = row.select_one(".gd_name").text 
                name = row.select_one(".info_auth").text if row.select_one(".info_auth") else ""
                price = row.select_one(".yes_b").text if row.select_one(".yes_b") else ""
                com = row.select_one(".info_pub").text if row.select_one(".info_pub") else ""
                ddatee = row.select_one(".info_date").text.strip() if row.select_one(".info_date") else ""
                img_tag = row.select_one(".img_bdr img")
                

                if img_tag:
                    img_url = img_tag.get("data-original") or img_tag.get("src")
                    
                    if img_url:
                        try: 
                            img_safe_title = re.sub(r'[\/:*?"<>|]', '', title) 
                            img_save = os.path.join(folder_path, f"{img_safe_title}.jpg")
                            urllib.request.urlretrieve(img_url, img_save)
                        except:
                            print(f"이미지 다운로드 실패 ({title}): {e}")
                            img_save = "다운로드 실패"
                            

                        
                search_list.append(keyword)
                title_list.append(title)
                name_list.append(name)
                price_list.append(price)
                com_list.append(com)
                date_list.append(ddatee)
                image_list.append(img_save)
            
                

            if page < max_page:
                next_start_index = page + 1
                try:
                    next_btn = wait.until(
                        EC.element_to_be_clickable((By.LINK_TEXT, str(next_start_index)))
                    )
                    next_btn.click()
                    time.sleep(3)
                except Exception as e:
                    print("이동할 페이지가 없어서 종료", e)
                    break
            else:
                print("목표 페이지에 도달")
            
    df = pd.DataFrame({
        "검색어": search_list,
        "도서명": title_list,
        "저자": name_list,
        "가격": price_list,
        "출판사": com_list,
        "출판일": date_list,
        "이미지 저장 경로": image_list
    })

    driver.close()
    return df



def kyobo_crawl(max_page):
    search_list = []
    title_list = []
    name_list = []
    price_list = []
    com_list = []
    date_list = []
    image_list = []

    folder_path = r"imes\kyobo"

    url = "https://product.kyobobook.co.kr"

    driver = webdriver.Chrome()
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    driver.get(url)

    while True:
        try:
            search_box = wait.until(EC.presence_of_element_located((By.ID, "searchKeyword")))
            keyword = input("검색어 입력: ")
            
            search_box.clear()
            time.sleep(3)
            for i in keyword:
                search_box.send_keys(i)
                time.sleep(0.5)
                
            search_box.send_keys(Keys.ENTER)

            try:
                confirm_btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '확인')]"))
                )
                confirm_btn.click()
                print("팝업 발생: 다시 입력하세요.")
                continue 
            
            except TimeoutException: # 검색 되면 끝낼거임
                break

        except Exception as e:
            print(f"오류 발생: {e}")
            driver.refresh()
            time.sleep(3)
            continue
        
    #---------------------------------------------------------------------- 사이트 열고 검색

    for page in range(1, max_page + 1):
            print(f"{page}번 페이지 크롤링")

            req = driver.page_source

            soup = BeautifulSoup(req, "html.parser")

            time.sleep(2)
            
            ALL_books = soup.find("ul", class_="prod_list").find_all("li")
            

            for row in ALL_books:
                if not row.select_one("a.prod_info"): 
                    continue
                
                title = row.select_one("a.prod_info").text 
                name = row.select_one("div.auto_overflow_wrap.prod_author_group").text if row.select_one("div.auto_overflow_inner") else ""
                name = name.replace("더보기", "")
                price = row.select_one(".val").text if row.select_one(".val") else ""
                com = row.select_one(".prod_publish").text if row.select_one(".prod_publish") else ""
                ddatee = row.select_one(".date").text.strip() if row.select_one(".date") else ""
                img_tag = row.select_one(".img_box img")


                title = re.sub(r'\s+', ' ', title).strip()
                name = re.sub(r'\s+', ' ', name).strip()
                price = re.sub(r'\s+', ' ', price).strip()
                com = re.sub(r'\s+', ' ', com).strip()
                ddatee = re.sub(r'\s+', ' ', ddatee).strip()
                

                if img_tag:
                    img_url = img_tag.get("data-original") or img_tag.get("src")
                    
                    if img_url:
                        try: 
                            img_safe_title = re.sub(r'[\\/:*?"<>|\n\r]', '', title).strip()
                            img_save = os.path.join(folder_path, f"{img_safe_title}.jpg")
                            urllib.request.urlretrieve(img_url, img_save)
                        except Exception as e:
                            print(f"이미지 다운로드 실패 ({title}): {e}")
                            img_save = "다운로드 실패"
                            

                        
                search_list.append(keyword)
                title_list.append(title)
                name_list.append(name)
                price_list.append(price)
                com_list.append(com)
                date_list.append(ddatee)
                image_list.append(img_save)
            
                next_start_index = page + 1

            try:
                next_btn = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, str(next_start_index)))
                
                )
                next_btn.click()
                time.sleep(5)

            except Exception as e:
                print("이동할 페이지 없어서 종료", e)
                break
            
    df = pd.DataFrame({
        "검색어": search_list,
        "도서명": title_list,
        "저자": name_list,
        "가격": price_list,
        "출판사": com_list,
        "출판일": date_list,
        "이미지 저장 경로": image_list
    })

    driver.close()
    return df










def crawl_start(yes24, kyobo, aladin):
    df01 = yes24_crawl(yes24)   
    df02 = kyobo_crawl(kyobo)
    df03 = aladin_crawl(aladin)

    with pd.ExcelWriter("finential.xlsx") as writer:
        df01.to_excel(writer, sheet_name="yes24 시트", index=False)
        df02.to_excel(writer, sheet_name="kyobo 시트", index=False)
        df03.to_excel(writer, sheet_name="aladin 시트", index=False)



crawl_start(3, 2, 4)