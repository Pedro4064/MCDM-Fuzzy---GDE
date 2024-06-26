import mysql.connector
from mysql.connector import pooling
from bs4 import BeautifulSoup
import threading
import requests
import json 

connection_pool = pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=10,
    pool_reset_session=True,
    host='localhost',
    database='GDE',
    user='root',
    password='db'
)

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="db",
#   database="GDE"
# )
# pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10)

MAX_NUMBER_PROFESSOR = 5683
# STARTING_PROFESSOR_INDEX = 1
STARTING_PROFESSOR_INDEX = 184
professor_id_range = list(range(STARTING_PROFESSOR_INDEX, MAX_NUMBER_PROFESSOR + 1))


def save_subjects_infos(subject_info:list[tuple], cursor):
    sql = "INSERT IGNORE INTO Subject (SubjectName, ID) VALUES (%s, %s)"
    cursor.executemany(sql, subject_info)


def save_professor_info(professor_info:tuple, cursor):
    sql = "INSERT IGNORE INTO Professor (NAME, ID) VALUES (%s, %s)"
    cursor.execute(sql, professor_info)


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

def update_professor_scores(professor_id:int, subjects:list[tuple], cursor):
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

        enough_validation = lambda tags_found: tags_found[0].text if len(tags_found) != 0 else None

        easy_score = enough_validation(soup.find_all('span', id=easy_tag_id))
        coherent_score = enough_validation(soup.find_all('span', id=coherent_tag_id))
        explanation_score = enough_validation(soup.find_all('span', id=explanation_tag_id))

        # Save data to sql
        sql = "INSERT IGNORE INTO ProfessorRankings (ProfessorID, SubjectID, Coerente, ExplicaBem, Facilidade) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (professor_id, subject[1], coherent_score, explanation_score, easy_score))

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

    with connection_pool.get_connection() as conn:
        with conn.cursor() as cursor:
            # Get all courses the professor teaches
            subjects_parsed = parse_courses_taught(soup)
            save_subjects_infos(subjects_parsed, cursor)

            # Get professor Name
            professor_name = parse_professor_name(soup)
            save_professor_info((professor_name, professor_id), cursor)

            # print(subjects_parsed)
            update_professor_scores(professor_id, subjects_parsed, cursor)

            conn.commit()

        # connection_pool.release_connection(conn)


def update_workers():
    while len(professor_id_range) != 0:
        professor_id = professor_id_range.pop(0)
        try:
            print('[UPDATING] Trying to update id:', professor_id)
            update_professor_infos(professor_id)
        except Exception as error:
            print('[ERROR] Failed to complete id:', professor_id)
            print(error)

if __name__ == '__main__':
    t1 = threading.Thread(target=update_workers)
    t2 = threading.Thread(target=update_workers)
    t3 = threading.Thread(target=update_workers)
    t4 = threading.Thread(target=update_workers)
    t5 = threading.Thread(target=update_workers)
    t6 = threading.Thread(target=update_workers)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()