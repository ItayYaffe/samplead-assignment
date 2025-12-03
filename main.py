import asyncio

from configurations.raw_data_config import RawDataConfig
from initiators.inspector_initiator import InspectorInitiator


async def main() -> None:
    """Run selector service"""
    inspector_initiator = InspectorInitiator()
    inspector = inspector_initiator.initiate()
    inspected_prospects = inspector.inspect_users_prospects()
    print(inspected_prospects)

    # await selector.update_selected_prospects(selected_prospects)


if __name__ == "__main__":
    asyncio.run(main())
