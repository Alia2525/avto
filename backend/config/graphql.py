import strawberry

from maintenance.graphql import Query


schema = strawberry.Schema(query=Query)

