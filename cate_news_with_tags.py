import requests


def get_info(news_id):
    res = requests.get(f'https://www.taiwannews.com.tw/en/news/{news_id}')
    res_html = res.text.split('\n')
    title_and_tags = []
    
    for line in res_html:
        if not title_and_tags:
            prefix = '<title>'
            suffix = '</title>'
        else:
            prefix = '<div class="fa fa-fw fa-tag"></div>'
            suffix = '</span></a>'

        i = line.find(prefix)
        if i > -1:
            j = line.find(suffix)
            title_and_tags.append(line[i + len(prefix):j])
    
    return title_and_tags


def get_news_id_list(cate_id, required=20):
    res = requests.get(f'https://www.taiwannews.com.tw/en/cate/{cate_id}')
    res_html = res.text.split('\n')
    all_news_id = []
    
    for line in res_html:
        prefix = '<header class="entry-header"><a href="/en/news/'
        i = line.find(prefix)
        if i > -1:
            news_id = []
            for c in line[i + len(prefix):]:
                if c.isdigit():
                    news_id.append(c)
                else:
                    break
            all_news_id.append(int(''.join(news_id)))
    
    res = requests.get(f'https://www.taiwannews.com.tw/news/pagination/category?offset={len(all_news_id) - 1}&paginate={required - len(all_news_id)}&cate={cate_id}')
    rj = res.json()
    for x in rj['data']:
        all_news_id.append(x['id'])
    
    return all_news_id


if __name__ == "__main__":
    world = 3
    politics = 9
    business = 5
    society = 7
    culture = 4
    opinion = 12
    travel_and_uisine = 10
    new_immigrants = 11
    sport_and_entertainment = 13
    environment = 14
    food_safety_and_health = 16
    photo_of_the_day = 37

    cate_to_parse = [world, politics]
    for cate_id in cate_to_parse:
        all_news_id_list = get_news_id_list(cate_id)
        for news_id in all_news_id_list:
            title_and_tags = get_info(news_id)
            print(title_and_tags)
