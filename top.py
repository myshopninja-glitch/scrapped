import json
import time

def run_scraper():
    print("Initiating multi-platform product scan...")
    
    # Placeholder scraper logic for Amazon, TikTok Shop, AliExpress, Etsy
top_10 = [
        {"rank": 1, "name": "Wireless Headphones", "platform": "Amazon", "img_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500", "url": "https://amazon.com"},
        {"rank": 2, "name": "Sunset Lamp Projector", "platform": "TikTok Shop", "img_url": "https://images.unsplash.com/photo-1507499739999-097706ad8914?w=500", "url": "https://tiktok.com"},
        {"rank": 3, "name": "Mini Label Printer", "platform": "AliExpress", "img_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500", "url": "https://aliexpress.com"},
        {"rank": 4, "name": "Custom Embroidered Hoodie", "platform": "Etsy", "img_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500", "url": "https://etsy.com"},
        {"rank": 5, "name": "Smart Fitness Band", "platform": "Amazon", "img_url": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500", "url": "https://amazon.com"},
        {"rank": 6, "name": "Thermal Neck Massager", "platform": "TikTok Shop", "img_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=500", "url": "https://tiktok.com"},
        {"rank": 7, "name": "LED Ambient Light Bar", "platform": "AliExpress", "img_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500", "url": "https://aliexpress.com"},
        {"rank": 8, "name": "Personalized Leather Keychain", "platform": "Etsy", "img_url": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=500", "url": "https://etsy.com"},
        {"rank": 9, "name": "Stainless Steel Tumbler", "platform": "Amazon", "img_url": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?w=500", "url": "https://amazon.com"},
        {"rank": 10, "name": "Aesthetic Handmade Mug", "platform": "Etsy", "img_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500", "url": "https://etsy.com"},
    ]
    
    next_15 = [
        {
            "Place Number": i,
            "Product Name": f"Up-and-Coming Item #{i}",
            "Source Platform": ["Amazon", "TikTok Shop", "AliExpress", "Etsy"][i % 4],
            "Sales Volume": 2400 - (i * 75),
            "Item Link": f"https://example.com/product_{i}"
        }
        for i in range(11, 26)
    ]
    
    dataset = {
        "last_updated_epoch": time.time(),
        "top_10": top_10,
        "next_15": next_15
    }
    
    with open("data.json", "w") as f:
        json.dump(dataset, f, indent=4)
        
    print("Scrape complete. Data saved to data.json")

if __name__ == "__main__":
    run_scraper()
