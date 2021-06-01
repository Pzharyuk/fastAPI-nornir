from fastapi import FastAPI
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F


app = FastAPI()



@app.get("/inventory")
def inventory():
    nr = InitNornir("config.yaml")
    my_list = nr.inventory.hosts.values()
    response =[]
    for data in my_list:
        response.append(dict(
            device = f"{data}",
            ip_address = data.hostname,
            device_platform = data.platform
            )
        )
    return response

@app.get("/running-config")
def running_config():
    nr = InitNornir("config.yaml")
    results = nr.run(task=send_command, command="show run")
    my_list = [v.scrapli_response.result for v in results.values()]
    run_config = []
    for config in my_list:
        run_config.append(dict(
            running_config = f"{config}".replace("\n", " ")
        )
                          )
    return run_config


@app.get("/version")
def version():
    nr = InitNornir(config_file="config.yaml")
    results = nr.run(task=send_command, command="show version")
    my_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
    show_version = []
    for data in my_list:
        show_version.append(
            dict(
                device = data['version']['hostname'],
                version = data['version']['version_short'],
                uptime = data['version']['uptime'],
                serial_number = data['version']['chassis_sn']
            )
        )
    return show_version


@app.get("/version/{hostname}")
def get_host_version(hostname):
    nr = InitNornir(config_file="config.yaml")
    filtered = nr.filter(F(hostname=hostname))
    results = filtered.run(task=send_command, command="show version")
    my_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
    show_version = []
    for data in my_list:
        show_version.append(
            dict(
                device = data['version']['hostname'],
                version = data['version']['version_short'],
                uptime = data['version']['uptime'],
                serial_number = data['version']['chassis_sn']
            )
        )
    return show_version

# @app.route("/greetings")
# def say_hello():
#     return "Hello There"
