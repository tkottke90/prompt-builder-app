from src.dao.base_dao import neo4j_base_dao

class TestMethod_Conditional_Creation():

  def test_with_id(self):
    # Arrange
    mockSchemaName = 'Test'
    instance = neo4j_base_dao.Neo4JBaseDao(name=mockSchemaName)

    # Act
    queryStr, params = instance._createConditional('n', { "id": 1 })

    # Assert
    assert params == dict(id=1)
    assert queryStr == "id(n) = $id"

  def test_with_name(self):
    # Arrange
    mockSchemaName = 'Test'
    instance = neo4j_base_dao.Neo4JBaseDao(name=mockSchemaName)

    # Act
    queryStr, params = instance._createConditional('n', { "name": "John" })

    # Assert
    assert params == dict({ "name": "John" })
    assert queryStr == "n.name = $name"

  def test_with_none_value(self):
    """
    We expect that when key has a None value, that it should be ignored and not included in the schema.
    """

    # Arrange
    mockSchemaName = 'Test'
    instance = neo4j_base_dao.Neo4JBaseDao(name=mockSchemaName)

    # Act
    queryStr, params = instance._createConditional('n', { "name": "John", "age": None })

    # Assert
    assert params == dict({ "name": "John" })
    assert queryStr == "n.name = $name"

class TestMethod_ID_Conditional_Creation():

  def test_with_id(self):
    # Arrange
    mockSchemaName = 'Test'
    instance = neo4j_base_dao.Neo4JBaseDao(name=mockSchemaName)

    # Act
    queryStr, params = instance._createIdConditional('n', 1)

    # Assert
    assert params == dict(id=1)
    assert queryStr == "id(n) = $id"

class TestMethod_Create_Node_Notation():
  
  def test_with_default(self):
    """
    The default behavior for this function is to return a lowercased version of the `_nodeType` (Neo4j suggests
    that node types should be Pascal Case). Node type is indented to populate the nodeType position in the query
    string.
    """

    # Arrange
    mockSchemaName = 'Test'
    instance = neo4j_base_dao.Neo4JBaseDao(name=mockSchemaName)

    # Act
    variableName, querySelector = instance._createNodeNotation()

    # Assert
    assert variableName == mockSchemaName.lower()
    assert querySelector == r'(test:Test)'

  def test_with_argument(self):
    """
    We want to be able to input a different variable name incase we need to do more complex queries in the future.
    """

    # Arrange
    mockSchemaName = 'Test'
    instance = neo4j_base_dao.Neo4JBaseDao(name=mockSchemaName)

    # Act
    variableName, querySelector = instance._createNodeNotation('n')

    # Assert
    assert variableName == 'n'
    assert querySelector == r'(n:Test)'

class TestMethod_Create_Params():
  
  def test_with_single_param(self):
    # Arrange
    mockSchemaName = 'Test'
    instance = neo4j_base_dao.Neo4JBaseDao(name=mockSchemaName)

    # Act
    paramStr = instance._createParams({ "name": "John" })

    # Assert
    assert paramStr == r'{name: $name}'

  def test_with_multiple(self):
    # Arrange
    mockSchemaName = 'Test'
    instance = neo4j_base_dao.Neo4JBaseDao(name=mockSchemaName)

    # Act
    paramStr = instance._createParams({ "name": "John", "age": 40 })

    # Assert
    assert paramStr == r'{name: $name, age: $age}'

class TestMethod_Create_Return_String():
  
  def test_without_select(self):
    # Arrange
    mockSchemaName = 'Test'
    instance = neo4j_base_dao.Neo4JBaseDao(name=mockSchemaName)

    # Act
    returnStr = instance._createReturnStr('n')

    # Assert
    assert returnStr == r'n{.*, id: id(n)}'

  def test_with_select(self):
    # Arrange
    mockSchemaName = 'Test'
    instance = neo4j_base_dao.Neo4JBaseDao(name=mockSchemaName)

    # Act
    returnStr = instance._createReturnStr('n', ['name', 'age'])

    # Assert
    assert returnStr == r'n{.name, .age, id: id(n)}'

class TestMethod_Parse_Results():
  
  def test_should_return_value_in_response(self):
    # Arrange
    mockSchemaName = 'Test'
    mockData = dict(n=dict(
      name='John'
    ))
    instance = neo4j_base_dao.Neo4JBaseDao(name=mockSchemaName)

    # Act
    data = instance._parseResults('n', mockData)

    # Assert
    assert data == mockData.get('n')

  def test_should_raise_if_key_not_found(self):
    # Arrange
    mockSchemaName = 'Test'
    mockData = dict(n=dict(
      name='John'
    ))
    instance = neo4j_base_dao.Neo4JBaseDao(name=mockSchemaName)

    # Act
    try:
      data = instance._parseResults('f', mockData)
    except Exception as e:
      # Assert
      assert isinstance(e, KeyError)

class TestMethod_Find_Node():
  ...
  # def test_should(self):
  #   # Arrange

  #   # Act

  #   # Assert

class TestMethod_Create_Node():
  ...
  # def test_should(self):
  #   # Arrange

  #   # Act

  #   # Assert

class TestMethod_Get_Node_By_Id():
  ...
  # def test_should(self):
  #   # Arrange

  #   # Act

  #   # Assert

class TestMethod_Update_Node():
  ...
  # def test_should(self):
  #   # Arrange

  #   # Act

  #   # Assert

class TestMethod_Delete_Node():
  ...
  # def test_should(self):
  #   # Arrange

  #   # Act

  #   # Assert