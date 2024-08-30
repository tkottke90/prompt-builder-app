from dotenv import load_dotenv
from fastapi import FastAPI
from src import database
from src.controllers import prompt_controller, root
from src.logging import initializeLogger
from src.exceptions import api_input, entity
from src.middleware import http_logging
import logging

def setupMiddleware(app: FastAPI): {
  app.add_middleware(http_logging.HttpLoggingMiddleware)
}

def setupExceptionHandlers(app: FastAPI):
  app.add_exception_handler(
    api_input.ApiInputError,
    api_input.handleAPIInputException
  )

  app.add_exception_handler(
    entity.EntityException,
    entity.handleEntityException
  )

def setupRouters(app: FastAPI):
  app.include_router(root.router)
  app.include_router(prompt_controller.router)

def main(app: FastAPI):
  database.initialize()
  setupRouters(app)
  setupExceptionHandlers(app)
  setupMiddleware(app)

initializeLogger()
appLogger = logging.getLogger('app')

if __name__ == "__main__":
  # Fast API needs a specific initialize procedure.  If the normal `python` command is used
  # the API wont function.  So we catch when the file is run directly and log an error
  appLogger.error('Error: Whoops! Seems like you ran this with Python.  Use the fastapi cli to start: fastapi dev main.py')
  exit(1)

app = FastAPI(
  title="AI Assistant API",
  description="REST API to interact with Large Language Models using prompts.  This application is used both to develop the prompts."
)

if __name__ == "main":
  load_dotenv()
  main(app) 