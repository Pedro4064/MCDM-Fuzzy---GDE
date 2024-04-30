import mysql.connector
from bs4 import BeautifulSoup
import requests
import json 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="db",
  database="GDE"
)
mycursor = mydb.cursor()


def save_subjects_infos(subject_info:list[tuple]):
    sql = "INSERT IGNORE INTO Subject (SubjectName, ID) VALUES (%s, %s)"
    mycursor.executemany(sql, subject_info)
    mydb.commit()

def save_professor_info(professor_info:tuple):
    sql = "INSERT IGNORE INTO Professor (NAME, ID) VALUES (%s, %s)"
    mycursor.execute(sql, professor_info)
    mydb.commit()

def parse_courses_taught(soup_data:BeautifulSoup):
    selectable_menu = soup_data.find_all('select',class_='avaliacao_oferecimento')

    # Get all the subjects the professor teaches, but the first tag retrieved is only the button label, so discart it
    subjects = selectable_menu[0].find_all('option')
    subjects.pop(0)

    subjects_parsed = [(subject_tag.text, subject_tag.get('value')) for subject_tag in subjects]
    return subjects_parsed

def parse_professor_name(soup_data:BeautifulSoup):
    name_tags = soup_data.find_all('div', id='perfil_cabecalho_nome')
    name = name_tags[0].text.replace('\n', '').replace('\t', '')
    return name

def update_professor_scores(professor_id:int, subjects:list[tuple]):
    cookies = {
        '_ga': 'GA1.1.1807215295.1713555027',
        '_ga_LF4MP0Z2VG': 'GS1.1.1714153287.19.1.1714153434.0.0.0',
        'GDES': 'p6f7lg2q0bcsj1dlcp3qn7slcq',
        '__utmc': '61793146',
        '__utmz': '61793146.1714403796.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
        'gde_token': '1791677.39896.ab6c7678566a820bd42f7a7107dc9519279eb86e7cc196bb5872e0c019710ddc8745d03671e7cd48104570ec31af6127999d181d2841647428036de9',
        'csrfptoken': '074a2ad29c78ee7a20e7d0ed9c89243b',
        '__utma': '61793146.1807215295.1713555027.1714428245.1714430186.4',
        '__utmt': '1',
        '__utmb': '61793146.32.10.1714430186',
    }
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8,my;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': '_ga=GA1.1.1807215295.1713555027; _ga_LF4MP0Z2VG=GS1.1.1714153287.19.1.1714153434.0.0.0; GDES=p6f7lg2q0bcsj1dlcp3qn7slcq; __utmc=61793146; __utmz=61793146.1714403796.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); gde_token=1791677.39896.ab6c7678566a820bd42f7a7107dc9519279eb86e7cc196bb5872e0c019710ddc8745d03671e7cd48104570ec31af6127999d181d2841647428036de9; csrfptoken=074a2ad29c78ee7a20e7d0ed9c89243b; __utma=61793146.1807215295.1713555027.1714428245.1714430186.4; __utmt=1; __utmb=61793146.32.10.1714430186',
        'Referer': 'https://grade.daconline.unicamp.br/perfil/?professor=2814',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }
    
    for subject in subjects:
        params = {
            'id_professor': professor_id,
            'id_disciplina': subject[1],
        }

        response = requests.get('https://grade.daconline.unicamp.br/ajax/avaliacoes.php', params=params, cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        coherent_tag_id = 'span_fixo_2_{PROFESSOR_ID}_{COURSE_ID}'.format(PROFESSOR_ID=professor_id, COURSE_ID=subject[1])
        explanation_tag_id = 'span_fixo_3_{PROFESSOR_ID}_{COURSE_ID}'.format(PROFESSOR_ID=professor_id, COURSE_ID=subject[1])
        easy_tag_id = 'span_fixo_4_{PROFESSOR_ID}_{COURSE_ID}'.format(PROFESSOR_ID=professor_id, COURSE_ID=subject[1])

        coherent_score = soup.find_all('span', id=coherent_score)
        print(coherent_score)

def update_professor_infos(professor_id:int):
    cookies = {
        '_ga': 'GA1.1.1807215295.1713555027',
        '_ga_LF4MP0Z2VG': 'GS1.1.1714153287.19.1.1714153434.0.0.0',
        'GDES': 'p6f7lg2q0bcsj1dlcp3qn7slcq',
        '__utmc': '61793146',
        '__utmz': '61793146.1714403796.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
        'gde_token': '1791677.39896.ab6c7678566a820bd42f7a7107dc9519279eb86e7cc196bb5872e0c019710ddc8745d03671e7cd48104570ec31af6127999d181d2841647428036de9',
        'csrfptoken': '074a2ad29c78ee7a20e7d0ed9c89243b',
        '__utma': '61793146.1807215295.1713555027.1714428245.1714430186.4',
        '__utmb': '61793146.45.10.1714430186',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8,my;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': '_ga=GA1.1.1807215295.1713555027; _ga_LF4MP0Z2VG=GS1.1.1714153287.19.1.1714153434.0.0.0; GDES=p6f7lg2q0bcsj1dlcp3qn7slcq; __utmc=61793146; __utmz=61793146.1714403796.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); gde_token=1791677.39896.ab6c7678566a820bd42f7a7107dc9519279eb86e7cc196bb5872e0c019710ddc8745d03671e7cd48104570ec31af6127999d181d2841647428036de9; csrfptoken=074a2ad29c78ee7a20e7d0ed9c89243b; __utma=61793146.1807215295.1713555027.1714428245.1714430186.4; __utmb=61793146.45.10.1714430186',
        'Referer': 'https://grade.daconline.unicamp.br/disciplina/4084/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    params = {
        'professor': professor_id,
    }

    response = requests.get('https://grade.daconline.unicamp.br/perfil/', params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get all courses the professor teaches
    subjects_parsed = parse_courses_taught(soup)
    save_subjects_infos(subjects_parsed)

    # Get professor Name
    professor_name = parse_professor_name(soup)
    save_professor_info((professor_name, professor_id))

    # print(subjects_parsed)
    update_professor_scores(professor_id, subjects_parsed)

if __name__ == '__main__':
    update_professor_infos(2814)