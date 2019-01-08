import pandas as pd
import time
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import string
import json
import itertools
import numpy as np
from bisect import bisect_left, bisect_right
from pprint import pprint
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from bs4 import BeautifulSoup


def scrapping_handicaps_odds(browser, all_days_id, handicaps):
    while 1:
        while 1:
            start = time.clock()
            try:
                browser.find_element_by_xpath('//*[@id="oMenuHDC"]').click()
                print('Successful! The handicap page is ready.')
                end = time.clock()
                break
            except:
                print("Loading handicap page...")

        print('Time consumed: ' + str(end - start))

        wait = WebDriverWait(browser, 10)
        try:
            wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_HDC_HG")]')))
            wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'cteams')))
            wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'cday')))
            wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'cflag')))
            wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_HDC_H")]')))
            wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_HDC_A")]')))
            wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_HDC_A")]')))
        except:
            print("Error! The " + type + " data cannot be found.")
        else:
            days_id = browser.find_elements_by_xpath('//*[contains(@id, "_HDC_HG")]')
            teams = browser.find_elements_by_class_name('cteams')[1:]
            match_league = browser.find_elements_by_class_name("cflag")[1:]
            days_and_ids = browser.find_elements_by_class_name('cday')[1:]
            homes_handicap_data = browser.find_elements_by_xpath('//*[contains(@id, "_HDC_H")]')[1:]
            aways_handicap_data = browser.find_elements_by_xpath('//*[contains(@id, "_HDC_A")]')[1:]

        for index in range(int(len(homes_handicap_data) / 3) + 1):
            day_id = days_id[index].get_attribute('id').split('_')[0]
            if day_id in set(all_days_id) == -1:
                home, away = teams[index].text.replace('[', ',[').split(' 對 ')
                home_name_temp, home_handicap_temp = home.split(',')
                away_name_temp, away_handicap_temp = away.split(',')
                temp_match_league = match_league[index].find_element_by_tag_name("img").get_attribute("title")
                # home_handicap_temp = list(map(float, home_handicap_temp[1:-1].split("/")))
                # away_handicap_temp = list(map(float, away_handicap_temp[1:-1].split("/")))
                home_handicap_temp = home_handicap_temp[1:-1].split("/")
                away_handicap_temp = away_handicap_temp[1:-1].split("/")

                # print(home_handicap_temp, away_handicap_temp)
                handicaps.append([day_id, "null" if temp_match_league == "賽事類別" else temp_match_league,
                                  home_name_temp, home_handicap_temp, away_name_temp, away_handicap_temp,
                                  homes_handicap_data[index * 3 + 1].text, aways_handicap_data[index * 3 + 1].text])

        try:
            browser.find_element_by_xpath(
                '//*[@id="ActiveMatchesOdds"]/div/div[1]/div[2]/div[1]/div[2]/span[2]/span[3]').click()
            continue
        except:
            break


def scrapping_HAD_odds(browser, handicaps, homes_aways_draw):
    while 1:
        start = time.clock()
        try:
            browser.find_element_by_xpath('//*[@id="oMenuHAD"]').click()
            print('Successful! The HAD data is ready.')
            end = time.clock()
            break
        except:
            print("Loading HAD data...")

    print('Time consumed: ' + str(end - start))
    wait = WebDriverWait(browser, 10)

    try:
        wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "rmid")]')))
        wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_HAD_H")]')))
        wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_HAD_A")]')))
        wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_HAD_D")]')))
    except:
        print("Error! The HAD data cannot be found.")
    finally:
        days_id = browser.find_elements_by_xpath('//*[contains(@id, "rmid")]')
        homes_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_HAD_H")]')[1:]
        aways_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_HAD_A")]')[1:]
        draws_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_HAD_D")]')[1:]

    count_irrelevant = 0
    counted_page = 0
    for index in range(len(handicaps)):
        while days_id[index + count_irrelevant - counted_page].get_attribute('id')[4:] \
                != handicaps[index][0]:
            if days_id[index + count_irrelevant - counted_page].get_attribute('id')[4:] \
                    == days_id[-1].get_attribute('id')[4:]:
                counted_page = index
                try:
                    wait.until(ec.element_to_be_clickable((By.XPATH,
                                                           '//*[@id="ActiveMatchesOdds"]/div/div[1]/div[2]/div['
                                                           '1]/div[2]/span[2]/span[3]')))
                    wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "rmid")]')))
                    wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_HAD_H")]')))
                    wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_HAD_A")]')))
                    wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_HAD_D")]')))
                except:
                    print("Error! The HAD data cannot be found.")
                finally:
                    browser.find_element_by_xpath(
                        '//*[@id="ActiveMatchesOdds"]/div/div[1]/div[2]/div[1]/div[2]/span[2]/span[3]').click()
                    days_id = browser.find_elements_by_xpath('//*[contains(@id, "rmid")]')
                    homes_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_HAD_H")]')[1:]
                    aways_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_HAD_A")]')[1:]
                    draws_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_HAD_D")]')[1:]

                count_irrelevant = 0
                continue

            count_irrelevant += 1

        homes_aways_draw.append((days_id[index + count_irrelevant - counted_page].get_attribute('id')[4:],
                                 handicaps[index][1],
                                 handicaps[index][3],
                                 homes_had_data[(index + count_irrelevant - counted_page) * 2].text,
                                 draws_had_data[(index + count_irrelevant - counted_page) * 2].text,
                                 aways_had_data[(index + count_irrelevant - counted_page) * 2].text))

        if days_id[index + count_irrelevant - counted_page].get_attribute('id')[4:] \
                == days_id[-1].get_attribute('id')[4:]:
            counted_page = index
            try:
                wait.until(ec.element_to_be_clickable((By.XPATH,
                                                       '//*[@id="ActiveMatchesOdds"]/div/div[1]/div[2]/div['
                                                       '1]/div[2]/span[2]/span[3]')))
                wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "rmid")]')))
                wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_HAD_H")]')))
                wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_HAD_A")]')))
                wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_HAD_D")]')))
            except:
                print("Error! The HAD data cannot be found.")
            else:
                browser.find_element_by_xpath(
                    '//*[@id="ActiveMatchesOdds"]/div/div[1]/div[2]/div[1]/div[2]/span[2]/span[3]').click()
                days_id = browser.find_elements_by_xpath('//*[contains(@id, "rmid")]')
                homes_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_HAD_H")]')[1:]
                aways_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_HAD_A")]')[1:]
                draws_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_HAD_D")]')[1:]

            count_irrelevant = 0
            continue


def scrapping_had_hhd_odds(browser, handicaps, result_data, type):
    while 1:
        start = time.clock()
        try:
            browser.find_element_by_xpath('//*[@id="oMenu%s"]' % type).click()
            print('Successful! The ' + type + ' page is ready.')
            end = time.clock()
            break
        except:
            print("Loading " + type + " page...")

    print('Time consumed: ' + str(end - start))

    wait = WebDriverWait(browser, 10)
    try:
        wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "rmid")]')))
        wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_%s_H")]' % type)))
        wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_%s_A")]' % type)))
        wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_%s_D")]' % type)))
    except:
        print("Error! The " + type + " data cannot be found.")
    else:
        days_id = browser.find_elements_by_xpath('//*[contains(@id, "rmid")]')
        homes_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_%s_H")]' % type)
        aways_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_%s_A")]' % type)
        draws_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_%s_D")]' % type)

    count_irrelevant = 0
    counted_page = 0

    for index in range(len(handicaps)):
        while days_id[index + count_irrelevant - counted_page].get_attribute('id')[4:] \
                != handicaps[index][0]:
            if days_id[index + count_irrelevant - counted_page].get_attribute('id')[4:] \
                    == days_id[-1].get_attribute('id')[4:]:
                counted_page = index
                try:
                    wait.until(ec.element_to_be_clickable((By.XPATH,
                                                           '//*[@id="ActiveMatchesOdds"]/div/div[1]/div[2]/div['
                                                           '1]/div[2]/span[2]/span[3]')))
                    wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "rmid")]')))
                    wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_%s_H")]' % type)))
                    wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_%s_A")]' % type)))
                    wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_%s_D")]' % type)))
                except:
                    print("Error! The " + type + " data cannot be found.")
                else:
                    browser.find_element_by_xpath(
                        '//*[@id="ActiveMatchesOdds"]/div/div[1]/div[2]/div[1]/div[2]/span[2]/span[3]').click()
                    days_id = browser.find_elements_by_xpath('//*[contains(@id, "rmid")]')
                    homes_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_%s_H")]' % type)
                    aways_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_%s_A")]' % type)
                    draws_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_%s_D")]' % type)

                count_irrelevant = 0
                continue

            count_irrelevant += 1

        if type == "HHA":
            result_data.append([days_id[index + count_irrelevant - counted_page].get_attribute('id')[4:],
                                handicaps[index][1], handicaps[index][2],
                                homes_had_data[(index + count_irrelevant - counted_page) * 3].text,
                                handicaps[index][4],
                                aways_had_data[(index + count_irrelevant - counted_page) * 3].text,

                                homes_had_data[(index + count_irrelevant - counted_page) * 3 + 2].text,
                                draws_had_data[(index + count_irrelevant - counted_page) * 2 + 1].text,
                                aways_had_data[(index + count_irrelevant - counted_page) * 3 + 2].text])
        elif type == 'HAD':
            diff = len(days_id) - len(homes_had_data) // 2
            result_data.append([days_id[index + count_irrelevant - counted_page].get_attribute('id')[4:],
                                handicaps[index][1], handicaps[index][2],
                                handicaps[index][4],
                                homes_had_data[(index + count_irrelevant - counted_page - diff) * 2 + 1].text,
                                draws_had_data[(index + count_irrelevant - counted_page - diff) * 2 + 1].text,
                                aways_had_data[(index + count_irrelevant - counted_page - diff) * 2 + 1].text])

        if days_id[index + count_irrelevant - counted_page].get_attribute('id')[4:] \
                == days_id[-1].get_attribute('id')[4:]:
            counted_page = index
            try:
                wait.until(ec.element_to_be_clickable((By.XPATH,
                                                       '//*[@id="ActiveMatchesOdds"]/div/div[1]/div[2]/div['
                                                       '1]/div[2]/span[2]/span[3]')))
            except:
                print("Last page of " + type)
            else:
                browser.find_element_by_xpath(
                    '//*[@id="ActiveMatchesOdds"]/div/div[1]/div[2]/div[1]/div[2]/span[2]/span[3]').click()
                try:
                    wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "rmid")]')))
                    wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_%s_H")]' % type)))
                    wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_%s_A")]' % type)))
                    wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@id, "_%s_D")]' % type)))
                except:
                    print("Error! The data of next page cannot be found.")
                else:
                    days_id = browser.find_elements_by_xpath('//*[contains(@id, "rmid")]')
                    homes_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_%s_H")]' % type)
                    aways_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_%s_A")]' % type)
                    draws_had_data = browser.find_elements_by_xpath('//*[contains(@id, "_%s_D")]' % type)

            count_irrelevant = 0
            continue


def scrapping_competition_result(browser, handicaps_day_id, handicaps, competition_result):
    while 1:
        start = time.clock()
        try:
            browser.find_element_by_xpath('//*[@id="thirdMenu"]/div/div[5]/div[1]').click()
            browser.find_element_by_xpath('//*[@id="pMenu2"]/div[1]').click()
            print('Successful! The competition result page is ready.')
            end = time.clock()
            break
        except:
            print("Loading the competition result page...")

    print('Time consumed: ' + str(end - start))

    wait = WebDriverWait(browser, 10)

    try:
        wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "span_vs")))
        wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "matchLeague")))
        wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "teamname")))
        wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "matchHalf") and '
                                                                  'not(contains(@class, "rBottomBorder"))]')))
        wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "matchFull") and '
                                                                  'not(contains(@class, "rBottomBorder"))]')))
    except:
        print("Error! The competition result cannot be found.")
    finally:
        days_id = browser.find_elements_by_class_name("span_vs")
        match_league = browser.find_elements_by_class_name("matchLeague")
        teams_name = browser.find_elements_by_class_name("teamname")
        half_match_result = browser.find_elements_by_xpath('//*[contains(@class, "matchHalf") and '
                                                           'not(contains(@class, "rBottomBorder"))]')
        full_match_result = browser.find_elements_by_xpath('//*[contains(@class, "matchFull") and '
                                                           'not(contains(@class, "rBottomBorder"))]')

    for index, day_id in enumerate(half_match_result):
        temp_day_id = days_id[index].get_attribute("id")[2:]
        temp_match_league = match_league[index].find_element_by_tag_name("img").get_attribute("title")

        competition_index = -1
        size = len(handicaps_day_id) - 1
        for i, target in enumerate(handicaps_day_id):
            if target == handicaps_day_id[size]:
                competition_index = i
                break

        if half_match_result[index].text != "-" and full_match_result[index].text != "-" \
                and competition_index != -1:
            half_match_result_temp = half_match_result[index].text.split(" : ")
            full_match_result_temp = list(map(float, full_match_result[index].text.split(" : ")))

            handicap_result = 0

            target_odds = list(map(float, handicaps[competition_index][3][1:-1].split(", ")))

            if len(target_odds) == 1:
                if target_odds == 0:
                    if full_match_result_temp[0] > full_match_result_temp[1]:
                        handicap_result = 1
                    elif full_match_result_temp[0] > full_match_result_temp[1]:
                        handicap_result = -1
                else:
                    handicap_home_first = [full_match_result_temp[0] - target_odds[0], 0]

                    if handicap_home_first[0] > handicap_home_first[1]:
                        handicap_result = 1
                    elif handicap_home_first[0] < handicap_home_first[1]:
                        handicap_result = -1
                    else:
                        handicap_result = 0

            else:
                handicap_home_first = [full_match_result_temp[0] - target_odds[0], 0]
                handicap_home_second = [full_match_result_temp[0] - target_odds[1], 0]

                if handicap_home_first[0] > handicap_home_first[1]:
                    handicap_result += 0.5
                    if handicap_home_second[0] > handicap_home_second[1]:
                        handicap_result += 0.5
                elif handicap_home_first[0] <= handicap_home_first[1]:
                    handicap_result = -1

            competition_result.append([temp_day_id, "null" if temp_match_league == "賽事類別" else temp_match_league,
                                       teams_name[2 * index].text, teams_name[2 * index + 1].text,
                                       half_match_result_temp, full_match_result_temp, handicap_result])


def main():
    url = "https://bet.hkjc.com/football/default.aspx"
    chrome_path = "/Users/wing/Desktop/Python_Project/machineLearning/chromedriver"
    browser = webdriver.Chrome(chrome_path)

    def check_exists_by_xpath(xpath):
        try:
            browser.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    handicaps_temp = list()
    handicaps_had_temp = list()
    homes_aways_draw_temp = list()
    competitions_result_temp = list()

    print("handicaps.csv:")
    handicaps = list(csv.reader(open('handicaps.csv')))
    print(handicaps)

    print("handicaps_had.csv:")
    handicaps_had = list(csv.reader(open('handicaps_had.csv')))
    print(handicaps_had)

    print("homes_aways_draw.csv:")
    homes_aways_draw = list(csv.reader(open('homes_aways_draw.csv')))
    print(homes_aways_draw)

    print("competitions_result.csv:")
    competitions_result = list(csv.reader(open('competitions_result.csv')))
    print(competitions_result)

    browser.get(url)

    while 1:
        start = time.clock()
        try:
            browser.switch_to.frame('info')
            print('Successful! The info frame is ready!')
            end = time.clock()
            break
        except:
            print("Searching info...")

    print('Time consumed: ' + str(end - start))

    all_days_id = [handicap[0] for handicap in handicaps]

    scrapping_handicaps_odds(browser, all_days_id, handicaps_temp)
    scrapping_had_hhd_odds(browser, handicaps_temp, homes_aways_draw_temp, "HAD")
    scrapping_had_hhd_odds(browser, handicaps_temp, handicaps_had_temp, "HHA")

    all_days_id_temp = [handicap_temp[0] for handicap_temp in handicaps_temp]
    all_days_id = set(all_days_id)
    for index, target in enumerate(all_days_id_temp):
        if target not in all_days_id:
            handicaps.append(handicaps_temp[index])
            homes_aways_draw.append(homes_aways_draw_temp[index])
            handicaps_had.append(handicaps_had_temp[index])

    scrapping_competition_result(browser, all_days_id, handicaps, competitions_result_temp)

    finished_all_days_id_temp = [competitions_result_temp[0] for competitions_result_temp in competitions_result_temp]

    for index, target in enumerate(finished_all_days_id_temp):
        if target in all_days_id:
            competitions_result.append(competitions_result_temp[index])

    print()

    print("The handicaps result:" + str(len(handicaps)))
    for i in handicaps:
        print(i)

    print()

    print("The homes_aways_draw result:" + str(len(homes_aways_draw)))
    for i in homes_aways_draw:
        print(i)

    print()

    print("The handicaps_had result:" + str(len(handicaps_had)))
    for i in handicaps_had:
        print(i)

    print()

    print("The competition result:" + str(len(competitions_result)))
    for i in competitions_result:
        print(i)

    pd.DataFrame(handicaps).to_csv("handicaps.csv", index=False, header=False)
    pd.DataFrame(homes_aways_draw).to_csv("homes_aways_draw.csv", index=False, header=False)
    pd.DataFrame(handicaps_had).to_csv("handicaps_had.csv", index=False, header=False)
    pd.DataFrame(competitions_result).to_csv("competitions_result.csv", index=False, header=False)


main()
