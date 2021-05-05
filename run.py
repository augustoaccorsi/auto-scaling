import asyncio, datetime, sys
from app import App
import weakref

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
        self._localApp.describe()

    def revew_local(self):
        self._localApp.commit_suicide()
        self._localApp = App("engine-asg", "sa-east-1")

    async def auto_scaling_check(self):
        count = 0
        while True:
            count +=1
            print("Executing Analysis "+str(count)+" on Auto Scaling Group "+auto_scaling_group+" at "+datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S'))
            print()
            self._app.read_instances()
            print("Analysis Completed")
            print("----------------------------------")
            await asyncio.sleep(300)

    async def auto_scaling_check_local(self):
        count = 0
        while True:
            count +=1
            print("Executing Analysis "+str(count)+" on Auto Scaling Group "+"engine-asg"+" at "+datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S'))
            print()
            self._localApp.read_instances()
            print("Analysis Completed")
            print("----------------------------------")
            try:
                await asyncio.sleep(int(sys.argv[1]))
            except:
                try:
                    await asyncio.sleep(int(sys.argv[1]))
                except:
                    if self._localApp._cooldown == False and self._localApp._timeseries == True and count >= 40:
                        await asyncio.sleep(5)
                    else:
                        await asyncio.sleep(60)

if __name__ == '__main__':
    run = Run()
    print("Starting Event Loop")
    if env == 'dev':
        loop = asyncio.get_event_loop()
        try:
            print("----------------------------------")
            asyncio.ensure_future(run.auto_scaling_check_local())
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print("Closing Event Loop")
            loop.close()
    else:
        loop = asyncio.get_event_loop()
        try:
            print("----------------------------------")
            asyncio.ensure_future(run.auto_scaling_check())
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print("Closing Loop")
            loop.close()
