from aws_cdk import (
    aws_lambda as _lambda,
    Stack,
)
from constructs import Construct
import dotenv
import os


class AuthorizationServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dotenv.load_dotenv()
        account_name = 'ukrainskyi_vitalii'
        secret_key = os.getenv(account_name)

        _lambda.Function(self, 'basicAuthorizer',
                         runtime=_lambda.Runtime.PYTHON_3_11,
                         code=_lambda.Code.from_asset('authorization_service/lambda_func/'),
                         handler='basic_authorizer.lambda_handler',
                         environment={
                             account_name: secret_key
                         },
                         function_name='AuthFunction'
                         )

        # use authorization_token = dWtyYWluc2t5aV92aXRhbGlpPVRFU1RfUEFTU1dPUkQ=