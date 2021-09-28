import asyncio

from tracardi_fullcontact_webhook.model.configuration import Configuration
from tracardi_fullcontact_webhook.model.full_contact_source_configuration import FullContactSourceConfiguration
from tracardi_fullcontact_webhook.plugin import FullContactAction


async def main():
    config = Configuration(**{
        "source": {
            "id": "some-id"
        },
        "pii": {
            "emails": ["kazi@gmail.com"]
        }
    })

    source = FullContactSourceConfiguration(token="***")

    plugin = FullContactAction(config, source)
    result = await plugin.run({})
    print(result)


asyncio.run(main())
