<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>RESELL App</title>
    <style>
        /* ================= ДИЗАЙН СИСТЕМА ================= */
        :root {
            --bg-base: #060709;        /* Максимально тёмный фон */
            --bg-surface: #101216;     /* Фон карточек */
            --bg-glass: rgba(16, 18, 22, 0.7); /* Стекло */
            --accent: #CFFF24;         /* Кислотный неон */
            --accent-glow: rgba(207, 255, 36, 0.3);
            --text-primary: #FFFFFF;
            --text-secondary: #8A8D93;
            --border-light: rgba(255, 255, 255, 0.06);
            --radius-lg: 24px;
            --radius-md: 16px;
            --radius-sm: 10px;
            --font-main: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: var(--font-main); -webkit-tap-highlight-color: transparent; }

        body {
            background-color: #000;
            color: var(--text-primary);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        /* Контейнер приложения */
        .app {
            width: 100%;
            max-width: 420px;
            height: 100vh;
            background: radial-gradient(circle at 50% 0%, #15181c 0%, var(--bg-base) 60%);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        @media (min-width: 421px) {
            .app { height: 850px; border-radius: 40px; border: 8px solid #1a1c23; box-shadow: 0 20px 60px rgba(0,0,0,0.8); }
        }

        /* ================= HEADER ================= */
        .header {
            padding: 20px 20px 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            z-index: 10;
        }

        .logo-text { font-size: 26px; font-weight: 900; font-style: italic; letter-spacing: 0.5px; }
        .logo-accent { color: var(--accent); }

        .balance-badge {
            background: rgba(207, 255, 36, 0.1);
            border: 1px solid rgba(207, 255, 36, 0.2);
            padding: 8px 14px;
            border-radius: 30px;
            font-weight: 700;
            font-size: 14px;
            color: var(--accent);
            box-shadow: 0 0 15px var(--accent-glow);
            transition: transform 0.2s;
        }
        .balance-badge:active { transform: scale(0.95); }

        /* ================= SCROLL AREA & PAGES ================= */
        .viewport {
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
            padding: 0 20px 120px; /* Отступ снизу для меню */
            scroll-behavior: smooth;
        }
        .viewport::-webkit-scrollbar { display: none; }

        .page {
            display: none;
            opacity: 0;
            transform: translateY(15px) scale(0.98);
            transition: opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1), transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .page.active {
            display: block;
            opacity: 1;
            transform: translateY(0) scale(1);
        }

        /* ================= UI КОМПОНЕНТЫ ================= */
        .search-container { position: relative; margin-bottom: 20px; }
        .search-icon { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); opacity: 0.5; }
        .search-input {
            width: 100%;
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            padding: 14px 14px 14px 44px;
            border-radius: var(--radius-md);
            color: white;
            font-size: 16px;
            outline: none;
            transition: all 0.3s ease;
        }
        .search-input:focus { border-color: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }

        .section-title { font-size: 20px; font-weight: 700; margin: 24px 0 16px; display: flex; align-items: center; justify-content: space-between; }
        .section-title span { color: var(--text-secondary); font-size: 14px; font-weight: 500; }

        /* Горизонтальные категории */
        .categories-scroll {
            display: flex;
            gap: 10px;
            overflow-x: auto;
            padding-bottom: 5px;
            margin-right: -20px;
            padding-right: 20px;
        }
        .categories-scroll::-webkit-scrollbar { display: none; }
        .category-pill {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            padding: 10px 18px;
            border-radius: 30px;
            font-size: 14px;
            font-weight: 600;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }
        .category-pill.active { background: var(--accent); color: black; border-color: var(--accent); }

        /* Карточка товара (Лента) */
        .feed-grid { display: grid; gap: 16px; }
        
        .listing-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            padding: 14px;
            display: flex;
            gap: 14px;
            position: relative;
            overflow: hidden;
            opacity: 0;
            transform: translateY(20px);
            animation: slideUpFade 0.5s forwards cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        @keyframes slideUpFade { to { opacity: 1; transform: translateY(0); } }

        .listing-img {
            width: 90px;
            height: 90px;
            border-radius: var(--radius-sm);
            background: linear-gradient(135deg, #2a2d35 0%, #1a1c23 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            flex-shrink: 0;
            position: relative;
        }

        .listing-info { flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
        .listing-title { font-size: 16px; font-weight: 600; line-height: 1.3; }
        .listing-price { font-size: 18px; font-weight: 800; color: var(--accent); margin-top: 4px; }
        
        .listing-meta {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 8px;
            font-size: 12px;
        }
        
        .seller-info { display: flex; align-items: center; gap: 6px; color: var(--text-secondary); }
        .seller-avatar { width: 20px; height: 20px; border-radius: 50%; background: #333; }

        .badge {
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 10px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .badge-exchange { background: rgba(187, 134, 252, 0.15); color: #bb86fc; }
        .badge-sale { background: rgba(255, 255, 255, 0.1); color: white; }
        .badge-hold { background: rgba(36, 182, 255, 0.15); color: #24b6ff; }

        /* Главная кнопка действия */
        .btn-primary {
            width: 100%;
            background: var(--accent);
            color: #000;
            border: none;
            padding: 18px;
            border-radius: var(--radius-md);
            font-size: 16px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 20px var(--accent-glow);
            transition: all 0.2s;
        }
        .btn-primary:active { transform: scale(0.97); box-shadow: 0 5px 10px var(--accent-glow); }

        /* ================= FLOATING BOTTOM NAV ================= */
        .nav-dock {
            position: absolute;
            bottom: 25px;
            left: 20px;
            right: 20px;
            background: var(--bg-glass);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid var(--border-light);
            border-radius: 30px;
            display: flex;
            justify-content: space-between;
            padding: 8px 16px;
            z-index: 100;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 50px;
            height: 50px;
            color: var(--text-secondary);
            border-radius: 20px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }

        .nav-item svg { width: 24px; height: 24px; fill: currentColor; transition: all 0.3s; }
        
        .nav-item.active { color: var(--accent); }
        .nav-item.active svg { transform: translateY(-2px); filter: drop-shadow(0 0 8px var(--accent-glow)); }

        /* Центральная Action-кнопка в меню */
        .nav-fab {
            width: 56px;
            height: 56px;
            background: var(--accent);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: black;
            transform: translateY(-15px);
            box-shadow: 0 8px 24px var(--accent-glow);
            border: 4px solid var(--bg-base);
            transition: transform 0.2s;
        }
        .nav-fab:active { transform: translateY(-12px) scale(0.95); }
        .nav-fab svg { fill: black; width: 28px; height: 28px; }

    </style>
</head>
<body>

<div class="app">
    <!-- Стеклянный градиент на фоне для глубины -->
    <div style="position: absolute; top: -100px; left: -100px; width: 300px; height: 300px; background: var(--accent); filter: blur(150px); opacity: 0.05; pointer-events: none; z-index: 0;"></div>

    <!-- HEADER -->
    <header class="header">
        <div class="logo-text">RES<span class="logo-accent">E</span>LL</div>
        <div class="balance-badge">28 450 ₽</div>
    </header>

    <!-- ОСНОВНАЯ ОБЛАСТЬ СКРОЛЛА -->
    <main class="viewport">

        <!-- СТРАНИЦА: ЛЕНТА (HOME) -->
        <section id="home" class="page active">
            <div class="search-container">
                <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <input type="text" class="search-input" placeholder="Поиск на районе...">
            </div>

            <div class="categories-scroll">
                <div class="category-pill active">🔥 Все</div>
                <div class="category-pill">👟 Кроссовки</div>
                <div class="category-pill">🎮 Техника</div>
                <div class="category-pill">👕 Шмот</div>
            </div>

            <h2 class="section-title">Свежее <span>Показать все</span></h2>
            
            <!-- Контейнер для генерации объявлений через JS -->
            <div class="feed-grid" id="feed-container">
                <!-- Карточки появятся здесь -->
            </div>
        </section>

        <!-- СТРАНИЦА: СДЕЛКИ И МЕНА-КРОСС -->
        <section id="deals" class="page">
            <h2 class="section-title" style="margin-top: 0;">Безопасная сделка</h2>
            
            <!-- Инфо-карточка из презентации -->
            <div style="background: var(--bg-surface); border: 1px solid var(--border-light); border-radius: var(--radius-lg); padding: 20px; margin-bottom: 20px; position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: var(--accent);"></div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <span style="font-weight: 700; font-size: 18px;">Эскроу активен</span>
                    <span class="badge badge-hold" style="font-size: 12px;">HOLD</span>
                </div>
                
                <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                    <div style="width: 60px; height: 60px; background: #222; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">👟</div>
                    <div>
                        <div style="font-weight: 600; margin-bottom: 4px;">Nike Dunk Low Panda</div>
                        <div style="color: var(--accent); font-weight: 700;">8 000 ₽</div>
                    </div>
                </div>

                <!-- Таймлайн статуса -->
                <div style="border-left: 2px solid var(--accent); margin-left: 10px; padding-left: 15px; display: flex; flex-direction: column; gap: 15px;">
                    <div style="position: relative;">
                        <div style="position: absolute; left: -20px; top: 2px; width: 8px; height: 8px; border-radius: 50%; background: var(--accent);"></div>
                        <div style="font-size: 14px; color: white;">Оплата покупателем</div>
                        <div style="font-size: 12px; color: var(--text-secondary);">14:22</div>
                    </div>
                    <div style="position: relative;">
                        <div style="position: absolute; left: -20px; top: 2px; width: 8px; height: 8px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 10px var(--accent);"></div>
                        <div style="font-size: 14px; color: white; font-weight: 600;">Ожидается товар</div>
                        <div style="font-size: 12px; color: var(--text-secondary);">Продавец должен отправить посылку</div>
                    </div>
                </div>
            </div>
            
            <button class="btn-primary" style="background: #24262E; color: white; border: 1px solid var(--border-light); box-shadow: none;">Открыть спор ⚖️</button>
        </section>

        <!-- СТРАНИЦА: СОЗДАТЬ -->
        <section id="create" class="page">
            <div style="text-align: center; padding: 40px 0;">
                <div style="font-size: 60px; margin-bottom: 20px;">📸</div>
                <h2 style="margin-bottom: 10px;">Добавь свой лут</h2>
                <p style="color: var(--text-secondary); font-size: 14px; margin-bottom: 30px; line-height: 1.5;">Продай за кэш или предложи обмен через Мена-Кросс. Никакой комиссии за размещение.</p>
                <button class="btn-primary">Загрузить фото</button>
            </div>
        </section>

    </main>

    <!-- ПАРЯЩИЙ DOCK НАВИГАЦИИ -->
    <nav class="nav-dock">
        <div class="nav-item active" onclick="switchPage('home', this)">
            <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
        </div>
        
        <div class="nav-item" onclick="switchPage('deals', this)">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
        </div>
        
        <!-- Большая кнопка ДОБАВИТЬ -->
        <div class="nav-fab" onclick="switchPage('create', this)">
            <svg viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
        </div>
        
        <div class="nav-item">
            <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/></svg>
        </div>
        
        <div class="nav-item">
            <svg viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
        </div>
    </nav>
</div>

<!-- ЛОГИКА ПРИЛОЖЕНИЯ -->
<script>
    // 1. ДАННЫЕ: Фейковые объявления из презентации
    const listingsData = [
        { title: "Nike Dunk Low Panda", price: "5 500 ₽", type: "sale", badge: "ПРОДАЖА", img: "👟", user: "sneakerhead", rating: "4.9" },
        { title: "PlayStation 4 Pro 1TB", price: "12 000 ₽", type: "exchange", badge: "ОБМЕН", img: "🎮", user: "Пацан Б", rating: "5.0" },
        { title: "iPhone 11 128GB", price: "15 000 ₽", type: "hold", badge: "ХОЛД", img: "📱", user: "apple_boy", rating: "4.8" },
        { title: "Jordan 4 Retro", price: "18 500 ₽", type: "sale", badge: "ПРОДАЖА", img: "🏀", user: "resell_king", rating: "5.0" },
        { title: "AirPods Pro 2", price: "8 000 ₽", type: "exchange", badge: "ОБМЕН", img: "🎧", user: "music_fan", rating: "4.5" }
    ];

    // 2. ГЕНЕРАЦИЯ ЛЕНТЫ С КАСКАДНОЙ АНИМАЦИЕЙ
    const feedContainer = document.getElementById('feed-container');
    
    listingsData.forEach((item, index) => {
        // Выбираем стиль бейджа
        let badgeClass = "badge-sale";
        if(item.type === "exchange") badgeClass = "badge-exchange";
        if(item.type === "hold") badgeClass = "badge-hold";

        // Добавляем задержку анимации для красивого появления
        const delay = index * 0.1; 

        const cardHTML = `
            <div class="listing-card" style="animation-delay: ${delay}s">
                <div class="listing-img">${item.img}</div>
                <div class="listing-info">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div class="listing-title">${item.title}</div>
                        </div>
                        <div class="listing-price">${item.price}</div>
                    </div>
                    <div class="listing-meta">
                        <div class="seller-info">
                            <div class="seller-avatar"></div>
                            ${item.user} • ⭐${item.rating}
                        </div>
                        <div class="badge ${badgeClass}">${item.badge}</div>
                    </div>
                </div>
            </div>
        `;
        feedContainer.insertAdjacentHTML('beforeend', cardHTML);
    });

    // 3. РОУТИНГ: Плавное переключение страниц
    function switchPage(pageId, element) {
        // Убираем активный класс со всех страниц
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });

        // Убираем активный класс со всех кнопок в доке
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });

        // Показываем нужную страницу (анимация сработает автоматически из-за CSS transition)
        setTimeout(() => {
            document.getElementById(pageId).classList.add('active');
        }, 50);

        // Подсвечиваем активную кнопку (если нажали не на центральный FAB)
        if (!element.classList.contains('nav-fab')) {
            element.classList.add('active');
        }
    }

    // Добавляем эффект нажатия для фильтров категорий
    document.querySelectorAll('.category-pill').forEach(pill => {
        pill.addEventListener('click', function() {
            document.querySelectorAll('.category-pill').forEach(p => p.classList.remove('active'));
            this.classList.add('active');
        });
    });
</script>
</body>
</html>