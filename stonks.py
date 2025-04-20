import asyncio
import json
import re
from decimal import Decimal, getcontext
from typing import List, Dict, Optional

import aiohttp
from bs4 import BeautifulSoup

getcontext().prec = 6

FINANCIAL_PORTAL = "https://markets.businessinsider.com"
STOCK_INDEX_URL = f"{FINANCIAL_PORTAL}/index/components/s&p_500?p="
CENTRAL_BANK_RATES = "https://www.cbr.ru/scripts/XML_daily.asp"


async def get_page_content(session: aiohttp.ClientSession, url: str, encoding: str = 'utf-8') -> str:
    async with session.get(url, timeout=10) as resp:
        resp.raise_for_status()
        return await resp.text(encoding=encoding)


async def fetch_exchange_rate(session: aiohttp.ClientSession) -> Decimal:
    content = await get_page_content(session, CENTRAL_BANK_RATES, 'windows-1251')
    currency_data = BeautifulSoup(content, 'lxml-xml')
    dollar_value = currency_data.find('Valute', ID="R01235").Value.string
    return Decimal(dollar_value.replace(',', '.'))


def convert_to_decimal(value: str) -> Decimal:
    clean_value = re.sub(r'[^\d.,-]', '', value).replace(',', '').strip()
    try:
        return Decimal(clean_value) if clean_value else Decimal('0')
    except Exception:
        return Decimal('0')


async def analyze_stock_data(
    session: aiohttp.ClientSession,
    stock_url: str,
    exchange_rate: Decimal
) -> Optional[Dict[str, float]]:
    page_html = await get_page_content(session, stock_url)
    stock_soup = BeautifulSoup(page_html, 'html.parser')

    header_section = stock_soup.select_one('h1.price-section__identifiers')
    if not header_section:
        return None

    stock_name = header_section.find('span', class_='price-section__label').get_text(strip=True)
    ticker = header_section.find('span', class_='price-section__category').get_text(strip=True)

    current_price = convert_to_decimal(
        stock_soup.select_one('span.price-section__current-value').text
    )
    ruble_price = current_price * exchange_rate

    pe_ratio_tag = stock_soup.find(string=re.compile(r'P/E Ratio', re.I))
    pe_ratio = convert_to_decimal(pe_ratio_tag.find_next('span').text) if pe_ratio_tag else Decimal('inf')

    try:
        low_52w = convert_to_decimal(
            stock_soup.find(string=re.compile(r'52 Week Low', re.I)).find_next('span').text
        )
        high_52w = convert_to_decimal(
            stock_soup.find(string=re.compile(r'52 Week High', re.I)).find_next('span').text
        )
        profit_potential = ((high_52w - low_52w) / low_52w) * 100 if low_52w else 0
    except AttributeError:
        profit_potential = 0

    return {
        'company': stock_name,
        'symbol': ticker,
        'price_rub': float(ruble_price),
        'pe_ratio': float(pe_ratio),
        'profit_potential': float(profit_potential),
    }


async def process_index_companies():
    results = []
    
    async with aiohttp.ClientSession() as http_session:
        current_rate = await fetch_exchange_rate(http_session)

        for page_num in (1, 2):
            page_url = f"{STOCK_INDEX_URL}{page_num}"
            index_content = await get_page_content(http_session, page_url)
            index_soup = BeautifulSoup(index_content, 'html.parser')

            for company_row in index_soup.select('table.table tbody tr'):
                columns = company_row.find_all('td')
                if len(columns) < 5:
                    continue

                company_path = columns[0].find('a')['href']
                company_url = f"{FINANCIAL_PORTAL}{company_path}"

                yearly_change_text = columns[-1].get_text(strip=True)
                yearly_change = convert_to_decimal(yearly_change_text.replace('%', ''))

                company_info = await analyze_stock_data(
                    http_session, company_url, current_rate
                )
                
                if company_info:
                    company_info['yearly_change'] = float(yearly_change)
                    results.append(company_info)

    await store_analysis_results(results)


def write_data_to_file(filename: str, records: List[Dict]):
    with open(filename, 'w', encoding='utf-8') as output_file:
        json.dump(records, output_file, indent=2, ensure_ascii=False)


async def store_analysis_results(companies_data: List[Dict]):
    write_data_to_file(
        'highest_priced.json',
        sorted(companies_data, key=lambda x: x['price_rub'], reverse=True)[:10]
    )
    
    write_data_to_file(
        'lowest_pe.json',
        sorted(companies_data, key=lambda x: x['pe_ratio'])[:10]
    )
    
    write_data_to_file(
        'fastest_growing.json',
        sorted(companies_data, key=lambda x: x['yearly_change'], reverse=True)[:10]
    )
    
    write_data_to_file(
        'highest_potential.json',
        sorted(companies_data, key=lambda x: x['profit_potential'], reverse=True)[:10]
    )


async def main():
    await process_index_companies()
    print("Data processing completed successfully")


if __name__ == '__main__':
    asyncio.run(main())