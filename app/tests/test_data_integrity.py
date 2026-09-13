import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "dummy_data.json"


def load_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def index_by(rows, key):
    return {
        row[key]: row
        for row in rows
        if key in row
    }


def test_all_foreign_key_targets_exist():
    data = load_data()

    restaurants = index_by(
        data["restaurantdescriptions"],
        "restaurant_id"
    )

    customers = index_by(
        data["customers"],
        "customer_id"
    )

    bookings = index_by(
        data["bookings"],
        "booking_id"
    )

    menus = index_by(
        data["menu"],
        "menu_id"
    )

    orders = index_by(
        data["orders"],
        "order_id"
    )

    bills = index_by(
        data["bills"],
        "bill_id"
    )

    # Menu → Restaurant
    for menu in data["menu"]:
        assert menu["restaurant_description_id"] in restaurants

    # Booking → Customer + Restaurant
    for booking in data["bookings"]:
        assert booking["customer_id"] in customers
        assert booking["restaurant_id"] in restaurants

    # Order → Customer + Restaurant + Booking
    for order in data["orders"]:
        assert order["customer_id"] in customers
        assert order["restaurant_description_id"] in restaurants

        if order.get("booking_id") is not None:
            assert order["booking_id"] in bookings

    # OrderItem → Order + Menu
    for item in data["orderitems"]:
        assert item["order_id"] in orders
        assert item["menu_id"] in menus

    # Bill → Order
    for bill in data["bills"]:
        assert bill["order_id"] in orders


def test_order_items_belong_to_same_restaurant():
    data = load_data()

    menus = index_by(
        data["menu"],
        "menu_id"
    )

    orders = index_by(
        data["orders"],
        "order_id"
    )

    mismatches = []

    for item in data["orderitems"]:
        order = orders[item["order_id"]]
        menu = menus[item["menu_id"]]

        order_restaurant = order["restaurant_description_id"]
        menu_restaurant = menu["restaurant_description_id"]

        if order_restaurant != menu_restaurant:
            mismatches.append({
                "order_item_id": item["order_item_id"],
                "order_id": item["order_id"],
                "order_restaurant": order_restaurant,
                "menu_id": item["menu_id"],
                "menu_restaurant": menu_restaurant,
            })

    assert not mismatches, (
        f"Found {len(mismatches)} order-item restaurant mismatches. "
        f"Examples: {mismatches[:5]}"
    )


def test_order_booking_customer_consistency():
    data = load_data()

    bookings = index_by(
        data["bookings"],
        "booking_id"
    )

    mismatches = []

    for order in data["orders"]:
        booking_id = order.get("booking_id")

        if booking_id is None:
            continue

        booking = bookings[booking_id]

        if order["customer_id"] != booking["customer_id"]:
            mismatches.append({
                "order_id": order["order_id"],
                "order_customer": order["customer_id"],
                "booking_id": booking_id,
                "booking_customer": booking["customer_id"],
            })

    assert not mismatches, (
        f"Found {len(mismatches)} order-booking customer mismatches. "
        f"Examples: {mismatches[:5]}"
    )


def test_order_booking_restaurant_consistency():
    data = load_data()

    bookings = index_by(
        data["bookings"],
        "booking_id"
    )

    mismatches = []

    for order in data["orders"]:
        booking_id = order.get("booking_id")

        if booking_id is None:
            continue

        booking = bookings[booking_id]

        if (
            order["restaurant_description_id"]
            != booking["restaurant_id"]
        ):
            mismatches.append({
                "order_id": order["order_id"],
                "order_restaurant": order["restaurant_description_id"],
                "booking_id": booking_id,
                "booking_restaurant": booking["restaurant_id"],
            })

    assert not mismatches, (
        f"Found {len(mismatches)} order-booking restaurant mismatches. "
        f"Examples: {mismatches[:5]}"
    )
