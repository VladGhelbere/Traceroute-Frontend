from app import web
from flask import render_template,redirect,url_for,request,session,abort
import hashlib
import os
from app.models import db
import subprocess
import json
@web.route("/")

@web.route("/index", methods=['GET','POST'])
def index():

    return render_template('index.html')

@web.route("/trace", methods=['GET','POST'])
def trace():
    if request.method=="POST":
        from app.models import TraceRoute_Table
        hostname=request.form.get('hostname')
        hops=request.form.get('hops')
        proc = subprocess.Popen(["traceroute","-F","-q 1","-m",hops, hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err= proc.communicate()

        print(out)
        result=""
        data = {}
        index = 0
        if err != "":
            data = err
        else:
            for line in out.splitlines():
                if index == 0:
                    data["title"] = line
                else:
                    if line.split()[1] == "*":
                        data["result"+str(index)] = {"id":line.split()[0],"hostname":"*","ipaddress":"*","time":"*","unit":"ms"}
                        result = TraceRoute_Table(hostname="*",ipaddress="*",time="* ms")
                    else:
                        data["result"+str(index)] = {"id":line.split()[0],"hostname":line.split()[1],"ipaddress":line.split()[2],"time":line.split()[3],"unit":line.split()[4]}
                        result = TraceRoute_Table(hostname=line.split()[1],ipaddress=line.split()[2],time=line.split()[3]+" ms")
                    db.session.add(result)
                    db.session.commit()
                index +=1
        return_data = json.dumps(data)
    return return_data
