import uuid


class IdGenerator:
    def get_id(self, prefix = "") -> str:
        id = str(uuid.uuid4())
        return prefix + id