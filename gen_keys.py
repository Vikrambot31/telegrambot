# gen_keys.py

def get_gate_description(gate_numbers):
    gate_data = {
        1: {"Дар": "Уникальность. Самовыражение.", "Тень": "Самоотвержение. Интропия.", "Описание": "Эти ворота могут блокировать проявление истинного «я» через навязчивое желание быть признанным. Человек начинает ориентироваться на вкусы и ожидания других, подавляя свои уникальные импульсы. Это приводит к внутреннему разочарованию, ощущению пустоты и кризису идентичности. Подлинное творчество умирает под гнётом самокритики и зависимости от чужого мнения."},
        2: {"Дар": "Внутреннее руководство", "Тень": "Дезориентация", "Описание": "Человек теряет связь с собственным путём, когда подменяет внутреннее руководство внешними ориентирами. Появляется тревожность, хаотичность, ощущение «я не знаю, куда иду»."},
        3: {"Дар": "Адаптация. Порядок.", "Тень": "Сопротивление переменам. Хаос.", "Описание": "Когда человек цепляется за стабильность и контроль, он подавляет естественный процесс обновления. Проявляется страх хаоса, прокрастинация, внутреннее напряжение от конфликта между страхом и необходимостью двигаться вперёд."},
        4: {"Дар": "Ментальная ясность. Формулизация.", "Тень": "Ментальный ригоризм. Поиск ответа.", "Описание": "Ум превращается в диктатора, стремящегося всё объяснить и разложить. Навязчивый анализ, поиск логики, ментальное выгорание и зацикленность — всё это мешает ясности мышления."},
        5: {"Дар": "Естественный поток. Ритм.", "Тень": "Страх неуспеть.", "Описание": "Жесткая рутина, страх сбиться с графика, тревожность от отклонений от плана. Настоящий поток заменяется на насилие над собой во имя режима."},
        6: {"Дар": "Миротворчество", "Тень": "Эмоциональное избегание", "Описание": "Боязнь конфликта приводит к тому, что человек замораживает эмоции, уходит от искренности. Это разрушает отношения и создаёт внутреннюю фрустрацию."},
        7: {"Дар": "Видение пути. Лидерство.", "Тень": "Иллюзорная власть", "Описание": "Вместо подлинного лидерства человек пытается управлять другими, чтобы чувствовать значимость. Возникает отчуждение и сопротивление со стороны окружения."},
        8: {"Дар": "Влияние. Вклад.", "Тень": "Демонстративность. Серость.", "Описание": "Желание быть признанным переходит в навязчивую демонстрацию. Человек теряет связь с собой, становится зависимым от одобрения."},
        9: {"Дар": "Концентрация. Фокус.", "Тень": "Обсессия. Расфокусировка.", "Описание": "Мозг застревает на деталях, создаётся иллюзия продуктивности. Реально — выгорание, тревожность и отсутствие движения."},
        10: {"Дар": "Аутентичность. Любовь к себе.", "Тень": "Зацикленность на себе", "Описание": "Личность подменяется социальными масками. Человек боится быть собой, боится быть отвергнутым и теряет подлинность."},
        11: {"Дар": "Вдохновение. Идейность.", "Тень": "Ментальная дезориентация. Страхи Ума", "Описание": "Идеи хаотичны, человек теряется в мыслях. Это мешает воплощению, создаёт внутренний шум и усталость от ума."},
        12: {"Дар": "Элегантность выражения", "Тень": "Эмоциональное подавление", "Описание": "Чувства сдерживаются, слова не находят выхода. Появляется отчуждение, одиночество, страх открыться."},
        13: {"Дар": "Сострадание. Слушанье.", "Тень": "Перегрузка чужими историями", "Описание": "Открытость к другим превращается в уязвимость. Человек впитывает чужую боль, теряет границы и чувствует эмоциональное истощение."},
        14: {"Дар": "Сила компетентности.", "Тень": "Энергетическая зависимость. Компромисс.", "Описание": "Потребность в поддержке превращается в зависимость. Человек боится потерять источник ресурса и идёт на компромиссы с собой."},
        15: {"Дар": "Уверенность", "Тень": "Мнительность. Крайности.", "Описание": "Человек сомневается в себе, боится быть осуждённым. Это вызывает тревожность, отказ от инициативы и жажду подтверждений извне."},
        16: {"Дар": "Принятие. Навыки. Талант.", "Тень": "Непринятие себя. Безразличие.", "Описание": "Внутренний критик разрушает самооценку. Человек чувствует, что его не принимают, и он сам себя отвергает."},
        17: {"Дар": "Проницательность. Объективность.", "Тень": "Мнение. Осуждение.", "Описание": "Одержимость быть правым. Мышление становится инструментом разделения, а не понимания."},
        18: {"Дар": "Целостность. Совершенствование.", "Тень": "Критика. Недовольство.", "Описание": "Навязчивая критика других и себя. Стремление к идеалу отравляет момент и мешает принятию."},
        19: {"Дар": "Чуткость. Сопереживание.", "Тень": "Зависимость. Нужда.", "Описание": "Желание быть нужным становится способом контроля. Страх быть покинутым приводит к манипуляциям."},
        20: {"Дар": "Осознанность в настоящем.", "Тень": "Поверхностность. Отсутствие связи.", "Описание": "Говорить, не чувствуя. Делать, не присутствуя. Энергия уходит в пустоту."},
        21: {"Дар": "Сила управления.", "Тень": "Контроль. Жесткость.", "Описание": "Навязчивая потребность всё держать в руках приводит к конфликтам и выгоранию."},
        22: {"Дар": "Грация. Слушание сердца.", "Тень": "Ожесточение. Неприятие чувств.", "Описание": "Закрытость к эмоциям других превращает человека в «ледяную королеву»."},
        23: {"Дар": "Ясность. Простота самовыражения.", "Тень": "Запутанность. Замыкание.", "Описание": "Человек не может выразить свои идеи и уходит в молчание или непонятость."},
        24: {"Дар": "Внутреннее знание. Интеграция.", "Тень": "Одержимость размышлениями.", "Описание": "Бесконечное «пережёвывание» мыслей мешает интуиции проявиться спонтанно."},
        25: {"Дар": "Безусловная любовь. Невинность.", "Тень": "Холодность. Отрешённость.", "Описание": "Закрытие сердца как защита от боли. Потеря связи с собой и другими."},
        26: {"Дар": "Харизма. Влияние.", "Тень": "Манипуляция. Преувеличение.", "Описание": "Использование слов и обаяния ради выгоды. Потеря доверия и подлинности."},
        27: {"Дар": "Забота. Щедрость.", "Тень": "Самоотречение. Пренебрежение собой.", "Описание": "Жертва ради других превращается в хроническое истощение и обиду."},
        28: {"Дар": "Храбрость. Смелость жить.", "Тень": "Бессмысленность. Отчаяние.", "Описание": "Жизнь кажется пустой и тяжёлой. Человек теряет цель и надежду."},
        29: {"Дар": "Принятие. Посвящение.", "Тень": "Переутомление. Слепая преданность.", "Описание": "Согласие на всё без внутреннего отклика приводит к потере энергии и выгоранию."},
        30: {"Дар": "Страсть. Эмоциональная зрелость.", "Тень": "Жажда опыта. Страдание.", "Описание": "Ожидание сильных эмоций приводит к разочарованиям и зависимостям."},
        31: {"Дар": "Вдохновляющее лидерство.", "Тень": "Популизм. Желание власти.", "Описание": "Потребность в признании управляет выбором, а не истина."},
        32: {"Дар": "Доверие к трансформации.", "Тень": "Страх провала. Сомнение.", "Описание": "Постоянное ожидание краха не даёт двигаться вперёд и рисковать."},
        33: {"Дар": "Ретроспекция. Память души.", "Тень": "Застревание в прошлом. Стыд.", "Описание": "Человек не может отпустить старые истории, переживания и идентичности."},
        34: {"Дар": "Сила в настоящем. Спонтанность.", "Тень": "Импульсивность. Резкость.", "Описание": "Энергия уходит на бессознательные действия и конфликты."},
        35: {"Дар": "Мудрость через опыт.", "Тень": "Насыщение. Беспокойство.", "Описание": "Погоня за новыми впечатлениями приводит к внутренней пустоте."},
        36: {"Дар": "Сострадание к эмоциям.", "Тень": "Тревога. Драматизация.", "Описание": "Эмоции становятся хаотичными, создавая мыльные оперы и страдания."},
        37: {"Дар": "Дружелюбие. Сотрудничество.", "Тень": "Жертва. Обязанность.", "Описание": "Человек служит из долга, а не из сердца. Возникает обида и отчуждение."},
        38: {"Дар": "Борец за ценности.", "Тень": "Конфликт. Упрямство.", "Описание": "Борьба ради борьбы. Неосознанное сопротивление миру и людям."},
        39: {"Дар": "Провокация к пробуждению.", "Тень": "Раздражение. Блокировка чувств.", "Описание": "Человек не осознаёт, что его действия вызывают сопротивление и отторжение."},
        40: {"Дар": "Сила отдачи. Надёжность.", "Тень": "Закрытие. Изоляция.", "Описание": "После перегрузки человек уходит в одиночество и теряет связь с другими."},
        41: {"Дар": "Воображение. Эмоциональное видение.", "Тень": "Фантазия. Иллюзия.", "Описание": "Желание новых чувств толкает на поиск драм и зависимости от внешних стимулов."},
        42: {"Дар": "Завершение. Синтез опыта.", "Тень": "Незавершённость. Ожидание конца.", "Описание": "Человек боится, что упустит что-то важное, и не проживает настоящее до конца."},
        43: {"Дар": "Озарение. Ментальная инновация.", "Тень": "Упрямство. Непонимание.", "Описание": "Гениальные идеи не могут быть донесены до других, вызывая изоляцию и страх быть странным."},
        44: {"Дар": "Прозорливость. Узнавание.", "Тень": "Подозрение. Прошлое управляет настоящим.", "Описание": "Старые шаблоны мешают видеть людей такими, какие они есть."},
        45: {"Дар": "Распределение. Единство.", "Тень": "Присвоение. Король без короны.", "Описание": "Контроль над ресурсами становится способом самоутверждения и доминирования."},
        46: {"Дар": "Любовь к телу. Принятие воплощения.", "Тень": "Серьёзность. Тревога о пути.", "Описание": "Жизнь ощущается как тяжесть, а тело — как препятствие, а не подарок."},
        47: {"Дар": "Трансформация. Интерпретация опыта.", "Тень": "Подавленность. Умственная перегрузка.", "Описание": "Человек не может найти смысл в событиях, застревает в прошлом."},
        48: {"Дар": "Глубина. Решение проблем.", "Тень": "Недостаточность. Сомнение.", "Описание": "Ощущение, что знаний никогда не хватит, блокирует проявление экспертности."},
        49: {"Дар": "Принципы. Чувствительность к справедливости.", "Тень": "Революция. Нетерпимость.", "Описание": "Эмоциональные реакции заменяют ясное восприятие, создавая разрыв в отношениях."},
        50: {"Дар": "Ответственность. Границы.", "Тень": "Коррупция. Игнорирование обязанностей.", "Описание": "Отказ заботиться о себе и других ведёт к разрушению стабильности."},
        51: {"Дар": "Пробуждение. Шок, ведущий к жизни.", "Тень": "Агрессия. Эгоизм.", "Описание": "Импульсивность и стремление быть первым создают конфликты и отторжение."},
        52: {"Дар": "Спокойствие. Концентрация.", "Тень": "Неподвижность. Застой.", "Описание": "Энергия не находит выхода, человек уходит в апатию или тревожное напряжение."},
        53: {"Дар": "Начало. Энтузиазм.", "Тень": "Нетерпение. Беспорядочность.", "Описание": "Постоянное стремление к новому мешает завершению и устойчивости."},
        54: {"Дар": "Амбиции. Восхождение.", "Тень": "Стремление к признанию. Зависимость от успеха.", "Описание": "Внутреннее ощущение неполноценности толкает на карьерную гонку без удовлетворения."},
        55: {"Дар": "Свобода. Эмоциональное изобилие.", "Тень": "Жертва эмоций. Настроенчивая жизнь.", "Описание": "Настроение диктует восприятие реальности. Человек теряет чувство устойчивости."},
        56: {"Дар": "Экспрессия. Истории как трансформация.", "Тень": "Отвлечение. Пустословие.", "Описание": "Желание впечатлить заменяет истинную передачу смысла."},
        57: {"Дар": "Интуиция. Восприятие в моменте.", "Тень": "Страх. Паника.", "Описание": "Подсознательный страх искажается как истина и мешает доверию к себе."},
        58: {"Дар": "Жизнелюбие. Радость улучшения.", "Тень": "Недовольство. Претензии.", "Описание": "Ориентированность на несовершенство подавляет спонтанную радость."},
        59: {"Дар": "Близость. Прозрачность.", "Тень": "Недоверие. Разделение.", "Описание": "Страх открыться делает невозможным истинную связь."},
        60: {"Дар": "Реализм. Принятие ограничений.", "Тень": "Ограниченность. Сопротивление.", "Описание": "Проблема воспринимается как конец, а не как портал к преобразованию."},
        61: {"Дар": "Священное знание. Вдохновение.", "Тень": "Одержимость тайной. Давление ума.", "Описание": "Поиск ответов отвлекает от жизни. Тайна заменяет реальность."},
        62: {"Дар": "Ясность. Вербализация.", "Тень": "Педантичность. Словесная броня.", "Описание": "Желание всё разложить по полочкам закрывает гибкость и интуицию."},
        63: {"Дар": "Доверие. Логическая проверка.", "Тень": "Подозрение. Сомнение во всём.", "Описание": "Ментальный контроль разрушает доверие к жизни и другим."},
        64: {"Дар": "Образность. Символическое мышление.", "Тень": "Замешательство. Разбросанность.", "Описание": "Человек захлёбывается образами и не может найти суть."},

    }

    descriptions = []
    for num in gate_numbers:
        gate = gate_data.get(num)
        if gate:
            desc = (
    f"- Дар: {gate['Дар']}\n"
    f"- Тень: {gate['Тень']}\n"
    f"- Описание тени: {gate['Описание']}"
)

            descriptions.append(desc)
        else:
            descriptions.append(f"\n⚠️ Ворота {num} не найдены в базе.")

    return "\n".join(descriptions)

# Пример вызова (для теста)
if __name__ == "__main__":
    gates = [1, 10, 15, 17, 34]
    print(get_gate_description(gates))
