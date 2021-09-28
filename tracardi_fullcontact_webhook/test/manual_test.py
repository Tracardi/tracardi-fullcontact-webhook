from tracardi.domain.context import Context
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.profile import Profile
from tracardi.domain.session import Session
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_fullcontact_webhook.plugin import FullContactAction

init = {
    "source": {
        "id": "f634f001-2580-4b2e-a7bb-df099ba9afbd"
    },
    "pii": {
        "email": "kazi@gmail.com"
    }
}
payload = {}
profile = Profile(id="profile-id")
event = Event(id="event-id",
              type="event-type",
              profile=profile,
              session=Session(id="session-id"),
              source=Entity(id="source-id"),
              context=Context())

result = run_plugin(FullContactAction, init, payload, profile)

print("OUTPUT:", result.output)
print("PROFILE:", result.profile)
