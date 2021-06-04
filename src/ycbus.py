import os
import re
import logging
import datetime
import time
from logging.config import fileConfig
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from os import path
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(log_file_path)
# fileConfig('logging_config.ini')
my_debug_log = logging.getLogger(__name__).debug


class AutoReserve:
    def __init__(self):
        # User Data
        self.xpath = None
        self.data = dict()
        data_file = os.getcwd() + "\\ycbus_data.txt"
        with open(data_file, 'r', encoding="utf-8") as file:
            f_read = file.read()

        split_symbol = '[=|\n]'
        self.data['name'] = re.split(split_symbol, f_read)[1]
        self.data['num'] = re.split(split_symbol, f_read)[3]
        self.data['date'] = re.split(split_symbol, f_read)[5]
        self.data['go_time'] = re.split(split_symbol, f_read)[7]
        self.data['back_time'] = re.split(split_symbol, f_read)[9]
        # goOn Address
        self.data['go_on_city'] = re.split(split_symbol, f_read)[11]
        self.data['go_on_area'] = re.split(split_symbol, f_read)[13]
        self.data['go_on_address'] = re.split(split_symbol, f_read)[15]
        # goOff Address
        self.data['go_off_city'] = re.split(split_symbol, f_read)[17]
        self.data['go_off_area'] = re.split(split_symbol, f_read)[19]
        self.data['go_off_address'] = re.split(split_symbol, f_read)[21]
        # Message
        self.data['Message'] = re.split(split_symbol, f_read)[23]
        # goOn Address
        self.data['back_on_city'] = re.split(split_symbol, f_read)[25]
        self.data['back_on_area'] = re.split(split_symbol, f_read)[27]
        self.data['back_on_address'] = re.split(split_symbol, f_read)[29]
        # goOff Address
        self.data['back_off_city'] = re.split(split_symbol, f_read)[31]
        self.data['back_off_area'] = re.split(split_symbol, f_read)[33]
        self.data['back_off_address'] = re.split(split_symbol, f_read)[35]

        # CSS Element
        self.css = dict()
        self.css['customerName'] = "input#cusname.w3-large"
        self.css['idCode'] = "input#idcode.w3-large"
        self.css['loginButton'] = "input#btn101.btn"
        self.css['checkNumber'] = "input#chknumber"
        self.css['checkMyID'] = "form#form1 h1:nth-child(4)"
        self.css['backMain'] = 'form#form1 div:nth-child(2) > input[name="btn1"]'

        self.css['sendButton'] = "input#next5"
        self.css['dateButton'] = 'input[type=button][value*="%s"]' % self.data['date']
        self.css['setGoButton'] = "input#setgom2"
        #                           input[type=radio][onclick*="go_time"]
        self.css['goTimeButton'] = 'input[type=radio][onclick*="%s"]' % self.data['go_time']
        self.css['setBackButton'] = "input#setgon"
        self.css['backTimeButton'] = 'input[type=radio][onclick*="%s"]' % self.data['back_time']
        # goOn Address
        self.css['goOnAreaIn'] = "input[name='areain']"
        self.css['goOnCitySelect'] = "select[name='city']"
        self.css['goOnAreaSelect'] = "select[name='areain_u']"
        self.css['goOnAddress'] = "input[type=text][name='pointin']"
        # goOff Address
        self.css['goOffAreaIn'] = "input[name='areaoff']"
        self.css['goOffCitySelect'] = "select[name='citya']"
        self.css['goOffAreaSelect'] = "select[name='areaoff_u']"
        self.css['goOffAddress'] = "input[type=text][name='pointoff']"
        # Message
        self.css['message'] = "textarea[name='pmark']"
        # backOn Address
        self.css['backOnAreaIn'] = "input[name='areain2']"
        self.css['backOnCitySelect'] = "select[name='cityb']"
        self.css['backOnAreaSelect'] = "select[name='areain2_u']"
        self.css['backOnAddress'] = "input[type=text][name='pointin2']"
        # backOff Address
        self.css['backOffAreaIn'] = "input[name='areaoff2']"
        self.css['backOffCitySelect'] = "select[name='citym']"
        self.css['backOffAreaSelect'] = "select[name='areaoffb_u']"
        self.css['backOffAddress'] = "input[type=text][name='pointoff2']"
        # time clock
        self.css['timeClock'] = "span#time"
        # booking
        self.css['bookingButton'] = "tr#chktmf input#uya"

        # webdriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('disable-gpu')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--enable-application-cache')
        # self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=chrome_options, executable_path=ChromeDriverManager().install())  # 启动时添加定制的选项
        try:
            self.driver.get('http://rayman.ycbus.org.tw/rayman/book_inq.php')
        except WebDriverException:
            self.driver.quit()
            exit('Cannot navigate to invalid URL !')

    def wait_element(self, element_name, selector='css', seconds=5):
        i = 0
        while i < 3:
            if selector == 'css':
                try:
                    wait_element = WebDriverWait(self.driver, seconds).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, self.css[element_name]))
                    )
                    return wait_element
                except TimeoutException as timeout:
                    i += 1
                    print(timeout)
                    print('%s is Timeout' % element_name)
                    print('Fail try %s count' % i)
            else:
                try:
                    wait_element = WebDriverWait(self.driver, seconds).until(EC.presence_of_element_located(
                        (By.XPATH, self.xpath[element_name]))
                    )
                    return wait_element
                except TimeoutException as timeout:
                    i += 1
                    print(timeout)
                    print('%s is Timeout' % element_name)
                    print('Fail try %s count' % i)

    def loop_now_time(self):
        status = 1
        while status == 1:
            time.sleep(1)
            time_get = self.driver.find_element_by_css_selector(self.css['timeClock']).text
            regex = re.compile(r'\d{4}-\d{2}-\d{2} (\d{2}:\d{2}):(\d{2})')
            search_time = regex.search(time_get)
            debug = 0
            lock_time = "07:00"
            try:
                if search_time.group(1) == lock_time and int(search_time.group(2)) > 0:
                    print("時間到: %s" % lock_time)
                    status = 0
                elif debug == 1:
                    status = 0
                else:
                    print("尚未到 %s, 現在時間: [%s]" % (lock_time, search_time.group(0)))
            except:
                pass

        self.reserve()

    def check_enter(self):
        try:
            WebDriverWait(self.driver, 0.5).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "form#form1 div > h1:nth-child(1)"))
            )
            self.reserve()
        except TimeoutException:
            print("不用 再輸入乘客編號\n")

    def login(self):
        try:
            self.wait_element('customerName').send_keys(self.data['name'])
            self.wait_element('idCode').send_keys(self.data['num'])
            (self.wait_element('loginButton')).click()
        except AttributeError as attrErr:
            print(attrErr)
            exit("The login function error.")

    def wait_load(self):
        wait = 1
        while wait == 1:
            time.sleep(0.1)
            try:
                self.driver.find_element_by_css_selector(self.css["backMain"])
            except NoSuchElementException:
                time.sleep(0.1)
                wait = 0

    def reserve(self):
        try:
            (self.wait_element('bookingButton', 'css')).click()
            # self.wait_load()
            time.sleep(2)
            (self.wait_element('checkNumber')).send_keys(self.data['num'])
            (self.wait_element('sendButton')).click()
        except (AttributeError, ElementNotInteractableException) as except_reserve:
            print(except_reserve)
            exit("The reserve function error.")

    def reduce_overflow(self, hh, mm, min):
        hh -= 1
        mm += 60
        new_time = datetime.time(hh, mm - min)
        return new_time.strftime("%H:%M")

    def add_overflow(self, hh, mm, min):
        hh += 1
        mm -= 60
        new_time = datetime.time(hh, mm + min)
        return new_time.strftime("%H:%M")

    def operation_time(self, hh, mm, min, mode):
        hh = int(hh)
        mm = int(mm)
        if mode == 'reduce':
            try:
                new_time = datetime.time(hh, mm - min)
                return new_time.strftime("%H:%M")
            except ValueError:
                return str(self.reduce_overflow(hh, mm, min))
        elif mode == 'add':
            try:
                new_time = datetime.time(hh, mm + min)
                return new_time.strftime("%H:%M")
            except ValueError:
                return str(self.add_overflow(hh, mm, min))

    def reset_time(self, mytime, mode):
        h, m = mytime.split(':')
        return self.operation_time(h, m, 15, mode)

    def check_has_car(self, get_car_time, time_data_name):
        print("== 檢查班次 是否有車班 ==")
        # regex = re.compile(r'%s \[(有車班|車班已滿\.排候補)\]' % self.data[time_data_name])
        regex = re.compile(r'%s \[(有車班|車班已滿\.排候補)]' % self.data[time_data_name])
        car_status = regex.search(get_car_time)
        # my_debug_log(car_status.groups())

        if car_status.group(1) != '有車班':
            print(self.data[time_data_name] + "=> 車班已滿")
            return 0
        else:
            print(self.data[time_data_name] + "=> 有車班")
            return 1

    def go_back_check(self, css_path_name, time_data_name, path_method):
        change_title = None
        if time_data_name == 'go_time':
            change_title = "去程"
        elif time_data_name == 'back_time':
            change_title = "回程"

        get_time = self.driver.find_element_by_css_selector("table#innerTable > tbody").text
        old_time = self.data[time_data_name]
        count = 0
        while count < 4:
            car_result = self.check_has_car(get_time, time_data_name)
            if car_result == 0:
                self.data[time_data_name] = self.reset_time(self.data[time_data_name], path_method)
            else:
                self.css[css_path_name] = 'input[type=radio][onclick*="%s"]' % self.data[time_data_name]
                print("更改[%s] %s => [%s]" % (change_title, old_time, self.data[time_data_name]))
                print("=======================\n")
                count = 999
            count += 1

    def choose(self):
        try:
            (self.wait_element('dateButton')).click()
            (self.wait_element('setGoButton')).click()
            self.go_back_check('goTimeButton', 'go_time', 'reduce')
            # self.check_enter()
            (self.wait_element('goTimeButton')).click()
            (self.wait_element('setBackButton')).click()
            # self.check_enter()
            self.go_back_check('backTimeButton', 'back_time', 'add')
            (self.wait_element('backTimeButton')).click()
            (self.wait_element('sendButton')).click()
        finally:
            pass
        # except AttributeError as attrErr:
        #     print(attrErr)
        #     exit("The choose function error.")

    def address(self):
        try:
            self.wait_element('goOnAreaIn').click()
            Select(self.wait_element('goOnCitySelect')).select_by_value(self.data['go_on_city'])
            Select(self.wait_element('goOnAreaSelect')).select_by_value(self.data['go_on_area'])
            go_on_addr = self.wait_element('goOnAddress')
            go_on_addr.clear()
            go_on_addr.send_keys(self.data['go_on_address'])

            (self.wait_element('goOffAreaIn')).click()
            Select(self.wait_element('goOffCitySelect')).select_by_value(self.data['go_off_city'])
            Select(self.wait_element('goOffAreaSelect')).select_by_value(self.data['go_off_area'])
            go_off_addr = self.wait_element('goOffAddress')
            go_off_addr.clear()
            go_off_addr.send_keys(self.data['go_off_address'])

            message = self.wait_element('message')
            message.clear()
            message.send_keys(self.data['Message'])

            (self.wait_element('backOnAreaIn')).click()
            Select(self.wait_element('backOnCitySelect')).select_by_value(self.data['back_on_city'])
            Select(self.wait_element('backOnAreaSelect')).select_by_value(self.data['back_on_area'])
            back_on_addr = self.wait_element('backOnAddress')
            back_on_addr.clear()
            back_on_addr.send_keys(self.data['back_on_address'])

            (self.wait_element('backOffAreaIn')).click()
            Select(self.wait_element('backOffCitySelect')).select_by_value(self.data['back_off_city'])
            Select(self.wait_element('backOffAreaSelect')).select_by_value(self.data['back_off_area'])
            back_off_addr = self.wait_element('backOffAddress')
            back_off_addr.clear()
            back_off_addr.send_keys(self.data['back_off_address'])
        except AttributeError as attrErr:
            print(attrErr)
            exit("The address function error.")

    def driver_quit(self):
        self.driver.quit()
        exit(0)


if __name__ == '__main__':
    ycbus = AutoReserve()
    print(u"如果瀏覽器上未使用完成請勿關閉此視窗\n")
    ycbus.login()
    ycbus.loop_now_time()
    # ycbus.reserve()
    ycbus.choose()
    ycbus.address()
    print("the %s is finish" % os.path.basename(__file__))

    q = 1
    while q == 1:
        confirm = input(u"確認使用完瀏覽器,請輸入 \"y\" Enter離開此程式與瀏覽器: ")
        if confirm == "y":
            q = 0
            ycbus.driver_quit()
