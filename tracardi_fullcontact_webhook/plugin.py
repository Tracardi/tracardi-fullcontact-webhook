from typing import Optional

from fullcontact import FullContactClient
from tracardi.service.storage.driver import storage
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

        pii = dot[self.config.pii]
        client = FullContactClient(self.source.token)
        async_result = client.person.enrich_async(**pii.dict())
        response = async_result.result()
        if response.is_successful:
            return Result(port="payload", value=response.get_details())
        return Result(port="payload", value={})


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_fullcontact_webhook.plugin',
            className='FullContactAction',
            inputs=["payload"],
            outputs=['payload'],
            version='0.1.2',
            license="MIT",
            author="Risto Kowaczewski",
            init={
                "source": {
                    "id": None
                },
                "pii": {
                    "email": None,
                    "phone": None
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
