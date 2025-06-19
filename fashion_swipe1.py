
import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Konfiguration der Streamlit-Seite
st.set_page_config(
    page_title="Fashion Swipe",
    page_icon="👗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS für besseres Styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF6B9D;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .fashion-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        margin: 20px 0;
    }
    
    .item-name {
        font-size: 1.8rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .item-brand {
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 0.5rem;
    }
    
    .item-price {
        font-size: 1.5rem;
        font-weight: bold;
        color: #FF6B9D;
        margin-bottom: 1rem;
    }
    
    .category-tag {
        background: linear-gradient(45deg, #FF6B9D, #4ECDC4);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
    }
    
    .stat-item {
        display: inline-block;
        margin: 0 20px;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        display: block;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .progress-bar {
        background: #f0f0f0;
        border-radius: 10px;
        height: 8px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(45deg, #FF6B9D, #4ECDC4);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Fashion Items Datenbank
@st.cache_data
def load_fashion_items():
    items = [
        {
            "id": 1,
            "name": "Oversized Denim Jacke",
            "brand": "Urban Style",
            "price": "89€",
            "category": "Jacken",
            "description": "Lässige Denim-Jacke im angesagten Oversized-Look",
            "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=600&fit=crop"
        },
        {
            "id": 2,
            "name": "Vintage Sneakers",
            "brand": "RetroKicks",
            "price": "120€",
            "category": "Schuhe",
            "description": "Stylische Vintage-Sneakers für den urbanen Look",
            "image_url": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=600&fit=crop"
        },
        {
            "id": 3,
            "name": "Minimalistisches Kleid",
            "brand": "Elegant Co.",
            "price": "65€",
            "category": "Kleider",
            "description": "Elegantes weißes Kleid für jeden Anlass",
            "image_url": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=600&fit=crop"
        },
        {
            "id": 4,
            "name": "Leder Ankle Boots",
            "brand": "BootCraft",
            "price": "150€",
            "category": "Schuhe",
            "description": "Hochwertige Leder-Stiefeletten in Schwarz",
            "image_url": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=400&h=600&fit=crop"
        },
        {
            "id": 5,
            "name": "Kuschel-Strickpullover",
            "brand": "WarmWear",
            "price": "75€",
            "category": "Pullover",
            "description": "Warmer und weicher Strickpullover für kalte Tage",
            "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=600&fit=crop"
        },
        {
            "id": 6,
            "name": "High-Waist Jeans",
            "brand": "DenimLove",
            "price": "95€",
            "category": "Hosen",
            "description": "Klassische High-Waist Jeans in perfekter Passform",
            "image_url": "https://images.unsplash.com/photo-1582418702059-97ebafb35d09?w=400&h=600&fit=crop"
        },
        {
            "id": 7,
            "name": "Seide Bluse",
            "brand": "LuxeFashion",
            "price": "110€",
            "category": "Blusen",
            "description": "Luxuriöse Seidenbluse für Business und Freizeit",
            "image_url": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=600&fit=crop"
        },
        {
            "id": 8,
            "name": "Canvas Shopper",
            "brand": "EcoStyle",
            "price": "35€",
            "category": "Taschen",
            "description": "Nachhaltige Canvas-Tasche für den Alltag",
            "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=600&fit=crop"
        },
        {
            "id": 9,
            "name": "Blazer Classic",
            "brand": "BusinessWear",
            "price": "135€",
            "category": "Blazer",
            "description": "Zeitloser Blazer für den professionellen Look",
            "image_url": "https://images.unsplash.com/photo-1591369822096-ffd140ec948d?w=400&h=600&fit=crop"
        },
        {
            "id": 10,
            "name": "Sommersandalen",
            "brand": "BeachVibes",
            "price": "55€",
            "category": "Schuhe",
            "description": "Bequeme Sandalen für heiße Sommertage",
            "image_url": "https://images.unsplash.com/photo-1603808033192-082d6919d3e1?w=400&h=600&fit=crop"
        }
    ]
    return items

# Session State initialisieren
def init_session_state():
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'liked_items' not in st.session_state:
        st.session_state.liked_items = []
    if 'disliked_items' not in st.session_state:
        st.session_state.disliked_items = []
    if 'items_shuffled' not in st.session_state:
        items = load_fashion_items()
        random.shuffle(items)
        st.session_state.items_shuffled = items
    if 'session_started' not in st.session_state:
        st.session_state.session_started = datetime.now()

def like_item():
    items = st.session_state.items_shuffled
    if st.session_state.current_index < len(items):
        current_item = items[st.session_state.current_index]
        st.session_state.liked_items.append(current_item)
        st.session_state.current_index += 1

def dislike_item():
    items = st.session_state.items_shuffled
    if st.session_state.current_index < len(items):
        current_item = items[st.session_state.current_index]
        st.session_state.disliked_items.append(current_item)
        st.session_state.current_index += 1

def reset_session():
    st.session_state.current_index = 0
    st.session_state.liked_items = []
    st.session_state.disliked_items = []
    items = load_fashion_items()
    random.shuffle(items)
    st.session_state.items_shuffled = items
    st.session_state.session_started = datetime.now()

def main():
    init_session_state()
    
    # Header
    st.markdown('<div class="main-header">👗 Fashion Swipe</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Entdecke deinen Style - Swipe dich durch die neuesten Trends!</div>', unsafe_allow_html=True)
    
    items = st.session_state.items_shuffled
    current_idx = st.session_state.current_index
    total_items = len(items)
    
    # Progress Bar
    progress = current_idx / total_items if total_items > 0 else 0
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress * 100}%"></div>
    </div>
    <p style="text-align: center; color: #666;">
        {current_idx} von {total_items} Artikeln angeschaut
    </p>
    """, unsafe_allow_html=True)
    
    # Statistiken
    liked_count = len(st.session_state.liked_items)
    disliked_count = len(st.session_state.disliked_items)
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-item">
            <span class="stat-number">❤️ {liked_count}</span>
            <span class="stat-label">Gefällt mir</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">👎 {disliked_count}</span>
            <span class="stat-label">Nicht interessiert</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hauptinhalt
    if current_idx >= total_items:
        # Session beendet
        st.markdown("## 🎉 Session beendet!")
        st.success(f"Du hast alle {total_items} Artikel durchgesehen!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ❤️ Deine Favoriten")
            if st.session_state.liked_items:
                for item in st.session_state.liked_items:
                    st.markdown(f"**{item['name']}** - {item['price']}")
            else:
                st.info("Keine Favoriten ausgewählt")
        
        with col2:
            st.markdown("### 👎 Nicht interessant")
            if st.session_state.disliked_items:
                for item in st.session_state.disliked_items:
                    st.markdown(f"**{item['name']}** - {item['price']}")
            else:
                st.info("Alle Artikel haben dir gefallen!")
        
        # Reset Button
        if st.button("🔄 Neue Session starten", type="primary", use_container_width=True):
            reset_session()
            st.rerun()
            
    else:
        # Aktueller Artikel
        current_item = items[current_idx]
        
        # Artikel anzeigen
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            st.markdown(f"""
            <div class="fashion-card">
                <div class="category-tag">{current_item['category']}</div>
                <div class="item-name">{current_item['name']}</div>
                <div class="item-brand">{current_item['brand']}</div>
                <div class="item-price">{current_item['price']}</div>
                <p style="color: #666; line-height: 1.6;">{current_item['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Bild anzeigen
            try:
                st.image(current_item['image_url'], use_container_width=True, caption=f"{current_item['name']} von {current_item['brand']}")
            except:
                st.info("🖼️ Bild wird geladen...")
        
        # Action Buttons
        st.markdown("---")
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])
        
        with col2:
            if st.button("👎 Nicht interessiert", type="secondary", use_container_width=True):
                dislike_item()
                st.rerun()
        
        with col4:
            if st.button("❤️ Gefällt mir!", type="primary", use_container_width=True):
                like_item()
                st.rerun()
        
        # Keyboard Shortcuts Info
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #888; font-size: 0.9rem;">
            💡 <strong>Tipp:</strong> Nutze die Buttons um durch die Artikel zu swipen!<br>
            ❤️ für Artikel die dir gefallen | 👎 für Artikel die dich nicht interessieren
        </div>
        """, unsafe_allow_html=True)

def main():
    init_session_state()
    
    # Header
    st.markdown('<div class="main-header">👗 Fashion Swipe</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Entdecke deinen Style - Swipe dich durch die neuesten Trends!</div>', unsafe_allow_html=True)
    
    items = st.session_state.items_shuffled
    current_idx = st.session_state.current_index
    total_items = len(items)
    
    # Progress Bar
    progress = current_idx / total_items if total_items > 0 else 0
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress * 100}%"></div>
    </div>
    <p style="text-align: center; color: #666;">
        {current_idx} von {total_items} Artikeln angeschaut
    </p>
    """, unsafe_allow_html=True)
    
    # Statistiken
    liked_count = len(st.session_state.liked_items)
    disliked_count = len(st.session_state.disliked_items)
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-item">
            <span class="stat-number">❤️ {liked_count}</span>
            <span class="stat-label">Gefällt mir</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">👎 {disliked_count}</span>
            <span class="stat-label">Nicht interessiert</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hauptinhalt
    if current_idx >= total_items:
        # Session beendet
        st.markdown("## 🎉 Session beendet!")
        st.success(f"Du hast alle {total_items} Artikel durchgesehen!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ❤️ Deine Favoriten")
            if st.session_state.liked_items:
                for item in st.session_state.liked_items:
                    st.markdown(f"**{item['name']}** - {item['price']}")
            else:
                st.info("Keine Favoriten ausgewählt")
        
        with col2:
            st.markdown("### 👎 Nicht interessant")
            if st.session_state.disliked_items:
                for item in st.session_state.disliked_items:
                    st.markdown(f"**{item['name']}** - {item['price']}")
            else:
                st.info("Alle Artikel haben dir gefallen!")
        
        # Reset Button
        if st.button("🔄 Neue Session starten", type="primary", use_container_width=True):
            reset_session()
            st.rerun()
            
    else:
        # Aktueller Artikel
        current_item = items[current_idx]
        
        # Artikel anzeigen
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            st.markdown(f"""
            <div class="fashion-card">
                <div class="category-tag">{current_item['category']}</div>
                <div class="item-name">{current_item['name']}</div>
                <div class="item-brand">{current_item['brand']}</div>
                <div class="item-price">{current_item['price']}</div>
                <p style="color: #666; line-height: 1.6;">{current_item['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Bild anzeigen
            try:
                st.image(current_item['image_url'], use_container_width=True, caption=f"{current_item['name']} von {current_item['brand']}")
            except:
                st.info("🖼️ Bild wird geladen...")
        
        # Action Buttons
        st.markdown("---")
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])
        
        with col2:
            if st.button("👎 Nicht interessiert", type="secondary", use_container_width=True):
                dislike_item()
                st.rerun()
        
        with col4:
            if st.button("❤️ Gefällt mir!", type="primary", use_container_width=True):
                like_item()
                st.rerun()
        
        # Keyboard Shortcuts Info
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #888; font-size: 0.9rem;">
            💡 <strong>Tipp:</strong> Nutze die Buttons um durch die Artikel zu swipen!<br>
            ❤️ für Artikel die dir gefallen | 👎 für Artikel die dich nicht interessieren
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar für zusätzliche Features
    with st.sidebar:
        st.markdown("## ⚙️ Einstellungen")
        
        if st.button("🔄 Session zurücksetzen"):
            reset_session()
            st.rerun()
        
        st.markdown("---")
        st.markdown("## 📊 Statistiken")
        
        if 'session_started' in st.session_state:
            time_elapsed = datetime.now() - st.session_state.session_started
            st.metric("⏱️ Zeit", f"{time_elapsed.seconds // 60}min {time_elapsed.seconds % 60}s")
        
        st.metric("🎯 Gesamt bewertet", st.session_state.current_index)
        st.metric("❤️ Likes", len(st.session_state.liked_items))
        st.metric("👎 Dislikes", len(st.session_state.disliked_items))
        
        if st.session_state.current_index > 0:
            like_rate = (len(st.session_state.liked_items) / st.session_state.current_index) * 100
            st.metric("📈 Like-Rate", f"{like_rate:.1f}%")

if __name__ == "__main__":
    main()