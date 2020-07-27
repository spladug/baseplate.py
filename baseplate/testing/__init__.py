from baseplate import RequestContext
from baseplate import ServerSpan
from baseplate import TraceInfo


def make_test_span(context):
    trace_info = TraceInfo.new()
    return ServerSpan(
        trace_id=trace_info.trace_id,
        parent_id=trace_info.parent_id,
        span_id=trace_info.span_id,
        sampled=trace_info.sampled,
        flags=trace_info.flags,
        name="test",
        context=context,
    )


class FakeContextFactory:
    def __init__(self, context_config):
        self.context_config = context_config

    def new(self):
        context = RequestContext(context_config=self.context_config)
        context.trace = make_test_span(context)
        return context
