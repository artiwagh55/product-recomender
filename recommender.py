import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

# Load data
df = pd.read_csv('products.csv')
product_col = 'name'
print(f"✅ Loaded {len(df)} products")
print(f"✅ Categories: {df['category'].unique().tolist()}")

# Create search text with category boost
df['search_text'] = df['category'] + ' ' + df['category'] + ' ' + df['name'] + ' ' + df['features']

# Create similarity matrix
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
tfidf_matrix = vectorizer.fit_transform(df['search_text'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print("✅ Similarity matrix created")

def search_products(query, max_results=20):
    """Search products by name, category, or features"""
    query_lower = query.lower().strip()
    results = []
    
    # Try exact matches first
    exact_matches = df[df[product_col].str.lower() == query_lower]
    if not exact_matches.empty:
        for _, row in exact_matches.iterrows():
            results.append({
                'name': row[product_col],
                'category': row['category'],
                'price': row['price'],
                'rating': row['rating'],
                'image_url': row['image_url'],
                'description': row['description']
            })
        return results
    
    # Check if query matches any category
    matched_category = None
    for cat in df['category'].unique():
        if query_lower in cat.lower() or cat.lower() in query_lower:
            matched_category = cat
            break
    
    # Search in name and category
    for _, row in df.iterrows():
        name_match = query_lower in row[product_col].lower()
        category_match = matched_category and row['category'] == matched_category
        feature_match = query_lower in row['features'].lower()
        
        if name_match or category_match or feature_match:
            results.append({
                'name': row[product_col],
                'category': row['category'],
                'price': row['price'],
                'rating': row['rating'],
                'image_url': row['image_url'],
                'description': row['description']
            })
        
        if len(results) >= max_results:
            break
    
    # If no results, try fuzzy matching
    if not results and len(query) > 2:
        all_names = df[product_col].tolist()
        matches = get_close_matches(query_lower, [n.lower() for n in all_names], n=max_results, cutoff=0.5)
        for match in matches:
            matched_row = df[df[product_col].str.lower() == match]
            if not matched_row.empty:
                row = matched_row.iloc[0]
                results.append({
                    'name': row[product_col],
                    'category': row['category'],
                    'price': row['price'],
                    'rating': row['rating'],
                    'image_url': row['image_url'],
                    'description': row['description']
                })
    
    return results

def get_recommendations(product_name, n_recommendations=8):
    """Get accurate recommendations from same category"""
    try:
        # Find product
        if product_name not in df[product_col].values:
            suggestions = search_products(product_name, 3)
            if suggestions:
                suggestion_names = [s['name'] for s in suggestions[:3]]
                return [], f"❌ '{product_name}' not found. Did you mean: {', '.join(suggestion_names)}?"
            return [], f"❌ Product '{product_name}' not found"
        
        # Get product index and category
        idx = df[df[product_col] == product_name].index[0]
        product_category = df.iloc[idx]['category']
        product_price = df.iloc[idx]['price']
        
        # Get similarity scores
        sim_scores = list(enumerate(cosine_sim[idx]))
        
        # Filter and sort
        recommendations = []
        for i, score in sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:]:
            if df.iloc[i]['category'] == product_category:
                price_diff = abs(df.iloc[i]['price'] - product_price) / product_price
                price_bonus = 1.2 if price_diff < 0.3 else (1.0 if price_diff < 0.6 else 0.9)
                final_score = score * price_bonus * 1.3  # Category bonus
                
                recommendations.append({
                    'name': df.iloc[i][product_col],
                    'category': df.iloc[i]['category'],
                    'price': f"${df.iloc[i]['price']:.2f}",
                    'rating': float(df.iloc[i]['rating']),
                    'image_url': df.iloc[i]['image_url'],
                    'description': df.iloc[i]['description'],
                    'similarity': round(final_score * 100, 1)
                })
            
            if len(recommendations) >= n_recommendations:
                break
        
        if not recommendations:
            # Fallback: show top products from same category
            same_category = df[df['category'] == product_category].head(n_recommendations + 1)
            for _, row in same_category.iterrows():
                if row[product_col] != product_name:
                    recommendations.append({
                        'name': row[product_col],
                        'category': row['category'],
                        'price': f"${row['price']:.2f}",
                        'rating': float(row['rating']),
                        'image_url': row['image_url'],
                        'description': row['description'],
                        'similarity': 85.0
                    })
                if len(recommendations) >= n_recommendations:
                    break
        
        if recommendations:
            return recommendations, f"✓ Found {len(recommendations)} {product_category} recommendations"
        else:
            return [], f"📭 No recommendations found"
            
    except Exception as e:
        return [], f"❌ Error: {str(e)}"

def get_trending_products(n=12):
    """Get top-rated trending products"""
    trending = df.nlargest(n, 'rating')
    products = []
    for _, row in trending.iterrows():
        products.append({
            'name': row[product_col],
            'category': row['category'],
            'price': f"${row['price']:.2f}",
            'rating': float(row['rating']),
            'image_url': row['image_url'],
            'description': row['description']
        })
    return products

def get_recommendations_by_category(category, n=6):
    """Get top products by category"""
    cat_products = df[df['category'] == category].nlargest(n, 'rating')
    products = []
    for _, row in cat_products.iterrows():
        products.append({
            'name': row[product_col],
            'category': row['category'],
            'price': f"${row['price']:.2f}",
            'rating': float(row['rating']),
            'image_url': row['image_url'],
            'description': row['description']
        })
    return products

def get_all_categories():
    return df['category'].unique().tolist()