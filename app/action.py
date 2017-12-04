import os
import threading
import string
from .models import DnsForwarder
from flask import render_template
from . import blp


lock = threading.Lock()

@blp.route('/submit', methods=['GET', 'POST'])
def submit_all():
    retcode = 0
    lock.acquire(True)
    try:
        dfs = DnsForwarder.query.all()
        with open("/tmp/iwgweb.conf", "w") as f:
            for df in dfs:
                dnsList = string.split(df.dns)
                f.write("zone \"%s\" IN {\n" % df.dm)
                f.write("type forward;\n")
                f.write("forward %s;\n" % df.typ)
                f.write("forwarders {\n")
                for dns in dnsList:
                    f.write("%s;\n" % dns.strip())
                f.write("};\n")
                f.write("};\n")
            f.close()

        retcode = os.system("rndc reload")
    except Exception,e:
        return e, 500
    lock.release()

    if retcode == 0:
        return "OK"
    else:
        return "Failed"
