import json
import sys
import os
from pathlib import Path

# Добавляем путь к папке backend в sys.path
backend_dir = Path(__file__).parent / 'backend'
sys.path.append(str(backend_dir))

# Теперь импортируем
from database import SessionLocal, engine
from models import Base, Product

# Данные товаров
products_data = [
    # Диваны (category: sofas)
    {
        "name": "Диван Комфорт",
        "description": "Угловой диван с механизмом трансформации. Идеально подходит для просторных гостиных. Обивка - велюр, наполнитель - пенополиуретан высокой плотности.",
        "price": 45990,
        "category": "sofas",
        "image": "🛋️",
        "specs": {
            "material": "велюр (100% полиэстер)",
            "frame": "массив сосны + фанера",
            "filler": "пенополиуретан HR 35 кг/м³",
            "size": "250 x 160 x 90 см",
            "bed_size": "200 x 140 см",
            "mechanism": "еврокнижка",
            "color": "бежевый",
            "load": "до 300 кг",
            "warranty": "5 лет"
        },
        "stock": "В наличии"
    },
    {
        "name": "Диван Уют",
        "description": "Прямой диван с подлокотниками. Компактный, идеально для небольших комнат. Обивка - микрофибра, наполнитель - холлофайбер.",
        "price": 38990,
        "category": "sofas",
        "image": "🛋️",
        "specs": {
            "material": "микрофибра",
            "frame": "ЛДСП + фанера",
            "filler": "холлофайбер",
            "size": "200 x 90 x 85 см",
            "bed_size": "190 x 140 см",
            "mechanism": "клик-кляк",
            "color": "серый",
            "load": "до 250 кг",
            "warranty": "3 года"
        },
        "stock": "В наличии"
    },
    {
        "name": "Диван Престиж",
        "description": "Кожаный диван с электроприводом. Регулировка положения спинки и подставки для ног. Премиум-класс для ценителей комфорта.",
        "price": 52990,
        "category": "sofas",
        "image": "🛋️",
        "specs": {
            "material": "натуральная кожа",
            "frame": "металл + массив дерева",
            "filler": "латекс + пенополиуретан",
            "size": "230 x 100 x 85 см",
            "electric": "2 мотора, 5 режимов",
            "color": "коричневый",
            "load": "до 350 кг",
            "warranty": "7 лет"
        },
        "stock": "Под заказ"
    },
    {
        "name": "Диван Компакт",
        "description": "Маленький диван для кухни или прихожей. Легкий, удобный, легко моется. Идеальное решение для небольших помещений.",
        "price": 32990,
        "category": "sofas",
        "image": "🛋️",
        "specs": {
            "material": "экокожа",
            "frame": "металл",
            "filler": "пенополиуретан",
            "size": "140 x 80 x 85 см",
            "color": "белый",
            "load": "до 200 кг",
            "warranty": "2 года"
        },
        "stock": "В наличии"
    },
    
    # Кровати (category: beds)
    {
        "name": "Кровать Спокойствие",
        "description": "Двуспальная кровать с ортопедическим основанием. Материал - массив сосны. Экологичная и надежная кровать для здорового сна.",
        "price": 32990,
        "category": "beds",
        "image": "🛏️",
        "specs": {
            "material": "массив сосны",
            "base": "ортопедическое с ламелями",
            "size": "160 x 200 см",
            "height": "45 см",
            "color": "натуральный",
            "load": "до 300 кг",
            "warranty": "5 лет"
        },
        "stock": "В наличии"
    },
    {
        "name": "Кровать Престиж",
        "description": "Кровать с мягким изголовьем из велюра. Очень уютная и стильная. Идеально подойдет для спальни в современном стиле.",
        "price": 45990,
        "category": "beds",
        "image": "🛏️",
        "specs": {
            "material": "велюр + ЛДСП",
            "headboard": "мягкое",
            "base": "ортопедическое",
            "size": "180 x 200 см",
            "color": "синий",
            "load": "до 350 кг",
            "warranty": "5 лет"
        },
        "stock": "В наличии"
    },
    {
        "name": "Кровать односпальная",
        "description": "Для подростковой или гостевой комнаты. Простая и надежная кровать из качественных материалов. Компактная и функциональная.",
        "price": 24990,
        "category": "beds",
        "image": "🛏️",
        "specs": {
            "material": "ЛДСП",
            "base": "реечное",
            "size": "90 x 200 см",
            "height": "40 см",
            "color": "белый",
            "load": "до 150 кг",
            "warranty": "3 года"
        },
        "stock": "В наличии"
    },
    {
        "name": "Кровать детская",
        "description": "С бортиками и безопасным дизайном. Для детей от 3 до 10 лет. Кровать изготовлена из экологичных материалов, имеет закругленные углы и защитные бортики.",
        "price": 39990,
        "category": "beds",
        "image": "🛏️",
        "specs": {
            "material": "массив березы",
            "size": "80 x 160 см",
            "sides": "съемные, высота 30 см",
            "color": "натуральный",
            "load": "до 100 кг",
            "warranty": "5 лет"
        },
        "stock": "Под заказ"
    },
    
    # Столы (category: tables)
    {
        "name": "Стол обеденный",
        "description": "Раскладной стол из массива дуба. Покрытие - матовый лак. Идеальное решение для семейных обедов и праздничных ужинов.",
        "price": 18990,
        "category": "tables",
        "image": "🪑",
        "specs": {
            "material": "дуб",
            "size_folded": "120 x 80 см",
            "size_unfolded": "180 x 80 см",
            "height": "75 см",
            "mechanism": "книжка",
            "color": "натуральный",
            "load": "до 150 кг",
            "warranty": "5 лет"
        },
        "stock": "В наличии"
    },
    {
        "name": "Стол письменный",
        "description": "Удобный письменный стол с ящиками для хранения. Организуйте свое рабочее пространство с комфортом. Идеально для дома или офиса.",
        "price": 24990,
        "category": "tables",
        "image": "🪑",
        "specs": {
            "material": "ЛДСП",
            "size": "140 x 70 см",
            "height": "75 см",
            "drawers": "3 шт (глубокие)",
            "color": "венге",
            "load": "до 100 кг",
            "warranty": "3 года"
        },
        "stock": "В наличии"
    },
    {
        "name": "Стол компьютерный",
        "description": "Эргономичный компьютерный стол с полкой для системного блока и выдвижной панелью для клавиатуры. Все необходимое для комфортной работы за компьютером.",
        "price": 32990,
        "category": "tables",
        "image": "🪑",
        "specs": {
            "material": "ЛДСП",
            "size": "160 x 80 см",
            "height": "75 см",
            "pc_holder": "есть",
            "keyboard_tray": "выдвижная",
            "drawers": "2 шт",
            "color": "черный",
            "load": "до 120 кг",
            "warranty": "3 года"
        },
        "stock": "В наличии"
    },
    {
        "name": "Стол журнальный",
        "description": "Стильный журнальный столик для гостиной. Легкий, изящный, но при этом прочный. Идеально подходит для книг, журналов и чашечки кофе.",
        "price": 15990,
        "category": "tables",
        "image": "🪑",
        "specs": {
            "material": "стекло + металл",
            "size": "80 x 50 см",
            "height": "45 см",
            "glass": "закаленное, 8 мм",
            "shelf": "нижняя металлическая",
            "color": "прозрачное стекло, хром",
            "load": "до 30 кг",
            "warranty": "2 года"
        },
        "stock": "В наличии"
    }
]

def init_products():
    print("🚀 Инициализация таблицы товаров...")
    
    # Создаём таблицы (если их нет)
    Base.metadata.create_all(bind=engine)
    
    # Получаем сессию
    db = SessionLocal()
    
    try:
        # Получаем список существующих товаров
        existing_products = db.query(Product).all()
        existing_names = {p.name for p in existing_products}
        
        added_count = 0
        updated_count = 0
        
        for product_data in products_data:
            # Проверяем, есть ли товар с таким названием
            existing = db.query(Product).filter(Product.name == product_data["name"]).first()
            
            specs_json = json.dumps(product_data["specs"], ensure_ascii=False)
            
            if existing:
                # Обновляем существующий товар
                existing.description = product_data["description"]
                existing.price = product_data["price"]
                existing.category = product_data["category"]
                existing.image = product_data["image"]
                existing.specs = specs_json
                existing.stock = product_data["stock"]
                updated_count += 1
                print(f"🔄 Обновлен: {product_data['name']}")
            else:
                # Добавляем новый товар
                product = Product(
                    name=product_data["name"],
                    description=product_data["description"],
                    price=product_data["price"],
                    category=product_data["category"],
                    image=product_data["image"],
                    specs=specs_json,
                    stock=product_data["stock"]
                )
                db.add(product)
                added_count += 1
                print(f"✅ Добавлен: {product_data['name']}")
        
        db.commit()
        print(f"\n📊 Итог: добавлено {added_count}, обновлено {updated_count} товаров")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_products()