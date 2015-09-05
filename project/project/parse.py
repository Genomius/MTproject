# coding: utf-8

"""
Методы, приведенные ниже, выкачивают с сайта всю базу по всем исполнителям и композициям
и сохраняет ее в локальную базу.
"""

import lxml.html
import lxml.etree
import urllib2


def get_document(domain, link):
    page = urllib2.urlopen(domain + link)
    return lxml.html.document_fromstring(page.read())

words = []  # Первые буквы исполнителей
authors = []  # Исполнители песен
songs = []  # Песни
results = []  # Группа Песня Текст Перевод Ссылка

doc = get_document('http://www.amalgama-lab.com', '')

for word in doc.cssselect('#az_nav ul li a'):  # Берем все первые буквы исполнителей
    words.append([word.text, ''.join(word.attrib.values())])  # Добавляем их в массив букв

# for word in words:
#     doc = get_document('http://www.amalgama-lab.com', word[1])
#
#     for author in doc.cssselect('.band_name_pict div a'):  # Берем всех исполнителей по каждой первой букве
#         authors.append([author.text, ''.join(author.attrib.values())])  # Добавляем их в массив исполнителей

authors.append(['ff', '/songs/1/1_giant_leap/'])
# authors.append(['ff', '/songs/r/rammstein/'])

for author in authors:
    doc = get_document('http://www.amalgama-lab.com', author[1])

    for song in doc.cssselect('#songs_nav ul ul li a'):  # Берем все композиции для каждого исполнителя
        songs.append([song.text, 'http://www.amalgama-lab.com' + author[1] + ''.join(song.attrib.values()), author[0]])
        # Добавляем их в массив композиций

for song in songs:
    doc = get_document('http://www.amalgama-lab.com/songs/r/rammstein/benzin.html', '')

    first_original_title = doc.cssselect('.texts div .original')[0].text
    first_translate_title = doc.cssselect('.texts div .translate')[0].text
    original_titles_line_number = []
    translate_titles_line_number = []
    text = ''

    original_text = []
    translate_text = []
    original_titles = [first_original_title]
    translate_titles = [first_translate_title]

    for other_title in doc.cssselect('.texts #click_area .original strong'):
        original_titles_line_number.append(other_title.sourceline)
        original_titles.append(other_title.text)

    for other_title in doc.cssselect('.texts #click_area .translate strong'):
        translate = other_title.text.encode('utf-8')

        translate_titles_line_number.append(other_title.sourceline)
        translate_titles.append(translate)

    titleLinesNumberCount = len(original_titles_line_number)  # Количество титолов всего
    last_element = doc.cssselect('.texts #click_area .original')[-1]  # Последняя строка

    for line in doc.cssselect('.texts #click_area .original'):
        if original_titles_line_number:
            if line.sourceline >= original_titles_line_number[0]:
                original_text.append(text)
                text = ''
                original_titles_line_number.pop(0)

        if line.text is not None:
            text += line.text

            if titleLinesNumberCount == len(original_titles_line_number):
                text += '\n'
        else:
            text += '\n'

        if line == last_element:
            original_text.append(text)

    text = ''
    titleLinesNumberCount = len(translate_titles_line_number)  # Количество титолов всего
    last_element = doc.cssselect('.texts #click_area .translate')[-1]  # Последняя строка

    for line in doc.cssselect('.texts #click_area .translate'):
        if translate_titles_line_number:
            if line.sourceline >= translate_titles_line_number[0]:
                translate_text.append(text)
                text = ''
                translate_titles_line_number.pop(0)

        if line.text is not None:
            text += line.text

            if titleLinesNumberCount == len(translate_titles_line_number):
                text += '\n'
        else:
            text += '\n'

        if line == last_element:
            translate_text.append(text)