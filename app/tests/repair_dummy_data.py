import argparse
import json
import shutil
from collections import defaultdict
from decimal import Decimal
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "dummy_data.json"
BACKUP_FILE = PROJECT_ROOT / "dummy_data.json.backup"


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def normalize(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def similarity_score(old_menu, candidate):
    score = 0

    # Strongest signals
    if old_menu.get("category_id") == candidate.get("category_id"):
        score += 50

    if normalize(old_menu.get("cuisine")) == normalize(candidate.get("cuisine")):
        score += 25

    if normalize(old_menu.get("food_type")) == normalize(candidate.get("food_type")):
        score += 20

    if old_menu.get("is_veg") == candidate.get("is_veg"):
        score += 15

    if normalize(old_menu.get("spice_level")) == normalize(candidate.get("spice_level")):
        score += 5

    return score


def choose_replacement(old_menu, candidates):
    if not candidates:
        return None

    ranked = sorted(
        candidates,
        key=lambda menu: (
            -similarity_score(old_menu, menu),
            menu["menu_id"],
        ),
    )

    return ranked[0]


def money(value):
    return Decimal(str(value))


def main():
    parser = argparse.ArgumentParser(
        description="Repair dummy-data integrity problems."
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually modify dummy_data.json.",
    )

    args = parser.parse_args()

    data = load_data()

    restaurants = {
        r["restaurant_id"]: r
        for r in data.get("restaurantdescriptions", [])
    }

    bookings = {
        b["booking_id"]: b
        for b in data.get("bookings", [])
    }

    menus = {
        m["menu_id"]: m
        for m in data.get("menu", [])
    }

    orders = {
        o["order_id"]: o
        for o in data.get("orders", [])
    }

    menus_by_restaurant = defaultdict(list)

    for menu in menus.values():
        menus_by_restaurant[
            menu["restaurant_description_id"]
        ].append(menu)

    customer_repairs = []
    restaurant_repairs = []
    item_repairs = []

    # ---------------------------------------------------------
    # 1. Repair Order -> Booking relationships
    # ---------------------------------------------------------

    for order in orders.values():

        booking_id = order.get("booking_id")

        if not booking_id:
            continue

        booking = bookings.get(booking_id)

        if not booking:
            continue

        if order["customer_id"] != booking["customer_id"]:
            customer_repairs.append(
                {
                    "order_id": order["order_id"],
                    "old": order["customer_id"],
                    "new": booking["customer_id"],
                }
            )

            if args.apply:
                order["customer_id"] = booking["customer_id"]

        if (
            order["restaurant_description_id"]
            != booking["restaurant_id"]
        ):
            restaurant_repairs.append(
                {
                    "order_id": order["order_id"],
                    "old": order["restaurant_description_id"],
                    "new": booking["restaurant_id"],
                }
            )

            if args.apply:
                order["restaurant_description_id"] = booking[
                    "restaurant_id"
                ]

    # ---------------------------------------------------------
    # 2. Repair OrderItem -> Menu -> Restaurant
    # ---------------------------------------------------------

    for item in data.get("orderitems", []):

        order = orders.get(item["order_id"])

        if not order:
            continue

        current_menu = menus.get(item["menu_id"])

        if not current_menu:
            continue

        required_restaurant = order["restaurant_description_id"]

        current_restaurant = current_menu[
            "restaurant_description_id"
        ]

        if current_restaurant == required_restaurant:
            continue

        candidates = menus_by_restaurant.get(
            required_restaurant,
            []
        )

        replacement = choose_replacement(
            current_menu,
            candidates,
        )

        if replacement is None:
            print(
                f"WARNING: No replacement found for "
                f"OrderItem {item['order_item_id']}"
            )
            continue

        item_repairs.append(
            {
                "order_item_id": item["order_item_id"],
                "order_id": item["order_id"],
                "old_menu_id": item["menu_id"],
                "old_menu_name": current_menu["food_name"],
                "new_menu_id": replacement["menu_id"],
                "new_menu_name": replacement["food_name"],
                "new_price": replacement["price"],
            }
        )

        if args.apply:
            item["menu_id"] = replacement["menu_id"]

            item["unit_price"] = replacement["price"]

            quantity = Decimal(str(item["quantity"]))
            price = money(replacement["price"])

            item["total_price"] = float(quantity * price)

    # ---------------------------------------------------------
    # 3. Backup before saving
    # ---------------------------------------------------------

    if args.apply:
        shutil.copy2(DATA_FILE, BACKUP_FILE)
        save_data(data)

    # ---------------------------------------------------------
    # REPORT
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print(
        "DUMMY DATA REPAIR"
        + (" — APPLIED" if args.apply else " — PREVIEW")
    )
    print("=" * 70)

    print(
        f"\nOrder customer repairs:    {len(customer_repairs)}"
    )

    print(
        f"Order restaurant repairs:  {len(restaurant_repairs)}"
    )

    print(
        f"OrderItem menu repairs:    {len(item_repairs)}"
    )

    print("\nSample OrderItem repairs:")

    for repair in item_repairs[:20]:
        print(
            f"  OrderItem {repair['order_item_id']}: "
            f"{repair['old_menu_id']} "
            f"({repair['old_menu_name']})"
            f" -> "
            f"{repair['new_menu_id']} "
            f"({repair['new_menu_name']})"
        )

    if len(item_repairs) > 20:
        print(
            f"  ... {len(item_repairs) - 20} more"
        )

    if args.apply:
        print(
            f"\nBackup created: {BACKUP_FILE}"
        )
        print(
            "dummy_data.json has been repaired."
        )
    else:
        print(
            "\nPreview only."
        )
        print(
            "No files were modified."
        )
        print(
            "\nIf the proposed changes look reasonable, run:"
        )
        print(
            "python app/tests/repair_dummy_data.py --apply"
        )

    print("=" * 70)


if __name__ == "__main__":
    main()
