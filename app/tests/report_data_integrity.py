import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "dummy_data.json"


def index_by(rows, key):
    return {row[key]: row for row in rows if key in row}


def main():
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)

    menus = index_by(data["menu"], "menu_id")
    orders = index_by(data["orders"], "order_id")
    bookings = index_by(data["bookings"], "booking_id")

    order_item_mismatches = []
    booking_customer_mismatches = []
    booking_restaurant_mismatches = []

    # ---------------------------------------------------------
    # 1. ORDER ITEM → RESTAURANT
    # ---------------------------------------------------------

    for item in data["orderitems"]:
        order = orders[item["order_id"]]
        menu = menus[item["menu_id"]]

        order_restaurant = order["restaurant_description_id"]
        menu_restaurant = menu["restaurant_description_id"]

        if order_restaurant != menu_restaurant:
            order_item_mismatches.append({
                "order_item_id": item["order_item_id"],
                "order_id": item["order_id"],
                "order_restaurant": order_restaurant,
                "menu_id": item["menu_id"],
                "menu_restaurant": menu_restaurant,
            })

    # ---------------------------------------------------------
    # 2. ORDER → BOOKING CUSTOMER
    # ---------------------------------------------------------

    for order in data["orders"]:
        booking_id = order.get("booking_id")

        if booking_id is None:
            continue

        booking = bookings[booking_id]

        if order["customer_id"] != booking["customer_id"]:
            booking_customer_mismatches.append({
                "order_id": order["order_id"],
                "order_customer": order["customer_id"],
                "booking_id": booking_id,
                "booking_customer": booking["customer_id"],
            })

    # ---------------------------------------------------------
    # 3. ORDER → BOOKING RESTAURANT
    # ---------------------------------------------------------

    for order in data["orders"]:
        booking_id = order.get("booking_id")

        if booking_id is None:
            continue

        booking = bookings[booking_id]

        if (
            order["restaurant_description_id"]
            != booking["restaurant_id"]
        ):
            booking_restaurant_mismatches.append({
                "order_id": order["order_id"],
                "order_restaurant": order["restaurant_description_id"],
                "booking_id": booking_id,
                "booking_restaurant": booking["restaurant_id"],
            })

    # ---------------------------------------------------------
    # REPORT
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("RESTAURANT SYSTEM DATA INTEGRITY REPORT")
    print("=" * 70)

    print(
        f"\n1. OrderItem → Restaurant mismatches: "
        f"{len(order_item_mismatches)}"
    )

    for row in order_item_mismatches:
        print(row)

    print(
        f"\n2. Order → Booking customer mismatches: "
        f"{len(booking_customer_mismatches)}"
    )

    for row in booking_customer_mismatches:
        print(row)

    print(
        f"\n3. Order → Booking restaurant mismatches: "
        f"{len(booking_restaurant_mismatches)}"
    )

    for row in booking_restaurant_mismatches:
        print(row)

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
