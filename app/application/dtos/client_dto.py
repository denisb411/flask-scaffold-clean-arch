from pydantic import BaseModel, EmailStr, Field

class ClientDTO(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str | None = None

    @staticmethod
    def from_request(data: dict) -> "ClientDTO":
        return ClientDTO(**data)
