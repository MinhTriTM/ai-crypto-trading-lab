"""IDs."""
import uuid, time, random, string

def gen_id(prefix: str = "", length: int = 8) -> str:
    return prefix + uuid.uuid4().hex[:length].upper()

def gen_branch_id() -> str:
    return "#" + uuid.uuid4().hex[:6].upper()

def gen_account_id() -> str:
    return "ACC" + uuid.uuid4().hex[:6].upper()

def gen_order_id() -> str:
    return "ORD" + str(int(time.time()*1000))[-8:] + ''.join(random.choices(string.ascii_uppercase, k=2))
