#!/usr/bin/env python3

from aws_cdk import core

from vpc.vpc_stack_constructor import VpcStackConstructor
from cluster_security_group.cluster_security_group_stack_constructor import ClusterSecurityGroupStackConstructor
from deployment_asset.deployment_asset_stack_constructor import DeploymentAssetStackConstructor
from master.master_stack_constructor import MasterStackConstructor

from utils.config_loader import ConfigLoader
import os
from utils.file_reader import FileReader

config = ConfigLoader(config_path=os.path.join("resource", "config", "config.json")).fetch_config_from_json_file()

app = core.App()
env = core.Environment(account=config["ACCOUNT"], region=config["REGION"])

vpc_stack = VpcStackConstructor(scope=app, env=env, config=config).execute()
cluster_security_group_stack = ClusterSecurityGroupStackConstructor(
    scope=app, env=env, config=config, vpc_stack=vpc_stack
).execute()
deployment_asset_stack = DeploymentAssetStackConstructor(scope=app, env=env, config=config).execute()

master_stack = MasterStackConstructor(
    scope=app,
    env=env,
    config=config,

    vpc_stack=vpc_stack,
    deployment_asset_stack=deployment_asset_stack,
).execute()

app.synth()