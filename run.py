import asyncio
from app import App

auto_scaling_group = "os.environ['AUTO_SCALING_GROUP']"
region = "os.environ['REGION']"
accessKeyId = "os.environ['ACCESS_KEY']"
secretAccessKey = "os.environ['SECRET_KEY']"
sessionToken = "os.environ['SESSION_TOKEN']"
env = "dev" #os.environ['ENV']

class Run:
    def __init__(self):        
        #self._app = App(auto_scaling_group, region, accessKeyId, secretAccessKey, sessionToken)   
        self._app = App("engine-asg", "sa-east-1")
        self._localApp = App("engine-asg", "sa-east-1") 

    async def auto_scaling_check(self):
        while True:
            print("Executing Analysis on Auto Scaling Group "+auto_scaling_group)
            self._app.create_files()
            self._app.read_instances()
            print("Analysis Completed")
            print("----------------------------------")
            await asyncio.sleep(20)

    async def auto_scaling_check_local(self):
        while True:
            print("Executing Analysis on Auto Scaling Group "+"engine-asg")
            self._localApp.create_files()
            self._localApp.read_instances()
            print("Analysis Completed")
            print("----------------------------------")
            await asyncio.sleep(20)

if __name__ == '__main__':
    run = Run()
    if env == 'dev':
        print("----------------------------------")
        loop = asyncio.get_event_loop()
        try:
            asyncio.ensure_future(run.auto_scaling_check_local())
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print("Closing Loop")
            loop.close()
    else:
        print("----------------------------------")
        loop = asyncio.get_event_loop()
        try:
            asyncio.ensure_future(run.auto_scaling_check())
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print("Closing Loop")
            loop.close()
