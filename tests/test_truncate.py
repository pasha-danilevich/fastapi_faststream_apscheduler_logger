from typing import Any

from faker import Faker
import random








class Some:
    def __init__(self):
        self.a = 10
        self.b = 20

def fun(a_: Any, b: Any = 12) -> Any:
    return ''

a = list(range(100))
a2 = list(range(20, 50))
a3 = list(range(20))
a4 = list(range(13))
c = {x for x in range(100)}
c2 = {x for x in range(10)}
d = {k: v for k, v in zip(a2, a3)}
e = Some()
f = fun
s = """select count(*)
from evnps
where 1 = 1
  and evn_disdt is not null
  and {condition};



select evnps.evn_id                                      as evn_id,
       evnps.person_id                                   as person_id,
       evnps.lpu_id,
       evnps.diag_id,

       lut.lpuunittype_name                              as lpuunittype_name,            --"Тип стационара",
       lsp.lpusectionprofile_name                        as lpusectionprofile_name,-- "Профиль отделения",
       lsbp.lpusectionbedprofile_name                    as lpusectionbedprofile_name,   --"Профиль койки",
       evnps.evn_setdt                                   as evnps_setdt,                 --"Дата госпитализации",
       evnps.evn_disdt                                   as evnps_disdt,                 --"Дата выписки",
       evnps.evn_upddt                                   as evn_upddt,                   --"Дата обновления записи",
       pht.prehosptype_name                              as prehosptype_name,            --"Форма",
       pha.prehosparrive_name                            as prehosparrive_name,          --"Доставлен",
       phs.prehospstatus_name                            as prehospstatus_name,          --"Статус",
       pwf.prehospwaifrefusecause_name                   as prehospwaifrefusecause_name, --"Причина отказа в госпитализации",
       rcl.resultclass_name                              as resultclass_name,            --"Результат при отказе",
       evnps.evnps_isfinish                              as evnps_isfinish,              --"Случай закончен",
       mf.medicalcareformtype_name                       as medicalcareformtype_name,    --"Форма оказания МП",

       evnps.evnps_timedesease                           as evnps_timedesease,           --"Время от начала заболевания",
       case
           when evnps.evnps_timedesease isnull then null
           when evnps.okei_id = 100 then 'час'
           when evnps.okei_id = 101 then 'день'
           when evnps.okei_id = 102 then 'неделя'
           when evnps.okei_id = 104 then 'месяц'
           when evnps.okei_id = 107 then 'год'
           end                                           as interval_type,--"Промежуток времени",

       lt.leavetype_name                                 as leavetype_name,              --"Результат",
       pt.paytype_name                                   as paytype_name,                --"Тип оплаты",
       reg.registrydata_itogsum                          as registrydata_itogsum,        --"Сумма оплаты",
       jsonb_object_field_text(reg.region_data, 'n_ksg') as ksg,                         --"КСГ"
       evnps.evn_deleted,
       evnps.evn_deldt,
       n.timesymptomonmk_name


from evnps
         join v_personstate using (person_id)

         left join leavetype lt using (leavetype_id) --результат госпитализации
         left join prehosptype pht using (prehosptype_id)
         left join prehosparrive pha using (prehosparrive_id)
         left join paytype pt using (paytype_id)
         left join prehospwaifrefusecause pwf using (prehospwaifrefusecause_id)
         left join prehospstatus phs using (prehospstatus_id)
         left join lpusection ls on evnps.lpusection_id = ls.lpusection_id
         join lpuunit lu using (lpuunit_id)
         join lpuunittype lut using (lpuunittype_id)
         left join lpusectionprofile lsp on ls.lpusectionprofile_id = lsp.lpusectionprofile_id
         left join lpusectionbedprofile lsbp on ls.lpusectionbedprofile_id = lsbp.lpusectionbedprofile_id
         left join resultclass rcl using (resultclass_id)
         left join fed.medicalcareformtype mf on mf.medicalcareformtype_id = evnps.medicalcareformtype_id
    --left join r91.registrydata reg on reg.evn_rid = evnps.evnps_id and registrydata_ispaid = 2 and reg.leavetype_id = evnps.leavetype_id

         left join LATERAL (select *
                            from r91.registrydata reg
                            where reg.evn_rid = evnps.evn_id
                              and registrydata_ispaid = 2
                              and reg.leavetype_id = evnps.leavetype_id
                            limit 1) as reg on true

         left join lateral (
    select n.timesymptomonmk_name

    from v_evnsection es
             join v_dataevndop dop on es.evnsection_id = dop.evn_id --and dop.dataevndopelement_id=5
             join nsi.TimeSymptomONMK n
                  on n.timesymptomonmk_code = dop.dataevndop_valueint and n.timesymptomonmk_name is not null
    where es.evnsection_rid = evnps.evn_id
    limit 1) n on true
where 1=1 and {condition}
and evn_disdt is not null
limit {limit} offset {offset}"""

items = [a, a2, a3, a4, c, c2, d, e, s, f]



fake = Faker()

# Генерация случайных данных
name = fake.name()          # Случайное имя
address = fake.address()    # Случайный адрес
email = fake.email()        # Случайный email
date_of_birth = fake.date_of_birth() # Случайная дата рождения
text_ = fake.text()          # Случайный текст
integer = random.randint(0, 100)  # Случайное целое число
float_number = random.random() * 100  # Случайное дробное число
boolean_value = random.choice([True, False])  # Случайное булевое значение
date = fake.date()         # Случайная дата
time = fake.time()         # Случайное время
date_time = fake.date_time()  # Случайная дата и время
url = fake.url()           # Случайный URL
ip_address = fake.ipv4()   # Случайный IP-адрес
phone_number = fake.phone_number()  # Случайный телефонный номер

# Создание списка с результатами
random_data = [
    {"type": "Имя", "value": name},
    {"type": "Адрес", "value": address},
    {"type": "Email", "value": email},
    {"type": "Дата рождения", "value": date_of_birth},
    {"type": "Текст", "value": text_},
    {"type": "Целое число", "value": integer},
    {"type": "Дробное число", "value": float_number},
    {"type": "Булевое значение", "value": boolean_value},
    {"type": "Дата", "value": date},
    {"type": "Время", "value": time},
    {"type": "Дата и время", "value": date_time},
    {"type": "URL", "value": url},
    {"type": "IP-адрес", "value": ip_address},
    {"type": "Телефонный номер", "value": phone_number},
]




def truncate(obj: Any) -> str:
    """Принимает результат метода repr"""
    text_repr = repr(obj)
    if len(text_repr) < 70:
        return f"{text_repr}"
    return f"{text_repr[:10].strip()} ... {text_repr[-10:]}"


for item in random_data:
    print(truncate(item['value']))
for i in items:
    print(truncate(i))