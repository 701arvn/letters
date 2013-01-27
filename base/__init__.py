from hashlib import md5
from datetime import datetime

def get_uniq_hash(request):
    uniq_hash = md5(str(datetime.now()) + request.user.username).hexdigest()[:7]
    return uniq_hash
