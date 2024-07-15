import requests
from bs4 import BeautifulSoup
import csv

# CSV文件名
csv_filename = 'contract_addresses.csv'

# 读取CSV文件中的智能合约地址并遍历
with open(csv_filename, newline='', encoding='utf-8') as csvfile:
    contract_reader = csv.DictReader(csvfile)  # 使用DictReader来读取列名

    for row in contract_reader:
        contract_address = row['Addresses']  # 读取名为'addresses'的列
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        # Etherscan的URL，用于获取合约源代码
        url = f'https://etherscan.io/address/{contract_address}#code'

        # 发送HTTP请求
        response = requests.get(url, headers=headers)

        # 检查请求是否成功
        if response.status_code == 200:
            # 获取网页内容
            webpage_content = response.text

            # 使用BeautifulSoup解析网页内容
            soup = BeautifulSoup(webpage_content, 'html.parser')

            # 查找所有class为"js-sourcecopyarea editor"的<pre>标签
            pre_tags = soup.find_all('pre', class_='js-sourcecopyarea editor')

            # 检查是否找到<pre>标签
            if pre_tags:
                # 假设每个智能合约只有一个<pre>标签
                pre_tag = pre_tags[0]
                # 获取<pre>标签的文本内容
                contract_source_code = pre_tag.get_text(strip=True)

                # 定义文件名
                contract_filename = f'{contract_address}.sol'

                # 将源代码写入文件，使用utf-8编码
                with open(contract_filename, 'w', encoding='utf-8') as file:
                    file.write(contract_source_code)

                print(f'Contract source code saved as {contract_filename}')
            else:
                print(f"No contract source code found for {contract_address}.")
        else:
            print(f'Error: {response.status_code} for {contract_address}')
