import requests
import re
from bs4 import BeautifulSoup

from writers import TxtWriter, CSVWriter, DBWriter, JSONWriter

ROOT = 'https://www.work.ua'


full_url = ROOT + '/ru/jobs/'
job_details_url = ROOT + '/jobs/'

page = 0

writers_list = [
    TxtWriter(),
    CSVWriter(),
    DBWriter(),
]

while True:
    page += 1
    print(f'Page: {page}')

    params = {
        'page': page,
    }
    if page == 2:
        break

    response = requests.get(full_url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_list_container = soup.find("div", {"id": "pjax-job-list"})

    # no jobs left
    if job_list_container is None:
        break

    jobs = job_list_container.find_all('div', {'class': 'card card-hover card-visited wordwrap job-link js-hot-block'})

    for job in jobs:
        href = job.find('a')['href']
        id_ = ''.join(char for char in href if char.isdigit())
        title = job.find('a').text
        job_info = {
            'href': href,
            'title': title,
            'id': id_,
        }

        response_d = requests.get(job_details_url + f'{job_info["id"]}/')
        soup = BeautifulSoup(response_d.text, 'html.parser')
        job_details_container = soup.find("div", {"class": "card wordwrap"})

        job_payment_raw = job_details_container.find('b', {'class': 'text-black'})
        if job_payment_raw is None:
            payment = "Payment is not specified"
        else:
            job_payment_raw_data = job_payment_raw.get_text()
            payment = re.sub(r'\s+', ' ', job_payment_raw_data).strip()

        job_title = job_details_container.find('h1', {'id': 'h1-name'}).get_text()

        job_description_raw = job_details_container.find('div', {'id': 'job-description'})
        children = job_description_raw.findChildren("p")
        job_description_str = children[0].get_text()
        job_description = job_description_str.translate({ord("'"): None})

        job_info = {
            'href': href,
            'title': title,
            'id': id_,
            'job_title': job_title,
            'payment': payment,
            'job_description': job_description,
        }
        for writer in writers_list:
            writer.write(job_info)

        # file.write(f"{job_info['href']} {job_info['title']} {job_info['id']}\n")
        # result.append(job_info)
JSONwr = JSONWriter()
JSONwr.get_json_data()
