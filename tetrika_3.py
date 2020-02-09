# Шаблон для БД
pattern_json_bd = {
        'lessons_1': {
            'id': {
                'id': '',
                'quality': []
            },
            'event_id': {
                    'event_id': '',
                    'users': [],
            },
            'subject': '',
            'scheduled_time': ''
        },
    }

def file_read(path):
    """
    Чтение файла.
    :param path: Путь и название
    :return: Текст
    """
    with open(path, 'r') as f:
        file = f.read()
    return file

def data_collection(lessons_split=None, quality_split=None, participants_split=None, users_split=None):
    """
    Заполннеие шаблона БД.
    :param lessons_split: Список (list)
    :param quality_split: Список (list)
    :param participants_split: Список (list)
    :param users_split: Список (list)
    :return: Заполненный словарь (dict) pattern_json_bd
    """
    # Создаем и заполняем уроки
    if lessons_split is not None:
        i = 1
        for split in lessons_split:
            pattern_json_bd.update({
                'lessons_' + str(i): {
                    'id': {
                        'id': split[0],
                        'quality': []
                    },
                    'event_id': {
                        'event_id': split[1],
                        'users': [],
                    },
                    'subject': split[2],
                    'scheduled_time': split[3],
                },
            })
            i += 1
    # Заполняем оценки
    if quality_split is not None:
        for split in quality_split:
            for lesson in pattern_json_bd:
                if pattern_json_bd[lesson]['id']['id'] == split[0]:
                    pattern_json_bd[lesson]['id']['quality'].append(split[1])
    # Заполняем id пользователей и
    # event_id (связь между уроками и пользователями)
    if participants_split is not None:
        for lesson in pattern_json_bd:
            lesson_evant_id = pattern_json_bd[lesson]['event_id']['event_id']
            for split in participants_split:
                participants_event_id = split[0]
                if lesson_evant_id == participants_event_id:
                    participants_user_id = split[1]
                    user_id = [{'user_id': participants_user_id, 'role': '', },]
                    users = pattern_json_bd[lesson]['event_id']['users']
                    try:
                        if users[0][0]['user_id'] != participants_user_id and users[1][0]['user_id'] != participants_user_id:
                            pattern_json_bd[lesson]['event_id']['users'].append(user_id)
                    except IndexError:
                        pattern_json_bd[lesson]['event_id']['users'].append(user_id)
    # Заполняем роли
    if users_split is not None:
        for lesson in pattern_json_bd:
            try:
                id_user_1 = pattern_json_bd[lesson]['event_id']['users'][0][0]['user_id']
                id_user_2 = pattern_json_bd[lesson]['event_id']['users'][1][0]['user_id']
                for split in users_split:
                    id_user_split = split[0]
                    role_split = split[1]
                    if id_user_split == id_user_1:
                        pattern_json_bd[lesson]['event_id']['users'][0][0]['role'] = role_split
                    elif id_user_split == id_user_2:
                        pattern_json_bd[lesson]['event_id']['users'][1][0]['role'] = role_split
            except IndexError:
                pass
    return pattern_json_bd

def lessons_split(text):
    """
    Приводит text к split формату
    :param text: Текст
    :return: Список (list)
    """
    text_split = []
    text_split_2 = []
    # Убираем из текста "| " и заполняем список text_split
    for i in text.splitlines()[2:]:
        text_split.append(i.split('| '))
    # Убираем лишние пробелы и заполняем список text_split_2
    for i in text_split:
        value = []
        try:
            for n in range(3):
                value.append(i[n].replace(' ', ''))
            value.append(i[3])
            text_split_2.append(value)
        except IndexError:
            pass
    return text_split_2

def quality_split(text):
    """
    Приводит text к split формату
    :param text: Текст
    :return: Список (list)
    """
    text_split = []
    text_split_2 = []
    # Убираем из текста "| " и заполняем список text_split
    for i in text.splitlines()[2:]:
        text_split.append(i.split('| '))
    # Убираем лишние пробелы и заполняем список text_split_2
    for i in text_split:
        value = []
        try:
            value.append(i[0].replace(' ',''))
            if len(i[1]) > 0:
                value.append(i[1].replace(' ',''))
            else:
                value.append(' ')
            text_split_2.append(value)
        except IndexError:
            pass
    return text_split_2

def participants_split(text):
    """
    Приводит text к split формату
    :param text: Текст
    :return: Список (list)
    """
    text_split = []
    text_split_2 = []
    # Убираем из текста "| " и заполняем список text_split
    for i in text.splitlines()[2:]:
        text_split.append(i.split('| '))
    # Убираем лишние пробелы и заполняем список text_split_2
    for i in text_split:
        value = []
        try:
            value.append(i[0].replace(' ',''))
            value.append(i[1])
            text_split_2.append(value)
        except IndexError:
            pass
    return text_split_2

def users_split(text):
    """
    Приводит text к split формату
    :param text: Текст
    :return: Список (list)
    """
    text_split = []
    text_split_2 = []
    # Убираем из текста "| " и заполняем список text_split
    for i in text.splitlines()[2:]:
        text_split.append(i.split('| '))
    # Убираем лишние пробелы и заполняем список text_split_2
    for i in text_split:
        value = []
        try:
            value.append(i[0].replace(' ', ''))
            value.append(i[1])
            text_split_2.append(value)
        except IndexError:
            pass
    return text_split_2

def sort_lessons_physics(json_bd):
    """
    Возвращает все уроки по физике
    :param json_bd: Словарь (dict)
    :return: Список (list)
    """
    lessons_physics = []
    for lesson in json_bd:
        lesson_subject = json_bd[lesson]['subject']
        lesson_id = json_bd[lesson]['id']['id']
        if lesson_subject == 'phys':
            lessons_physics.append(lesson_id)
    return lessons_physics

def conversion(json_bd, sort_lessons_physics):
    """
    Возвращает день и список всех преподавателей в этот день и их уроки.
    :param json_bd: Список (list)
    :param sort_lessons_physics: Список (list)
    :return: Список (list).
    [['дата', {'id учителя_1':['id_урока_1', 'id_урока_2' ...], 'id учителя_2':['id_урока_1', 'id_урока_2' ...], n ...}],
    [['дата', {'id учителя_1':['id_урока_1', 'id_урока_2' ...], 'id учителя_2':['id_урока_1', 'id_урока_2' ...], n ...}]]
    """
    day_and_tutor = []
    # Цикл по всем урокам
    for lesson in json_bd:
        id_lesson = json_bd[lesson]['id']['id']
        # Цикл по урокам физики
        for lesson_phys in sort_lessons_physics:
            # Если урок = уроку по физике тогда
            if id_lesson == lesson_phys:
                # Есть ли оценка в этом уроке
                if len(json_bd[lesson]['id']['quality']) > 0 and json_bd[lesson]['id']['quality'][0] != '':
                    # Дата урока
                    data_lesson = json_bd[lesson]['scheduled_time'].split(' ')[0]
                    # Находим id преподавателя
                    for id in json_bd[lesson]['event_id']['users']:
                        if id[0]['role'] == 'tutor':
                            id_tutor = id[0]['user_id']

                    triger = False
                    for data in day_and_tutor:
                        if data[0] == data_lesson:
                            triger = True

                    if triger == True:
                        i = 0
                        for data in day_and_tutor:
                            if data[0] == data_lesson:
                                # Есть ли преподователь
                                if id_tutor in data[1].keys():
                                    day_and_tutor[i][1][id_tutor].append(id_lesson)
                                else:
                                    day_and_tutor[i][1].update({id_tutor:[id_lesson]})
                            i += 1
                    else:
                        text = [data_lesson, {id_tutor: [id_lesson], }]
                        day_and_tutor.append(text)
    return day_and_tutor

def arithmetic_mean():
    """
    Вычисление средней арифметической оценки преподавателя за один день.
    :return: Список (list)
    """
    list_lessons = conversion(pattern_json_bd, sort_lessons_physics(pattern_json_bd))
    list_arithmetic = []

    for split in list_lessons:
        dict_arithmetic = {}
        dict_tutor = split[1]

        for id_tutor, list_id_lesson in dict_tutor.items():
            # Складываю все оценки
            quality_sum = 0
            for lesson in pattern_json_bd:
                for id_lesson in list_id_lesson:
                    id_lesson_json = pattern_json_bd[lesson]['id']['id']
                    if id_lesson == id_lesson_json:
                        list_quality = pattern_json_bd[lesson]['id']['quality']
                        for i in list_quality:
                            if i != '':
                                quality_sum += int(i)
            # Вычисляем среднюю арифметическую оценку
            arithmetic_sum = quality_sum / len(list_id_lesson)
            # Заполняем словарь одной даты {'id учителя': ср.ариф. за день, ...}
            dict_arithmetic.update({id_tutor: round(arithmetic_sum, 2)})
        list_arithmetic.append([split[0], dict_arithmetic])
    return list_arithmetic

def low_arithmetic_rating(arithmetic_mean):
    """
    Находит самую низкую среднюю арифметическую оценку за уроки прнеподователя.
    :param arithmetic_mean: Спсиок (list) средних арефметических оценок
    :return: Список (list)
    """
    rating = []
    for split in arithmetic_mean:
        dict_tutor = split[1]
        min_number = 1000
        id_tutor_and_number = ''
        # Нахожу учителя, который в этот день имеет самую низкую среднюю арифметическую оценку
        for id_tutor, number in dict_tutor.items():
            if number < min_number:
                min_number = number
                id_tutor_and_number = id_tutor + ' - ' + str(min_number)
        rating.append([split[0], id_tutor_and_number])
    return rating

if __name__ == '__main__':
    # quality.txt
    quality = file_read('quality.txt')
    # users.txt
    users = file_read('users.txt')
    # lessons.txt
    lessons = file_read('lessons.txt ')
    # participants.txt
    participants = file_read('participants.txt')

    data_collection(lessons_split=lessons_split(lessons),
                    quality_split=quality_split(quality),
                    participants_split=participants_split(participants),
                    users_split=users_split(users))
    # print(pattern_json_bd)
    # print('1) ', sort_lessons_physics(pattern_json_bd))
    # print('2) ', arithmetic_mean())
    print(low_arithmetic_rating(arithmetic_mean()))
