from datetime import datetime
from typing import Any, List
import uuid
import base64
import os

class ChatMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
    
    def jsonFragment(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content
        }

def chat_message_from_json(json: dict[str, Any]) -> ChatMessage:
    return ChatMessage(
        json["role"],
        json["content"]
    )

class ChatConversation:
    def __init__(self, id: str, created: datetime, updated: datetime, 
                 messages: List[ChatMessage]):
        self.id = id
        self.created = created
        self.updated = updated
        self.messages = messages
    
    def jsonFragment(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "created": self.created,
            "updated": self.updated,
            "messages": [x.jsonFragment() for x in self.messages]
        }

def chat_conversation_from_json(json: dict[str, Any]) -> ChatConversation:
    return ChatConversation(
        json["id"],
        json["created"],
        json["updated"],
        [chat_message_from_json(m) for m in json["messages"]]
    )

class ChatPost:
    def __init__(self, app_id: int, department_id: uuid.UUID, conversation: ChatConversation) -> None:
        self.app_id = app_id
        self.department_id = department_id
        self.conversation = conversation
        
    def jsonFragment(self) -> dict[str, Any]:
        return {
            "appId": self.app_id,
            "departmentId": str(self.department_id),
            "conversation": self.conversation.jsonFragment()
        }
    
def chat_post_from_json(json: dict[str, Any]) -> ChatPost:
    return ChatPost(
        json["appId"],
        uuid.UUID(json["departmentId"]),
        chat_conversation_from_json(json["conversation"])
    )

class Error:
    def __init__(self, message: str, type: str=None, code: str=None, param: str=None) -> None:
        self.message = message
        self.type = type
        self.code = code
        self.param = param
    
    def jsonFragment(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "type": self.type,
            "code": self.code,
            "param": self.param
        }

def error_from_json(json: dict[str, Any]) -> Error:
    return Error(
        json["message"],
        json["type"],
        json["code"],
        json["param"]
    )

class ChatMessageRated():
    def __init__(self, id: str, text: str, rating: int = 0):
        self.id = id
        self.text = text
        self.rating = rating

    def jsonFragment(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating
        }

def chatMessageRated_from_json(json) -> ChatMessageRated:
    return ChatMessageRated(
        json['id'],
        json['text'],
        json['rating']
    )

class ChatResponse:
    def __init__(self, message: ChatMessageRated, err: Error = None) -> None:
        self.message = message
        self.err = err
    
    def jsonFragment(self) -> dict[str, Any]:
        return {
            "message": None if self.message is None else self.message.jsonFragment(),
            "error": None if self.err is None else self.err.jsonFragment()
        }

class CodegenResponse:
    def __init__(self,generatedCode:str,lang:str ,execStatus:str, err:Error=None) -> None:
        self.generatedCode= generatedCode
        self.lang = lang
        self.err = err
        self.execStatus = execStatus
         
    def jsonFragment(self) -> dict[str, Any]:
        return {
            "generatedCode": self.generatedCode,
            "lang": self.lang,
            "error": None if self.err is None else self.err.jsonFragment(),
            "execStatus" : self.execStatus 
        }
class CodegenExec:
    def __init__(self, langName: str, langVersion: str) -> None:
        self.langName = langName
        self.langVersion = langVersion

def codegenExec_from_json(json:dict[str:Any]) ->CodegenExec:
    return CodegenExec(
        json["langName"],
        json["langVersion"]
       )

class CodegenPost:
    def __init__(self, app_id: int, department_id: uuid.UUID, prompt: str, lang:str, purpose:str,codegenExec:CodegenExec) -> None:
        self.app_id = app_id
        self.department_id = department_id
        self.prompt = prompt
        self.lang = lang
        self.purpose = purpose
        self.codegenExec = codegenExec

      
def codegen_post_from_json(json: dict[str, Any]) -> CodegenPost:
    codegenExec= None if "codegenExec" not in json.keys() else codegenExec_from_json(json["codegenExec"])
    return CodegenPost(
        json["appId"],
        uuid.UUID(json["departmentId"]),
        json["prompt"],
        json["lang"],
        json["purpose"],
        codegenExec)
    
class Usage:
    def __init__(self, id: str, app_id: int, message_id: str, conversation_id: str, prompt_tokens: int, completion_tokens: int, total_tokens: int) -> None:
        self.id = id
        self.app_id = app_id
        self.message_id = message_id
        self.conversation_id = conversation_id
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens


    def jsonFragment(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "app_id": self.app_id,
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
        }
    
def usage_from_json(json: dict[str, Any]) -> Usage:
    if json:
        return Usage(
            json["id"],
            json.get("message_id"),
            json["app_id"],
            json["conversation_id"],
            json["prompt_tokens"],
            json["completion_tokens"],
            json["total_tokens"])
    return None


class UserFeedbackRow:
    def __init__(self, username: str, question: str, response: str, useful:int, timestamp:str, version: int, assistant: str, config_type: str) -> None:
        self.username = username
        self.question = question
        self.response = response
        self.useful = useful
        self.timestamp = timestamp
        self.version = version
        self.assistant = assistant
        self.config_type = config_type

    def jsonFragment(self) -> dict[str, Any]:
        return {
            "username": self.username,
            "question": self.question,
            "response": self.response,
            "useful": self.useful,
            "timestamp": self.timestamp,
            "version": self.version,
            "assistant": self.assistant,
            "config_type": self.config_type,
        }
    

class ChatSegment:
    def __init__(self, text: str) -> None:
        self.text = text
        self.response_id:str = None

    def jsonFragment(self) -> dict[str, Any]:
        result = {
            "text": self.text
        }

        if self.response_id:
            result["response_id"] = self.response_id

        return result

class TempFileHeader:
    def __init__(self, length: int, name: str, hash: str) -> None:
        self.length = length
        self.name = name
        self.hash = hash

    def jsonFragment(self) -> dict[str, Any]:
        return {
            "length": self.length,
            "name": self.name,
            "hash": self.hash,
        }
    
    def file_extension(self) -> str:
        file, ext = os.path.splitext(self.name)
        return ext
    
def temp_file_header_from_json(json: dict[str, Any]) -> TempFileHeader:
    if json:
        return TempFileHeader(
            json.get("length"),
            json.get("name"),
            json.get("hash"))
    return None

class TempFile(TempFileHeader):
    def __init__(self, length: int, name: str, hash: str, content: str) -> None:
        super().__init__(length, name, hash)
        self.content = content

    def get_file_bytes(self) -> bytes:
        return base64.b64decode(self.content)

    def getHeaderJsonFragment(self) -> dict[str, Any]:
        return super().jsonFragment()

    def jsonFragment(self) -> dict[str, Any]:
        result = super().jsonFragment()
        result["content"] = self.content
    
def temp_file_from_json(json: dict[str, Any]) -> TempFile:
    if json:
        return TempFile(
            json.get("length"),
            json.get("name"),
            json.get("hash"),
            json["content"])
    return None