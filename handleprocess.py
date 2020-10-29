import psutil
import os

def kill_process_tree(pid,sig,include_parent=True):
    if pid==os.getpid():#我不能杀掉我自己
        raise RuntimeError("I can't kill myself!")
    parent=psutil.Process(pid)
    children=parent.children(recursive=True)
    if include_parent:
        children.append(parent)
    for p in children:
        p.send_signal(sig)

