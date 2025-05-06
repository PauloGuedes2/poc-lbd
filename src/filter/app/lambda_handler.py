from entrypoints.service.lambda_service import LambdaService


def lambda_handler(event, context):
    service = LambdaService()
    return service.entry_process(event, context)
