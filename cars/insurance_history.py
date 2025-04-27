import requests
import json
from .settings_insurance import CREDENTIALS, URLs, TRANSLATE
import re
from time import sleep


def extract_lots_from_api(offset):
    """Забираем по внешнему API список лотов"""

    response = requests.get(
        url=URLs.lots.format(offset=offset)
    )

    return re.findall(r'<LOT>(\d+)</LOT>', response.text)


def get_vehicle_info(lot):
    """Собираем некоторую полезную информацию об авто, включая vehicleNo. Необходимо для обращения к другому ЕП"""

    response = requests.get(
        url=URLs.vehicle_info.format(lot=lot),
        headers=CREDENTIALS.headers.value
    )

    car_json = json.loads(response.text)
    return {
        'year_month': car_json['category']['yearMonth'],  # Год/месяц выпуска авто
        'seat_count': car_json['spec']['seatCount'],  # Колиество посадочных мест авто
        'vehicle_no': car_json['vehicleNo'],  # Государственный номер (может содержать Unicode)
    }


def get_vehicle_record(lot, vehicle_no):
    """
    Собираем страхову историю авто

    accidents - список словарей, где:
    type: 1 - вина владельца, 2 - вина третьих лиц, 3 - обоюдная
    date: Дата аварии
    insuranceBenefit: Выплата по страховкеpart
    Cost: Стоимость запчастей
    laborCost: Стоимость работ
    paintingCost: Стоимость покраски
    """

    response = requests.get(
        url=URLs.vehicle_record.format(lot=lot, vehicle_no=vehicle_no),
        headers=CREDENTIALS.headers.value
    )

    if response.status_code == 200:
        car_json = json.loads(response.text)
        return {
            'owner_change_cnt': car_json['ownerChangeCnt'],  # Количество смен владельцев
            'not_join_date1': car_json['notJoinDate1'],  # Период без страховки
            'not_join_date2': car_json['notJoinDate2'],  # Период без страховки
            'not_join_date3': car_json['notJoinDate3'],  # Период без страховки
            'not_join_date4': car_json['notJoinDate4'],  # Период без страховки
            'not_join_date5': car_json['notJoinDate5'],  # Период без страховки
            'robber_cnt': car_json['robberCnt'],  # Количество угоноа
            'flood_total_loss_cnt': car_json['floodTotalLossCnt'],  # Количество затоплений
            'government': car_json['government'],  # Использование госорганами: 0 - не использовался; government > 0 - использовался
            'business': car_json['business'], # Использование для бизнеса: 0 - не использовался; business > 0 - использовался
            'loan': car_json['loan'],  # Залог: 0 - нет; loan > 0 - был задлог
            'my_accident_cnt': car_json['myAccidentCnt'],  # Количество по вине владельца
            'other_accident_cnt': car_json['otherAccidentCnt'],  # Количество по вине других
            'total_loss_cnt': car_json['totalLossCnt'],  # Количество тотальных потерь
            'accident_cnt': car_json['accidentCnt'],  # Количество всего зарегистрированных аварий
            'my_accident_cost': car_json['myAccidentCost'],  # Общий ущерб от аварий владельца (KRW)
            'other_accident_cost': car_json['otherAccidentCost'],  # Ущерб от аварий других (KRW)
            'accidents': car_json['accidents'],  # Подробная история аварий
        }
    else:
        return None


def save_to_json(data, filename):
    """Сохраняет данные в JSON-файл."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main(count):
    for i in range(count):
        for lot in extract_lots_from_api(offset=i):
            car_info = get_vehicle_info(lot)

            car_record = get_vehicle_record(lot, car_info["vehicle_no"])

            if car_record is not None:
                save_to_json({**car_info, **car_record}, f'car_info_{lot}.json')
                print(f"Данные сохранены в файлы: record_{lot}.json")
            else:
                print(f"Страховой истории не обнаружено: {lot}")


if __name__ == '__main__':
    main(count=4)
