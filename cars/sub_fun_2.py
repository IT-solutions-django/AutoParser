from datetime import datetime
from currencies.models import Currency
from commission.models import Commission

import logging

logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат сообщений
)


def get_currency():
    currency = {}

    currency['JPY'] = float(Currency.get_jpy().exchange_rate_batareyka)
    currency['CNY'] = float(Currency.get_cny().exchange_rate_batareyka)
    currency['USD'] = float(Currency.get_usd().exchange_rate_batareyka)
    currency['EUR'] = float(Currency.get_eur().exchange_rate_batareyka)
    currency['KRW'] = float(Currency.get_krw().exchange_rate_batareyka)

    return currency


def get_commission(table: str):
    commission = Commission.objects.get(table=table)

    delivery = commission.delivery
    our_commision = commission.commission
    broker = commission.commission_broker

    if commission.japan_sanction_percent:
        commision_sanctions = commission.japan_sanction_percent
        delivery_sanctions = commission.japan_sanction_delivery
        insurance = commission.japan_insurance
    else:
        commision_sanctions = 0
        delivery_sanctions = 0
        insurance = 0

    return delivery, our_commision, broker, commision_sanctions, delivery_sanctions, insurance


def calc_price(price: int, year: int, volume: int, table: str, engine_type: str = None):
    try:
        currency = get_currency()
        delivery, our_commision, broker, commision_sanctions, delivery_sanctions, insurance = get_commission(table)

        price = int(price)
        volume = int(volume)
        year = int(year)
        commision_sanctions_ = 0
        insurance_rus = 0
        yts = 0

        # Перевод цены в рубли
        if table == 'main' or table == 'stats':
            one_rub = currency["JPY"]

            # Санционные авто
            if (volume > 1800 or engine_type == 3 or engine_type == 2):
                if ('%' in commision_sanctions):
                    commision_sanctions = int(commision_sanctions.replace('%', ''))
                    commision_sanctions_ = price * commision_sanctions / 100
                else:
                    commision_sanctions_ = price + int(commision_sanctions)
                price_rus = round((price + commision_sanctions_) * one_rub)
                delivery = delivery_sanctions


            else:
                price_rus = round(price * one_rub)
                insurance_rus = round(insurance * one_rub)

        elif table == "china":
            one_rub = currency["CNY"]

        elif table == 'korea':
            one_rub = currency['KRW']

        price_rus = round(price * one_rub)

        tof = get_tof(price_rus)

        age = datetime.now().year - year
        if age < 3:
            # if volume >= 3500:
            #     yts = 2285200
            # elif (volume >= 3000) and (volume <= 3499):
            #     yts = 1794600
            # else:
            #     yts = 3400

            evroprice = price_rus / currency["EUR"]
            if engine_type == 2:
                duty = evroprice * 0.15
            elif evroprice <= 8500:
                duty = evroprice * 0.54
                if duty / volume < 2.5:
                    duty = volume * 2.5
            elif (evroprice > 8500) and (evroprice <= 16700):
                duty = evroprice * 0.48
                if duty / volume < 3.5:
                    duty = volume * 3.5
            elif (evroprice > 16700) and (evroprice <= 42300):
                duty = evroprice * 0.48
                if duty / volume < 5.5:
                    duty = volume * 5.5
            elif (evroprice > 42300) and (evroprice <= 84500):
                duty = evroprice * 0.48
                if duty / volume < 7.5:
                    duty = volume * 7.5
            elif (evroprice > 84500) and (evroprice <= 169000):
                duty = evroprice * 0.48
                if duty / volume < 15:
                    duty = volume * 15
            else:
                duty = evroprice * 0.48
                if duty / volume < 20:
                    duty = volume * 20

        elif (age >= 3) and (age <= 5):
            # if volume >= 3500:
            #     yts = 3004000
            # elif (volume >= 3000) and (volume <= 3499):
            #     yts = 2747200
            # else:
            #     yts = 5200

            evroprice = price_rus / currency["EUR"]
            if engine_type == 2:
                duty = evroprice * 0.15
            elif volume <= 1000:
                duty = volume * 1.5
            elif (volume >= 1001) and (volume <= 1500):
                duty = volume * 1.7
            elif (volume >= 1501) and (volume <= 1800):
                duty = volume * 2.5
            elif (volume >= 1801) and (volume <= 2300):
                duty = volume * 2.7
            elif (volume >= 2301) and (volume <= 3000):
                duty = volume * 3
            else:
                duty = volume * 3.6
        elif age > 5:
            # if volume >= 3500:
            #     yts = 3004000
            # elif (volume >= 3000) and (volume <= 3499):
            #     yts = 2747200
            # else:
            #     yts = 5200

            evroprice = price_rus / currency["EUR"]
            if engine_type == 2:
                duty = evroprice * 0.15
            elif volume <= 1000:
                duty = volume * 3
            elif (volume >= 1001) and (volume <= 1500):
                duty = volume * 3.2
            elif (volume >= 1501) and (volume <= 1800):
                duty = volume * 3.5
            elif (volume >= 1801) and (volume <= 2300):
                duty = volume * 4.8
            elif (volume >= 2301) and (volume <= 3000):
                duty = volume * 5
            else:
                duty = volume * 5.7

        if engine_type == 2:
            toll = price_rus * 0.15
        else:
            toll = duty * currency["EUR"]

        if age <= 3:
            if engine_type == 2:
                yts = 20000 * 0.17
            elif volume <= 1000:
                yts = 20000 * 0.17
            elif (volume >= 1001) and (volume <= 2000):
                yts = 20000 * 0.17
            elif (volume >= 2001) and (volume <= 3000):
                yts = 20000 * 0.17
            elif (volume >= 3001) and (volume <= 3500):
                yts = 20000 * 107.67
            else:
                yts = 20000 * 137.11
        else:
            if engine_type == 2:
                yts = 20000 * 0.26
            elif volume <= 1000:
                yts = 20000 * 0.26
            elif (volume >= 1001) and (volume <= 2000):
                yts = 20000 * 0.26
            elif (volume >= 2001) and (volume <= 3000):
                yts = 20000 * 0.26
            elif (volume >= 3001) and (volume <= 3500):
                yts = 20000 * 165.84
            else:
                yts = 20000 * 180.24

        res_rus = toll + (delivery * one_rub) + our_commision + broker + insurance_rus + tof + yts

        result = {
            'total': round((res_rus + price_rus) / 1000) * 1000,
            'toll': toll,
            'yts': yts,
            'tof': tof,
            'car_price_rus': price_rus,
            'insurance': insurance,
            'insurance_rus': insurance_rus,
            'delivery': delivery,
            'delivery_rus': delivery * one_rub,
            'commision_sanctions_rus': commision_sanctions_,
            'commision_sanctions_rus': commision_sanctions_ * one_rub,
            'our_commision': our_commision,
            'broker': broker,
            'currency': currency
        }

        return result
    except Exception as e:
        print(e)


def get_tof(price_rus: int):
    if price_rus < 200000:
        return 1067
    elif (price_rus < 450000) and (price_rus >= 200000):
        return 2134
    elif (price_rus < 1200000) and (price_rus >= 450000):
        return 4269
    elif (price_rus < 2700000) and (price_rus >= 1200000):
        return 11746
    elif (price_rus < 4200000) and (price_rus >= 2700000):
        return 16524
    elif (price_rus < 5500000) and (price_rus >= 4200000):
        return 21344
    elif (price_rus < 7000000) and (price_rus >= 5500000):
        return 27540
    else:
        return 30000


def get_akz(power: int, volume: int):
    power = int(power)
    volume = int(volume)
    if power <= 90:
        return 0
    elif (power >= 90.01) and (power <= 150):
        return power * 61
    elif (power >= 150.01) and (power <= 200):
        return power * 583
    elif (power >= 200.01) and (power <= 300):
        return power * 955
    elif (power >= 300.01) and (power <= 400):
        return power * 1685
    elif (power >= 400.01) and (power <= 500):
        return power * 1685
    else:
        return power * 1740


def calc_price_calculator(price: int, year: int, volume: int, table: str, engine_type: int):
    try:
        currency = get_currency()

        delivery, our_commision, broker, commision_sanctions, delivery_sanctions, insurance = get_commission(table)

        price = float(price)
        volume = int(volume)
        year = int(year)
        commision_sanctions_ = 0
        insurance_rus = 0

        # Перевод цены в рубли
        if table == 'stats':
            one_rub = currency["JPY"]
            # Санционные авто
            if (volume > 1800 or engine_type == 3 or engine_type == 2):
                commision_sanctions_ = price * commision_sanctions / 100
                price_rus = round((price + commision_sanctions_) * one_rub)
                delivery = delivery_sanctions
            else:
                price_rus = round(price * one_rub)
                insurance_rus = round(insurance * one_rub)

        elif table == "china":
            one_rub = currency["CNY"]
            price_rus = round(price * one_rub)

        elif table == 'korea':
            one_rub = currency['KRW']
            price_rus = round(price * one_rub)

        tof = get_tof(price_rus)
        evroprice = price_rus / currency["EUR"]
        age = datetime.now().year - year

        if age <= 3:
            if volume <= 1000:
                yts = 20000 * 9.01
            elif (volume >= 1001) and (volume <= 2000):
                yts = 20000 * 33.37
            elif (volume >= 2001) and (volume <= 3000):
                yts = 20000 * 93.77
            elif (volume >= 3001) and (volume <= 3500):
                yts = 20000 * 107.67
            else:
                yts = 20000 * 137.11
        else:
            if volume <= 1000:
                yts = 20000 * 23
            elif (volume >= 1001) and (volume <= 2000):
                yts = 20000 * 58.7
            elif (volume >= 2001) and (volume <= 3000):
                yts = 20000 * 141.97
            elif (volume >= 3001) and (volume <= 3500):
                yts = 20000 * 165.84
            else:
                yts = 20000 * 180.24

        if engine_type == 0:
            if age <= 3:
                if (volume <= 2800):
                    duty = (price_rus * 0.15) / currency["EUR"]

                else:
                    duty = (price_rus * 0.125) / currency["EUR"]

            elif (age > 3) and (age <= 7):
                if volume <= 1000:
                    duty = evroprice * 0.2
                    if duty / volume < 0.36:
                        duty = volume * 0.36
                elif (volume >= 1001) and (volume <= 1500):
                    duty = evroprice * 0.2
                    if duty / volume < 0.4:
                        duty = volume * 0.4
                elif (volume >= 1501) and (volume <= 1800):
                    duty = evroprice * 0.2
                    if duty / volume < 0.36:
                        duty = volume * 0.36
                elif (volume >= 1801) and (volume <= 3000):
                    duty = evroprice * 0.2
                    if duty / volume < 0.44:
                        duty = volume * 0.44
                else:
                    duty = evroprice * 0.2
                    if duty / volume < 0.8:
                        duty = volume * 0.8
            else:
                if volume <= 1000:
                    duty = volume * 1.4
                elif (volume >= 1001) and (volume <= 1500):
                    duty = volume * 1.5
                elif (volume >= 1501) and (volume <= 1800):
                    duty = volume * 1.6
                elif (volume >= 1801) and (volume <= 3000):
                    duty = volume * 2.2
                else:
                    duty = volume * 3.2
        elif engine_type == 1:
            if age <= 3:
                evroprice = price_rus / currency["EUR"]
                duty = evroprice * 0.15
                yts = 20000 * 33.37
            elif (age > 3) and (age <= 7):
                if volume <= 1500:
                    duty = evroprice * 0.2
                    if duty / volume < 0.32:
                        duty = volume * 0.32
                elif (volume >= 1501) and (volume <= 2500):
                    duty = evroprice * 0.2
                    if duty / volume < 0.4:
                        duty = volume * 0.4
                else:
                    duty = evroprice * 0.2
                    if duty / volume < 0.8:
                        duty = volume * 0.8
            else:
                if volume <= 1500:
                    duty = evroprice * 1.5
                elif (volume >= 1501) and (volume <= 2500):
                    duty = evroprice * 2.2
                else:
                    duty = evroprice * 3.2
        elif engine_type == 2:
            if age <= 3:
                evroprice = price_rus / currency["EUR"]
                duty = evroprice * 0.15
                yts = 20000 * 33.37

            else:
                evroprice = price_rus / currency["EUR"]
                duty = evroprice * 0.15
                yts = 20000 * 58.7

        toll = duty * currency["EUR"]

        res_rus = toll + (delivery * one_rub) + our_commision + broker + insurance_rus + tof

        result = {
            'total': round((res_rus + price_rus) / 1000) * 1000,
            'toll': toll,
            'yts': yts,
            'tof': tof,
            'car_price_rus': price_rus,
            'insurance': insurance,
            'insurance_rus': insurance_rus,
            'delivery': delivery,
            'delivery_rus': delivery * one_rub,
            'commision_sanctions_rus': commision_sanctions_,
            'commision_sanctions_rus': commision_sanctions_ * one_rub,
            'currency': currency
        }

        return result
    except Exception as e:
        print(e)