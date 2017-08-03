
import docker
client = docker.from_env()

from docker import client
cli = Client(base_url='unix://var/run/docker.sock')
print cli.containers()
