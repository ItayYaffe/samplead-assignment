import asyncio

from initiators.inspector_initiator import InspectorInitiator


async def main() -> None:
    """Run selector service"""
    inspector_initiator = InspectorInitiator()
    inspector = inspector_initiator.initiate()
    inspected_prospects = inspector.inspect_users_prospects()

    # Exporting the result to csv
    inspector.export_inspected_prospects_to_csv(inspected_prospects)

    # I encountered issues running Docker on my machine, so I wasn’t able to fully validate this function. :(
    # await inspector.insert_inspected_prospects_to_postgres(inspected_prospects)


if __name__ == "__main__":
    asyncio.run(main())
