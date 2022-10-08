#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click


@click.group()
def cli():
    pass


@cli.command()
def test():
    """
    打印配置
    :return:
    """
    print(os.path.realpath(__file__))


@cli.command()
@click.option('-n', '--name', help='项目名', required=True)
def init(name):
    """初始化脚手架
    """
    from fx_flask.init.init import InitFlaskProjectProcessor
    processor = InitFlaskProjectProcessor(project_name=name)
    processor.init()


if __name__ == '__main__':
    cli()
