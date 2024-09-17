import bs4
import xlsxwriter
import requests

# URL страницы для парсинга
main_url = 'https://trade59.ru/'

# Заголовки для запроса (иногда требуется для обхода блокировок)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

data = [['Наименование', 'Цена', 'URL', 'Картинка']]


# Функция для получения и парсинга страницы
def get_soup(url):
    res = requests.get(url, headers=headers)
    return bs4.BeautifulSoup(res.text, 'html.parser')


# Парсим страницу категорий
categories_page = get_soup(main_url + 'catalog.html?cid=7')
categories = categories_page.findAll('a', class_='cat_item_color')

# Проходим по каждой категории
for cat in categories:
    subcategories_page = get_soup(main_url + cat['href'])

    # Парсим подкатегории для каждой категории
    subcategories = subcategories_page.findAll('a', class_='cat_item_color')

    for subcat in subcategories:
        iphones_page = get_soup(main_url + subcat['href'])

        # Ищем товары
        iphones = iphones_page.findAll('div', class_='items-list')

        for iphone in iphones:
            # Извлекаем название товара
            title_tag = iphone.find('a')
            title = title_tag['title'].strip() if title_tag else 'No Title'

            # Извлекаем цену
            price_tag = iphone.find('div', class_='price')
            price = price_tag.get_text(strip=True) if price_tag else 'No Price'

            # Извлекаем URL товара
            url = title_tag['href'].strip() if title_tag else 'No URL'

            # Извлекаем URL картинки
            img_div = iphone.find('div', class_='image')
            if img_div and 'style' in img_div.attrs:
                img = img_div['style'].split('url(')[1].split(')')[0].replace('/tn/', '/source/')
            else:
                img = 'No Image'

            # Добавляем данные в таблицу
            data.append([title, price, main_url + url, main_url + img])

# Сохраняем данные в Excel
with xlsxwriter.Workbook('iphones.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, info in enumerate(data):
        worksheet.write_row(row_num, 0, info)

print("Парсинг завершен, данные сохранены в 'iphones.xlsx'.")
