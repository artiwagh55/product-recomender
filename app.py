from flask import Flask, render_template, request
import pandas as pd
import random

app = Flask(__name__)

# Real product images for different categories
category_images = {
    'Smartphones': [
        'https://images.unsplash.com/photo-1592899677977-9e10cb6be28e?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1616348436168-de43ad0db179?w=300&h=200&fit=crop'
    ],
    'Laptops': [
        'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=300&h=200&fit=crop'
    ],
    'Headphones': [
        'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=300&h=200&fit=crop'
    ],
    'Tablets': [
        'https://images.unsplash.com/photo-1589739900243-4b52cd9dd104?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1561154464-82e9adf32764?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1544244015-0df4b3ff2a3b?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1529162226152-4862f70d4d6c?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1491933382434-500287f9b54b?w=300&h=200&fit=crop'
    ],
    'Smartwatches': [
        'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1434494878577-86c23bcb06b9?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=300&h=200&fit=crop'
    ],
    'Televisions': [
        'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1584283998046-5d6f4a60da3a?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1567696911980-2ee69ceaf898?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=300&h=200&fit=crop'
    ],
    'Cameras': [
        'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1452780212940-6f5c0d14d848?w=300&h=200&fit=crop',
        'https://images.unsplash.com/photo-1504208434309-cb69f4fe52b0?w=300&h=200&fit=crop'
    ]
}

# Product data
products_data = {
    'Smartphones': [
        'iPhone 15 Pro Max', 'iPhone 15 Pro', 'iPhone 15 Plus', 'iPhone 15', 'Samsung Galaxy S24 Ultra',
        'Samsung Galaxy S24 Plus', 'Samsung Galaxy S24', 'Google Pixel 8 Pro', 'Google Pixel 8', 'OnePlus 12'
    ],
    'Laptops': [
        'MacBook Pro 14', 'MacBook Pro 16', 'MacBook Air M2', 'Dell XPS 15', 'Dell XPS 13',
        'Lenovo ThinkPad X1', 'HP Spectre x360', 'ASUS ROG Zephyrus', 'Microsoft Surface Laptop 5', 'Razer Blade 15'
    ],
    'Headphones': [
        'Sony WH-1000XM5', 'Bose QC45', 'Apple AirPods Pro 2', 'Samsung Galaxy Buds 2 Pro', 'Sennheiser Momentum 4',
        'JBL Tune 760NC', 'Beats Studio Pro', 'Anker Soundcore Q45', 'Jabra Elite 5', 'Sony WF-1000XM5'
    ],
    'Tablets': [
        'iPad Pro 12.9', 'iPad Air', 'iPad Mini', 'Samsung Tab S9 Ultra', 'Samsung Tab S9',
        'Microsoft Surface Pro 9', 'Lenovo Tab P12', 'Amazon Fire HD 10', 'Xiaomi Pad 6', 'Google Pixel Tablet'
    ],
    'Smartwatches': [
        'Apple Watch Ultra 2', 'Apple Watch Series 9', 'Samsung Galaxy Watch 6', 'Garmin Fenix 7', 'Fitbit Sense 2',
        'Xiaomi Watch 2 Pro', 'Amazfit GTR 4', 'Huawei Watch GT 4', 'Google Pixel Watch 2', 'TicWatch Pro 5'
    ],
    'Televisions': [
        'Samsung QN90C', 'LG C3 OLED', 'Sony A80L', 'TCL 6-Series', 'Hisense U8K',
        'Vizio P-Series', 'Panasonic MZ2000', 'Philips OLED+', 'Sharp Aquos', 'Xiaomi TV Q2'
    ],
    'Cameras': [
        'Sony Alpha A7 IV', 'Canon EOS R6', 'Nikon Z8', 'Fujifilm X-T5', 'GoPro HERO12',
        'DJI Osmo Pocket 3', 'Panasonic Lumix S5', 'Olympus OM-1', 'Leica Q3', 'Insta360 X3'
    ]
}

# Generate products with real images
products = []
for category, names in products_data.items():
    images = category_images.get(category, category_images['Smartphones'])
    for i, name in enumerate(names):
        image_url = images[i % len(images)]
        price = {
            'Smartphones': random.randint(699, 1499),
            'Laptops': random.randint(999, 3499),
            'Headphones': random.randint(199, 549),
            'Tablets': random.randint(499, 1299),
            'Smartwatches': random.randint(299, 799),
            'Televisions': random.randint(999, 3999),
            'Cameras': random.randint(999, 4999)
        }.get(category, random.randint(299, 999))
        
        rating = round(random.uniform(4.0, 4.9), 1)
        
        products.append({
            'name': name,
            'category': category,
            'price': price,
            'image_url': image_url,
            'description': f'Premium {category.lower()} with cutting-edge technology and exceptional performance. Perfect for everyday use and professional needs.',
            'rating': rating,
            'features': f'{category.lower()} premium quality advanced features'
        })

df = pd.DataFrame(products)
print(f"✅ Loaded {len(df)} products with real images")

def search_products(query):
    query_lower = query.lower().strip()
    results = []
    for _, row in df.iterrows():
        if query_lower in row['name'].lower() or query_lower in row['category'].lower():
            results.append({
                'name': row['name'],
                'category': row['category'],
                'price': f"${row['price']:.2f}",
                'rating': row['rating'],
                'image_url': row['image_url'],
                'description': row['description']
            })
    return results[:20]

def get_recommendations(product_name, n=8):
    product_row = df[df['name'] == product_name]
    if product_row.empty:
        return [], f"❌ Product not found"
    
    category = product_row.iloc[0]['category']
    product_price = product_row.iloc[0]['price']
    
    same_category = df[df['category'] == category].copy()
    same_category = same_category[same_category['name'] != product_name]
    same_category['price_diff'] = abs(same_category['price'] - product_price) / product_price
    same_category['similarity'] = (1 - same_category['price_diff']) * 100
    same_category = same_category.nlargest(n, 'similarity')
    
    recommendations = []
    for _, row in same_category.iterrows():
        recommendations.append({
            'name': row['name'],
            'category': row['category'],
            'price': f"${row['price']:.2f}",
            'rating': row['rating'],
            'image_url': row['image_url'],
            'description': row['description'],
            'similarity': round(row['similarity'], 1)
        })
    return recommendations, f"✓ Found {len(recommendations)} {category} recommendations"

def get_trending_products(n=12):
    trending = df.nlargest(n, 'rating')
    products_list = []
    for _, row in trending.iterrows():
        products_list.append({
            'name': row['name'],
            'category': row['category'],
            'price': f"${row['price']:.2f}",
            'rating': row['rating'],
            'image_url': row['image_url'],
            'description': row['description']
        })
    return products_list

products_list = [{'name': row['name'], 'price': f"${row['price']:.2f}"} for _, row in df.iterrows()]
categories = sorted(df['category'].unique())
trending_products = get_trending_products(12)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    selected_product = None
    recommendation_message = ""
    search_results = []
    search_query = ""
    
    if request.method == 'POST':
        if 'search_query' in request.form:
            search_query = request.form.get('search_query', '')
            if search_query:
                search_results = search_products(search_query)
        else:
            product_name = request.form.get('product')
            if product_name:
                recommendations, recommendation_message = get_recommendations(product_name)
                product_row = df[df['name'] == product_name]
                if not product_row.empty:
                    row = product_row.iloc[0]
                    selected_product = {
                        'name': row['name'],
                        'category': row['category'],
                        'price': f"${row['price']:.2f}",
                        'rating': row['rating'],
                        'image_url': row['image_url'],
                        'description': row['description']
                    }
    
    return render_template('index.html',
                         products=products_list,
                         categories=categories,
                         selected_product=selected_product,
                         recommendations=recommendations,
                         recommendation_message=recommendation_message,
                         trending_products=trending_products,
                         search_results=search_results,
                         search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)