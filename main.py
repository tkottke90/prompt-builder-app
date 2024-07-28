from fastapi import FastAPI
from src import database
from src.controllers import prompt_controller, root
from src.logging import initializeLogger
import logging

initializeLogger()
appLogger = logging.getLogger('app')

def main(app: FastAPI):
  database.initialize()

  app.include_router(root.router)
  app.include_router(prompt_controller.router)

if __name__ == "__main__":
  appLogger.error('Error: Whoops! Seems like you ran this with Python.  Use the fastapi cli to start: fastapi dev main.py')
  exit(1)

app = FastAPI(
  title="AI Assistant API",
  description="REST API to interact with Large Language Models using prompts.  This application is used both to develop the prompts."
)
if __name__ == "main":
  main(app)