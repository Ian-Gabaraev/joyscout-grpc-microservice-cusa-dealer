from concurrent import futures

import grpc
import grpc.experimental.aio

import asyncio

from identifier_pb2 import (
    Identifier,
    IdentifierRequest,
    IdentifierResponse
)

from psstore4ru.core.asynchronous import PSStore

import identifier_pb2_grpc


class PSGameIdentifiersService(
    identifier_pb2_grpc.IdentifiersServicer
):
    async def GetIdentifiers(self, request, context):

        result = await PSStore.get_all_games_links(iterations=2)

        ids = [
            Identifier(identifier=cusa) for cusa in result
        ]

        return IdentifierResponse(identifiers=ids)


async def serve():

    grpc.experimental.aio.init_grpc_aio()
    server = grpc.experimental.aio.server()
    server.add_insecure_port("[::]:50051")
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    identifier_pb2_grpc.add_IdentifiersServicer_to_server(
        PSGameIdentifiersService(), server
    )

    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":

    asyncio.run(serve())
