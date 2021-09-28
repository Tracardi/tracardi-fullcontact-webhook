from typing import Optional

import aiohttp
import asyncio
from aiohttp import ClientConnectorError
from tracardi.service.storage.driver import storage
from tracardi_dot_notation.dict_traverser import DictTraverser
from tracardi_dot_notation.dot_accessor import DotAccessor
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result

from tracardi_fullcontact_webhook.model.configuration import Configuration
from tracardi_fullcontact_webhook.model.full_contact_source_configuration import FullContactSourceConfiguration


class FullContactAction(ActionRunner):

    @staticmethod
    async def build(**kwargs) -> 'FullContactAction':
        config = Configuration(**kwargs)
        source = await storage.driver.resource.load(config.source.id)
        source = FullContactSourceConfiguration(**source.config)
        return FullContactAction(config, source)

    def __init__(self, config: Configuration, source: Optional[FullContactSourceConfiguration]):
        self.source = source
        self.config = config

    async def run(self, payload):
        dot = DotAccessor(self.profile, self.session, payload, self.event, self.flow)

        try:

            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:

                mapper = DictTraverser(dot)
                payload = mapper.reshape(reshape_template=self.config.pii.dict())
                print(self.config.pii.dict())
                print(payload)

                async with session.request(
                        method="POST",
                        headers={
                            "Content-type": "application/json",
                            "Authorization": f"Bearer {self.source.token}"
                        },
                        url='https://api.fullcontact.com/v3/person.enrich',
                        json=payload
                ) as response:
                    # todo add headers and cookies
                    result = {
                        "status": response.status,
                        "body": await response.json()
                    }

                    if response.status in [200, 201, 202, 203, 204]:
                        return Result(port="payload", value=result), Result(port="error", value=None)
                    else:
                        return Result(port="payload", value=None), Result(port="error", value=result)

        except ClientConnectorError as e:
            return Result(port="payload", value=None), Result(port="error", value=str(e))

        except asyncio.exceptions.TimeoutError:
            return Result(port="payload", value=None), Result(port="error", value="FullContact webhook timed out.")


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_fullcontact_webhook.plugin',
            className='FullContactAction',
            inputs=["payload"],
            outputs=['payload', "error"],
            version='0.1.3',
            license="MIT",
            author="Risto Kowaczewski",
            init={
                "source": {
                    "id": None
                },
                "pii": {
                    "email": None,
                    "emails": [],
                    "phone": None,
                    "phones": [],
                    "location": None,
                    "name": None
                }
            }
        ),
        metadata=MetaData(
            name='Full contact webhook',
            desc='This plugin gets data about the provided e-mail from FullContact service.',
            type='flowNode',
            width=200,
            height=100,
            icon='fullcontact',
            group=["Connectors"]
        )
    )
