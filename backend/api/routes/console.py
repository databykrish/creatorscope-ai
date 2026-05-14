"""WebSocket console routes."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import asyncio
from datetime import datetime

from models.schemas import LogEntry
from core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["console"])

# Connected WebSocket clients
connected_clients = []


@router.websocket("/ws/console")
async def websocket_console(websocket: WebSocket):
    """WebSocket endpoint for real-time console logs.

    Args:
        websocket: WebSocket connection
    """
    await websocket.accept()
    connected_clients.append(websocket)
    logger.info(f"Console client connected. Total clients: {len(connected_clients)}")

    try:
        # Send initial connection message
        await websocket.send_json({
            "timestamp": datetime.utcnow().isoformat(),
            "type": "info",
            "message": "Connected to CreatorScope AI processing console",
        })

        # Start streaming log entries
        log_messages = [
            ("info", "Initializing CreatorScope AI engine v3.2.1..."),
            ("success", "Connected to influencer data pipeline"),
            ("process", "Scanning creators — engagement analysis in progress"),
            ("success", "Creator profile scanned: Maya Rodriguez [CAMPAIGN READY]"),
            ("process", "Running sentiment analysis on comments..."),
            ("info", "Sentiment score: 94.2% positive | 3.1% neutral | 2.7% negative"),
            ("process", "Scanning creators — audience overlap analysis"),
            ("success", "Audience match: 78% overlap with target demographic"),
            ("warning", "Some creators — upload consistency below threshold"),
            ("process", "Generating AI recommendations for campaign roster..."),
            ("success", "Campaign readiness report generated"),
            ("info", "Barcode scan complete. All creator profiles indexed."),
        ]

        for idx, (log_type, message) in enumerate(log_messages):
            try:
                # Check if client is still connected
                if websocket.client_state.name == "DISCONNECTED":
                    break

                # Send log entry
                log_entry = LogEntry(
                    timestamp=datetime.utcnow().isoformat(),
                    type=log_type,
                    message=message,
                )

                await websocket.send_json(log_entry.model_dump())
                logger.debug(f"Sent log message {idx + 1}/{len(log_messages)}")

                # Add delay between messages
                await asyncio.sleep(2)

            except Exception as e:
                logger.error(f"Error sending log: {str(e)}")
                break

        # Keep connection alive indefinitely
        # Client can send commands, or connection stays open for new logs
        while True:
            try:
                # Wait for client messages (with timeout to avoid blocking forever)
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=300.0  # 5 minute timeout
                )
                logger.debug(f"Received from console: {data}")
                
                # Echo back or process commands in future
                if data.lower() == "clear":
                    await websocket.send_json({
                        "timestamp": datetime.utcnow().isoformat(),
                        "type": "info",
                        "message": "Console cleared",
                    })
                    
            except asyncio.TimeoutError:
                # Send keepalive message
                await websocket.send_json({
                    "timestamp": datetime.utcnow().isoformat(),
                    "type": "info",
                    "message": "Connection active",
                })
            except WebSocketDisconnect:
                logger.info("Console client disconnected")
                break
            except Exception as e:
                logger.error(f"WebSocket error: {str(e)}")
                break

    except WebSocketDisconnect:
        logger.info("Console client disconnected during initialization")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        logger.info(f"Console client removed. Total clients: {len(connected_clients)}")


async def broadcast_log(log_entry: LogEntry) -> None:
    """Broadcast a log entry to all connected clients.

    Args:
        log_entry: Log entry to broadcast
    """
    disconnected = []
    for client in connected_clients:
        try:
            await client.send_json(log_entry.model_dump())
        except Exception as e:
            logger.error(f"Failed to send to client: {str(e)}")
            disconnected.append(client)

    # Clean up disconnected clients
    for client in disconnected:
        if client in connected_clients:
            connected_clients.remove(client)
