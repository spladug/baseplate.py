import json

import pyramid.testing

from baseplate import RequestContext
from baseplate.frameworks.pyramid import BaseplateRequest
from pyramid.request import Request

from baseplate.testing import make_test_span


class DummyBaseplateRequest(RequestContext, pyramid.testing.DummyRequest):
    def __init__(self, *args, **kwargs):
        context_config = kwargs.pop("context_config", None)
        RequestContext.__init__(self, context_config=context_config)
        pyramid.testing.DummyRequest.__init__(self, *args, **kwargs)

    @property
    def json_body(self):
        try:
            return self.__dict__["json_body"]
        except KeyError:
            return json.loads(self.body)


class FakeRequestFactory:
    def __init__(self, context_config):
        self.context_config = context_config

    def new(self, *args, **kwargs):
        request = DummyBaseplateRequest(
            *args,
            context_config=self.context_config,
            **kwargs,
        )
        request.trace = make_test_span(request)
        return request

    def from_file(self, fp):
        context_config = self.context_config

        request = Request.from_file(fp)
        return self.new(
            body=request.body,
            content_length=request.content_length,
            environ=request.environ,
            headers=request.headers,
            http_version=request.http_version,
            method=request.method,
        )

    def from_path(self, path):
        with open(path) as fp:
            return self.from_file(fp)

    def from_bytes(self, b):
        io = BytesIO(b)
        return self.from_file(io)
