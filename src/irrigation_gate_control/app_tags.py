from pydoover.tags import Tag, Tags


class IrrigationGateControlTags(Tags):
    gate_state = Tag("string", default="off")
