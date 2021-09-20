import requests
import re
from bs4 import BeautifulSoup

from writers import TxtWriter, CSVWriter


ROOT = 'https://www.work.ua'


full_url = ROOT + '/ru/jobs/'
job_details_url = ROOT + '/jobs/'

page = 1

params = {
    'page': page,
}

response = requests.get(full_url, params=params)
soup = BeautifulSoup(response.text, 'html.parser')
job_list_container = soup.find("div", {"id": "pjax-job-list"})

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
    print(response_d.url)
    soup = BeautifulSoup(response_d.text, 'html.parser')
    job_details_container = soup.find("div", {"class": "card wordwrap"})

    job_payment_raw = job_details_container.find('b', {'class': 'text-black'})
    if job_payment_raw is None:
        payment = "Payment is not specified"
    else:
        job_payment_raw_data = job_payment_raw.get_text()
        payment = re.sub(r'\s+', ' ', job_payment_raw_data).strip()

    job_title = job_details_container.find('h1', {'id': 'h1-name'}).get_text()

    # job_hot_label = job_details_container.find('span', {'class': 'label label-hot'}).get_text()
    # company_details_data = job_details_container.find_all('a')
    # children = company_details_data.findChildren()
    # # company_name = company_details_data.findChildren['b'].text
    # company_name = children[0].get_text()
    # company_name = company_details_data.find('b').get_text()
    job_description_raw = job_details_container.find('div', {'id': 'job-description'})
    children_1 = job_description_raw.findChildren("p")
    job_description = children_1[0].get_text()

    job_info = {
        'href': href,
        'title': title,
        'id': id_,
        'Job Title': job_title,
        'payment': payment,
        'job_description': job_description,
    }

    print(job_info)

        # file.write(f"{job_info['href']} {job_info['title']} {job_info['id']}\n")
        # result.append(job_info)
