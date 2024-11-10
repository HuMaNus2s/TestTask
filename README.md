# Задание 1
### 1. Запуск проекта
#### Требования:

- Python 3.8 или выше
- Установленные библиотеки, указанные в `requirements.txt`

#### Установка зависимостей(в этой задаче это необязательно):

Для установки всех необходимых зависимостей, используйте следующую команду:

```bash
pip install -r requirements.txt
```

#### Запуск приложения:

Для запуска приложения используйте команду:

```bash
python SearchSystem.py
```

Программа будет ожидать ввод ключевого слова для поиска товара в консоли.
Так же программа находит совпадения ключевых слов с данными товаров и включает генератор, который подбирает окончания слов, если они есть, повышая тем самым точность и релевантность поиска.
### 2. Структура данных

Товары хранятся в формате CSV-файла с полями:

- `product_id` — уникальный идентификатор товара.
- `name` — название товара.
- `description` — описание товара.
- `tags` — список тегов, связанных с товаром.

Пример структуры данных в файле `file.csv`:

```csv
product_id,name,description,tags
1,Смартфон Samsung Galaxy S21,"Samsung Galaxy S21 смартфон с экраном 6.2 дюйма, процессором Exynos 2100 и камерой 64 МП. Смартфон идеально подходит для повседневных задач, игр и съёмки фото. Доступен в цветах: красный, красно-лавовый, черный, белый, фиолетовый.","смартфон, электроника, Samsung"
2,Смартфон Apple iPhone 13,"iPhone 13 с экраном 6.1 дюйма и процессором A15 Bionic. Камера 12 МП с возможностью съемки в 4K и ночным режимом. Доступен в цветах: синий, красный, черный, розовый.","смартфон, электроника, Apple"
3,Смартфон Xiaomi Redmi Note 10,"Xiaomi Redmi Note 10 с экраном 6.43 дюйма AMOLED и процессором Snapdragon 678. Камера 48 МП и аккумулятор 48 мАч для длительной работы. Доступен в белом, черном, красном цветах.","смартфон, электроника, Xiaomi"
4,Смартфон OnePlus 9,"OnePlus 9 с экраном 6.55 дюйма Fluid AMOLED и процессором Snapdragon 888. Камера 48 МП с потрясающими ночными снимками. Цвета: арктический белый, метеоритный черный, красный.","смартфон, электроника, OnePlus"
5,Смартфон Motorola Moto G100,"Motorola Moto G100 с экраном 6.7 дюйма и процессором Snapdragon 870. Камера 64 МП и аккумулятор на 5000 мАч для длительной работы. Доступен в цветах: синий, белый, красный.","смартфон, электроника, Motorola"
6,Телефон Nokia 105,"Телефон Nokia 105 с экраном 1.8 дюйма и батареей на 800 мАч. Поддерживает базовые функции, такие как звонки и текстовые сообщения. Доступен в черном, красном и синем цветах.","телефон, электроника, Nokia"
7,Смартфон Samsung Galaxy A72,"Samsung Galaxy A72 с процессором Snapdragon 720G и экраном Super AMOLED 6.7 дюйма. Камера 64 МП для создания качественных фотографий. Смартфон в синем и черном цветах, а также красном.","смартфон, электроника, Samsung"
8,Смартфон Apple iPhone 12,"iPhone 12 с экраном 6.1 дюйма Super Retina и процессором A14 Bionic. Камера 12 МП для съемки в высоком качестве. Доступен в черном, белом и красном цветах.","смартфон, электроника, Apple"
9,Смартфон Xiaomi Mi 11,"Xiaomi Mi 11 с экраном 6.81 дюйма AMOLED и процессором Snapdragon 888. Камера 108 МП и отличное качество видео. Смартфон в синем и черном цветах, а также в розовом.","смартфон, электроника, Xiaomi"
10,Смартфон OnePlus Nord 2,"OnePlus Nord 2 с экраном 6.43 дюйма AMOLED и процессором Dimensity 1200. Камера 50 МП с ночным режимом. Цвета: голубой, серый, красный.","смартфон, электроника, OnePlus"
11,Смартфон Motorola Moto G60,"Motorola Moto G60 с экраном 6.8 дюйма и процессором Snapdragon 732G. Камера 108 МП для профессиональных снимков. Смартфон в черном и сером цветах, а также красном.","смартфон, электроника, Motorola"
12,Смартфон Samsung Galaxy Note 20,"Samsung Galaxy Note 20 с экраном 6.9 дюйма и процессором Exynos 990. Камера 108 МП для фото в любых условиях. Также поддерживает стилус S Pen. Доступен в черном, бронзовом и красном цветах.","смартфон, электроника, Samsung"
13,Наушники Sony WH-1000XM4,"Наушники Sony WH-1000XM4 с активным шумоподавлением и длительным временем работы. Поддерживают Hi-Res Audio и быструю зарядку. Цвет: черный, серебристый.","наушники, электроника, Sony"
14,Наушники Apple AirPods Pro,"Наушники Apple AirPods Pro с активным шумоподавлением и адаптивным эквалайзером. Обеспечивают отличное качество звука и комфорт. Цвет: белый.","наушники, электроника, Apple"
15,Наушники Bose QuietComfort 35 II,"Наушники Bose QuietComfort 35 II с функцией активного шумоподавления. Обеспечивают кристально чистый звук и комфорт при длительном использовании. Доступны в черном и серебристом цветах.","наушники, электроника, Bose"

```

### 3. Описание функций поиска

#### Функция поиска по ключевым словам

Функция `search_products(keyword)` принимает строку `keyword` и ищет товары, которые содержат это ключевое слово в любом из полей (название, описание, теги). Алгоритм учитывает синонимичные формы слов и выполняет поиск по частичному совпадению.

#### Пример запроса:

```bash
Введите ключевое слово для поиска: телефон
```

Программа будет искать товары, связанные с ключевым словом "телефон" и выведет результаты с наибольшим количеством совпадений.

### 4. Примеры работы программы

#### Пример 1: Поиск по ключевому слову "телефон"

- **Ввод**:
    ```bash
    Введите ключевое слово для поиска: телефон
    ```

- **Результат**:
    ```
    Обнаруженные ключевые слова: ['телефон']
    Название продукта: Телефон Nokia 105 | id: 6
    Описание:
    Телефон Nokia 105 с экраном 1.8 дюйма и батареей на 800 мАч. Поддерживает базовые функции, такие как звонки и текстовые сообщения. Доступен в черном, красном и синем цветах.
    Теги: телефон, электроника, Nokia
    Найдено в описании: 1
    Найдено в тегах: 1
    Общее количество очков: 102
    ```

#### Пример 2: Поиск по нескольким ключевым словам "красный телефон"

- **Ввод**:
    ```bash
    Введите ключевое слово для поиска: красный телефон
    ```

- **Результат**:
    ```
    Обнаруженные ключевые слова: ['красный', 'телефон']
    Название продукта: Телефон Nokia 105 | id: 6
    Описание:
    Телефон Nokia 105 с экраном 1.8 дюйма и батареей на 800 мАч. Поддерживает базовые функции, такие как звонки и текстовые сообщения. Доступен в черном, красном и синем цветах.
    Теги: телефон, электроника, Nokia
    Найдено в описании: 2
    Найдено в тегах: 1
    Общее количество очков: 103
    ```
