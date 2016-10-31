#!/usr/bin/env python

import asyncio, asyncssh, sys
import concurrent.futures

executor = concurrent.futures.ProcessPoolExecutor()
loop = asyncio.get_event_loop()
loop.set_default_executor(executor)

import config, biothings
biothings.config_for_app(config)

import dataload
import biothings.dataload.uploader as uploader
import biothings.dataload.dumper as dumper
umanager = uploader.SourceManager(loop)
dmanager = dumper.SourceManager(loop)
umanager.register_sources(dataload.__sources_dict__)
dmanager.register_sources(dataload.__sources_dict__)

COMMANDS = {
        "dm" : dmanager,
        "dump" : dmanager.dump_src,
        "dump_all" : dmanager.dump_all,
        # upload commands
        "um" : umanager,
        "upload" : umanager.upload_src,
        "upload_all": umanager.upload_all,
        }

passwords = {
        'guest': '', # guest account with no password
        }

from biothings.utils.hub import start_server

server = start_server(passwords=passwords,port=8022,commands=COMMANDS)

try:
    loop.run_until_complete(server)
except (OSError, asyncssh.Error) as exc:
    sys.exit('Error starting server: ' + str(exc))

loop.run_forever()

