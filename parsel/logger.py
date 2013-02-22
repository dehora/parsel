#!/usr/bin/env python


import re
import shlex
import subprocess
import sys
import time
import exceptions

from exceptions import SystemExit

# Based on ComboAMI, see https://github.com/riptano/ComboAMI

configfile = '/var/log/parsel/parsel.log'


def exit_path(config, instance_data, errorMsg, append_msg=False):
    if not append_msg:
        p = re.search('(-p\s+)(\S*)', str(instance_data['user-data']))
        if p:
            instance_data['user-data'] = instance_data['user-data'].replace(p.group(2), '****')
        p = re.search('(--password\s+)(\S*)', instance_data['user-data'])
        if p:
            instance_data['user-data'] = instance_data['user-data'].replace(p.group(2), '****')
        append_msg = " Aborting installation.\n\nPlease verify your settings:\n{0}".format(instance_data['user-data'])
    errorMsg += append_msg

    error(errorMsg)
    config.set_config("instance", "Error", errorMsg)

    raise exceptions.AttributeError


def log(text):
    with open(configfile, "a") as f:
        f.write(text + "\n")
        print text


def exe(command, log=True, expectError=False, shellEnabled=False):
    if shellEnabled:
        process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    else:
        process = subprocess.Popen(shlex.split(command), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = process.communicate()
    t = time.strftime("%m/%d/%y-%H:%M:%S", time.localtime())
    if log:
        if len(output[0]) > 0:
            log(t + ' ' + command + ":\n" + output[0])
        elif len(output[1]) > 0:
            if expectError:
                log(t + ' ' + command + ":\n" + output[1])
            else:
                log(t + ' ' + command + ":\n" + output[1])
    if not log or (len(output[0]) == 0 and len(output[1]) == 0):
        log(t + ' ' + command)
    return output


def pipe(command1, command2, log=True):
    p1 = subprocess.Popen(shlex.split(command1), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(shlex.split(command2), stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    read = p2.stdout.read()
    t = time.strftime("%m/%d/%y-%H:%M:%S", time.localtime())
    if not log:
        read = ""
    if len(read) > 0:
        log(t + ' ' + command1 + ' | ' + command2 + ":\n" + read)
    else:
        log(t + ' ' + command1 + ' | ' + command2)
    output = p2.communicate()[0]
    if log:
        if read and len(read) > 0:
            log(t + ' ' + command1 + ' | ' + command2 + ":\n" + read)
        if output and len(output[0]) > 0:
            log(t + ' ' + command1 + ' | ' + command2 + ":\n" + output[0])
        if output and len(output[1]) > 0:
            log(t + ' ' + command1 + ' | ' + command2 + ":\n" + output[1])
        return output


def debug(infotext):
    log('[DEBUG] ' + str(infotext))


def info(infotext):
    log('[INFO] ' + str(infotext))


def warn(infotext):
    log('[WARN] ' + str(infotext))


def error(infotext):
    log('[ERROR] ' + str(infotext))


def exception(filename):
    if type(sys.exc_info()[1]) == SystemExit:
        return

    log("[ERROR] Exception seen in %s:" % filename)
    import traceback

    log(traceback.format_exc())
    sys.exit(1)
