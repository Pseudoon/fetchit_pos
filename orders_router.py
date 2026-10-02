import io
import re
from datetime import date, datetime
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db  # assumes fetch.it already has this dependency
from models import Order, OrderItem
from schemas import OrderCreate, OrderOut, DailySummaryOut
from menu_data import MENU, DELIVERY_CHARGE

router = APIRouter(prefix="/orders", tags=["orders"])
menu_router = APIRouter(prefix="/menu", tags=["menu"])


# --- Helper for Tally PDFs ---
def get_category_items(category_names):
    """category_names can be a single string or a list of category names to combine."""
    if isinstance(category_names, str):
        category_names = [category_names]
    item_names = set()
    for cat in MENU:
        if cat["category"] in category_names:
            for item in cat["items"]:
                item_names.add(item["name"])
    return item_names

def generate_tally_pdf(orders, category_name, target_date, display_title=None):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    display_title = display_title or category_name
    category_items_set = get_category_items(category_name)
    
    # Aggregate data: item_name -> qty
    # Only strip a trailing " (Half)" / " (Full)" variant suffix — NOT the first
    # "(" in the name, since some item names (e.g. "Paneer Steamed Momos (5pc / 10pc)")
    # already contain their own parentheses as part of the real name.
    tally = defaultdict(int)
    for o in orders:
        for i in o.items:
            base_name = re.sub(r"\s*\((Half|Full)\)\s*$", "", i.item_name)
            if base_name in category_items_set or i.item_name in category_items_set:
                tally[i.item_name] += i.quantity

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"{display_title} Tally ({target_date.strftime('%d %b %Y')})", styles["Title"]))
    elements.append(Spacer(1, 14))

    if not tally:
        elements.append(Paragraph(f"No {display_title} items sold on this date.", styles["Normal"]))
    else:
        data = [["Item Name", "Total Qty Sold"]]
        total_qty = 0
        for item_name, qty in tally.items():
            data.append([item_name, str(qty)])
            total_qty += qty
        
        data.append(["GRAND TOTAL", str(total_qty)])

        table = Table(data, colWidths=[250, 150])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3a1c12")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#eaf5fb")),
        ]))
        elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
# -----------------------------


@menu_router.get("/")
def get_menu():
    return MENU


@router.post("/", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")

    today = datetime.utcnow().date()

    last_number = (
        db.query(func.max(Order.daily_number))
        .filter(Order.order_date == today)
        .scalar()
    )
    next_number = (last_number or 0) + 1

    subtotal = sum(item.price * item.quantity for item in payload.items)
    total = subtotal + DELIVERY_CHARGE

    order = Order(
        order_date=today,
        daily_number=next_number,
        customer_name=payload.customer_name,
        customer_phone=payload.customer_phone,
        delivery_spot=payload.delivery_spot,
        time_slot=payload.time_slot,
        subtotal=subtotal,
        delivery_charge=DELIVERY_CHARGE,
        total=total,
    )
    db.add(order)
    db.flush() 

    for item in payload.items:
        db.add(OrderItem(
            order_id=order.id,
            item_name=item.item_name,
            quantity=item.quantity,
            price=item.price,
        ))

    db.commit()
    db.refresh(order)
    return order


@router.put("/{order_date}/{daily_number}", response_model=OrderOut)
def update_order(order_date: date, daily_number: int, payload: OrderCreate, db: Session = Depends(get_db)):
    """Edit an existing order's customer info, delivery spot, and items."""
    order = (
        db.query(Order)
        .filter(Order.order_date == order_date, Order.daily_number == daily_number)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not payload.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")

    order.customer_name = payload.customer_name
    order.customer_phone = payload.customer_phone
    order.delivery_spot = payload.delivery_spot
    order.time_slot = payload.time_slot

    db.query(OrderItem).filter(OrderItem.order_id == order.id).delete()

    subtotal = sum(item.price * item.quantity for item in payload.items)
    order.subtotal = subtotal
    order.total = subtotal + DELIVERY_CHARGE

    for item in payload.items:
        db.add(OrderItem(
            order_id=order.id,
            item_name=item.item_name,
            quantity=item.quantity,
            price=item.price,
        ))

    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_date}/{daily_number}")
def delete_order(order_date: date, daily_number: int, db: Session = Depends(get_db)):
    """Delete a single order (and its items) by date + daily number."""
    order = (
        db.query(Order)
        .filter(Order.order_date == order_date, Order.daily_number == daily_number)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)  # cascade="all, delete-orphan" on Order.items removes the items too
    db.commit()
    return {"detail": f"Order #{daily_number} on {order_date} deleted"}


@router.get("/lookup", response_model=OrderOut)
def get_order(order_date: date, daily_number: int, db: Session = Depends(get_db)):
    """Look up a single order by its date + simple daily number, e.g. order #3 on 2026-09-27."""
    order = (
        db.query(Order)
        .filter(Order.order_date == order_date, Order.daily_number == daily_number)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/", response_model=list[OrderOut])
def list_orders(order_date: date | None = None, time_slot: str | None = None, db: Session = Depends(get_db)):
    """List orders, optionally filtered to a single calendar date and/or time slot."""
    query = db.query(Order)
    if order_date:
        query = query.filter(Order.order_date == order_date)
    if time_slot:
        query = query.filter(Order.time_slot == time_slot)
    return query.order_by(Order.daily_number.asc()).all()


@router.get("/summary/daily", response_model=DailySummaryOut)
def daily_summary(order_date: date | None = None, time_slot: str | None = None, db: Session = Depends(get_db)):
    """Order count and revenue totals for a given day (defaults to today) and optional time slot."""
    target_date = order_date or datetime.utcnow().date()

    query = db.query(Order).filter(Order.order_date == target_date)
    if time_slot:
        query = query.filter(Order.time_slot == time_slot)
    orders = query.all()

    total_orders = len(orders)
    total_subtotal = sum(o.subtotal for o in orders)
    total_delivery = sum(o.delivery_charge for o in orders)
    total_revenue = sum(o.total for o in orders)

    return DailySummaryOut(
        date=target_date,
        total_orders=total_orders,
        total_subtotal=total_subtotal,
        total_delivery_charges=total_delivery,
        total_revenue=total_revenue,
    )


@router.get("/export/daily-pdf")
def export_daily_pdf(order_date: date | None = None, time_slot: str | None = None, db: Session = Depends(get_db)):
    """Download a PDF of all orders for a given day (defaults to today) and optional time slot."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    target_date = order_date or datetime.utcnow().date()
    query = db.query(Order).filter(Order.order_date == target_date)
    if time_slot:
        query = query.filter(Order.time_slot == time_slot)
        
    orders = query.order_by(Order.daily_number.asc()).all()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm)
    styles = getSampleStyleSheet()
    elements = []

    title_suffix = f" - {time_slot}" if time_slot else ""
    elements.append(Paragraph(f"Fetchit &mdash; Daily Orders ({target_date.strftime('%d %b %Y')}){title_suffix}", styles["Title"]))
    elements.append(Spacer(1, 10))

    total_subtotal = sum(o.subtotal for o in orders)
    total_delivery = sum(o.delivery_charge for o in orders)
    total_revenue = sum(o.total for o in orders)
    summary_text = (
        f"Total Orders: {len(orders)} &nbsp;|&nbsp; "
        f"Items Revenue: Rs. {total_subtotal:.0f} &nbsp;|&nbsp; "
        f"Delivery Collected: Rs. {total_delivery:.0f} &nbsp;|&nbsp; "
        f"Total Revenue: Rs. {total_revenue:.0f}"
    )
    elements.append(Paragraph(summary_text, styles["Normal"]))
    elements.append(Spacer(1, 14))

    if not orders:
        elements.append(Paragraph("No orders for this date.", styles["Normal"]))
    else:
        data = [["#", "Customer", "Phone", "Spot", "Items", "Time", "Total"]]
        for o in orders:
            items_str = ", ".join(f"{i.item_name} x{i.quantity}" for i in o.items)
            data.append([
                str(o.daily_number),
                o.customer_name,
                o.customer_phone,
                o.delivery_spot,
                Paragraph(items_str, styles["Normal"]),
                o.created_at.strftime("%I:%M %p"),
                f"Rs. {o.total:.0f}",
            ])

        table = Table(data, colWidths=[18, 65, 60, 55, 155, 48, 48])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e0532f")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f7f7")]),
        ]))
        elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    filename = f"fetchit-orders-{target_date.isoformat()}.pdf"
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/export/customer-list-pdf")
def export_customer_list_pdf(order_date: date | None = None, time_slot: str | None = None, db: Session = Depends(get_db)):
    """Download a simple PDF: just date, order #, customer name and phone — no revenue/stats."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    target_date = order_date or datetime.utcnow().date()
    query = db.query(Order).filter(Order.order_date == target_date)
    if time_slot:
        query = query.filter(Order.time_slot == time_slot)
        
    orders = query.order_by(Order.daily_number.asc()).all()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm)
    styles = getSampleStyleSheet()
    elements = []

    title_suffix = f" - {time_slot}" if time_slot else ""
    elements.append(Paragraph(f"Fetchit &mdash; Customer List ({target_date.strftime('%d %b %Y')}){title_suffix}", styles["Title"]))
    elements.append(Spacer(1, 14))

    if not orders:
        elements.append(Paragraph("No orders for this date.", styles["Normal"]))
    else:
        data = [["#", "Customer Name", "Phone Number", "Delivery Spot", "Items"]]
        for o in orders:
            items_str = ", ".join(f"{i.item_name} x{i.quantity}" for i in o.items)
            data.append([
                str(o.daily_number),
                o.customer_name,
                o.customer_phone,
                o.delivery_spot,
                Paragraph(items_str, styles["Normal"]),
            ])

        table = Table(data, colWidths=[25, 110, 85, 85, 165])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4a2318")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f7f7")]),
        ]))
        elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    filename = f"fetchit-customer-list-{target_date.isoformat()}.pdf"
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )

@router.get("/export/tally-chinese-pdf")
def export_chinese_tally_pdf(order_date: date | None = None, time_slot: str | None = None, db: Session = Depends(get_db)):
    target_date = order_date or datetime.utcnow().date()
    query = db.query(Order).filter(Order.order_date == target_date)
    if time_slot:
        query = query.filter(Order.time_slot == time_slot)
    
    buffer = generate_tally_pdf(query.all(), "Chinese", target_date)
    return StreamingResponse(
        buffer, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=chinese-tally-{target_date.isoformat()}.pdf"}
    )

@router.get("/export/tally-fastfood-pdf")
def export_fastfood_tally_pdf(order_date: date | None = None, time_slot: str | None = None, db: Session = Depends(get_db)):
    target_date = order_date or datetime.utcnow().date()
    query = db.query(Order).filter(Order.order_date == target_date)
    if time_slot:
        query = query.filter(Order.time_slot == time_slot)
    
    buffer = generate_tally_pdf(query.all(), "Fast Food & Continental", target_date)
    return StreamingResponse(
        buffer, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=fastfood-tally-{target_date.isoformat()}.pdf"}
    )

@router.get("/export/tally-momos-pdf")
def export_momos_tally_pdf(order_date: date | None = None, time_slot: str | None = None, db: Session = Depends(get_db)):
    target_date = order_date or datetime.utcnow().date()
    query = db.query(Order).filter(Order.order_date == target_date)
    if time_slot:
        query = query.filter(Order.time_slot == time_slot)

    buffer = generate_tally_pdf(query.all(), "Momos", target_date)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=momos-tally-{target_date.isoformat()}.pdf"}
    )

@router.get("/export/tally-rest-pdf")
def export_rest_tally_pdf(order_date: date | None = None, time_slot: str | None = None, db: Session = Depends(get_db)):
    """Tally for everything not already covered by the Chinese / Fast Food / Momos PDFs — currently South Indian and Punjabi & Roti."""
    target_date = order_date or datetime.utcnow().date()
    query = db.query(Order).filter(Order.order_date == target_date)
    if time_slot:
        query = query.filter(Order.time_slot == time_slot)

    rest_categories = ["South Indian", "Punjabi & Roti"]
    buffer = generate_tally_pdf(query.all(), rest_categories, target_date, display_title="South Indian")
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=rest-of-menu-tally-{target_date.isoformat()}.pdf"}
    )