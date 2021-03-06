import click
from tabulate import tabulate

from mycloud.mycloudapi import MyCloudRequestExecutor
from mycloud.mycloudapi.requests.drive import UsageRequest


async def print_usage(request_executor: MyCloudRequestExecutor):
    request = UsageRequest()
    response = await request_executor.execute(request)
    formatted = await response.formatted()
    data = []
    for item in formatted:
        data.append([
            item,
            formatted[item]
        ])

    click.echo(tabulate(data, ['Name', 'Value'], tablefmt='fancy_grid'))
