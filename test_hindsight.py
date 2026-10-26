import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)

bank_id = os.getenv("HINDSIGHT_BANK_ID")

try:
    client.retain(
        bank_id=bank_id,
        content=(
            "Demo patient DR-TEST-001 had a previous "
            "screening marked as Non-Referable DR. "
            "This is synthetic demo data, not a real patient."
        ),
    )
    print("Memory retained successfully.")

    result = client.recall(
        bank_id=bank_id,
        query="What was the previous screening result for DR-TEST-001?",
    )

    print("\nRecalled memories:")
    for memory in result.results:
        print("-", memory.text)

except Exception as e:
    print("Hindsight test failed:", type(e).__name__, str(e)[:500])

finally:
    client.close()