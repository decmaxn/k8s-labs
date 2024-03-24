#!/usr/bin/env python3

from aws_cdk import core

from vpc.vpc_stack_constructor import VpcStackConstructor

from utils.config_loader import ConfigLoader
import os
from utils.file_reader import FileReader

config = ConfigLoader(config_path=os.path.join("resource", "config", "config.json")).fetch_config_from_json_file()

app = core.App()
env = core.Environment(account=config["ACCOUNT"], region=config["REGION"])

vpc_stack = VpcStackConstructor(scope=app, env=env, config=config).execute()

app.synth()