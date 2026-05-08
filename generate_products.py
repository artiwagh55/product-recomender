import pandas as pd
import random

# Categories and their products
categories = {
    'Smartphones': {
        'brands': ['Apple', 'Samsung', 'Google', 'OnePlus', 'Xiaomi', 'Motorola', 'Nothing', 'Sony', 'Huawei', 'Realme', 'Vivo', 'Oppo', 'Asus', 'LG', 'Nokia'],
        'models': ['Pro Max', 'Pro', 'Plus', 'Ultra', 'Lite', 'SE', 'FE', 'GT', 'Neo', 'X', 'Z', 'A Series', 'M Series', 'Edge', 'Razr'],
        'price_range': [299, 1999],
        'image_base': 'smartphone'
    },
    'Laptops': {
        'brands': ['Apple', 'Dell', 'Lenovo', 'HP', 'Asus', 'Acer', 'Microsoft', 'Razer', 'MSI', 'Gigabyte', 'Samsung', 'LG', 'Huawei', 'Xiaomi', 'Alienware'],
        'models': ['Pro', 'Air', 'XPS', 'ThinkPad', 'Spectre', 'Zenbook', 'ROG', 'Legion', 'Surface', 'Predator', 'Swift', 'Gram', 'Book', 'Blade', 'TUF'],
        'price_range': [499, 3999],
        'image_base': 'laptop'
    },
    'Headphones': {
        'brands': ['Sony', 'Bose', 'Apple', 'Samsung', 'JBL', 'Sennheiser', 'Audio-Technica', 'Beats', 'Skullcandy', 'Anker', 'Jabra', 'Plantronics', 'Razer', 'Logitech', 'Corsair'],
        'models': ['WH-1000XM', 'QC', 'AirPods', 'Galaxy Buds', 'Tune', 'Momentum', 'ATH', 'Studio', 'Crusher', 'Soundcore', 'Elite', 'Voyager', 'BlackShark', 'G Pro', 'Virtuoso'],
        'price_range': [49, 549],
        'image_base': 'headphone'
    },
    'Tablets': {
        'brands': ['Apple', 'Samsung', 'Lenovo', 'Microsoft', 'Amazon', 'Huawei', 'Xiaomi', 'Google', 'Asus', 'Acer', 'LG', 'Nokia', 'TCL', 'Alcatel', 'Blackview'],
        'models': ['iPad Pro', 'iPad Air', 'iPad Mini', 'Galaxy Tab', 'Tab', 'Surface', 'Fire', 'MatePad', 'Pad', 'Pixel Tablet', 'ZenPad', 'Iconia', 'Gram', 'Tab', 'Ultra'],
        'price_range': [99, 1499],
        'image_base': 'tablet'
    },
    'Smartwatches': {
        'brands': ['Apple', 'Samsung', 'Garmin', 'Fitbit', 'Xiaomi', 'Amazfit', 'Huawei', 'Google', 'Fossil', 'TicWatch', 'Withings', 'Suunto', 'Coros', 'Polar', 'Casio'],
        'models': ['Watch Ultra', 'Watch Series', 'Galaxy Watch', 'Fenix', 'Venu', 'Charge', 'Sense', 'Mi Band', 'Amazfit', 'Watch GT', 'Pixel Watch', 'Gen', 'Pro', 'Elite', 'G-Shock'],
        'price_range': [49, 899],
        'image_base': 'watch'
    },
    'Televisions': {
        'brands': ['Samsung', 'LG', 'Sony', 'TCL', 'Hisense', 'Vizio', 'Panasonic', 'Philips', 'Sharp', 'Xiaomi', 'Realme', 'OnePlus', 'Insignia', 'Element', 'Sceptre'],
        'models': ['OLED', 'QLED', 'NanoCell', 'Crystal', 'Frame', 'A80L', 'C3', 'U8', '6-Series', 'M-Series', 'P-Series', 'EZIO', 'V-Series', 'Fire TV', 'Android TV'],
        'price_range': [199, 3999],
        'image_base': 'tv'
    },
    'Cameras': {
        'brands': ['Sony', 'Canon', 'Nikon', 'Fujifilm', 'Panasonic', 'GoPro', 'DJI', 'Leica', 'Olympus', 'Pentax', 'Ricoh', 'Kodak', 'Polaroid', 'Insta360', 'Blackmagic'],
        'models': ['Alpha', 'EOS', 'Z', 'X-T', 'Lumix', 'HERO', 'Osmo', 'Q', 'OM-D', 'K', 'GR', 'PIXPRO', 'Now', 'One X', 'Pocket'],
        'price_range': [199, 5999],
        'image_base': 'camera'
    },
    'Gaming': {
        'brands': ['Sony', 'Microsoft', 'Nintendo', 'Razer', 'Logitech', 'Corsair', 'SteelSeries', 'HyperX', 'Alienware', 'Asus', 'MSI', 'Acer', 'Lenovo', 'HP', 'Dell'],
        'models': ['PlayStation', 'Xbox', 'Switch', 'Steam Deck', 'ROG Ally', 'Legion Go', 'DualSense', 'Elite', 'Pro Controller', 'Joy-Con', 'Razer Kaira', 'G Pro', 'Void', 'Cloud', 'Oculus'],
        'price_range': [29, 1999],
        'image_base': 'gaming'
    },
    'Audio': {
        'brands': ['Sonos', 'Bose', 'JBL', 'Sony', 'Marshall', 'Harman Kardon', 'Bang & Olufsen', 'Ultimate Ears', 'Anker', 'Tribit', 'Doss', 'Oontz', 'Altec Lansing', 'IKEA', 'Google'],
        'models': ['Arc', 'Beam', 'SoundLink', 'Flip', 'Charge', 'XBOOM', 'Stanmore', 'Aura', 'Blast', 'Mega', 'Wonderboom', 'Soundcore', 'Swan', 'Eneby', 'Nest Audio'],
        'price_range': [29, 899],
        'image_base': 'speaker'
    },
    'Monitors': {
        'brands': ['Dell', 'LG', 'Samsung', 'Asus', 'Acer', 'BenQ', 'ViewSonic', 'MSI', 'Gigabyte', 'HP', 'Lenovo', 'AOC', 'Philips', 'Alienware', 'Razer'],
        'models': ['UltraSharp', 'UltraGear', 'Odyssey', 'ROG', 'Predator', 'DesignVue', 'Elite', 'Optix', 'M27Q', 'E-Series', 'ThinkVision', 'C-Series', 'E-Series', 'AW', 'Raptor'],
        'price_range': [149, 1999],
        'image_base': 'monitor'
    },
    'Printers': {
        'brands': ['HP', 'Canon', 'Epson', 'Brother', 'Xerox', 'Lexmark', 'Samsung', 'Kyocera', 'Ricoh', 'Dell', 'Panasonic', 'Kodak', 'OKI', 'Sharp', 'Konica Minolta'],
        'models': ['LaserJet', 'Smart Tank', 'EcoTank', 'WorkForce', 'Home', 'Office', 'Color', 'Monochrome', 'All-in-One', 'Wireless', 'Photo', 'Business', 'Multifunction', 'Compact', 'Portable'],
        'price_range': [79, 599],
        'image_base': 'printer'
    }
}

# Generate 500+ products
products = []
product_id = 1

for category, data in categories.items():
    brands = data['brands']
    models = data['models']
    price_min, price_max = data['price_range']
    image_base = data['image_base']
    
    # Generate 50-60 products per category
    num_products = random.randint(45, 60)
    
    for i in range(num_products):
        brand = random.choice(brands)
        model = random.choice(models)
        
        # Create product name
        if random.random() > 0.5:
            name = f"{brand} {model} {random.randint(1, 10)}"
        else:
            name = f"{brand} {model}"
        
        # Add series numbers for some products
        if 'Series' not in name and random.random() > 0.7:
            name += f" {random.choice(['2024', '2025', 'Pro', 'Max', 'Plus', 'Ultra', 'Elite', 'Premium'])}"
        
        # Generate price
        price = round(random.uniform(price_min, price_max), 2)
        
        # Generate rating (4.0 to 5.0)
        rating = round(random.uniform(4.0, 5.0), 1)
        
        # Generate description
        descriptions = [
            f"Latest {brand} {model} with cutting-edge technology",
            f"High-performance {category.lower()} for professionals",
            f"Premium {category.lower()} with amazing features",
            f"Affordable {category.lower()} with great value",
            f"Flagship {category.lower()} with best-in-class specs",
            f"Compact and portable {category.lower()} for everyday use",
            f"Advanced {category.lower()} with AI features",
            f"Next-gen {category.lower()} with innovation",
            f"Powerful {category.lower()} for creators",
            f"Ultimate {category.lower()} experience"
        ]
        description = random.choice(descriptions)
        
        # Generate features
        features = f"{category.lower()} {brand.lower()} {model.lower()} premium quality"
        
        # Use realistic image URLs
        image_id = random.randint(1, 100)
        if category == 'Smartphones':
            image_url = f"https://cdn.pixabay.com/photo/2023/{image_id}/smartphone-{image_id}_640.jpg"
        elif category == 'Laptops':
            image_url = f"https://cdn.pixabay.com/photo/2020/{image_id}/laptop-{image_id}_640.jpg"
        elif category == 'Headphones':
            image_url = f"https://cdn.pixabay.com/photo/2018/{image_id}/headphones-{image_id}_640.jpg"
        elif category == 'Tablets':
            image_url = f"https://cdn.pixabay.com/photo/2018/{image_id}/tablet-{image_id}_640.jpg"
        elif category == 'Smartwatches':
            image_url = f"https://cdn.pixabay.com/photo/2018/{image_id}/watch-{image_id}_640.jpg"
        elif category == 'Televisions':
            image_url = f"https://cdn.pixabay.com/photo/2016/{image_id}/tv-{image_id}_640.jpg"
        elif category == 'Cameras':
            image_url = f"https://cdn.pixabay.com/photo/2016/{image_id}/camera-{image_id}_640.jpg"
        elif category == 'Gaming':
            image_url = f"https://cdn.pixabay.com/photo/2017/{image_id}/gaming-{image_id}_640.jpg"
        elif category == 'Audio':
            image_url = f"https://cdn.pixabay.com/photo/2019/{image_id}/speaker-{image_id}_640.jpg"
        elif category == 'Monitors':
            image_url = f"https://cdn.pixabay.com/photo/2018/{image_id}/monitor-{image_id}_640.jpg"
        else:
            image_url = f"https://cdn.pixabay.com/photo/2015/{image_id}/printer-{image_id}_640.jpg"
        
        # Fallback images
        fallback_images = {
            'Smartphones': 'https://cdn.pixabay.com/photo/2015/05/27/15/00/samsung-786600_640.jpg',
            'Laptops': 'https://cdn.pixabay.com/photo/2020/05/22/18/52/laptop-5209429_640.jpg',
            'Headphones': 'https://cdn.pixabay.com/photo/2018/12/20/10/15/headphones-3886111_640.jpg',
            'Tablets': 'https://cdn.pixabay.com/photo/2018/04/07/19/05/ipad-3298665_640.jpg',
            'Smartwatches': 'https://cdn.pixabay.com/photo/2017/11/20/22/12/smartwatch-2965226_640.jpg',
            'Televisions': 'https://cdn.pixabay.com/photo/2018/12/31/10/32/tv-3904746_640.jpg',
            'Cameras': 'https://cdn.pixabay.com/photo/2016/11/29/02/08/camera-1867185_640.jpg',
            'Gaming': 'https://cdn.pixabay.com/photo/2015/09/02/12/45/game-918381_640.jpg',
            'Audio': 'https://cdn.pixabay.com/photo/2016/09/03/21/37/speaker-1646639_640.jpg',
            'Monitors': 'https://cdn.pixabay.com/photo/2014/09/28/23/38/monitor-464675_640.jpg',
            'Printers': 'https://cdn.pixabay.com/photo/2015/01/26/18/18/printer-613314_640.jpg'
        }
        
        # Use fallback if needed
        final_image_url = image_url if random.random() > 0.3 else fallback_images.get(category, 'https://cdn.pixabay.com/photo/2015/05/27/15/00/samsung-786600_640.jpg')
        
        products.append({
            'name': name,
            'category': category,
            'price': price,
            'image_url': final_image_url,
            'description': description,
            'rating': rating,
            'features': features
        })
        
        product_id += 1
        
        # Stop at 500 products
        if product_id > 500:
            break
    
    if product_id > 500:
        break

# Create DataFrame
df = pd.DataFrame(products)

# Save to CSV
df.to_csv('products.csv', index=False)

print(f"✅ Generated {len(df)} products")
print(f"✅ Categories: {df['category'].unique().tolist()}")
print(f"✅ Price range: ${df['price'].min():.2f} - ${df['price'].max():.2f}")
print("✅ Products saved to products.csv")

# Show sample
print("\n📊 Sample products:")
for i in range(min(10, len(df))):
    print(f"  {i+1}. {df.iloc[i]['name']} - ${df.iloc[i]['price']:.2f} ({df.iloc[i]['category']})")