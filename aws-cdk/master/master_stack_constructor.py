from utils.instance_constructor import PrivateInstanceConstructor
from aws_cdk.core import Construct
from aws_cdk.core import Stack
from aws_cdk.core import Environment
from vpc.vpc_stack_constructor import VpcStack

class MasterStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        config: dict,
        vpc_stack: VpcStack,
        # deployment_asset_stack: DeploymentAssetStack,
        # security_group: SecurityGroup,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        self.master_instance = PrivateInstanceConstructor(
            scope=self,
            config=config,
            instance_id="master",
            vpc_stack=vpc_stack,
        ).execute()



class MasterStackConstructor:
    def __init__(
        self,
        scope: Construct,
        env: Environment,
        config: dict,

        vpc_stack: VpcStack,
    ):
        self.__scope = scope
        self.__env = env
        self.__config = config

        self.__vpc_stack = vpc_stack

    def execute(self):
        return MasterStack(
            scope=self.__scope,
            env=self.__env,
            id="{}Master".format(self.__config["ENVIRONMENT_NAME"]),

            config=self.__config,

            vpc_stack=self.__vpc_stack,
        )