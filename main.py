import asyncio

from initiators.inspector_initiator import InspectorInitiator


async def main() -> None:
    """Run selector service"""
    inspector_initiator = InspectorInitiator()
    inspector = inspector_initiator.initiate()
    inspected_prospects = inspector.inspect_users_prospects()
    print(inspected_prospects)

    # Insert to postgres
    await inspector.insert_inspected_prospects(inspected_prospects)


if __name__ == "__main__":
    asyncio.run(main())
