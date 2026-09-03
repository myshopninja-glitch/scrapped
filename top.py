import json
import time

def run_scraper():
    print("Initiating multi-platform product scan...")
    
    # Placeholder scraper logic for Amazon, TikTok Shop, AliExpress, Etsy
    top_10 = [
        {"rank": 1, "name": "Wireless Headphones", "platform": "Amazon", "img_url": "https://via.placeholder.com/300x300?text=Rank+1", "url": "https://amazon.com"},
        {"rank": 2, "name": "Sunset Lamp Projector", "platform": "TikTok Shop", "img_url": "https://via.placeholder.com/150x150?text=Rank+2", "url": "https://tiktok.com"},
        {"rank": 3, "name": "Mini Label Printer", "platform": "AliExpress", "img_url": "https://via.placeholder.com/150x150?text=Rank+3", "url": "https://aliexpress.com"},
        {"rank": 4, "name": "Custom Embroidered Hoodie", "platform": "Etsy", "img_url": "https://via.placeholder.com/150x150?text=Rank+4", "url": "https://etsy.com"},
        {"rank": 5, "name": "Smart Fitness Band", "platform": "Amazon", "img_url": "https://via.placeholder.com/150x150?text=Rank+5", "url": "https://amazon.com"},
        {"rank": 6, "name": "Thermal Neck Massager", "platform": "TikTok Shop", "img_url": "https://via.placeholder.com/150x150?text=Rank+6", "url": "https://tiktok.com"},
        {"rank": 7, "name": "LED Ambient Light Bar", "platform": "AliExpress", "img_url": "https://via.placeholder.com/150x150?text=Rank+7", "url": "https://aliexpress.com"},
        {"rank": 8, "name": "Personalized Leather Keychain", "platform": "Etsy", "img_url": "https://via.placeholder.com/150x150?text=Rank+8", "url": "https://etsy.com"},
        {"rank": 9, "name": "Stainless Steel Tumbler", "platform": "Amazon", "img_url": "https://via.placeholder.com/150x150?text=Rank+9", "url": "https://amazon.com"},
        {"rank": 10, "name": "Aesthetic Handmade Mug", "platform": "Etsy", "img_url": "https://via.placeholder.com/150x150?text=Rank+10", "url": "https://etsy.com"},
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