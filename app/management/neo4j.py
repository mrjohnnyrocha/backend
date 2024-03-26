# from django.core.management.base import BaseCommand
# from loka.services import Neo4jService
# from loka.ml import extract_entities_from_markdown

# class Command(BaseCommand):
#     help = 'Import documentation into Neo4j'

#     def handle(self, *args, **kwargs):
#         entities = extract_entities_from_markdown('/path/to/documentation.md')
#         neo4j_service = Neo4jService('bolt://localhost:7687', 'neo4j', 'password')
#         for entity in entities:
#             neo4j_service.create_service(entity)
#         neo4j_service.close()
