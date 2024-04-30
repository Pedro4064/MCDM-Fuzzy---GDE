import requests
import json

# cookies = {
#     '_ga': 'GA1.1.1807215295.1713555027',
#     '_ga_LF4MP0Z2VG': 'GS1.1.1714153287.19.1.1714153434.0.0.0',
#     'GDES': 'p6f7lg2q0bcsj1dlcp3qn7slcq',
#     '__utmc': '61793146',
#     '__utmz': '61793146.1714403796.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
#     'gde_token': '1791677.39896.ab6c7678566a820bd42f7a7107dc9519279eb86e7cc196bb5872e0c019710ddc8745d03671e7cd48104570ec31af6127999d181d2841647428036de9',
#     'csrfptoken': '074a2ad29c78ee7a20e7d0ed9c89243b',
#     '__utma': '61793146.1807215295.1713555027.1714428245.1714430186.4',
#     '__utmt': '1',
#     '__utmb': '61793146.9.10.1714430186',
# }

# headers = {
#     'Connection': 'keep-alive',
#     # 'Cookie': '_ga=GA1.1.1807215295.1713555027; _ga_LF4MP0Z2VG=GS1.1.1714153287.19.1.1714153434.0.0.0; GDES=p6f7lg2q0bcsj1dlcp3qn7slcq; __utmc=61793146; __utmz=61793146.1714403796.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); gde_token=1791677.39896.ab6c7678566a820bd42f7a7107dc9519279eb86e7cc196bb5872e0c019710ddc8745d03671e7cd48104570ec31af6127999d181d2841647428036de9; csrfptoken=074a2ad29c78ee7a20e7d0ed9c89243b; __utma=61793146.1807215295.1713555027.1714428245.1714430186.4; __utmt=1; __utmb=61793146.9.10.1714430186',
#     'Origin': 'https://grade.daconline.unicamp.br',
#     'Referer': 'https://grade.daconline.unicamp.br/planejador/',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
#     'accept': '*/*',
#     'accept-language': 'en-US,en;q=0.9,pt;q=0.8,my;q=0.7',
#     'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Linux"',
#     'x-csrfp-token': '074a2ad29c78ee7a20e7d0ed9c89243b',
#     'x-requested-with': 'XMLHttpRequest',
# }

# data = {
#     'id': '545273',
#     'a': 'c',
#     'c': '0',
#     'pp': '20242',
#     'pa': '',
# }

# response = requests.post('https://grade.daconline.unicamp.br/ajax/planejador.php', cookies=cookies, headers=headers, data=data)
# print(json.dumps(response.json(), indent=4))

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

params = {
    'id_professor': '2814',
    'id_disciplina': '9219',
}

response = requests.get('https://grade.daconline.unicamp.br/ajax/avaliacoes.php', params=params, cookies=cookies, headers=headers)
print(response.text)