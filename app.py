from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'pinkmiya-cat-pink-white-2025-secret'

# ==================== DATA ====================
PRODUCTS = [
    {"id": 1, "name": "핑크 리본 캣타워", "price": 89000, "category": "침구",
     "desc": "부드러운 화이트 패브릭과 핑크 리본 장식이 어우러진 3단 캣타워예요. 고양이가 가장 좋아하는 높은 곳에서 편안하게 쉼 수 있어요. 안정감 있는 구조와 부드러운 소재로 오랜 시간 사랑받고 있어요.",
     "emoji": "🏠", "badge": "베스트", "stock": 23},
    {"id": 2, "name": "소프트 화이트 쿠션 베드", "price": 45000, "category": "침구",
     "desc": "구름처럼 폭신한 화이트 쿠션 베드. 가장자리가 살짝 올라와 고양이의 몸을 포근하게 감싸줍니다. 세탁이 쉬운 커버와 분홍색 포인트가 귀여운 포인트예요.",
     "emoji": "🛏️", "badge": None, "stock": 47},
    {"id": 3, "name": "레이스 핑크 하네스", "price": 22000, "category": "악세서리",
     "desc": "산책할 때 착용하기 좋은 가벽운 레이스 하네스. 분홍색 리본과 하트 장식이 달려 있어요. 부드러운 소재로 목과 가슴에 부담이 적고 조절이 쉬워요.",
     "emoji": "🎀", "badge": "신상", "stock": 65},
    {"id": 4, "name": "하트 자동 레이져 토이", "price": 35000, "category": "장난감",
     "desc": "랜덤으로 움직이는 귀여운 하트 모양 레이져. 고양이가 혼자서도 오래동안 놀 수 있어요. 타이머 기능이 있어서 배터리 걱정 없이 사용 가능합니다.",
     "emoji": "❤️", "badge": None, "stock": 38},
    {"id": 5, "name": "플러시 캣닂 장난감 세트", "price": 18000, "category": "장난감",
     "desc": "고양이가 제일 좋아하는 캣닂이 가득 들어있는 플러시 장난감 3종 세트. 귀여운 분홍색과 화이트 컬러로 구성되어 있어요. 물고 뜨없고 놀기 딱!",
     "emoji": "🧶", "badge": None, "stock": 81},
    {"id": 6, "name": "세라믹 핑크 급수기", "price": 29000, "category": "급식/위생",
     "desc": "고양이가 물을 더 많이 마시게 돕는 조용한 세라믹 급수기. 부드러운 핑크 컬러와 미니멀한 디자인으로 인테리어 소품처럼 예뻐요. 필터 포함.",
     "emoji": "💧", "badge": "베스트", "stock": 29},
    {"id": 7, "name": "미니멀 화이트 스크래처", "price": 32000, "category": "침구",
     "desc": "단순하지만 예뻐 디자인의 대형 스크래처. 소파를 보호하면서 고양이의 스트레스 해소에 도움을 줍니다. 바닥 미끄럼 방지 패드 포함.",
     "emoji": "📦", "badge": None, "stock": 54},
    {"id": 8, "name": "핑크 체크 고양이 후드티", "price": 27000, "category": "의류",
     "desc": "겨울에 입히기 좋은 부드러운 후드티. 따뜻한 안감과 귀여운 체크 패턴, 작은 리본 장식까지. 3kg~6kg 고양이에게 잘 맞아요.",
     "emoji": "👕", "badge": "신상", "stock": 19},
    {"id": 9, "name": "참치&연어 동결건조 간식", "price": 15000, "category": "간식",
     "desc": "100% 자연산 참치와 연어로 만든 고양이 전용 동결건조 간식. 인공 첨가물 없이 건강하게 줄 수 있어요. 한 봉지에 40g 들어있습니다.",
     "emoji": "🐟", "badge": None, "stock": 120},
    {"id": 10, "name": "핑크 손잡이 빗 세트", "price": 19000, "category": "급식/위생",
     "desc": "엉킨 털을 부드럽게 풀어주는 슬리커 브러시 + 코트 빗 세트. 핑크색 손잡이가 너무 귀여운요. 매일 빗질로 고양이와의 유대감을 높여보세요.",
     "emoji": "✨", "badge": None, "stock": 72},
    {"id": 11, "name": "화이트 숨숨집 (캣버터리)", "price": 68000, "category": "침구",
     "desc": "고양이가 제일 좋아하는 밀폐형 숨숨집. 화이트 컬러에 분홍색 쿠션으로 포인트를 줘어요. 겨울에는 따뜻하고 여름에는 시원하게 사용할 수 있어요.",
     "emoji": "🏠", "badge": "베스트", "stock": 14},
    {"id": 12, "name": "반짝이 방울 목걸이", "price": 12000, "category": "악세서리",
     "desc": "가벽운 핑크 컬러 목걸이. 작은 방울 소리가 나서 고양이 위치를 쉽게 알 수 있어요. 안전을 위해 풀림이 쉬운 구조로 만들었어요.",
     "emoji": "🔔", "badge": None, "stock": 93},
]

CATEGORIES = ['전체', '침구', '장난감', '악세서리', '급식/위생', '의류', '간식']

# ==================== HELPERS ====================
def get_cart():
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']

def save_cart(cart):
    session['cart'] = cart
    session.modified = True

def get_user():
    return session.get('user')

def require_login():
    if not get_user():
        flash('로그인이 필요해요. 먼저 로그인해주세요!', 'warning')
        return redirect(url_for('login', next=request.path))
    return None

def find_product(pid):
    for p in PRODUCTS:
        if p['id'] == pid:
            return p
    return None

def get_cart_items():
    cart = get_cart()
    items = []
    total = 0
    for entry in cart:
        prod = find_product(entry['id'])
        if prod:
            qty = entry.get('qty', 1)
            subtotal = prod['price'] * qty
            total += subtotal
            items.append({
                'id': prod['id'], 'name': prod['name'], 'price': prod['price'],
                'emoji': prod['emoji'], 'category': prod['category'],
                'qty': qty, 'subtotal': subtotal
            })
    return items, total

def add_to_cart_session(product_id, qty=1):
    cart = get_cart()
    for item in cart:
        if item['id'] == product_id:
            item['qty'] = item.get('qty', 1) + qty
            save_cart(cart)
            return True
    cart.append({'id': product_id, 'qty': qty})
    save_cart(cart)
    return True

# Wishlist helpers
def get_wishlist():
    if 'wishlist' not in session:
        session['wishlist'] = []
    return session['wishlist']

def save_wishlist(wishlist):
    session['wishlist'] = wishlist
    session.modified = True

def toggle_wishlist_session(product_id):
    wishlist = get_wishlist()
    if product_id in wishlist:
        wishlist.remove(product_id)
        saved = False
    else:
        wishlist.append(product_id)
        saved = True
    save_wishlist(wishlist)
    return saved

def get_wishlist_items():
    wishlist = get_wishlist()
    items = []
    for pid in wishlist:
        prod = find_product(pid)
        if prod:
            items.append(prod)
    return items

# ==================== ROUTES ====================

@app.route('/')
def home():
    user = get_user()
    wishlist = get_wishlist()
    featured = [p for p in PRODUCTS if p.get('badge') in ('베스트', '신상')][:6] or PRODUCTS[:8]
    return render_template('index.html', products=PRODUCTS, featured=featured,
                           categories=CATEGORIES, user=user, wishlist=wishlist, page='home')

@app.route('/shop')
def shop():
    user = get_user()
    q = request.args.get('q', '').strip().lower()
    category = request.args.get('category', '전체')
    wishlist = get_wishlist()

    filtered = PRODUCTS[:]
    if category != '전체':
        filtered = [p for p in filtered if p['category'] == category]
    if q:
        filtered = [p for p in filtered if q in p['name'].lower() or q in p['desc'].lower()]

    return render_template('shop.html', products=filtered, all_products=PRODUCTS,
                           categories=CATEGORIES, current_category=category,
                           search_query=q, user=user, wishlist=wishlist, page='shop')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    user = get_user()
    product = find_product(product_id)
    if not product:
        flash('상품을 찾을 수 없어요.', 'error')
        return redirect(url_for('shop'))

    wishlist = get_wishlist()
    related = [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != product_id][:4]
    if len(related) < 4:
        extra = [p for p in PRODUCTS if p['id'] != product_id][:4 - len(related)]
        related += extra

    return render_template('product.html', product=product, related=related,
                           user=user, categories=CATEGORIES, wishlist=wishlist, page='product')

# ==================== CART ====================
@app.route('/cart')
def cart():
    user = get_user()
    items, total = get_cart_items()
    return render_template('cart.html', cart_items=items, total=total, user=user, page='cart')

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form.get('product_id'))
    qty = int(request.form.get('qty', 1))
    product = find_product(product_id)
    if not product:
        flash('상품이 존재하지 않아요.', 'error')
        return redirect(url_for('shop'))

    add_to_cart_session(product_id, qty)
    flash(f'{product["name"]}을(를) 장바구니에 담았어요!', 'success')

    next_page = request.form.get('next') or request.referrer
    if next_page and '/product/' in (next_page or ''):
        return redirect(url_for('product_detail', product_id=product_id))
    return redirect(url_for('cart'))

@app.route('/update-cart', methods=['POST'])
def update_cart():
    product_id = int(request.form.get('product_id'))
    action = request.form.get('action')
    cart = get_cart()
    for item in cart:
        if item['id'] == product_id:
            if action == 'plus':
                item['qty'] = item.get('qty', 1) + 1
            elif action == 'minus':
                item['qty'] = max(1, item.get('qty', 1) - 1)
            elif action == 'remove':
                cart.remove(item)
            break
    save_cart(cart)
    return redirect(url_for('cart'))

@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    session['cart'] = []
    flash('장바구니를 비웠어요.', 'success')
    return redirect(url_for('cart'))

# ==================== WISHLIST ====================
@app.route('/wishlist')
def wishlist():
    user = get_user()
    if not user:
        return redirect(url_for('login'))
    items = get_wishlist_items()
    return render_template('wishlist.html', wishlist_items=items, user=user, page='wishlist')

@app.route('/toggle-wishlist', methods=['POST'])
def toggle_wishlist():
    product_id = int(request.form.get('product_id'))
    product = find_product(product_id)
    if not product:
        return redirect(url_for('shop'))

    saved = toggle_wishlist_session(product_id)
    if saved:
        flash(f'{product["name"]}을(를) 위시리스트에 추가했어요 ♡', 'success')
    else:
        flash(f'{product["name"]}을(를) 위시리스트에서 제거했어요', 'success')

    ref = request.referrer or url_for('shop')
    return redirect(ref)

# ==================== AUTH ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if get_user():
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('이메일과 비밀번호를 모두 입력해주세요.', 'error')
            return render_template('login.html', user=None, page='login')

        if len(password) < 4:
            flash('비밀번호는 4자 이상이어야 해요.', 'error')
            return render_template('login.html', user=None, page='login')

        name = email.split('@')[0].capitalize()
        session['user'] = {'name': name, 'email': email}
        flash(f'환영합니다, {name}님! 🐾', 'success')

        next_url = request.args.get('next') or url_for('home')
        return redirect(next_url)

    return render_template('login.html', user=None, page='login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if get_user():
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        pw = request.form.get('password', '')
        pw2 = request.form.get('password2', '')

        if not name or not email or not pw or not pw2:
            flash('모든 항목을 입력해주세요.', 'error')
            return render_template('register.html', user=None, page='register')
        if pw != pw2:
            flash('비밀번호가 일치하지 않아요.', 'error')
            return render_template('register.html', user=None, page='register')
        if len(pw) < 4:
            flash('비밀번호는 4자 이상 입력해주세요.', 'error')
            return render_template('register.html', user=None, page='register')

        session['user'] = {'name': name, 'email': email}
        flash(f'{name}님, 회원가입을 축하드려요! 귀여운 상품들을 구경해보세요 🐱', 'success')
        return redirect(url_for('shop'))

    return render_template('register.html', user=None, page='register')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('wishlist', None)
    flash('로그아웃 되었어요. 다음에 또 만나요!', 'success')
    return redirect(url_for('home'))

# ==================== USER ====================
@app.route('/profile')
def profile():
    user = get_user()
    if not user:
        return redirect(url_for('login'))

    fake_orders = [
        {"order_no": "PK-241219", "date": "2024-12-19", "items": "핑크 리본 캣타워 외 1건", "total": 134000, "status": "배송완료"},
        {"order_no": "PK-250107", "date": "2025-01-07", "items": "하트 자동 레이져 토이", "total": 35000, "status": "배송완료"},
    ]
    wishlist_count = len(get_wishlist())
    return render_template('profile.html', user=user, orders=fake_orders, wishlist_count=wishlist_count, page='profile')

# ==================== CHECKOUT ====================
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    user = get_user()
    redirect_resp = require_login()
    if redirect_resp:
        return redirect(redirect_resp)

    items, total = get_cart_items()
    if not items:
        flash('장바구니가 비어있어요.', 'warning')
        return redirect(url_for('shop'))

    if request.method == 'POST':
        order_number = f"PK-{random.randint(100000, 999999)}"
        session['last_order'] = {
            'number': order_number,
            'total': total,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'items_count': len(items)
        }
        session['cart'] = []
        flash('주문이 성공적으로 완료되었어요!', 'success')
        return redirect(url_for('order_success', order_no=order_number))

    return render_template('checkout.html', cart_items=items, total=total, user=user, page='checkout')

@app.route('/order-success')
def order_success():
    user = get_user()
    order_no = request.args.get('order_no') or session.get('last_order', {}).get('number', 'PK-000000')
    order_info = session.get('last_order', {'number': order_no, 'total': 0, 'date': '방금', 'items_count': 1})
    return render_template('success.html', order_no=order_no, order_info=order_info, user=user, page='success')

# ==================== API ====================
@app.route('/api/add-to-cart', methods=['POST'])
def api_add_to_cart():
    data = request.get_json() or {}
    pid = data.get('product_id')
    if not pid:
        return jsonify({'success': False}), 400
    product = find_product(int(pid))
    if not product:
        return jsonify({'success': False}), 404
    add_to_cart_session(int(pid), data.get('qty', 1))
    return jsonify({'success': True, 'cart_count': sum(i.get('qty', 1) for i in get_cart())})

@app.route('/api/cart-count')
def api_cart_count():
    return jsonify({'count': sum(i.get('qty', 1) for i in get_cart())})

@app.route('/api/wishlist-count')
def api_wishlist_count():
    return jsonify({'count': len(get_wishlist())})

if __name__ == '__main__':
    print("\n🐱 핑크미야 Flask 쇼핑몰이 시작됩니다!")
    print("→ http://127.0.0.1:5000\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
