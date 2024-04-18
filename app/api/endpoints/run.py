from fastapi import APIRouter
from app.schemas.run import RunRequest,RunResponse
from app.schemas.clean_session import CleanSessionRequest, CleanSessionResponse
import subprocess
from pathlib import Path
from datetime import datetime
import uuid
from app.utils import run_cmd,RunCmd
from app.utils import create_js_file, remove_file

router = APIRouter()

@router.post("/run", response_model=RunResponse)
def run(req_body:RunRequest):
    fp=create_js_file(req_body.script)
    stdout,stderr= run_cmd(RunCmd(
        session_id=req_body.session_id,
        command=rf"npx playwright test {fp}",
        output=req_body.output,
        keyword=req_body.keyword,
        timeout=req_body.timeout,
        ))
    remove_file(fp)
    return RunResponse(result=stdout+'\n'+stderr,session_id=req_body.session_id)


@router.post("/clean_session",response_model=CleanSessionResponse)
def clean_session(req_body:CleanSessionRequest):
    try:
        result=subprocess.check_output("tmux ls -f '#{m:"+req_body.prefix+"*,#{session_name}}' -F '#{session_name}'",shell=True,stdin=subprocess.DEVNULL,stderr=subprocess.STDOUT,text=True)
        result=str(result).split('\n')
        result.remove('')
        subprocess.run("tmux ls -f '#{m:"+req_body.prefix+"*,#{session_name}}' -F '#{session_name}' | xargs -r -n 1 tmux kill-session -t; exit 0",shell=True)
    except:
        result=[]
    return CleanSessionResponse(result=result)
