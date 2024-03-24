from aws_cdk.core import Construct
from aws_cdk.core import Environment
import os
from aws_cdk import core
from aws_cdk.aws_s3_assets import Asset


class DeploymentAssetStack(core.Stack):
    def __init__(
        self, scope: core.Construct, id: str,
        public_key_path: str,
        private_key_path: str,
        create_user_script_path: str,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        self.public_key_asset = self.__create_asset(id="public_key_asset", path=public_key_path)
        self.private_key_asset = self.__create_asset(id="private_key_asset", path=private_key_path)
        self.create_user_script_asset = self.__create_asset(id="create_user_script_asset", path=create_user_script_path)


    def __create_asset(self, id: str, path: str):
        return Asset(scope=self, id=id, path=path)


class DeploymentAssetStackConstructor:
    def __init__(self, scope: Construct, env: Environment, config: dict):
        self.__scope = scope
        self.__env = env
        self.__config = config

    def execute(self):

        return DeploymentAssetStack(
            scope=self.__scope,
            id="{}Assets".format(self.__config["ENVIRONMENT_NAME"]),
            env=self.__env,

            private_key_path=os.path.join("resource", "key", "id_rsa"),
            public_key_path=os.path.join("resource", "key", "id_rsa.pub"),
            create_user_script_path=os.path.join("resource", "script", "create_user.sh")
        )