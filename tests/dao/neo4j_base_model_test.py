from dataclasses import dataclass
from src.dao.base_dao import neo4j_base_dao

# Test class which inherits the base class
@dataclass
class MockModel(neo4j_base_dao.Neo4jBaseModel):
  name: str

class TestBaseModelHelpers():

  def test_get_properties(self):
    # Arrange
    instance = MockModel(**{ "name": "John" })

    # Act
    data = instance.getProperties()

    # Assert
    assert data == dict(name="John")

  def test_iter(self):
    # Arrange
    instance = MockModel(**{ "name": "John" })

    # Act
    data = instance.__iter__()
    firstProperty = data.__next__()

    # Assert
    assert firstProperty == 'John'