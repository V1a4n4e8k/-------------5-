import threading
import time
from bs4 import BeautifulSoup, element
from selenium import webdriver
import pandas as pd
url = 'https://www.avito.ru/brands/i357584534/items/all/odezhda_obuv_aksessuary?s=profile_search_show_all&sellerId=0ef4c451e53ee39b40d7a251d5721b08'

def parse(url):
    driver = webdriver.Firefox()
    driver.get(url)
    scroll_pause_time = 0.3  
    screen_height = driver.execute_script("return window.screen.height;")  
    i = 1
    immage_list = []
    href_list = []
    title_list = []
    while True:
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)

        if i > 300:
            break
            
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    atag = soup.find_all("a", class_="iva-item-sliderLink-uLz1v")
    
    for item in atag:
        href = 'https://www.avito.ru' + item.get('href')
        href_list.append(href)

        title = item.get('title')
        title = str(title).lstrip('Объявление «')[:-14]
        title_list.append(title)

        immagediv = item.find('li', class_='photo-slider-list-item-h3A51')
        if isinstance(immagediv, element.Tag):
            immage = immagediv.get('data-marker')
            immage = str(immage).lstrip('slider-image/image-')
            immage_list.append(immage)
        else:
            immage_list.append('no_image')

    driver.quit()

    info_dict = {'href': href_list, 'title': title_list, 'image': immage_list}
    return info_dict
parsed_dict = parse(url)
def start_parsing():
    while True:
        info_d = parse(url)
        print(info_d)
        time.sleep(20)
def filter_and_save():   
    df_to_add = pd.DataFrame(parsed_dict)
    df_been_sent = pd.read_csv('been_sent.csv', index_col=0)
    filtered_df = df_to_add[~df_to_add.apply(tuple, 1).isin(df_been_sent.apply(tuple, 1))]
    df_been_sent = pd.concat([df_been_sent, filtered_df]).drop_duplicates().reset_index(drop=True)
    df_been_sent.to_csv('been_sent.csv', index_label='index')



#thread = threading.Thread(target=start_parsing)
#thread.start()

#while True:
    #time.sleep(10)
    #print('1')
    
print(filter_and_save())
