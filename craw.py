import os
import requests
from bs4 import BeautifulSoup

def download_pic(chapter_name,largest_page_num,image_link):
    print("Total ",largest_page_num, " images needed to be downloaded")
    if(largest_page_num>30):
        choose=input("The download may be slow for so many pics,do you still want to download?(y/n)")
        if choose == 'y':
            flag = 1
        else:
            flag = 0
            print("Download abort.")
    else:
        flag = 1

    if flag==1:
        su_count = 0
        for i in range(1,largest_page_num):
            img_name = str(i)+".jpg"
            url = image_link.replace(image_link.split('/')[-1],img_name)
            if not os.path.exists(chapter_name):
                os.mkdir(chapter_name)
            if requests.get(url).status_code == 200:
                 with open(os.path.join(chapter_name, img_name), 'wb') as imgf:
                    imgf.write(requests.get(url).content)
                    print("Saving image " ,img_name)
                    su_count+=1
            else:
                print("Fail to fetch images",img_name)
        print(su_count,"/",largest_page_num," of the pics download successfully")


def go_request(proxies,search_url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/71.0.3578.98 Safari/537.36"

    resp= requests.get(search_url, proxies=proxies, headers={"User-Agent": user_agent},timeout=5)
    if resp.status_code == 404:
        return None
    else:
        soup = BeautifulSoup(resp.content,'html.parser')
        return soup

def ask_for_pic(proxies,search_url):
    soup = go_request(proxies,search_url)
    chapter_name = soup.h1.text
    soup = go_request(proxies,search_url+"/1")
    largest_page_num = int(soup.find_all('span')[5].text)
    image_link = soup.find_all('img')[1].get('src')
    print("Manga " ,chapter_name," found.Start downloading..")
    download_pic(chapter_name,largest_page_num,image_link)



#using proxy if needed
#install requests[socks] before using the socks5 proxy of the requests lib.

proxies = {
    'http': 'http://127.0.0.1:2000',
    'https': 'https://127.0.0.1:2000'
}

if __name__ == '__main__':
    #use this to get manga page
    manga_no = input("please enter the id of manga\n")
    url_body = "https://nhentai.net/g/"
    search_url = url_body+manga_no
    if(go_request(proxies,search_url)!=None):
        ask_for_pic(proxies,search_url)
    else:
        print("Manga doesn't exist!")










