from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .data_processing import process

PAGE_URL='https://finki.edupage.org/timetable/'
driver=webdriver.Chrome()
driver.get(PAGE_URL)

try:
    svg_selector=(By.CSS_SELECTOR,'svg')

    driver_wait=WebDriverWait(driver, 2)
    driver_wait.until(EC.presence_of_element_located(svg_selector))

    cls_dropdown=driver.find_element(By.CSS_SELECTOR,'span[title="Classes"]')
    cls_dropdown.click()
    driver_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.dropDownPanel')))

    cls_list=driver.find_elements(By.CSS_SELECTOR,'.dropDownPanel > li > a')
    cls_list[-11].click()

    driver_wait.until(EC.presence_of_element_located(svg_selector))

    indexhtml_fd=open("./src/index.html","w")
    svg_el=driver.find_element(By.CSS_SELECTOR,'svg')
    indexhtml_fd.write(svg_el.get_attribute('innerHTML'))

    process()
except Exception as e:
    print(e)
finally:
    driver.quit()