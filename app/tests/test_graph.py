from app.database import SessionLocal
from app.ai.graph.service import RestaurantGraphService


def main():
    db = SessionLocal()

    try:
        print("=" * 50)
        print("Initializing RestaurantGraphService...")

        graph_service = RestaurantGraphService(db)

        print("✅ Graph compiled successfully!")

        print("=" * 50)
        print("Executing graph...")

        response = graph_service.run(
            customer_id=1,
            user_message="Hello"
        )

        print("=" * 50)
        print("Graph executed successfully!")
        print("Response:")
        print(response)

    except Exception as e:
        print("=" * 50)
        print("❌ ERROR")
        raise e

    finally:
        db.close()


if __name__ == "__main__":
    main()
