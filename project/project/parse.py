# coding: utf-8
import lxml.html
import lxml.etree
import urllib2
import cssselect


def get_document(domain, link):
    page = urllib2.urlopen(domain + link)
    return lxml.html.document_fromstring(page.read())

words = []  # Первые буквы исполнителей
authors = []  # Исполнители песен
songs = []  # Песни
results = []  # Группа Песня Текст Перевод Ссылка

doc = get_document('http://www.amalgama-lab.com', '')

for word in doc.cssselect('#az_nav ul li a'):
    words.append([word.text, ''.join(word.attrib.values())])

# for word in words:
#     doc = get_document('http://www.amalgama-lab.com', word[1])
#
#     for author in doc.cssselect('.band_name_pict div a'):
#         authors.append([author.text, ''.join(author.attrib.values())])

authors.append(['ff', '/songs/1/1_giant_leap/'])
#authors.append(['ff', '/songs/r/rammstein/'])

for author in authors:
    doc = get_document('http://www.amalgama-lab.com', author[1])

    for song in doc.cssselect('#songs_nav ul ul li a'):
        songs.append([song.text, 'http://www.amalgama-lab.com' + author[1] + ''.join(song.attrib.values()), author[0]])

for song in songs:
    doc = get_document('http://www.amalgama-lab.com/songs/r/rammstein/du_hast.html', '')
    original_text = []
    translate_text = []

    title = doc.cssselect('.texts div h2')[0].text
    text = ''
    titleLines = []

    for title in doc.cssselect('.texts div .original strong'):
        titleLines.append(title.sourceline)

    for line in doc.cssselect('.texts div .original'):
        print line.sourceline
        print titleLines
        if titleLines.count(line.sourceline+2):
            text = '---->' + title + '\n' + text
            original_text.append(text)
            text = ''
            title = line.text

        if line.text is not None:
            text += line.text
            text += '\n'
        else:
            text += '\n'

    print text
