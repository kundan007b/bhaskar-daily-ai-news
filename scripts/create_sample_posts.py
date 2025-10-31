#!/usr/bin/env python3
"""
Create sample posts to populate the website immediately
"""
import datetime
from pathlib import Path
from PIL import Image
import hashlib

# Setup paths
REPO = Path(__file__).resolve().parents[1]
POSTS = REPO / "_posts"
IMGDIR = REPO / "assets" / "images"
POSTS.mkdir(exist_ok=True)
IMGDIR.mkdir(parents=True, exist_ok=True)

# Sample posts data
SAMPLE_POSTS = [
    {
        "category": "Technology",
        "title_en": "India's AI Revolution: Tech Giants Invest Billions in Indian Startups",
        "title_hi": "भारत की एआई क्रांति: तकनीकी दिग्गज भारतीय स्टार्टअप में अरबों का निवेश",
        "excerpt_en": "Major technology companies announce significant investments in India's artificial intelligence sector, marking a new era of technological advancement.",
        "excerpt_hi": "प्रमुख प्रौद्योगिकी कंपनियों ने भारत के कृत्रिम बुद्धिमत्ता क्षेत्र में महत्वपूर्ण निवेश की घोषणा की।",
        "content_en": "In a major boost to India's technology sector, leading global tech companies have announced investments worth over $5 billion in Indian AI startups. This move is expected to create thousands of jobs and position India as a global AI hub.\n\nThe investments will focus on developing AI solutions for healthcare, agriculture, and education sectors. Industry experts believe this could transform India's digital economy and accelerate innovation across multiple sectors.\n\nKey highlights include partnerships with top Indian institutes and the establishment of research centers in major cities.",
        "content_hi": "भारत के प्रौद्योगिकी क्षेत्र को बड़ा बढ़ावा देते हुए, प्रमुख वैश्विक तकनीकी कंपनियों ने भारतीय एआई स्टार्टअप में 5 बिलियन डॉलर से अधिक के निवेश की घोषणा की है। इस कदम से हजारों रोजगार सृजित होने और भारत को वैश्विक एआई केंद्र के रूप में स्थापित करने की उम्मीद है।\n\nनिवेश स्वास्थ्य सेवा, कृषि और शिक्षा क्षेत्रों के लिए एआई समाधान विकसित करने पर केंद्रित होगा। उद्योग विशेषज्ञों का मानना है कि यह भारत की डिजिटल अर्थव्यवस्था को बदल सकता है।",
        "color": "#4285f4"
    },
    {
        "category": "Business",
        "title_en": "Indian Stock Markets Hit All-Time High on Strong Economic Data",
        "title_hi": "मजबूत आर्थिक आंकड़ों पर भारतीय शेयर बाजार सर्वकालिक उच्च स्तर पर",
        "excerpt_en": "India's benchmark indices reach record levels as GDP growth exceeds expectations and foreign investments surge.",
        "excerpt_hi": "जीडीपी वृद्धि उम्मीदों से अधिक होने और विदेशी निवेश बढ़ने से भारत के बेंचमार्क सूचकांक रिकॉर्ड स्तर पर पहुंचे।",
        "content_en": "The Indian stock market witnessed a historic milestone today as both BSE Sensex and NSE Nifty touched new all-time highs. The rally was driven by robust GDP growth numbers and increased foreign institutional investments.\n\nAnalysts attribute this surge to strong corporate earnings, favorable government policies, and positive global sentiment. The manufacturing and technology sectors led the gains, with several stocks hitting upper circuits.\n\nMarket experts remain optimistic about continued growth, citing India's strong fundamentals and reform initiatives.",
        "content_hi": "भारतीय शेयर बाजार ने आज एक ऐतिहासिक मील का पत्थर देखा क्योंकि बीएसई सेंसेक्स और एनएसई निफ्टी दोनों ने नए सर्वकालिक उच्च स्तर को छुआ। यह तेजी मजबूत जीडीपी वृद्धि संख्या और विदेशी संस्थागत निवेश में वृद्धि से प्रेरित थी।\n\nविश्लेषक इस उछाल का श्रेय मजबूत कॉर्पोरेट आय, अनुकूल सरकारी नीतियों और सकारात्मक वैश्विक भावना को देते हैं।",
        "color": "#34a853"
    },
    {
        "category": "Politics",
        "title_en": "Government Launches Digital India 2.0 Initiative for Rural Development",
        "title_hi": "सरकार ने ग्रामीण विकास के लिए डिजिटल इंडिया 2.0 पहल शुरू की",
        "excerpt_en": "New initiative aims to bring high-speed internet and digital services to every village across India by 2026.",
        "excerpt_hi": "नई पहल का उद्देश्य 2026 तक भारत के प्रत्येक गांव में हाई-स्पीड इंटरनेट और डिजिटल सेवाएं पहुंचाना है।",
        "content_en": "The Indian government today unveiled Digital India 2.0, an ambitious program to extend high-speed internet connectivity and digital services to rural areas. The initiative includes investment in fiber optic networks, digital literacy programs, and e-governance platforms.\n\nPrime Minister emphasized the importance of bridging the digital divide and ensuring inclusive growth. The program will also focus on digital healthcare, online education, and farmer support systems.\n\nThe initiative is expected to benefit over 600 million rural citizens and create numerous employment opportunities in the technology sector.",
        "content_hi": "भारत सरकार ने आज डिजिटल इंडिया 2.0 का अनावरण किया, जो ग्रामीण क्षेत्रों में हाई-स्पीड इंटरनेट कनेक्टिविटी और डिजिटल सेवाओं को विस्तारित करने का एक महत्वाकांक्षी कार्यक्रम है।\n\nप्रधानमंत्री ने डिजिटल विभाजन को पाटने और समावेशी विकास सुनिश्चित करने के महत्व पर जोर दिया। यह पहल 600 मिलियन से अधिक ग्रामीण नागरिकों को लाभान्वित करने की उम्मीद है।",
        "color": "#ea4335"
    },
    {
        "category": "Finance",
        "title_en": "RBI Announces New Measures to Boost Digital Payments and Financial Inclusion",
        "title_hi": "आरबीआई ने डिजिटल भुगतान और वित्तीय समावेशन को बढ़ावा देने के लिए नए उपाय घोषित किए",
        "excerpt_en": "Reserve Bank introduces reforms to strengthen digital payment infrastructure and expand banking access to underserved areas.",
        "excerpt_hi": "रिजर्व बैंक ने डिजिटल भुगतान बुनियादी ढांचे को मजबूत करने के लिए सुधार पेश किए।",
        "content_en": "The Reserve Bank of India has introduced a comprehensive set of measures aimed at enhancing digital payment systems and promoting financial inclusion. The new guidelines focus on improving UPI infrastructure, reducing transaction costs, and expanding banking services to remote areas.\n\nKey announcements include simplified KYC norms for small accounts, incentives for digital transactions, and support for fintech innovations. The RBI also outlined plans to strengthen cybersecurity frameworks.\n\nThese measures are expected to accelerate India's transition to a cashless economy and bring millions of unbanked citizens into the formal financial system.",
        "content_hi": "भारतीय रिजर्व बैंक ने डिजिटल भुगतान प्रणाली को बढ़ाने और वित्तीय समावेशन को बढ़ावा देने के उद्देश्य से व्यापक उपायों की शृंखला पेश की है।\n\nप्रमुख घोषणाओं में छोटे खातों के लिए सरलीकृत केवाईसी मानदंड, डिजिटल लेनदेन के लिए प्रोत्साहन शामिल हैं। ये उपाय भारत के नकदी रहित अर्थव्यवस्था में परिवर्तन को तेज करने की उम्मीद है।",
        "color": "#fbbc04"
    },
    {
        "category": "Startups",
        "title_en": "Indian Startup Ecosystem Sees Record Funding Despite Global Slowdown",
        "title_hi": "वैश्विक मंदी के बावजूद भारतीय स्टार्टअप पारिस्थितिकी तंत्र में रिकॉर्ड फंडिंग",
        "excerpt_en": "Indian startups raise $12 billion in Q3 2025, defying global trends with strong investor confidence.",
        "excerpt_hi": "भारतीय स्टार्टअप ने 2025 की तीसरी तिमाही में 12 बिलियन डॉलर जुटाए, मजबूत निवेशक विश्वास के साथ वैश्विक रुझानों को चुनौती दी।",
        "content_en": "Despite global economic uncertainties, India's startup ecosystem has demonstrated remarkable resilience with record-breaking funding in the third quarter of 2025. Investors continue to show strong confidence in Indian entrepreneurs and innovation.\n\nThe funding was led by technology, fintech, and e-commerce sectors. Several startups achieved unicorn status, bringing India's total unicorn count to over 150. Tier 2 and Tier 3 cities are emerging as new startup hubs.\n\nExperts attribute this success to India's large market, digital adoption, and government support through initiatives like Startup India.",
        "content_hi": "वैश्विक आर्थिक अनिश्चितताओं के बावजूद, भारत के स्टार्टअप पारिस्थितिकी तंत्र ने 2025 की तीसरी तिमाही में रिकॉर्ड तोड़ फंडिंग के साथ उल्लेखनीय लचीलापन प्रदर्शित किया है।\n\nफंडिंग का नेतृत्व प्रौद्योगिकी, फिनटेक और ई-कॉमर्स क्षेत्रों ने किया। विशेषज्ञ इस सफलता का श्रेय भारत के बड़े बाजार, डिजिटल अपनाने को देते हैं।",
        "color": "#9334e6"
    }
]

def create_placeholder_image(color, category, filename):
    """Create a simple placeholder image"""
    img = Image.new('RGB', (1200, 630), color=color)
    filepath = IMGDIR / filename
    img.save(filepath, "JPEG", quality=85)
    return f"/assets/images/{filename}"

def create_post(post_data, date_offset=0):
    """Create a blog post file"""
    # Generate date
    post_date = datetime.datetime.now() - datetime.timedelta(hours=date_offset)
    date_str = post_date.strftime("%Y-%m-%d")
    time_str = post_date.strftime("%H:%M:%S +0530")
    
    # Create image
    img_filename = hashlib.md5(post_data['title_en'].encode()).hexdigest()[:10] + ".jpg"
    img_path = create_placeholder_image(post_data['color'], post_data['category'], img_filename)
    
    # Create post filename
    slug = post_data['title_en'].lower()[:50].replace(' ', '-').replace(':', '').replace(',', '')
    filename = f"{date_str}-{slug}.md"
    
    # Create post content
    content = f"""---
layout: post
title: "{post_data['title_en']}"
title_hi: "{post_data['title_hi']}"
date: {date_str} {time_str}
categories: [{post_data['category']}]
author: "AI News Team"
excerpt: "{post_data['excerpt_en']}"
excerpt_hi: "{post_data['excerpt_hi']}"
image: {img_path}
lang: "en"
---

## {post_data['title_en']}

{post_data['content_en']}

---

## {post_data['title_hi']}

{post_data['content_hi']}

---

*This is a sample news article. Automated news generation will begin shortly.*
"""
    
    # Write file
    filepath = POSTS / filename
    filepath.write_text(content)
    print(f"✅ Created: {filename}")

def main():
    print("📰 Creating sample posts to populate the website...\n")
    
    for i, post in enumerate(SAMPLE_POSTS):
        create_post(post, date_offset=i)
    
    print(f"\n🎉 Successfully created {len(SAMPLE_POSTS)} sample posts!")
    print(f"📁 Posts directory: {POSTS}")
    print(f"🖼️  Images directory: {IMGDIR}")

if __name__ == "__main__":
    main()
