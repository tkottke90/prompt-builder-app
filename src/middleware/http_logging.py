from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from uuid import uuid4
from datetime import datetime
import hashlib
import logging
import time

class HttpLoggingMiddleware(BaseHTTPMiddleware):

  def requestTimer(self):
    start = time.time()

    def complete():
      return time.time() - start
    
    return complete

  async def dispatch(self, request: Request, call_next):
    reqLogger = logging.getLogger('HttpRequest')
    # do something with the request object, for example
    requestIdStr: str = uuid4().hex + datetime.now().strftime("%Y%m%d%H%M%S%f")
    request.state.request_id = hashlib.md5(requestIdStr.encode()).hexdigest()
    request.state.logger = reqLogger

    timerComplete = self.requestTimer()

    reqLogger.info(f'HTTP {request.method} {request.url}', extra={ "request_id": request.state.request_id, "timestamp": datetime.now().isoformat() })

    # process the request and get the response    
    response = await call_next(request)
    
    duration = timerComplete()
    reqLogger.info(f'Request completed in {duration} sec', extra={ "executionTime": { "value": duration, "units": 'sec' }, "request_id": requestIdStr })

    return response
