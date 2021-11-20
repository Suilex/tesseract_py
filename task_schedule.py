import sys

sys.path.append(r'D:\www\Apache24\htdocs\armd\tesseract_py\venv\Lib\site-packages')

from py_tesseract import main

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=10)
def timed_job():
    text = main()
    if text:
        with open("log.txt", "a") as file:
            file.write(text)


sched.start()
