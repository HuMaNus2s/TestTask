import csv
import os

filename = 'file.csv'
def generator_words(word):
    endings = ['ый', 'ие', 'ого', 'ая', 'ое', 'ые', 'o']
    words = [word]
    if len(word) > 3:
         base_word = word
         if any(word.endswith(ending) for ending in endings):
             base_word = word[:-2]
             
         for ending in endings:
             words.append(base_word + ending)
    return words      

def found_keywords(options, keywords):
    founds = []
    words = options.replace(",", " ").lower().split()
    for word in words:
        for keyword in keywords:
            if keyword in word:
                founds.append(word)
            else: 
                variants = generator_words(keyword)
                for variant in variants:
                    if variant in word:
                        founds.append(word)
    return founds

def search_products(keywords):
    keywords = keywords.replace(",", " ").lower().split()
    keywords = [k.lower() for k in keywords]
    products = []
    print(f"Обнаруженные ключевые слова: {keywords}")
    
    with open(filename, newline="", encoding="utf-8") as file:
        read_csv = csv.reader(file)
        next(read_csv)
        for product_id, name, description, tags in read_csv:         
            score = 0
            
            found_words_description = found_keywords(description, keywords)
            found_words_tags = found_keywords(tags, keywords)
            print(found_words_description)
            
            for keyword in keywords:
                if keyword in name.lower():
                        score += 100                  
                score += len(found_words_description) + len(found_words_tags)
                
                products.append({
                    "product_id": product_id,
                    "name": name,
                    "description": description,
                    "tags": tags,
                    "score": score,
                    "found_in_description": len(found_words_description),
                    "found_in_tags": len(found_words_tags)
                })
                
        products.sort(key=lambda x: x["score"], reverse=True)
        
        for product in products:
            print(f"\nНазвание продукта: {product['name']} | id: {product['product_id']}")
            print(f"Описание:\n{product['description']}")
            print(f"Теги: {product['tags']}")
            print(f"Найдено в описании: {product['found_in_description']}")
            print(f"Найдено в тегах: {product['found_in_tags']}")
            print(f"Общее количество очков: {product['score']}\n")
        
        
while(True):
    keyword = input("Введите ключевое слово для поиска: ")
    search_products(keyword)
    print("=========================================================================")
