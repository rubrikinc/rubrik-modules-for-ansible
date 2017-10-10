from rubrik_lib import (
    RubrikLib as RubrikLib,
    models as RbkMods
    )
from rubrik_lib_int import (
    RubrikLib_Int,
    models as RbkModsInt
    )
from msrest import Serializer, Deserializer
from msrest.service_client import ServiceClient
from msrest.authentication import BasicAuthentication,BasicTokenAuthentication
import inspect


def create(host, user, password):
    """
    Create RubrikClient
    """
    base_url = format("https://%s/api" % host)
    _Rubrik = type('Rubrik', (RubrikLib, RubrikLib_Int), dict())
    _rbkModels = {k: v for k, v in RbkMods.__dict__.items() if isinstance(v, type)}
    _rbkModelsInt = {k: v for k, v in RbkModsInt.__dict__.items() if isinstance(v, type)}
    _RubrikModels = dict(_rbkModelsInt, **_rbkModels)
    _auth = BasicAuthentication(
        user,
        password
    )
    print format("Base URL: %s" % base_url)
    self = _Rubrik(base_url)

    self._serialize = Serializer(_RubrikModels)
    self._deserialize = Deserializer(_RubrikModels)
    self._client.config.connection.verify = False
    self._client.creds = _auth

    token = self.create_session().token
    print token
    auth = BasicTokenAuthentication(token={"access_token":token})
    self._client = ServiceClient(auth, self.config)
    print inspect.getmembers(self)

    return self
