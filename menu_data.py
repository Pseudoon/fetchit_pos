# Fetchit menu data.
# Items with a single price use {"label": "Regular", "price": X}.
# Items with half/full pricing use two variants.

MENU = [
    {
        "category": "Fast Food & Continental",
        "subcategory": "Appetizers",
        "items": [
            {"name": "French Fries", "variants": [{"label": "Regular", "price": 60}]},
            {"name": "Cheesy Easy", "variants": [{"label": "Regular", "price": 70}]},
            {"name": "Peri-Peri Fries", "variants": [{"label": "Regular", "price": 70}]},
        ],
    },
    {
        "category": "Fast Food & Continental",
        "subcategory": "Open Toast",
        "items": [
            {"name": "Garlic Toast", "variants": [{"label": "Regular", "price": 40}]},
            {"name": "Mozzarella Pesto Toast", "variants": [{"label": "Regular", "price": 50}]},
            {"name": "Paneer Tikka Toast", "variants": [{"label": "Regular", "price": 60}]},
        ],
    },
    {
        "category": "Fast Food & Continental",
        "subcategory": "Maggi",
        "items": [
            {"name": "Masala Maggi", "variants": [{"label": "Regular", "price": 50}]},
            {"name": "Peri-Peri Maggi", "variants": [{"label": "Regular", "price": 60}]},
            {"name": "Caramel Maggi", "variants": [{"label": "Regular", "price": 90}]},
            {"name": "Mac & Cheese Maggi", "variants": [{"label": "Regular", "price": 110}]},
        ],
    },
    {
        "category": "Fast Food & Continental",
        "subcategory": "Pasta",
        "items": [
            {"name": "Fusilli", "variants": [{"label": "Regular", "price": 60}]},
            {"name": "Cheesy Schezwan", "variants": [{"label": "Regular", "price": 90}]},
            {"name": "Maccheroni", "variants": [{"label": "Regular", "price": 90}]},
            {"name": "Lasagna", "variants": [{"label": "Regular", "price": 100}]},
            {"name": "Cheesy Paneer", "variants": [{"label": "Regular", "price": 110}]},
            {"name": "Spaghetti", "variants": [{"label": "Regular", "price": 140}]},
        ],
    },
    {
        "category": "Fast Food & Continental",
        "subcategory": "Panini",
        "items": [
            {"name": "Samosa Bun", "variants": [{"label": "Regular", "price": 40}]},
            {"name": "Korean Garlic Bun", "variants": [{"label": "Regular", "price": 50}]},
            {"name": "Korean Pizza Bun", "variants": [{"label": "Regular", "price": 60}]},
            {"name": "Garlic Bread", "variants": [{"label": "Regular", "price": 50}]},
        ],
    },
    {
        "category": "Fast Food & Continental",
        "subcategory": "Pizza (8-inch)",
        "items": [
            {"name": "Classic Delight", "variants": [{"label": "Regular", "price": 70}]},
            {"name": "Cheesy Corn", "variants": [{"label": "Regular", "price": 90}]},
            {"name": "Alfredo Pizza", "variants": [{"label": "Regular", "price": 120}]},
            {"name": "Cheese Burst", "variants": [{"label": "Regular", "price": 140}]},
            {"name": "Peppy Paneer", "variants": [{"label": "Regular", "price": 160}]},
            {"name": "Pasta Pizza", "variants": [{"label": "Regular", "price": 180}]},
        ],
    },
    {
        "category": "Fast Food & Continental",
        "subcategory": "Burger",
        "items": [
            {"name": "Hamburger", "variants": [{"label": "Regular", "price": 50}]},
            {"name": "Cheese Burger", "variants": [{"label": "Regular", "price": 60}]},
            {"name": "Cheesy Corn Burger", "variants": [{"label": "Regular", "price": 60}]},
            {"name": "Cheese Burst Burger", "variants": [{"label": "Regular", "price": 80}]},
            {"name": "Paneer Tikka Burger", "variants": [{"label": "Regular", "price": 90}]},
        ],
    },
    {
        "category": "Fast Food & Continental",
        "subcategory": "Samosas",
        "items": [
            {"name": "Small Samosa (4 pc)", "variants": [{"label": "Regular", "price": 25}]},
            {"name": "Big Samosa (2 pc)", "variants": [{"label": "Regular", "price": 25}]},
        ],
    },
    {
        "category": "Fast Food & Continental",
        "subcategory": "Sandwich",
        "items": [
            {"name": "Kartoffel Grill", "variants": [{"label": "Regular", "price": 40}]},
            {"name": "Gemüse Grill", "variants": [{"label": "Regular", "price": 50}]},
            {"name": "Mozzarella Pesto Grill", "variants": [{"label": "Regular", "price": 70}]},
            {"name": "Cheesy Wheel", "variants": [{"label": "Regular", "price": 120}]},
        ],
    },
    {
        "category": "Fast Food & Continental",
        "subcategory": "Beverage",
        "items": [
            {"name": "Cold Coffee", "variants": [{"label": "Regular", "price": 35}]},
        ],
    },
    {
        "category": "Chinese",
        "subcategory": "Manchurian",
        "items": [
            {"name": "Manchurian Dry", "variants": [{"label": "Half", "price": 100}, {"label": "Full", "price": 130}]},
            {"name": "Manchurian Gravy", "variants": [{"label": "Half", "price": 100}, {"label": "Full", "price": 130}]},
        ],
    },
    {
        "category": "Chinese",
        "subcategory": "Noodles",
        "items": [
            {"name": "Manchurian Noodles", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
            {"name": "Hakka Noodles", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
            {"name": "Schezwan Noodles", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
            {"name": "Singapuri Noodles", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
        ],
    },
    {
        "category": "Chinese",
        "subcategory": "Rice",
        "items": [
            {"name": "Manchurian Rice", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
            {"name": "Fry Rice", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
            {"name": "Schezwan Rice", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
            {"name": "Combination Rice", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
            {"name": "Singapuri Rice", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
        ],
    },
    {
        "category": "Chinese",
        "subcategory": "Bhel",
        "items": [
            {"name": "Chinese Bhel", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
            {"name": "Bombay Bhel", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
        ],
    },
    {
        "category": "Chinese",
        "subcategory": "Soup",
        "items": [
            {"name": "Manchurian Soup", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
            {"name": "Hot & Sour Soup", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
            {"name": "Manchau Soup", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 120}]},
        ],
    },
    {
        "category": "Chinese",
        "subcategory": "Rice — Special",
        "items": [
            {"name": "Triple Rice", "variants": [{"label": "Regular", "price": 230}]},
        ],
    },
    {
        "category": "South Indian",
        "subcategory": "Idly / Vada",
        "items": [
            {"name": "Idly", "variants": [{"label": "Regular", "price": 50}]},
            {"name": "Mendu Vada", "variants": [{"label": "Regular", "price": 60}]},
            {"name": "Idly Vada", "variants": [{"label": "Regular", "price": 60}]},
            {"name": "Dahi Vada", "variants": [{"label": "Regular", "price": 105}]},
            {"name": "Dahi Idly", "variants": [{"label": "Regular", "price": 95}]},
        ],
    },
    {
        "category": "South Indian",
        "subcategory": "Dosa",
        "items": [
            {"name": "Plain Dosa", "variants": [{"label": "Regular", "price": 80}]},
            {"name": "Butter Plain Dosa", "variants": [{"label": "Regular", "price": 100}]},
            {"name": "Masala Dosa", "variants": [{"label": "Regular", "price": 100}]},
            {"name": "Butter Masala Dosa", "variants": [{"label": "Regular", "price": 125}]},
            {"name": "Cheese Butter Masala Dosa", "variants": [{"label": "Regular", "price": 150}]},
            {"name": "Mysore Sada Dosa", "variants": [{"label": "Regular", "price": 100}]},
            {"name": "Mysore Masala Dosa", "variants": [{"label": "Regular", "price": 120}]},
            {"name": "Butter Mysore Masala Dosa", "variants": [{"label": "Regular", "price": 140}]},
            {"name": "Butter Mysore Cheese Dosa", "variants": [{"label": "Regular", "price": 160}]},
            {"name": "Rava Dosa", "variants": [{"label": "Regular", "price": 130}]},
            {"name": "Rava Butter Dosa", "variants": [{"label": "Regular", "price": 150}]},
            {"name": "Rava Butter Cheese Dosa", "variants": [{"label": "Regular", "price": 190}]},
            {"name": "Set Dosa", "variants": [{"label": "Regular", "price": 130}]},
            {"name": "Set Butter Dosa", "variants": [{"label": "Regular", "price": 150}]},
            {"name": "Set Butter Cheese Dosa", "variants": [{"label": "Regular", "price": 170}]},
        ],
    },
    {
        "category": "South Indian",
        "subcategory": "Uttapa",
        "items": [
            {"name": "Onion Uttapa", "variants": [{"label": "Regular", "price": 110}]},
            {"name": "Butter Onion Uttapa", "variants": [{"label": "Regular", "price": 130}]},
            {"name": "Butter Onion Cheese Uttapa", "variants": [{"label": "Regular", "price": 155}]},
            {"name": "Masala Uttapa", "variants": [{"label": "Regular", "price": 115}]},
            {"name": "Butter Masala Uttapa", "variants": [{"label": "Regular", "price": 135}]},
            {"name": "Cheese Butter Masala Uttapa", "variants": [{"label": "Regular", "price": 155}]},
            {"name": "Mix Veg Uttapa", "variants": [{"label": "Regular", "price": 130}]},
            {"name": "Butter Mix Veg Uttapa", "variants": [{"label": "Regular", "price": 150}]},
            {"name": "Cheese Butter Mix Veg Uttapa", "variants": [{"label": "Regular", "price": 170}]},
        ],
    },
    {
        "category": "South Indian",
        "subcategory": "Extras",
        "items": [
            {"name": "Extra Chutney", "variants": [{"label": "Regular", "price": 15}]},
            {"name": "Extra Sambhar", "variants": [{"label": "Regular", "price": 15}]},
        ],
    },
    {
        "category": "Punjabi & Roti",
        "subcategory": "Paneer",
        "items": [
            {"name": "Paneer Tikka", "variants": [{"label": "Regular", "price": 170}]},
            {"name": "Paneer Mattar", "variants": [{"label": "Regular", "price": 170}]},
            {"name": "Paneer Masala", "variants": [{"label": "Regular", "price": 170}]},
            {"name": "Paneer Angara", "variants": [{"label": "Regular", "price": 250}]},
            {"name": "Kaju Paneer", "variants": [{"label": "Regular", "price": 230}]},
        ],
    },
    {
        "category": "Punjabi & Roti",
        "subcategory": "Dal / Sabzi",
        "items": [
            {"name": "Chana Masala", "variants": [{"label": "Regular", "price": 130}]},
            {"name": "Aloo Mattar", "variants": [{"label": "Regular", "price": 110}]},
            {"name": "Sev Tamatar", "variants": [{"label": "Regular", "price": 100}]},
            {"name": "Dal Tadka", "variants": [{"label": "Regular", "price": 110}]},
            {"name": "Kaju Kadhai", "variants": [{"label": "Regular", "price": 230}]},
            {"name": "Mix Veg", "variants": [{"label": "Regular", "price": 150}]},
        ],
    },
    {
        "category": "Punjabi & Roti",
        "subcategory": "Rice / Biryani",
        "items": [
            {"name": "Dal Rice", "variants": [{"label": "Regular", "price": 100}]},
            {"name": "Veg Pulav", "variants": [{"label": "Regular", "price": 140}]},
            {"name": "Veg Biryani", "variants": [{"label": "Regular", "price": 150}]},
            {"name": "Veg Kolhapuri", "variants": [{"label": "Regular", "price": 170}]},
        ],
    },
    {
        "category": "Punjabi & Roti",
        "subcategory": "Roti",
        "items": [
            {"name": "Chapati", "variants": [{"label": "Regular", "price": 10}]},
            {"name": "Butter Chapati", "variants": [{"label": "Regular", "price": 15}]},
        ],
    },
    {
        "category": "Momos",
        "subcategory": "Fried Momos",
        "items": [
            {"name": "Veg Fried Momos (6pc / 12pc)", "variants": [{"label": "Half", "price": 60}, {"label": "Full", "price": 100}]},
            {"name": "Paneer Fried Momos (5pc / 10pc)", "variants": [{"label": "Half", "price": 80}, {"label": "Full", "price": 120}]},
            {"name": "Cheese Fried Momos (5pc / 10pc)", "variants": [{"label": "Half", "price": 90}, {"label": "Full", "price": 130}]},
            {"name": "Paneer Cheese Fried Momos (5pc / 10pc)", "variants": [{"label": "Half", "price": 100}, {"label": "Full", "price": 160}]},
            {"name": "Cheese Corn Fried Momos (5pc / 10pc)", "variants": [{"label": "Half", "price": 100}, {"label": "Full", "price": 150}]},
        ],
    },
    {
        "category": "Momos",
        "subcategory": "Steamed Momos",
        "items": [
            {"name": "Veg Steamed Momos (6pc / 12pc)", "variants": [{"label": "Half", "price": 60}, {"label": "Full", "price": 100}]},
            {"name": "Paneer Steamed Momos (5pc / 10pc)", "variants": [{"label": "Half", "price": 80}, {"label": "Full", "price": 120}]},
        ],
    },
]

DELIVERY_CHARGE = 20.0
DELIVERY_SLOTS = ["7:00 PM – 8:00 PM", "10:00 PM – 11:00 PM"]