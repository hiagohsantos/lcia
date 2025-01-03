from pydantic import BaseModel, Field

class OrganizationInputModel(BaseModel):
    name: str = Field(..., max_length=100, title="Organization Name")
    db_server: str = Field(..., max_length=255, title="Database Server")
    db_name: str = Field(..., max_length=100, title="Database Name")
    db_user: str = Field(..., max_length=50, title="Database User")
    db_password: str = Field(..., max_length=100, title="Database Password")

    class Config:
        from_attributes = True
