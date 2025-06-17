import streamlit as st
import pandas as pd
import random
from datetime import datetime
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64

# Konfiguration der Streamlit-Seite
st.set_page_config(
    page_title="Fashion Swipe",
    page_icon="👗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS für besseres Styling + Swipe Funktionalität
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
        transition: transform 0.3s ease, opacity 0.3s ease;
        position: relative;
        cursor: grab;
        user-select: none;
        touch-action: pan-x;
    }
    
    .fashion-card:active {
        cursor: grabbing;
    }
    
    .fashion-card.dragging {
        transition: none;
    }
    
    .fashion-card.swipe-left {
        transform: translateX(-100px) rotate(-10deg);
        opacity: 0.5;
    }
    
    .fashion-card.swipe-right {
        transform: translateX(100px) rotate(10deg);
        opacity: 0.5;
    }
    
    .swipe-indicator {
        position: absolute;
        top: 20px;
        font-size: 3rem;
        font-weight: bold;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 10;
        pointer-events: none;
    }
    
    .swipe-indicator.left {
        left: 20px;
        color: #ff4757;
    }
    
    .swipe-indicator.right {
        right: 20px;
        color: #2ed573;
    }
    
    .fashion-card.show-left .swipe-indicator.left {
        opacity: 1;
    }
    
    .fashion-card.show-right .swipe-indicator.right {
        opacity: 1;
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
    
    .swipe-instructions {
        background: linear-gradient(45deg, #FF6B9D, #4ECDC4);
        color: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        font-size: 1rem;
    }
    
    .swipe-arrows {
        font-size: 1.5rem;
        margin: 10px 0;
    }
    
    .fashion-image {
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        background: white;
        padding: 10px;
        pointer-events: none;
    }
    
    .fashion-image img {
        pointer-events: none;
    }
    
    .hidden-buttons {
        opacity: 0;
        height: 0;
        overflow: hidden;
        position: absolute;
        top: -1000px;
    }
</style>
""", unsafe_allow_html=True)

# Fashion-MNIST Klassen
FASHION_CLASSES = {
    0: "T-Shirt/Top",
    1: "Hose", 
    2: "Pullover",
    3: "Kleid",
    4: "Mantel",
    5: "Sandalen",
    6: "Hemd",
    7: "Sneaker",
    8: "Tasche",
    9: "Stiefeletten"
}

# Fashion-MNIST Daten laden
@st.cache_data
def load_fashion_mnist():
    try:
        # Fashion-MNIST laden
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
        
        # Alle Daten zusammenführen
        x_all = np.concatenate([x_train, x_test])
        y_all = np.concatenate([y_train, y_test])
        
        return x_all, y_all
    except Exception as e:
        st.error(f"Fehler beim Laden von Fashion-MNIST: {e}")
        return None, None

# Bild zu Base64 konvertieren
def image_to_base64(image_array):
    # Normalisieren und zu PIL Image konvertieren
    image = Image.fromarray(image_array.astype(np.uint8))
    
    # Bild vergrößern für bessere Darstellung
    image = image.resize((280, 280), Image.NEAREST)
    
    # Zu Base64 konvertieren
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

# 10 zufällige Fashion Items auswählen
@st.cache_data
def select_random_fashion_items():
    x_all, y_all = load_fashion_mnist()
    
    if x_all is None:
        return []
    
    # 10 zufällige Indizes auswählen
    random_indices = random.sample(range(len(x_all)), 10)
    
    items = []
    for i, idx in enumerate(random_indices):
        image = x_all[idx]
        label = y_all[idx]
        category = FASHION_CLASSES[label]
        
        # Zufällige Preise und Marken generieren
        brands = ["StyleCo", "FashionHub", "TrendWear", "UrbanStyle", "ClassicMode", 
                 "ModernLook", "ChicWear", "ElegantStyle", "CasualFit", "PremiumWear"]
        prices = ["25€", "35€", "45€", "55€", "65€", "75€", "85€", "95€", "105€", "115€"]
        
        item = {
            "id": i + 1,
            "name": f"{category} #{idx}",
            "brand": random.choice(brands),
            "price": random.choice(prices),
            "category": category,
            "description": f"Stilvolle {category.lower()} aus der Fashion-MNIST Kollektion",
            "image_data": image_to_base64(image),
            "original_index": idx
        }
        items.append(item)
    
    return items

# Session State initialisieren
def init_session_state():
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'liked_items' not in st.session_state:
        st.session_state.liked_items = []
    if 'disliked_items' not in st.session_state:
        st.session_state.disliked_items = []
    if 'fashion_items' not in st.session_state:
        with st.spinner("Lade Fashion-MNIST Datensatz..."):
            st.session_state.fashion_items = select_random_fashion_items()
    if 'session_started' not in st.session_state:
        st.session_state.session_started = datetime.now()

def like_item():
    items = st.session_state.fashion_items
    if st.session_state.current_index < len(items):
        current_item = items[st.session_state.current_index]
        st.session_state.liked_items.append(current_item)
        st.session_state.current_index += 1

def dislike_item():
    items = st.session_state.fashion_items
    if st.session_state.current_index < len(items):
        current_item = items[st.session_state.current_index]
        st.session_state.disliked_items.append(current_item)
        st.session_state.current_index += 1

def reset_session():
    st.session_state.current_index = 0
    st.session_state.liked_items = []
    st.session_state.disliked_items = []
    with st.spinner("Lade neue Fashion-MNIST Bilder..."):
        st.session_state.fashion_items = select_random_fashion_items()
    st.session_state.session_started = datetime.now()

def main():
    init_session_state()
    
    # Header
    st.markdown('<div class="main-header">👗 Fashion Swipe</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Entdecke deinen Style mit Fashion-MNIST Datensatz!</div>', unsafe_allow_html=True)
    
    items = st.session_state.fashion_items
    current_idx = st.session_state.current_index
    total_items = len(items)
    
    if not items:
        st.error("Fehler beim Laden der Fashion-MNIST Daten. Bitte installieren Sie TensorFlow: `pip install tensorflow`")
        return
    
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
        st.success(f"Du hast alle {total_items} Fashion-MNIST Artikel durchgesehen!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ❤️ Deine Favoriten")
            if st.session_state.liked_items:
                for item in st.session_state.liked_items:
                    st.markdown(f"**{item['name']}** ({item['category']}) - {item['price']}")
            else:
                st.info("Keine Favoriten ausgewählt")
        
        with col2:
            st.markdown("### 👎 Nicht interessant")
            if st.session_state.disliked_items:
                for item in st.session_state.disliked_items:
                    st.markdown(f"**{item['name']}** ({item['category']}) - {item['price']}")
            else:
                st.info("Alle Artikel haben dir gefallen!")
        
        # Kategorie-Analyse
        if st.session_state.liked_items:
            st.markdown("### 📊 Deine Lieblingskategorien")
            liked_categories = [item['category'] for item in st.session_state.liked_items]
            category_counts = pd.Series(liked_categories).value_counts()
            
            for category, count in category_counts.items():
                st.markdown(f"**{category}**: {count} mal geliked")
        
        # Reset Button
        if st.button("🔄 Neue Session starten", type="primary", use_container_width=True):
            reset_session()
            st.rerun()
            
    else:
        # Swipe Instructions
        st.markdown("""
        <div class="swipe-instructions">
            <div class="swipe-arrows">← 👎 Swipe zum Bewerten 👍 →</div>
            <strong>Nach links wischen:</strong> Nicht interessiert &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Nach rechts wischen:</strong> Gefällt mir!
        </div>
        """, unsafe_allow_html=True)
        
        # Aktueller Artikel
        current_item = items[current_idx]
        
        # Versteckte Buttons für JavaScript-Trigger (müssen VOR der Karte stehen!)
        st.markdown('<div class="hidden-buttons">', unsafe_allow_html=True)
        
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            dislike_btn = st.button("👎 Skip", key=f"hidden_dislike_{current_idx}")
        with col_h2:
            like_btn = st.button("❤️ Like", key=f"hidden_like_{current_idx}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Artikel anzeigen
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            st.markdown(f"""
            <div class="fashion-card" id="fashion-card-{current_idx}">
                <div class="swipe-indicator left">👎</div>
                <div class="swipe-indicator right">👍</div>
                <div class="category-tag">{current_item['category']}</div>
                <div class="item-name">{current_item['name']}</div>
                <div class="item-brand">{current_item['brand']}</div>
                <div class="item-price">{current_item['price']}</div>
                <p style="color: #666; line-height: 1.6;">{current_item['description']}</p>
                <div class="fashion-image">
                    <img src="{current_item['image_data']}" style="width: 100%; border-radius: 10px;" alt="{current_item['name']}" draggable="false">
                </div>
                <p style='text-align: center; color: #888; margin-top: 10px;'>Fashion-MNIST Index: {current_item['original_index']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Sichtbare Fallback-Buttons
        st.markdown("---")
        st.markdown("<p style='text-align: center; color: #888;'>Oder nutze die Buttons:</p>", unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])
        
        with col2:
            if st.button("👎 Nicht interessiert", type="secondary", use_container_width=True, key=f"visible_dislike_{current_idx}"):
                dislike_item()
                st.rerun()
        
        with col4:
            if st.button("❤️ Gefällt mir!", type="primary", use_container_width=True, key=f"visible_like_{current_idx}"):
                like_item()
                st.rerun()
        
        # Prüfen ob versteckte Buttons geklickt wurden
        if dislike_btn:
            dislike_item()
            st.rerun()
        
        if like_btn:
            like_item()
            st.rerun()
    
    # JavaScript für Swipe-Funktionalität
    st.markdown(f"""
    <script>
    (function() {{
        let startX = 0;
        let startY = 0;
        let currentX = 0;
        let currentY = 0;
        let isDragging = false;
        let swipeThreshold = 80;
        let card = null;
        
        function initSwipe() {{
            card = document.querySelector('#fashion-card-{current_idx}');
            if (!card) return;
            
            // Entferne alte Event Listener
            card.removeEventListener('touchstart', handleTouchStart);
            card.removeEventListener('touchmove', handleTouchMove);
            card.removeEventListener('touchend', handleTouchEnd);
            card.removeEventListener('mousedown', handleMouseDown);
            card.removeEventListener('mousemove', handleMouseMove);
            card.removeEventListener('mouseup', handleMouseUp);
            card.removeEventListener('mouseleave', handleMouseUp);
            
            // Touch Events
            card.addEventListener('touchstart', handleTouchStart, {{ passive: false }});
            card.addEventListener('touchmove', handleTouchMove, {{ passive: false }});
            card.addEventListener('touchend', handleTouchEnd, {{ passive: false }});
            
            // Mouse Events für Desktop
            card.addEventListener('mousedown', handleMouseDown);
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', handleMouseUp);
        }}
        
        function handleTouchStart(e) {{
            e.preventDefault();
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            isDragging = true;
            card.classList.add('dragging');
        }}
        
        function handleTouchMove(e) {{
            if (!isDragging) return;
            e.preventDefault();
            
            currentX = e.touches[0].clientX - startX;
            currentY = e.touches[0].clientY - startY;
            
            updateCardPosition();
        }}
        
        function handleTouchEnd(e) {{
            if (!isDragging) return;
            e.preventDefault();
            isDragging = false;
            card.classList.remove('dragging');
            
            handleSwipeEnd();
        }}
        
        function handleMouseDown(e) {{
            startX = e.clientX;
            startY = e.clientY;
            isDragging = true;
            card.classList.add('dragging');
            e.preventDefault();
        }}
        
        function handleMouseMove(e) {{
            if (!isDragging) return;
            
            currentX = e.clientX - startX;
            currentY = e.clientY - startY;
            
            updateCardPosition();
        }}
        
        function handleMouseUp(e) {{
            if (!isDragging) return;
            isDragging = false;
            card.classList.remove('dragging');
            
            handleSwipeEnd();
        }}
        
        function updateCardPosition() {{
            if (!card) return;
            
            const rotation = currentX * 0.1;
            card.style.transform = `translateX(${{currentX}}px) rotate(${{rotation}}deg)`;
            
            // Zeige Swipe-Indikatoren
            card.classList.remove('show-left', 'show-right');
            if (Math.abs(currentX) > 50) {{
                if (currentX > 0) {{
                    card.classList.add('show-right');
                }} else {{
                    card.classList.add('show-left');
                }}
            }}
        }}
        
        function handleSwipeEnd() {{
            if (!card) return;
            
            if (Math.abs(currentX) > swipeThreshold) {{
                if (currentX > 0) {{
                    // Swipe Right - Like
                    triggerLike();
                }} else {{
                    // Swipe Left - Dislike  
                    triggerDislike();
                }}
            }} else {{
                // Zurück zur Originalposition
                card.style.transform = '';
                card.classList.remove('show-left', 'show-right');
            }}
            
            currentX = 0;
            currentY = 0;
        }}
        
        function triggerLike() {{
            const likeButton = document.querySelector('button[key="hidden_like_{current_idx}"]');
            if (likeButton) {{
                likeButton.click();
            }}
        }}
        
        function triggerDislike() {{
            const dislikeButton = document.querySelector('button[key="hidden_dislike_{current_idx}"]');
            if (dislikeButton) {{
                dislikeButton.click();
            }}
        }}
        
        // Initialisiere Swipe
        setTimeout(initSwipe, 100);
        
        // Re-initialisiere bei Änderungen
        const observer = new MutationObserver(function(mutations) {{
            setTimeout(initSwipe, 100);
        }});
        
        observer.observe(document.body, {{
            childList: true,
            subtree: true
        }});
    }})();
    </script>
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
        
        st.markdown("---")
        st.markdown("## 📱 Swipe Anleitung")
        st.markdown("""
        **Desktop:** Klicken und ziehen
        
        **Mobile:** Touch und wischen
        
        - **Nach links:** 👎 Nicht interessiert
        - **Nach rechts:** 👍 Gefällt mir
        
        *Die Karte zeigt Indikatoren während des Swipens*
        """)
        
        st.markdown("---")
        st.markdown("## 🎯 Fashion-MNIST Info")
        st.markdown(f"""
        **Datensatz:** 70.000 Bilder
        
        **Kategorien:** {len(FASHION_CLASSES)}
        
        **Aktuelle Session:** {len(items)} zufällige Bilder
        
        **Bildgröße:** 28x28 Pixel (vergrößert auf 280x280)
        """)
        
        # Kategorie-Übersicht
        st.markdown("### 📋 Alle Kategorien:")
        for class_id, class_name in FASHION_CLASSES.items():
            st.markdown(f"• {class_name}")

if __name__ == "__main__":
    main()