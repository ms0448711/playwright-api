from fastapi import APIRouter
from app.schemas import *
import subprocess
import traceback
from app.utils import run_cmd,RunCmd
from app.utils import create_js_file, remove_file

router = APIRouter()

@router.post("/run_playwright", response_model=RunResponse)
def run(req_body:RunRequest):
    try:
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
    except Exception as e:
        print(type(e),':',traceback.format_exc())
        return e
    


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

@router.get("/session", response_model=GetSessionResponse)
def get_session(req_body:GetSessionRequest):
    try:
        result=subprocess.check_output("tmux ls -f '#{m:"+req_body.prefix+"*,#{session_name}}' -F '#{session_name}'",shell=True,stdin=subprocess.DEVNULL,stderr=subprocess.STDOUT,text=True)
        result=str(result).split('\n')
        result.remove('')
    except:
        result=[]
    return GetSessionResponse(result=result)


