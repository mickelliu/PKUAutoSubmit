import datetime
import time
import warnings
from urllib.parse import quote

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

warnings.filterwarnings('ignore')


def login(driver, userName, password, retry=0):
    if retry == 3:
        raise Exception('门户登录失败')

    print('门户登陆中...')

    appID = 'portal2017'
    iaaaUrl = 'https://iaaa.pku.edu.cn/iaaa/oauth.jsp'
    appName = quote('北京大学校内信息门户新版')
    redirectUrl = 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'

    driver.get('https://portal.pku.edu.cn/portal2017/')
    driver.get(
        f'{iaaaUrl}?appID={appID}&appName={appName}&redirectUrl={redirectUrl}')
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'logon_button')))
    driver.find_element(By.ID, 'user_name').send_keys(userName)
    time.sleep(0.1)
    driver.find_element(By.ID, 'password').send_keys(password)
    time.sleep(0.1)
    driver.find_element(By.ID, 'logon_button').click()
    try:
        WebDriverWait(driver,
                      5).until(EC.visibility_of_element_located((By.ID, 'all')))
        print('门户登录成功！')
    except:
        print('Retrying...')
        login(driver, userName, password, retry + 1)


def go_to_simso(driver):
    butt_all = driver.find_element(By.ID, 'all')
    driver.execute_script('arguments[0].click();', butt_all)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'tag_s_stuCampusExEnReq')))
    driver.find_element(By.ID, 'tag_s_stuCampusExEnReq').click()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))


def go_to_application_out(driver):
    go_to_simso(driver)
    driver.find_element(By.CLASS_NAME, 'el-card__body').click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//button/span[contains(text(), "确定")]'))).click()


def go_to_application_in(driver, userName, password):
    driver.back()
    time.sleep(0.5)
    driver.back()
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))
        time.sleep(0.5)
        driver.find_element_by_class_name('el-card__body').click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'el-select')))
    except:
        print('检测到会话失效，重新登陆中...')
        login(driver, userName, password)
        go_to_simso(driver)
        driver.find_element_by_class_name('el-card__body').click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'el-select')))


def submit(driver):
    driver.find_element_by_xpath(
        '//button/span[contains(text(),"保存")]').click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '(//button/span[contains(text(),"提交")])[3]')))
    driver.find_element_by_xpath(
        '(//button/span[contains(text(),"提交")])[3]').click()
    time.sleep(0.1)


def fill_out(driver, config_dict):
    print('开始填报出入校申请')

    print('出入校日期    ', end='')
    driver.find_elements(By.CLASS_NAME, 'el-input__inner')[0].clear()
    driver.find_elements(By.CLASS_NAME, 'el-input__inner')[0].send_keys((datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
    print('Done')
    time.sleep(0.5)

    print('出入校事由    ', end='')
    driver.find_elements(By.CLASS_NAME, 'el-input__inner')[1].click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_any_elements_located(
            (By.XPATH, f'//li/span[text()="{config_dict["出入校事由"]}"]')))[-1].click()
    print('Done')
    time.sleep(0.5)

    print('出入校起点    ', end='')
    driver.find_elements(By.CLASS_NAME, 'el-input__inner')[2].click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_any_elements_located(
            (By.XPATH, f'//li/span[text()="{config_dict["出入校起点"]}"]')))[-1].click()
    print('Done')
    time.sleep(0.5)

    print('出入校终点    ', end='')
    driver.find_elements(By.CLASS_NAME, 'el-input__inner')[3].click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_any_elements_located(
            (By.XPATH, f'//li/span[text()="{config_dict["出入校终点"]}"]')))[-1].click()
    print('Done')
    time.sleep(0.5)

    print('出入校具体事项    ', end='')
    driver.find_elements(By.CLASS_NAME, 'el-textarea__inner')[0].send_keys(config_dict["出入校具体事项"])
    print('Done')
    time.sleep(0.5)

    if config_dict["出入校终点"] == '校外（社会面）' or config_dict["出入校起点"] == '校外（社会面）':
        print('起终点具体地址    ', end='')
        province = config_dict.get("终点所在省") or config_dict.get("起点所在省")
        driver.find_elements(By.CLASS_NAME, 'el-input__inner')[5].click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_any_elements_located(
                (By.XPATH, f'//li/span[text()="{province}"]')))[-1].click()
        time.sleep(0.5)

        muni = config_dict.get("终点所在地级市") or config_dict.get("起点所在地级市")
        driver.find_elements(By.CLASS_NAME, 'el-input__inner')[6].click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_any_elements_located(
                (By.XPATH, f'//li/span[text()="{muni}"]')))[-1].click()
        time.sleep(0.5)

        district = config_dict.get("起点所在区县") or config_dict.get("终点所在区县")
        driver.find_elements(By.CLASS_NAME, 'el-input__inner')[7].click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_any_elements_located(
                (By.XPATH, f'//li/span[text()="{district}"]')))[-1].click()
        time.sleep(0.5)

        street = config_dict.get("起点所在街道") or config_dict.get("终点所在街道")
        driver.find_elements(By.CLASS_NAME, 'el-input__inner')[8].send_keys(street)
        print('Done')

    print('详细轨迹', end='')
    driver.find_elements(By.CLASS_NAME, 'el-textarea__inner')[1].send_keys(config_dict["详细轨迹"])
    print('Done')

    print('补充说明', end='')
    driver.find_elements(By.CLASS_NAME, 'el-textarea__inner')[2].send_keys(config_dict["补充说明"])
    print('Done')

    driver.find_element(By.XPATH, f'//button/span[text()="保存 "]').click()
    if WebDriverWait(driver, 2).until(
            EC.visibility_of_any_elements_located(
                (By.CLASS_NAME, 'el-message--error'))):
        print('已经有申请了，不能再次申请。')
    else:
        WebDriverWait(driver, 2).until(
            EC.visibility_of_any_elements_located(
                (By.XPATH, f'//button/span[contains(text(), "提交")]')))[-1].click()
        print('填报完毕！')


def run(driver, credentials, config_dict):
    login(driver, credentials['username'], credentials['password'])
    print('=================================')

    go_to_application_out(driver)
    fill_out(driver, config_dict)
    print('=================================')


if __name__ == '__main__':
    pass
