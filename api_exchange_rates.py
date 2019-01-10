# -*- coding:utf-8 -*-

import pymysql
import urllib.request
from itertools import count
import json


#   환율 크롤링 함수
def crawling_exchange_rates():
    #   환율 제공 API
    url = "https://api.exchangeratesapi.io/latest?base=KRW"

    #   API는 JSON 형태로 반환되므로, json.load 함수를 이용하여 dict 객체로 받아온다.
    data = json.load(urllib.request.urlopen(url))

    #   dict 객체에서 맨 앞의 rates를 받아온다.
    rates = data.get('rates')

    #   rates 또한 dict 객체이므로 각 환율의 키값을 받아온다.
    currencies = rates.keys()

    #   환율(KRW 기준) 프린트
    for currency in currencies:
        print(currency + " : %f" % (rates.get(currency) * 1000))

    # MySQL Connection 연결
    conn = pymysql.connect(host='localhost', port=3305, user='root', password='1234',
                           db='test', charset='utf8')

    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()

    try:
        #   currency를 루프하면서 값을 DB에 업데이트
        for currency in currencies:
            #   SQL문 작성, INSERT 문
            sql = "INSERT INTO EXCHANGE_RATES (CURRENCIES, RATES) VALUES('%s', %f)" % (currency, rates.get(currency) * 1000);

            #   UPDATE 문
            #sql = "UPDATE EXCHANGE_RATES SET CURRENCIES='%s', RATES=%f" % (currency, rates.get(currency) * 1000);

            #   SQL문 실행
            curs.execute(sql)

        #   커밋
        conn.commit()

    finally:
        #   Connection 닫기
        conn.close()


#   크롤링 함수 실행 코드
if __name__ == "__main__":
    #   어트랙션 링크 크롤링
    crawling_exchange_rates()