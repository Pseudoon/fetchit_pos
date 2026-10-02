# Integrating the Fetchit POS into your app

## Files
- `menu_data.py` — static menu (from the Fetchit menu PDF), ₹20 delivery charge constant
- `models.py` — `Order` / `OrderItem` SQLAlchemy models
- `schemas.py` — Pydantic request/response schemas, incl. `DailySummaryOut`
- `orders_router.py` — `orders` router (create/list/daily-summary) + `menu` router
- `pos.html` — standalone frontend (menu, cart, place order, daily dashboard)

## 1. Adjust imports
In `models.py` and `orders_router.py`, fix these two lines to match your actual app:
```python
from database import Base       # models.py
from database import get_db     # orders_router.py
```

## 2. Register both routers in your main FastAPI app
```python
from orders_router import router as orders_router, menu_router

app.include_router(orders_router)
app.include_router(menu_router)
```

## 3. Create the tables
If you're not using Alembic yet:
```python
from database import Base, engine
import models
Base.metadata.create_all(bind=engine)
```
Otherwise, generate a migration as usual.

## 4. Serve / open the frontend
`pos.html` is plain HTML+JS with no build step. Two options:
- Serve it as a static file from FastAPI: `app.mount("/pos", StaticFiles(directory="static"), name="pos")` and open `/pos/pos.html`
- Or just open the file directly in a browser during testing

**Important:** at the top of `pos.html`'s `<script>`, set:
```js
const API_BASE = "http://localhost:8000";  // change to your actual backend URL
```

## Endpoints this gives you
- `GET /menu/` — full categorized menu
- `POST /orders/` — place an order → returns Order ID + bill
- `GET /orders/?order_date=YYYY-MM-DD` — list orders (optionally filtered by day)
- `GET /orders/summary/daily?order_date=YYYY-MM-DD` — order count + revenue totals for that day (defaults to today)

## Notes
- Delivery charge (₹20) lives in one place: `menu_data.DELIVERY_CHARGE`
- Half/Full priced items (Chinese section) are stored as separate menu variants, e.g. "Hakka Noodles (Half)" — kept as the item name at order time so old orders stay accurate even if you edit the menu later
- Daily summary groups by the order's `created_at` date, so no extra scheduled job is needed
