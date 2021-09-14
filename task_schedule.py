import sys

sys.path.append(r'D:\www\Apache24\htdocs\armd\tesseract_py\venv\Lib\site-packages')

from py_tesseract import to_start

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=10)
def timed_job():
    text = to_start()
    if text:
        with open("log.txt", "a") as file:
            file.write(text)


sched.start()
