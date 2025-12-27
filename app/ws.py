from fastapi import WebSocket, WebSocketDisconnect 

#Websocketdisconnet-specific Error (Exception) that FastAPI raises when the user closes the tab or loses internet.

async def websocket_endpoint(websocket: WebSocket):

#async tells to do something else while waiting for this
#TypeHinting, we are telling it is a Websocket datatype

    await websocket.accept() 

#await tells to wait till the HTTP request gets upgraded to a websocket

    print("WebSocket connected")

#exception handling has to be included else if network connection problems or when a tab is closed it will crash

    try:

        while True:

            # Keep the connection alive, but do NOTHING

            await websocket.receive_text()

#putting await here else the loop will unnecessarily run thousands of time
#running a loop so the connection won't be closed after recieving a single message

    except WebSocketDisconnect:
        print("WebSocket disconnected")

